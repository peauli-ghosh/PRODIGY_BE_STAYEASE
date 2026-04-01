from sqlalchemy.orm import Session, joinedload
from uuid import uuid4
from fastapi import HTTPException

from app.models.room_model import Room
from app.models.hotel_model import Hotel


def create_room(db: Session, data):
    hotel = db.query(Hotel).filter(Hotel.id == data.hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    new_room = Room(
        id=str(uuid4()),
        hotel_id=data.hotel_id,
        room_number=data.room_number,
        room_type=data.room_type,
        price=data.price,
        is_available=True
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    # No manual assignment needed anymore
    return new_room


def get_rooms_by_hotel(db: Session, hotel_id: str):
    rooms = (
        db.query(Room)
        .options(joinedload(Room.hotel))
        .filter(Room.hotel_id == hotel_id)
        .all()
    )

    return rooms


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

# Search_room_service

from sqlalchemy import or_
from fastapi import HTTPException

def search_rooms_service(
    db: Session,
    location: str = None,
    room_type: str = None,
    min_price: int = None,
    max_price: int = None
):
    base_query = (
        db.query(Room)
        .join(Hotel)
        .options(joinedload(Room.hotel))
    )

    # STEP 1 — LOCATION FILTER (MANDATORY)
    if location:
        location_filter = or_(
            Hotel.location.ilike(f"%{location}%"),
            Hotel.name.ilike(f"%{location}%"),
            Hotel.description.ilike(f"%{location}%")
        )

        base_query = base_query.filter(location_filter)

        # Check if location exists at all
        location_exists = (
            db.query(Hotel)
            .filter(location_filter)
            .first()
        )

        if not location_exists:
            raise HTTPException(
                status_code=404,
                detail=f"No hotels available in '{location}'"
            )

    # STEP 2 — APPLY ROOM TYPE (BUT DON'T FORCE IT)
    filtered_query = base_query

    if room_type:
        filtered_query = filtered_query.filter(
            Room.room_type.ilike(f"%{room_type}%")
        )

    # STEP 3 — PRICE FILTER
    if min_price is not None:
        filtered_query = filtered_query.filter(Room.price >= min_price)

    if max_price is not None:
        filtered_query = filtered_query.filter(Room.price <= max_price)

    results = filtered_query.all()

    # STEP 4 — FALLBACK (IMPORTANT)
    if not results and location:
        # fallback to location-only results
        fallback_results = base_query.all()

        if fallback_results:
            return fallback_results

    # FINAL CHECK
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No rooms match your search criteria"
        )

    return results