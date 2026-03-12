from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import audit_repo


def log_action(
    db: Session,
    *,
    actor_user_id: int | None,
    action: str,
    entity_type: str,
    entity_id: int | None = None,
):
    return audit_repo.create_audit_log(
        db,
        actor_user_id=actor_user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
    )