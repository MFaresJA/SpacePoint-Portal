from fastapi import APIRouter, Depends
from app.deps.roles import require_roles

from sqlalchemy.orm import Session

from app.deps.db import get_db


from app.schemas.roles import RolesListResponse, RoleActionResponse
from app.services.role_service import (
    list_user_roles,
    assign_role_to_user,
    remove_role_from_user,
)

from app.schemas.roles import UserStatusResponse
from app.services.role_service import (
    set_user_active,
    set_user_verified,
    set_user_suspended,
)

from app.schemas.users import AdminUsersListResponse
from app.services.admin_user_service import list_users_with_roles, get_user_detail

from app.schemas.admin import AdminUserDetailResponse
#from app.services.admin_user_service import get_user_detail
from app.schemas.approvals import ApprovalDecisionIn
from app.services.approval_service import decide_quiz, decide_scenario

from app.schemas.admin_approvals import PendingApprovalsResponse
from app.services.admin_approval_service import get_pending_approvals

from app.schemas.journey import JourneyProgressOut
from app.services.journey_service import get_journey_progress

from app.schemas.submission_history import (
    OnboardingHistoryResponse,
    QuizHistoryResponse,
    ScenarioHistoryResponse,
)
from app.services.submission_history_service import (
    get_onboarding_history,
    get_quiz_history,
    get_scenario_history,
)

router = APIRouter()

#@router.get("/ping")
#def admin_ping(user = Depends(require_roles("admin"))):
#    return {"ok": True, "msg": "admin access granted"}


@router.get("/ping")
def admin_ping(_: dict = Depends(require_roles("admin"))):
    return {"status": "ok", "role": "admin"}

@router.get("/users", response_model=AdminUsersListResponse)
def admin_list_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    # safety caps
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = list_users_with_roles(db, skip=skip, limit=limit)
    return {"total": total, "items": items}

@router.get("/users/{user_id}/roles", response_model=RolesListResponse)
def admin_list_roles(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    roles = list_user_roles(db, user_id)
    return {"user_id": user_id, "roles": roles}

@router.post("/users/{user_id}/roles/{role_name}", response_model=RoleActionResponse)
def admin_assign_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return assign_role_to_user(db, user_id, role_name)

@router.delete("/users/{user_id}/roles/{role_name}", response_model=RoleActionResponse)
def admin_remove_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return remove_role_from_user(db, user_id, role_name)

@router.patch("/users/{user_id}/activate", response_model=UserStatusResponse)
def admin_activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return set_user_active(db, user_id, True)


@router.patch("/users/{user_id}/deactivate", response_model=UserStatusResponse)
def admin_deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return set_user_active(db, user_id, False)


@router.patch("/users/{user_id}/verify", response_model=UserStatusResponse)
def admin_verify_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return set_user_verified(db, user_id, True)


@router.patch("/users/{user_id}/suspend", response_model=UserStatusResponse)
def admin_suspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return set_user_suspended(db, user_id, True)


@router.patch("/users/{user_id}/unsuspend", response_model=UserStatusResponse)
def admin_unsuspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return set_user_suspended(db, user_id, False)

@router.get("/users/{user_id}", response_model=AdminUserDetailResponse)
def admin_get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return get_user_detail(db, user_id)

@router.post("/approvals/quiz/{quiz_id}")
def admin_decide_quiz(
    quiz_id: int,
    payload: ApprovalDecisionIn,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    return decide_quiz(
        db=db,
        admin_user_id=admin.user_id,
        quiz_id=quiz_id,
        decision=payload.decision,
        reason=payload.reason,
    )


@router.post("/approvals/scenario/{scenario_id}")
def admin_decide_scenario(
    scenario_id: int,
    payload: ApprovalDecisionIn,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    return decide_scenario(
        db=db,
        admin_user_id=admin.user_id,
        scenario_id=scenario_id,
        decision=payload.decision,
        reason=payload.reason,
    )

@router.get("/approvals/pending", response_model=PendingApprovalsResponse)
def admin_list_pending_approvals(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    return get_pending_approvals(db=db, skip=skip, limit=limit)

@router.get("/users/{user_id}/journey/progress", response_model=JourneyProgressOut)
def admin_get_user_journey_progress(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return get_journey_progress(db=db, user_id=user_id)

@router.get("/users/{user_id}/submissions/onboarding", response_model=OnboardingHistoryResponse)
def admin_get_user_onboarding_history(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    return get_onboarding_history(db=db, user_id=user_id, skip=skip, limit=limit)

@router.get("/users/{user_id}/submissions/quiz", response_model=QuizHistoryResponse)
def admin_get_user_quiz_history(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    return get_quiz_history(db=db, user_id=user_id, skip=skip, limit=limit)

@router.get("/users/{user_id}/submissions/scenario", response_model=ScenarioHistoryResponse)
def admin_get_user_scenario_history(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    return get_scenario_history(db=db, user_id=user_id, skip=skip, limit=limit)
