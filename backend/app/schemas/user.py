from __future__ import annotations

from pydantic import BaseModel, EmailStr
from typing import List


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    is_suspended: bool = False
    roles: List[str] = []

    class Config:
        from_attributes = True