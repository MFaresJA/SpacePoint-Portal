from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class OpportunityCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    link_url: str = Field(..., max_length=500)


class OpportunityUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    link_url: str | None = Field(None, max_length=500)
    is_active: bool | None = None


class OpportunityOut(BaseModel):
    id: int
    owner_user_id: int
    title: str
    description: str
    link_url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OpportunitiesListResponse(BaseModel):
    total: int
    items: list[OpportunityOut]