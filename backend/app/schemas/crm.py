from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class CRMLeadCreate(BaseModel):
    organization_name: str = Field(..., max_length=200)
    contact_name: str = Field(..., max_length=200)
    contact_email: EmailStr
    notes: str | None = None


class CRMLeadUpdateAdmin(BaseModel):
    status: str | None = None
    admin_notes: str | None = None


class CRMLeadOut(BaseModel):
    id: int
    instructor_user_id: int
    organization_name: str
    contact_name: str
    contact_email: EmailStr
    notes: str | None
    status: str
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CRMLeadsListResponse(BaseModel):
    total: int
    items: list[CRMLeadOut]