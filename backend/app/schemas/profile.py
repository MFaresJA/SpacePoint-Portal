from pydantic import BaseModel, EmailStr, Field


class UpdateMyProfileIn(BaseModel):
    email: EmailStr


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class MyProfileOut(BaseModel):
    user_id: int
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_suspended: bool
    roles: list[str]