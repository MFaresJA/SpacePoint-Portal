from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import crm_repo
from app.services.audit_service import log_action

_ALLOWED_STATUSES = {"SUBMITTED", "APPROVED", "REJECTED", "UNDER_REVIEW"}


def submit_lead(
    db: Session,
    *,
    instructor_user_id: int,
    organization_name: str,
    contact_name: str,
    contact_email: str,
    notes: str | None,
):
    organization_name = organization_name.strip()
    contact_name = contact_name.strip()
    contact_email = contact_email.strip()

    if not organization_name:
        raise HTTPException(status_code=400, detail="organization_name is required")
    if not contact_name:
        raise HTTPException(status_code=400, detail="contact_name is required")
    if not contact_email:
        raise HTTPException(status_code=400, detail="contact_email is required")

    obj = crm_repo.create_lead(
        db,
        instructor_user_id=instructor_user_id,
        organization_name=organization_name,
        contact_name=contact_name,
        contact_email=contact_email,
        notes=notes.strip() if notes else None,
    )

    log_action(
        db,
        actor_user_id=instructor_user_id,
        action="crm_lead_submitted",
        entity_type="crm_lead",
        entity_id=obj.id,
    )
    return obj


def admin_update_lead(
    db: Session,
    *,
    admin_user_id: int,
    lead_id: int,
    status: str | None,
    admin_notes: str | None,
):
    obj = crm_repo.get_lead(db, lead_id)
    if not obj:
        raise HTTPException(status_code=404, detail="CRM lead not found")

    if status is not None:
        status = status.strip().upper()
        if status not in _ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    updated = crm_repo.update_lead_admin(
        db,
        obj,
        status=status,
        admin_notes=admin_notes.strip() if admin_notes else None,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="crm_lead_updated",
        entity_type="crm_lead",
        entity_id=updated.id,
    )
    return updated