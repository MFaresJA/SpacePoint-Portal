from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.points import PointsLedger
from app.models.role import Role
from app.models.user_role import UserRole


def add_points(
    db: Session,
    *,
    user_id: int,
    points: int,
    reason: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
) -> PointsLedger | None:
    row = PointsLedger(
        user_id=user_id,
        points=points,
        reason=reason,
        entity_type=entity_type,
        entity_id=entity_id,
    )
    db.add(row)

    try:
        db.commit()
        db.refresh(row)
        return row
    except IntegrityError:
        db.rollback()

        if entity_type is not None and entity_id is not None:
            existing = (
                db.query(PointsLedger)
                .filter(
                    PointsLedger.entity_type == entity_type,
                    PointsLedger.entity_id == entity_id,
                    PointsLedger.reason == reason,
                )
                .order_by(PointsLedger.id.desc())
                .first()
            )
            return existing

        return None


def _leaderboard_base_query(db: Session, role: str | None = None):
    q = db.query(
        PointsLedger.user_id,
        func.coalesce(func.sum(PointsLedger.points), 0).label("total_points"),
    )

    if role:
        q = (
            q.join(UserRole, UserRole.user_id == PointsLedger.user_id)
             .join(Role, Role.role_id == UserRole.role_id)
             .filter(func.lower(Role.name) == role.lower())
        )

    return q.group_by(PointsLedger.user_id)


def get_user_total_points(db: Session, user_id: int) -> int:
    total = (
        db.query(func.coalesce(func.sum(PointsLedger.points), 0))
        .filter(PointsLedger.user_id == user_id)
        .scalar()
    )
    return int(total or 0)


def get_leaderboard(
    db: Session,
    *,
    limit: int = 20,
    offset: int = 0,
    role: str | None = None,
) -> list[tuple[int, int]]:
    rows = (
        _leaderboard_base_query(db, role=role)
        .order_by(func.coalesce(func.sum(PointsLedger.points), 0).desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [(int(uid), int(tp)) for uid, tp in rows]


def get_leaderboard_total_users(db: Session, role: str | None = None) -> int:
    subq = _leaderboard_base_query(db, role=role).subquery()
    cnt = db.query(func.count()).select_from(subq).scalar()
    return int(cnt or 0)


def get_user_rank(db: Session, user_id: int, role: str | None = None) -> int | None:
    base = _leaderboard_base_query(db, role=role).subquery()

    my_row = db.query(base.c.user_id, base.c.total_points).filter(base.c.user_id == user_id).first()
    if not my_row:
        return None

    user_total = int(my_row.total_points or 0)

    higher_count = (
        db.query(func.count())
        .select_from(base)
        .filter(base.c.total_points > user_total)
        .scalar()
    )

    return int(higher_count or 0) + 1


def list_user_ledger(db: Session, user_id: int, limit: int = 50, offset: int = 0):
    return (
        db.query(PointsLedger)
        .filter(PointsLedger.user_id == user_id)
        .order_by(PointsLedger.created_at.desc(), PointsLedger.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_user_ledger(db: Session, user_id: int) -> int:
    cnt = db.query(func.count(PointsLedger.id)).filter(PointsLedger.user_id == user_id).scalar()
    return int(cnt or 0)