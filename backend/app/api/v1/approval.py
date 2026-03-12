# app/api/v1/approvals.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.approval import ApprovalDecisionIn
from app.services.approval_service import decide_quiz, decide_scenario

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("/quiz/{quiz_id}")
def approve_quiz(
    quiz_id: int,
    payload: ApprovalDecisionIn,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    # NOTE: enforce admin role here later if you have RBAC dependency
    return decide_quiz(
        db,
        admin_user_id=me.user_id,
        quiz_id=quiz_id,
        decision=payload.decision,
        reason=payload.reason,
    )


@router.post("/scenario/{scenario_id}")
def approve_scenario(
    scenario_id: int,
    payload: ApprovalDecisionIn,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    # NOTE: enforce admin role here later if you have RBAC dependency
    return decide_scenario(
        db,
        admin_user_id=me.user_id,
        scenario_id=scenario_id,
        decision=payload.decision,
        reason=payload.reason,
    )