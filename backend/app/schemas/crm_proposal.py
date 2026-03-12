from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class CRMProposalCreate(BaseModel):
    lead_id: int
    proposal_url: str = Field(..., max_length=500)
    notes: str | None = None


class CRMProposalUpdateAdmin(BaseModel):
    status: str | None = None
    admin_notes: str | None = None


class CRMProposalOut(BaseModel):
    id: int
    lead_id: int
    instructor_user_id: int
    proposal_url: str
    notes: str | None
    status: str
    admin_notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CRMProposalsListResponse(BaseModel):
    total: int
    items: list[CRMProposalOut]