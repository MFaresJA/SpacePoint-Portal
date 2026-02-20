from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.roles import require_roles
from app.deps.db import get_db  
from app.schemas.journey import OnboardingSubmitIn, QuizSubmitIn, ScenarioSubmitIn, SubmissionOut
from app.services import instructor_service

from app.services.journey_service import get_journey_progress
from app.schemas.journey import JourneyProgressOut

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


@router.get("/ping")
def instructor_ping(user=Depends(require_roles("instructor", "admin"))):
    return {"ok": True, "msg": "instructor access granted"}


@router.post("/onboarding", response_model=SubmissionOut)
def submit_onboarding(
    payload: OnboardingSubmitIn,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor")),
):
    obj = instructor_service.submit_onboarding(db=db, user_id=user.user_id, reference_url=str(payload.reference_url))
    return {"id": obj.id, "status": getattr(obj, "status", "PENDING"), "created_at": obj.created_at}


@router.post("/quiz", response_model=SubmissionOut)
def submit_quiz(
    payload: QuizSubmitIn,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor")),
):
    obj = instructor_service.submit_quiz(db=db, user_id=user.user_id, score=payload.score, passed=payload.passed)
    return {"id": obj.id, "status": obj.status, "created_at": obj.created_at}


@router.post("/scenario", response_model=SubmissionOut)
def submit_scenario(
    payload: ScenarioSubmitIn,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor")),
):
    obj = instructor_service.submit_scenario(db=db, user_id=user.user_id, scenario_url=str(payload.scenario_url))
    return {"id": obj.id, "status": obj.status, "created_at": obj.created_at}

@router.get("/journey/progress", response_model=JourneyProgressOut)
def journey_progress(
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_journey_progress(db=db, user_id=user.user_id)

@router.get("/submissions/onboarding", response_model=OnboardingHistoryResponse)
def onboarding_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_onboarding_history(db=db, user_id=user.user_id, skip=skip, limit=limit)


@router.get("/submissions/quiz", response_model=QuizHistoryResponse)
def quiz_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_quiz_history(db=db, user_id=user.user_id, skip=skip, limit=limit)


@router.get("/submissions/scenario", response_model=ScenarioHistoryResponse)
def scenario_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_scenario_history(db=db, user_id=user.user_id, skip=skip, limit=limit)
