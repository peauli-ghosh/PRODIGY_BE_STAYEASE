from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse   # ✅ NEW
)

from app.services.user_service import (
    create_user,
    get_all_users,
    get_user,
    update_user,
    delete_user,
    login_user
)

from app.db.database import get_db

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users")
def get_all(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_single(user_id: str, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@router.put("/users/{user_id}", response_model=UserResponse)
def update(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


@router.delete("/users/{user_id}")
def delete(user_id: str, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


# 🔐 LOGIN ROUTE (FIXED)
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user.email, user.password)