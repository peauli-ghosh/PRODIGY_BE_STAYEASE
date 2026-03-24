from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    TokenResponse,
    AuthLogin
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
from app.core.deps import get_current_user
from app.models.user_model import User

router = APIRouter()


# ✅ CREATE USER (PUBLIC)
@router.post("/users", response_model=UserResponse)
def create(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# 🔐 GET ALL USERS (ADMIN ONLY)
@router.get("/users", response_model=list[UserResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")

    return get_all_users(db)


# 🔐 GET SINGLE USER
@router.get("/users/{user_id}", response_model=UserResponse)
def get_single(user_id: str, db: Session = Depends(get_db)):
    return get_user(db, user_id)


# 🔐 UPDATE (ONLY SELF — ADMIN ALSO RESTRICTED)
@router.put("/users/{user_id}", response_model=UserResponse)
def update(
    user_id: str,
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own profile"
        )

    return update_user(db, user_id, user)


# 🔐 DELETE (SMART ROLE CONTROL)
@router.delete("/users/{user_id}")
def delete(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_user = get_user(db, user_id)

    # ✅ ADMIN LOGIC
    if current_user.role.lower() == "admin":

        # ❌ Admin cannot delete another admin (unless self)
        if (
            target_user.role.lower() == "admin"
            and str(current_user.id) != user_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Admins cannot delete other admins"
            )

        return delete_user(db, user_id)

    # ✅ USER LOGIC (only self)
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own profile"
        )

    return delete_user(db, user_id)


# 🔐 LOGIN (Swagger OAuth)
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data.username, form_data.password)


# 🔐 CLEAN LOGIN (Frontend)
@router.post("/auth/login", response_model=TokenResponse)
def auth_login(user: AuthLogin, db: Session = Depends(get_db)):
    return login_user(db, user.email, user.password)


# 🔐 CURRENT USER
@router.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user