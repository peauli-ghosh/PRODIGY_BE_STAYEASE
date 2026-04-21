from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BookingCreate(BaseModel):
    room_id: str
    check_in: datetime
    check_out: datetime


class BookingResponse(BaseModel):
    id: UUID

    room_id: UUID
    user_id: UUID

    check_in: datetime
    check_out: datetime

    total_price: int
    status: str  # NEW

    class Config:
        from_attributes = True