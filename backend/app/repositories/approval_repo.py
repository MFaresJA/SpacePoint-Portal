from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.approvals import Approval


def create_approval(
    db: Session,
    *,
    entity_type: str,
    entity_id: int,
    decision: str,
    reason: str | None,
    approved_by_user_id: int | None,
) -> Approval:
    row = Approval(
        entity_type=entity_type,
        entity_id=entity_id,
        decision=decision,
        reason=reason.strip() if reason else None,
        approved_by_user_id=approved_by_user_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_approvals(
    db: Session,
    *,
    entity_type: str | None = None,
    entity_id: int | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Approval]:
    q = db.query(Approval)

    if entity_type is not None:
        q = q.filter(Approval.entity_type == entity_type)
    if entity_id is not None:
        q = q.filter(Approval.entity_id == entity_id)

    return (
        q.order_by(Approval.id.desc())
        .offset(max(offset, 0))
        .limit(min(max(limit, 1), 200))
        .all()
    )