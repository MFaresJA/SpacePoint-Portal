from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.repositories import points_repo
from app.schemas.points import PointsHistoryResponse, PointsLedgerRow

from app.deps.roles import require_roles


router = APIRouter(prefix="/points", tags=["Points"])


@router.get("/me/history", response_model=PointsHistoryResponse)
def my_points_history(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0

    rows = points_repo.list_user_ledger(db, user_id=me.user_id, limit=limit, offset=offset)
    total = points_repo.count_user_ledger(db, user_id=me.user_id)

    return {
        "total": total,
        "items": [PointsLedgerRow.model_validate(r) for r in rows],
    }


@router.get("/user/{user_id}/history", response_model=PointsHistoryResponse)
def user_points_history_admin(
    user_id: int,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0

    rows = points_repo.list_user_ledger(db, user_id=user_id, limit=limit, offset=offset)
    total = points_repo.count_user_ledger(db, user_id=user_id)

    return {
        "total": total,
        "items": [PointsLedgerRow.model_validate(r) for r in rows],
    }