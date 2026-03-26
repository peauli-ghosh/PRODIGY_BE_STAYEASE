from fastapi import FastAPI

from app.routes.user_routes import router as user_router
from app.routes.hotel_routes import router as hotel_router

from app.db.database import engine, Base
from app.models import user_model
from app.models import hotel_model


app = FastAPI()


# Create database tables
Base.metadata.create_all(bind=engine)


# Include routes
app.include_router(user_router)
app.include_router(hotel_router)


@app.get("/")
def root():
    return {"message": "Stayease API is running"}