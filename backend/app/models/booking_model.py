from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)

    total_price = Column(Integer, nullable=False)

    # NEW: booking lifecycle control AND values: confirmed / cancelled

    status = Column(String, default="confirmed", nullable=False)

    # Relationships
    user = relationship("User", backref="bookings")
    room = relationship("Room", backref="bookings")