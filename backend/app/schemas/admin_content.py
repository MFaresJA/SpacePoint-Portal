from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class AdminContentCreateIn(BaseModel):
    key: str = Field(..., max_length=50)
    title: str = Field(..., max_length=200)
    url: str = Field(..., max_length=500)
    is_active: bool = True


class AdminContentUpdateIn(BaseModel):
    key: str | None = Field(None, max_length=50)
    title: str | None = Field(None, max_length=200)
    url: str | None = Field(None, max_length=500)
    is_active: bool | None = None


class AdminContentOut(BaseModel):
    id: int
    key: str
    title: str
    url: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AdminContentListResponse(BaseModel):
    total: int
    items: list[AdminContentOut]