from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from uuid import uuid4

from app.models.booking_model import Booking
from app.models.room_model import Room
from app.core.redis import redis_client


def create_booking(db: Session, user_id: str, data):
    room = db.query(Room).filter(Room.id == data.room_id).first()

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if data.check_in >= data.check_out:
        raise HTTPException(status_code=400, detail="Invalid date range")

    overlapping_booking = (
        db.query(Booking)
        .filter(
            Booking.room_id == data.room_id,
            Booking.status != "cancelled",
            Booking.check_in < data.check_out,
            Booking.check_out > data.check_in
        )
        .first()
    )

    if overlapping_booking:
        raise HTTPException(
            status_code=400,
            detail="Room already booked for selected dates"
        )

    nights = (data.check_out - data.check_in).days

    if nights <= 0:
        raise HTTPException(status_code=400, detail="Invalid booking duration")

    total_price = nights * room.price

    new_booking = Booking(
        id=str(uuid4()),
        user_id=user_id,
        room_id=data.room_id,
        check_in=data.check_in,
        check_out=data.check_out,
        total_price=total_price,
        status="confirmed"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # 🔥 Invalidate cache
    redis_client.flushdb()

    return new_booking


def get_my_bookings(db: Session, user_id: str):
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .all()
    )


def cancel_booking(db: Session, booking_id: str, user_id: str, role: str):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user_id and role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking already cancelled")

    booking.status = "cancelled"

    db.commit()
    db.refresh(booking)

    # 🔥 Invalidate cache
    redis_client.flushdb()

    return booking


# ADMIN: GET ALL BOOKINGS
def get_all_bookings(db: Session):
    return db.query(Booking).all()


# ADMIN: STATS
def get_booking_stats(db: Session):
    total_bookings = db.query(func.count(Booking.id)).scalar()

    total_revenue = (
        db.query(func.sum(Booking.total_price))
        .filter(Booking.status != "cancelled")
        .scalar()
    )

    return {
        "total_bookings": total_bookings or 0,
        "total_revenue": total_revenue or 0
    }