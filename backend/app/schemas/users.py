from pydantic import BaseModel, EmailStr
from typing import List


class AdminUserItem(BaseModel):
    user_id: int
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_suspended: bool
    roles: List[str] = []


class AdminUsersListResponse(BaseModel):
    total: int
    items: List[AdminUserItem]
