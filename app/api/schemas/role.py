from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional


class RoleBase(BaseModel):
    name: str


class RoleInDBBase(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
