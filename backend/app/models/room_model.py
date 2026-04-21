from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True)

    hotel_id = Column(String, ForeignKey("hotels.id"), nullable=False)

    room_number = Column(String, nullable=False)
    room_type = Column(String, nullable=False)

    # Phase 2 additions
    capacity = Column(Integer, nullable=False, default=2)
    amenities = Column(String)

    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

    # Relationship
    hotel = relationship("Hotel", back_populates="rooms")