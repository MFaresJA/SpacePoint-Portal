from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles

from app.repositories import ambassador_repo
from app.schemas.ambassador import (
    RecruitmentListResponse,
    RecruitmentEntryOut,
    AdminUpdateRecruitmentIn,
    ImpactReportListResponse,
    ImpactReportOut,
    AdminUpdateImpactReportIn,
)
from app.services.ambassador_service import admin_update_recruitment, admin_update_impact

router = APIRouter(prefix="/admin/ambassador", tags=["Admin - Ambassador"])


@router.get("/recruitment", response_model=RecruitmentListResponse)
def list_recruitment(
    skip: int = 0,
    limit: int = 50,
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    total, items = ambassador_repo.list_recruitment_entries(
        db,
        skip=skip,
        limit=limit,
        status=status.upper() if status else None,
    )
    return {"total": total, "items": items}


@router.patch("/recruitment/{entry_id}", response_model=RecruitmentEntryOut)
def update_recruitment(
    entry_id: int,
    payload: AdminUpdateRecruitmentIn,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return admin_update_recruitment(
        db,
        entry_id=entry_id,
        status=payload.status,
        notes=payload.notes,
    )


@router.get("/impact", response_model=ImpactReportListResponse)
def list_impact(
    skip: int = 0,
    limit: int = 50,
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    total, items = ambassador_repo.list_impact_reports(
        db,
        skip=skip,
        limit=limit,
        status=status.upper() if status else None,
    )
    return {"total": total, "items": items}


@router.patch("/impact/{report_id}", response_model=ImpactReportOut)
def update_impact(
    report_id: int,
    payload: AdminUpdateImpactReportIn,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return admin_update_impact(db, report_id=report_id, status=payload.status)