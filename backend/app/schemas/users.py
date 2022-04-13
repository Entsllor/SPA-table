from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    email: str


class UserPublic(UserBase):
    """Public user data"""
    id: int
    created_at: datetime


class UserPrivate(UserPublic):
    """Private user data (other users shouldn't see this)"""
    email: str


class User(UserPrivate):
    """Secret user data (even the user should not know it)"""
    hashed_password: str
    is_active: bool = True
