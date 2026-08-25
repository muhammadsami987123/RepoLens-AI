from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserInDB(BaseModel):
    id: str
    name: str
    email: str
    hashed_password: str
    created_at: str
    analyses_count: int = 0


class UserPublic(BaseModel):
    id: str
    name: str
    email: str
    created_at: str
    analyses_count: int = 0
