from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional


class MenuBase(BaseModel):
    name: str


class MenuInDBBase(MenuBase):
    model_config = ConfigDict(from_attributes=True)

    # id: int
