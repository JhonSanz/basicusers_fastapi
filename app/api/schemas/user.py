from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from app.api.schemas.role import RoleBase, RoleInDBBase


class UserBase(BaseModel):
    identification: str
    name: str
    phone: str


class UserCreate(UserBase):
    password: str
    role_id: int


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)


    id: int
    roles: List[RoleInDBBase]


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
