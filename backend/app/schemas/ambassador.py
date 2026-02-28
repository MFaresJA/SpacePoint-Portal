from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, Field


# ---------- Recruitment Entries ----------

class RecruitmentEntryCreate(BaseModel):
    name: str = Field(..., max_length=200)
    contact: str = Field(..., max_length=200)
    notes: str | None = Field(None, max_length=1000)


class RecruitmentEntryOut(BaseModel):
    id: int
    ambassador_user_id: int
    name: str
    contact: str
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecruitmentListResponse(BaseModel):
    total: int
    items: list[RecruitmentEntryOut]


class AdminUpdateRecruitmentIn(BaseModel):
    status: str | None = None   # PENDING / APPROVED / REJECTED / etc
    notes: str | None = Field(None, max_length=1000)


# ---------- Impact Reports ----------

class ImpactReportCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str

    evidence_url: str = Field(..., max_length=500)
    location: str = Field(..., max_length=200)
    event_date: date

    hours: int = 0
    people_reached: int = 0


class ImpactReportOut(BaseModel):
    id: int
    ambassador_user_id: int
    title: str
    description: str

    evidence_url: str
    location: str
    event_date: date

    status: str
    hours: int
    people_reached: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImpactReportListResponse(BaseModel):
    total: int
    items: list[ImpactReportOut]


class AdminUpdateImpactReportIn(BaseModel):
    status: str | None = None
    # we reuse "notes" behavior by storing it in recruitment only; impact has no notes column now