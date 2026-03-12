from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.badge import Badge


def create_badge(
    db: Session,
    *,
    user_id: int,
    title: str,
    badge_code: str | None,
    badge_image_url: str | None,
    issued_by_user_id: int | None,
) -> Badge:
    obj = Badge(
        user_id=user_id,
        title=title,
        badge_code=badge_code,
        badge_image_url=badge_image_url,
        issued_by_user_id=issued_by_user_id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_user_badges(
    db: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
):
    q = db.query(Badge).filter(Badge.user_id == user_id)

    total = q.count()
    items = (
        q.order_by(Badge.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items


def get_user_badge_by_title(
    db: Session,
    *,
    user_id: int,
    title: str,
) -> Badge | None:
    return (
        db.query(Badge)
        .filter(Badge.user_id == user_id, Badge.title == title)
        .first()
    )