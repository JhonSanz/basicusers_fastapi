from pydantic import BaseModel, EmailStr
from typing import List, Optional


class RoleBase(BaseModel):
    name: str


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True
