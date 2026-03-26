from sqlalchemy.orm import Session
from uuid import uuid4
from fastapi import HTTPException

from app.models.hotel_model import Hotel


def create_hotel(db: Session, data, owner_id: str):
    new_hotel = Hotel(
        id=str(uuid4()),
        name=data.name,
        location=data.location,
        description=data.description,
        owner_id=owner_id
    )

    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)

    return new_hotel


def get_all_hotels(db: Session):
    return db.query(Hotel).all()


def get_hotel(db: Session, hotel_id: str):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return hotel


def update_hotel(db: Session, hotel_id: str, data):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    hotel.name = data.name
    hotel.location = data.location
    hotel.description = data.description

    db.commit()
    db.refresh(hotel)

    return hotel


def delete_hotel(db: Session, hotel_id: str):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db.delete(hotel)
    db.commit()

    return {"message": "Hotel deleted successfully"}