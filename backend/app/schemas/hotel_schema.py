from pydantic import BaseModel
from uuid import UUID


class HotelCreate(BaseModel):
    name: str
    location: str
    description: str


class HotelResponse(BaseModel):
    id: UUID
    name: str
    location: str
    description: str
    owner_id: UUID

    class Config:
        from_attributes = True