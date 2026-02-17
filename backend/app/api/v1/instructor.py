from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.roles import require_roles
from app.deps.db import get_db  # <-- if your project uses a different path, change it
from app.schemas.journey import OnboardingSubmitIn, QuizSubmitIn, ScenarioSubmitIn, SubmissionOut
from app.services import instructor_service

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
