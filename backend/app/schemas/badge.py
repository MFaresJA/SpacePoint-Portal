from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class BadgeCreate(BaseModel):
    user_id: int
    title: str = Field(..., max_length=200)
    badge_code: str | None = Field(None, max_length=100)
    badge_image_url: str | None = Field(None, max_length=500)


class BadgeOut(BaseModel):
    id: int
    user_id: int
    title: str
    badge_code: str | None
    badge_image_url: str | None
    issued_by_user_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class BadgesListResponse(BaseModel):
    total: int
    items: list[BadgeOut]