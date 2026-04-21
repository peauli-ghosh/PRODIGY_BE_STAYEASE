from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.booking_schema import BookingCreate, BookingResponse
from app.services.booking_service import (
    create_booking,
    get_my_bookings,
    cancel_booking,
    get_all_bookings,
    get_booking_stats
)
from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user_model import User

router = APIRouter()


# CREATE BOOKING
@router.post("/bookings", response_model=BookingResponse)
def create_booking_route(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_booking(db, current_user.id, booking)


# GET MY BOOKINGS
@router.get("/bookings/me", response_model=list[BookingResponse])
def get_my_bookings_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_bookings(db, current_user.id)


# CANCEL BOOKING
@router.put("/bookings/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking_route(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cancel_booking(
        db,
        booking_id,
        current_user.id,
        current_user.role
    )


# ADMIN: GET ALL BOOKINGS
@router.get("/bookings", response_model=list[BookingResponse])
def get_all_bookings_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return get_all_bookings(db)


# ADMIN: BOOKING STATS
@router.get("/bookings/stats")
def booking_stats_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return get_booking_stats(db)