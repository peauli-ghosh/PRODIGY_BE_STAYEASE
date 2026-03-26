from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.schemas.hotel_schema import HotelCreate, HotelResponse
from app.services.hotel_service import (
    create_hotel,
    get_all_hotels,
    get_hotel,
    update_hotel,
    delete_hotel
)
from app.db.database import get_db
from app.core.deps import get_current_user
from app.models.user_model import User
from app.models.hotel_model import Hotel

router = APIRouter()


# CREATE HOTEL (ADMIN ONLY)
@router.post("/hotels", response_model=HotelResponse)
def create(
    hotel: HotelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return create_hotel(db, hotel, current_user.id)


# GET ALL HOTELS (PUBLIC)
@router.get("/hotels", response_model=list[HotelResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_hotels(db)


# SEARCH HOTELS (PUBLIC) — MUST BE ABOVE {hotel_id}
@router.get("/hotels/search", response_model=list[HotelResponse])
def search_hotels(
    name: str = None,
    location: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Hotel)

    filters = []

    if name:
        filters.append(Hotel.name.ilike(f"%{name}%"))

    if location:
        filters.append(Hotel.location.ilike(f"%{location}%"))

    if filters:
        query = query.filter(or_(*filters))

    return query.all()


# GET SINGLE HOTEL (PUBLIC)
@router.get("/hotels/{hotel_id}", response_model=HotelResponse)
def get_single(hotel_id: str, db: Session = Depends(get_db)):
    return get_hotel(db, hotel_id)


# UPDATE HOTEL (ADMIN ONLY)
@router.put("/hotels/{hotel_id}", response_model=HotelResponse)
def update(
    hotel_id: str,
    hotel: HotelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action"
        )

    return update_hotel(db, hotel_id, hotel)


# DELETE HOTEL (ADMIN ONLY)
@router.delete("/hotels/{hotel_id}")
def delete(
    hotel_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action"
        )

    return delete_hotel(db, hotel_id)