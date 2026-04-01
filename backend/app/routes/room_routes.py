from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.room_schema import RoomCreate, RoomResponse
from app.services.room_service import (
    create_room,
    get_rooms_by_hotel,
    get_room,
    search_rooms_service
)
from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user_model import User

router = APIRouter()


# CREATE ROOM (ADMIN ONLY)
@router.post("/rooms", response_model=RoomResponse)
def create(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return create_room(db, room)


# GET ROOMS BY HOTEL
@router.get("/hotels/{hotel_id}/rooms", response_model=list[RoomResponse])
def get_by_hotel(
    hotel_id: str,
    db: Session = Depends(get_db)
):
    return get_rooms_by_hotel(db, hotel_id)


# ✅ IMPORTANT: SEARCH ROUTE MUST COME BEFORE /rooms/{room_id}
@router.get("/rooms/search", response_model=list[RoomResponse])
def search_rooms(
    location: Optional[str] = None,
    room_type: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return search_rooms_service(
        db,
        location,
        room_type,
        min_price,
        max_price
    )


# GET SINGLE ROOM
@router.get("/rooms/{room_id}", response_model=RoomResponse)
def get_single(
    room_id: str,
    db: Session = Depends(get_db)
):
    return get_room(db, room_id)