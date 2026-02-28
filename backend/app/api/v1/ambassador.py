from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles

from app.repositories import ambassador_repo
from app.schemas.ambassador import (
    RecruitmentEntryCreate,
    RecruitmentEntryOut,
    RecruitmentListResponse,
    ImpactReportCreate,
    ImpactReportOut,
    ImpactReportListResponse,
)
from app.services.ambassador_service import submit_recruitment_entry, submit_impact_report

router = APIRouter()


@router.get("/ping")
def ambassador_ping(user=Depends(require_roles("ambassador", "admin"))):
    return {"ok": True, "msg": "ambassador access granted"}


# ---------------- Recruitment ----------------

@router.post("/recruitment", response_model=RecruitmentEntryOut)
def create_recruitment(
    payload: RecruitmentEntryCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ambassador")),
):
    return submit_recruitment_entry(
        db,
        ambassador_user_id=user.user_id,
        name=payload.name,
        contact=payload.contact,
        notes=payload.notes,
    )


@router.get("/me/recruitment", response_model=RecruitmentListResponse)
def my_recruitment(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ambassador")),
):
    total, items = ambassador_repo.list_recruitment_entries(
        db,
        skip=skip,
        limit=limit,
        status=status.upper() if status else None,
        ambassador_user_id=user.user_id,
    )
    return {"total": total, "items": items}


# ---------------- Impact Reports ----------------

@router.post("/impact", response_model=ImpactReportOut)
def create_impact(
    payload: ImpactReportCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ambassador")),
):
    return submit_impact_report(
        db,
        ambassador_user_id=user.user_id,
        title=payload.title,
        description=payload.description,
        evidence_url=payload.evidence_url,
        location=payload.location,
        event_date=payload.event_date,
        hours=payload.hours,
        people_reached=payload.people_reached,
    )


@router.get("/me/impact", response_model=ImpactReportListResponse)
def my_impact(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ambassador")),
):
    total, items = ambassador_repo.list_impact_reports(
        db,
        skip=skip,
        limit=limit,
        status=status.upper() if status else None,
        ambassador_user_id=user.user_id,
    )
    return {"total": total, "items": items}