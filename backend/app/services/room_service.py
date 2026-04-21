from sqlalchemy.orm import Session, joinedload
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy import or_
from datetime import datetime
import json

from app.models.room_model import Room
from app.models.hotel_model import Hotel
from app.models.booking_model import Booking
from app.core.redis import redis_client


# CREATE ROOM
def create_room(db: Session, data):
    hotel = db.query(Hotel).filter(Hotel.id == data.hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    new_room = Room(
        id=str(uuid4()),
        hotel_id=data.hotel_id,
        room_number=data.room_number,
        room_type=data.room_type,
        capacity=data.capacity,
        amenities=data.amenities,
        price=data.price,
        is_available=True
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    # Invalidate cache
    redis_client.flushdb()

    return new_room


# GET ROOMS BY HOTEL
def get_rooms_by_hotel(db: Session, hotel_id: str):
    return (
        db.query(Room)
        .options(joinedload(Room.hotel))
        .filter(Room.hotel_id == hotel_id)
        .all()
    )


# GET SINGLE ROOM
def get_room(db: Session, room_id: str):
    room = (
        db.query(Room)
        .options(joinedload(Room.hotel))
        .filter(Room.id == room_id)
        .first()
    )

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    return room


# SEARCH ROOMS (SMART + AVAILABILITY + REDIS CACHE)
def search_rooms_service(
    db: Session,
    location: str = None,
    room_type: str = None,
    min_price: int = None,
    max_price: int = None,
    check_in: datetime = None,
    check_out: datetime = None
):
    # 🔥 safer cache key (no None / datetime issues)
    cache_key = f"rooms:{location or ''}:{room_type or ''}:{min_price or ''}:{max_price or ''}:{check_in.isoformat() if check_in else ''}:{check_out.isoformat() if check_out else ''}"

    # 1️⃣ Check cache
    cached = redis_client.get(cache_key)
    if cached:
        print("CACHE HIT")
        return json.loads(cached)

    print("CACHE MISS")

    query = (
        db.query(Room)
        .join(Hotel)
        .options(joinedload(Room.hotel))
    )

    # LOCATION
    if location:
        location_filter = or_(
            Hotel.location.ilike(f"%{location}%"),
            Hotel.name.ilike(f"%{location}%"),
            Hotel.description.ilike(f"%{location}%")
        )

        query = query.filter(location_filter)

        if not db.query(Hotel).filter(location_filter).first():
            raise HTTPException(
                status_code=404,
                detail=f"No hotels available in '{location}'"
            )

    # ROOM TYPE
    if room_type:
        query = query.filter(
            Room.room_type.ilike(f"%{room_type}%")
        )

    # PRICE
    if min_price is not None:
        query = query.filter(Room.price >= min_price)

    if max_price is not None:
        query = query.filter(Room.price <= max_price)

    # AVAILABILITY
    if check_in and check_out:

        if check_in >= check_out:
            raise HTTPException(
                status_code=400,
                detail="Invalid date range"
            )

        overlapping_bookings = db.query(Booking.room_id).filter(
            Booking.check_in < check_out,
            Booking.check_out > check_in,
            Booking.status != "cancelled"
        )

        query = query.filter(~Room.id.in_(overlapping_bookings))

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No rooms available for given criteria"
        )

    # Serialize
    response_data = [
    {
        "id": r.id,
        "room_number": r.room_number,
        "room_type": r.room_type,
        "capacity": r.capacity,
        "amenities": r.amenities,        
        "price": r.price,
        "is_available": r.is_available,
        "hotel": {
            "id": r.hotel.id,
            "name": r.hotel.name,
            "location": r.hotel.location,
            "description": r.hotel.description
        }
    }
    for r in results
]

    # Cache (TTL 60s)
    redis_client.setex(cache_key, 60, json.dumps(response_data))

    return response_data