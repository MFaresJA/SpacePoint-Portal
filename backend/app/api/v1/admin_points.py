from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.schemas.admin_points import AdminPointsAdjustIn, AdminPointsAdjustOut
from app.services.points_service import award_points
from app.services.audit_service import log_action

router = APIRouter()


@router.post("/points/adjust", response_model=AdminPointsAdjustOut)
def admin_adjust_points(
    payload: AdminPointsAdjustIn,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    award_points(
        db,
        user_id=payload.user_id,
        points=payload.points,
        reason=payload.reason.strip(),
        entity_type="manual_adjustment",
        entity_id=payload.user_id,
    )

    log_action(
        db,
        actor_user_id=admin.user_id,
        action="admin_points_adjusted",
        entity_type="user",
        entity_id=payload.user_id,
    )

    return {
        "message": "Points adjusted successfully",
        "user_id": payload.user_id,
        "points": payload.points,
        "reason": payload.reason.strip(),
    }