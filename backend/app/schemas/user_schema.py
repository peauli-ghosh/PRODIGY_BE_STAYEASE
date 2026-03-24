from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
    password: str
    role: str = "customer"


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    age: int
    role: str

    class Config:
        from_attributes = True   # ✅ VERY IMPORTANT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class AuthLogin(BaseModel):
    email: EmailStr
    password: str