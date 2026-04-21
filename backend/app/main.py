from fastapi import FastAPI

from app.routes.user_routes import router as user_router
from app.routes.hotel_routes import router as hotel_router
from app.routes.room_routes import router as room_router
from app.routes.booking_routes import router as booking_router

from app.db.database import engine, Base

# Register models
from app.models import user_model
from app.models import hotel_model
from app.models import room_model
from app.models import booking_model


# CREATE APP FIRST
app = FastAPI()


# REGISTER ROUTES AFTER APP EXISTS
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(room_router)
app.include_router(booking_router)


# Create tables
Base.metadata.create_all(bind=engine)