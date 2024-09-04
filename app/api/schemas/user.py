from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    identification: str
    name: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode: True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
