from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.repositories import points_repo
from app.schemas.leaderboard import LeaderboardResponse, LeaderboardRow, MyLeaderboardResponse

router = APIRouter()


@router.get("", response_model=LeaderboardResponse)
def leaderboard(
    limit: int = 20,
    offset: int = 0,
    role: str | None = None,
    db: Session = Depends(get_db),
):
    if limit > 100:
        limit = 100
    if offset < 0:
        offset = 0

    pairs = points_repo.get_leaderboard(db, limit=limit, offset=offset, role=role)
    total = points_repo.get_leaderboard_total_users(db, role=role)

    user_ids = [uid for uid, _ in pairs]
    users = db.query(User).filter(User.user_id.in_(user_ids)).all()
    email_map = {u.user_id: u.email for u in users}

    items = [
        LeaderboardRow(user_id=uid, email=email_map.get(uid, "unknown@example.com"), total_points=tp)
        for uid, tp in pairs
    ]
    return {"total": total, "items": items}


@router.get("/me", response_model=MyLeaderboardResponse)
def my_points(
    role: str | None = None,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    total = points_repo.get_user_total_points(db, me.user_id)
    rank = points_repo.get_user_rank(db, me.user_id, role=role)
    return {"user_id": me.user_id, "email": me.email, "total_points": total, "rank": rank}