from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ApplicationOut(BaseModel):
    id: int
    user_id: int

    track: str
    full_name: str
    phone_number: str
    email: str
    university: str
    highest_degree: str

    city_of_residence: str
    deliver_cities: list[str]
    background_areas: list[str]

    video1_summary: str
    video2_summary: str
    video3_summary: str

    space_terms_pdf_path: str
    cv_pdf_path: str

    status: str
    admin_notes: str | None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationsListResponse(BaseModel):
    total: int
    items: list[ApplicationOut]


class AdminUpdateApplicationIn(BaseModel):
    status: str | None = None  # e.g. "SUBMITTED", "UNDER_REVIEW", "APPROVED", "REJECTED"
    admin_notes: str | None = None