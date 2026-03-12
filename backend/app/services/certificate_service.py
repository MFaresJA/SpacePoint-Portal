from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import certificate_repo, user_repo
from app.services.audit_service import log_action

JOURNEY_COMPLETION_CERTIFICATE_TITLE = "SpacePoint Instructor Completion Certificate"


def issue_certificate(
    db: Session,
    *,
    admin_user_id: int,
    user_id: int,
    title: str,
    certificate_url: str | None,
):
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    obj = certificate_repo.create_certificate(
        db,
        user_id=user_id,
        title=title,
        certificate_url=certificate_url.strip() if certificate_url else None,
        issued_by_user_id=admin_user_id,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="certificate_issued",
        entity_type="certificate",
        entity_id=obj.id,
    )
    return obj


def auto_issue_journey_completion_certificate(
    db: Session,
    *,
    user_id: int,
    issued_by_user_id: int | None,
):
    existing = certificate_repo.get_user_certificate_by_title(
        db,
        user_id=user_id,
        title=JOURNEY_COMPLETION_CERTIFICATE_TITLE,
    )
    if existing:
        return existing

    obj = certificate_repo.create_certificate(
        db,
        user_id=user_id,
        title=JOURNEY_COMPLETION_CERTIFICATE_TITLE,
        certificate_url=None,
        issued_by_user_id=issued_by_user_id,
    )

    log_action(
        db,
        actor_user_id=issued_by_user_id,
        action="certificate_auto_issued",
        entity_type="certificate",
        entity_id=obj.id,
    )
    return obj