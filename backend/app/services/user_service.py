from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4
import os

from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password


def create_user(db: Session, user: UserCreate):
    # Check duplicate email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # ADMIN CREATION CONTROL
    if user.role.lower() == "admin":
        ADMIN_SECRET = os.getenv("ADMIN_SECRET")

        if not ADMIN_SECRET or not user.password.startswith(ADMIN_SECRET):
            raise HTTPException(
                status_code=403,
                detail="Invalid admin creation key"
            )

    hashed_password = hash_password(user.password)

    new_user = User(
        id=str(uuid4()),
        name=user.name,
        email=user.email,
        age=user.age,
        password=hashed_password,
        role=user.role.lower()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(db: Session, user_id: str, user: UserCreate):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check duplicate email
    email_check = db.query(User).filter(User.email == user.email).first()
    if email_check and email_check.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age
    existing_user.password = hash_password(user.password)
    existing_user.role = user.role.lower()

    db.commit()
    db.refresh(existing_user)

    return existing_user


def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# LOGIN SERVICE
def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from app.core.security import verify_password, create_access_token

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }