from pydantic import BaseModel, EmailStr
from typing import List, Optional


class RoleBase(BaseModel):
    id: int
    name: str
