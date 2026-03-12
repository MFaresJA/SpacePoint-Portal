from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import points_repo


def award_points(
    db: Session,
    *,
    user_id: int,
    points: int,
    reason: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
):
    # basic safety
    if points == 0:
        return None
    if not reason or not reason.strip():
        reason = "points_awarded"

    return points_repo.add_points(
        db,
        user_id=user_id,
        points=points,
        reason=reason.strip(),
        entity_type=entity_type,
        entity_id=entity_id,
    )