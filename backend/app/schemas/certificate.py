from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class CertificateCreate(BaseModel):
    user_id: int
    title: str = Field(..., max_length=200)
    certificate_url: str | None = Field(None, max_length=500)


class CertificateOut(BaseModel):
    id: int
    user_id: int
    title: str
    certificate_url: str | None
    issued_by_user_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class CertificatesListResponse(BaseModel):
    total: int
    items: list[CertificateOut]