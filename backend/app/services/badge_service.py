from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import badge_repo, user_repo
from app.services.audit_service import log_action

JOURNEY_COMPLETION_BADGE_TITLE = "Master Trainer Badge"
JOURNEY_COMPLETION_BADGE_CODE = "MASTER-TRAINER-AUTO"


def issue_badge(
    db: Session,
    *,
    admin_user_id: int,
    user_id: int,
    title: str,
    badge_code: str | None,
    badge_image_url: str | None,
):
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    obj = badge_repo.create_badge(
        db,
        user_id=user_id,
        title=title,
        badge_code=badge_code.strip() if badge_code else None,
        badge_image_url=badge_image_url.strip() if badge_image_url else None,
        issued_by_user_id=admin_user_id,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="badge_issued",
        entity_type="badge",
        entity_id=obj.id,
    )
    return obj


def auto_issue_journey_completion_badge(
    db: Session,
    *,
    user_id: int,
    issued_by_user_id: int | None,
):
    existing = badge_repo.get_user_badge_by_title(
        db,
        user_id=user_id,
        title=JOURNEY_COMPLETION_BADGE_TITLE,
    )
    if existing:
        return existing

    obj = badge_repo.create_badge(
        db,
        user_id=user_id,
        title=JOURNEY_COMPLETION_BADGE_TITLE,
        badge_code=JOURNEY_COMPLETION_BADGE_CODE,
        badge_image_url=None,
        issued_by_user_id=issued_by_user_id,
    )

    log_action(
        db,
        actor_user_id=issued_by_user_id,
        action="badge_auto_issued",
        entity_type="badge",
        entity_id=obj.id,
    )
    return obj