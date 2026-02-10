from pydantic import BaseModel
from typing import List

class RolesListResponse(BaseModel):
    user_id: int
    roles: List[str]

class RoleActionResponse(BaseModel):
    message: str
