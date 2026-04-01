from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(String, primary_key=True, index=True)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String)

    owner_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Relationship to rooms
    rooms = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete-orphan"
    )