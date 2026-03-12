from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import crm_repo, crm_proposal_repo
from app.services.audit_service import log_action

_ALLOWED_STATUSES = {"SUBMITTED", "APPROVED", "REJECTED", "UNDER_REVIEW"}


def submit_proposal(
    db: Session,
    *,
    instructor_user_id: int,
    lead_id: int,
    proposal_url: str,
    notes: str | None,
):
    lead = crm_repo.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="CRM lead not found")

    if lead.instructor_user_id != instructor_user_id:
        raise HTTPException(status_code=403, detail="Not allowed to submit proposal for this lead")

    if lead.status != "APPROVED":
        raise HTTPException(status_code=400, detail="Lead must be APPROVED before proposal submission")

    proposal_url = proposal_url.strip()
    if not proposal_url:
        raise HTTPException(status_code=400, detail="proposal_url is required")

    obj = crm_proposal_repo.create_proposal(
        db,
        lead_id=lead_id,
        instructor_user_id=instructor_user_id,
        proposal_url=proposal_url,
        notes=notes.strip() if notes else None,
    )

    log_action(
        db,
        actor_user_id=instructor_user_id,
        action="crm_proposal_submitted",
        entity_type="crm_proposal",
        entity_id=obj.id,
    )
    return obj


def admin_update_proposal(
    db: Session,
    *,
    admin_user_id: int,
    proposal_id: int,
    status: str | None,
    admin_notes: str | None,
):
    obj = crm_proposal_repo.get_proposal(db, proposal_id)
    if not obj:
        raise HTTPException(status_code=404, detail="CRM proposal not found")

    if status is not None:
        status = status.strip().upper()
        if status not in _ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    updated = crm_proposal_repo.update_proposal_admin(
        db,
        obj,
        status=status,
        admin_notes=admin_notes.strip() if admin_notes else None,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="crm_proposal_updated",
        entity_type="crm_proposal",
        entity_id=updated.id,
    )
    return updated