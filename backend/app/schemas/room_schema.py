from pydantic import BaseModel
from uuid import UUID


class HotelMini(BaseModel):
    id: UUID
    name: str
    location: str
    description: str

    class Config:
        from_attributes = True


class RoomCreate(BaseModel):
    hotel_id: str
    room_number: str
    room_type: str
    capacity: int
    amenities: str
    price: int


class RoomResponse(BaseModel):
    id: UUID
    room_number: str
    room_type: str
    capacity: int
    amenities: str
    price: int
    is_available: bool

    hotel: HotelMini

    class Config:
        from_attributes = True