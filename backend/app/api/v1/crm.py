from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import crm_repo
from app.schemas.crm import CRMLeadCreate, CRMLeadOut, CRMLeadsListResponse
from app.services.crm_service import submit_lead

from app.schemas.crm_proposal import CRMProposalCreate, CRMProposalOut, CRMProposalsListResponse
from app.repositories import crm_proposal_repo
from app.services.crm_proposal_service import submit_proposal

router = APIRouter()


@router.post("/leads", response_model=CRMLeadOut)
def create_lead(
    payload: CRMLeadCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return submit_lead(
        db,
        instructor_user_id=user.user_id,
        organization_name=payload.organization_name,
        contact_name=payload.contact_name,
        contact_email=payload.contact_email,
        notes=payload.notes,
    )


@router.get("/leads/me", response_model=CRMLeadsListResponse)
def my_leads(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = crm_repo.list_leads(
        db,
        skip=skip,
        limit=limit,
        instructor_user_id=user.user_id,
        status=status.upper() if status else None,
    )
    return {"total": total, "items": items}

@router.post("/proposals", response_model=CRMProposalOut)
def create_proposal(
    payload: CRMProposalCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return submit_proposal(
        db,
        instructor_user_id=user.user_id,
        lead_id=payload.lead_id,
        proposal_url=payload.proposal_url,
        notes=payload.notes,
    )


@router.get("/proposals/me", response_model=CRMProposalsListResponse)
def my_proposals(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = crm_proposal_repo.list_proposals(
        db,
        skip=skip,
        limit=limit,
        instructor_user_id=user.user_id,
        status=status.upper() if status else None,
    )
    return {"total": total, "items": items}