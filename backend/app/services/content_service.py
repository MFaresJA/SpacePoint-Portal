from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.submissions import QuizSubmission, ScenarioSubmission
from app.utils.enums import SubmissionStatus
from app.repositories import content_repo


def _require_quiz_approved(db: Session, user_id: int):
    approved = (
        db.query(QuizSubmission)
        .filter(
            QuizSubmission.user_id == user_id,
            QuizSubmission.status == SubmissionStatus.APPROVED,
        )
        .order_by(QuizSubmission.id.desc())
        .first()
    )
    if not approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Intro slides are locked until your quiz is approved.",
        )


def _require_scenario_approved(db: Session, user_id: int):
    approved = (
        db.query(ScenarioSubmission)
        .filter(
            ScenarioSubmission.user_id == user_id,
            ScenarioSubmission.status == SubmissionStatus.APPROVED,
        )
        .order_by(ScenarioSubmission.id.desc())
        .first()
    )
    if not approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Advanced slides are locked until your scenario is approved.",
        )


def get_intro_slides(db: Session, user_id: int):
    _require_quiz_approved(db, user_id)
    items = content_repo.get_active_items_by_key(db, "intro-slides")
    content_repo.log_access(db, user_id=user_id, content_key="intro-slides")
    return {"key": "intro-slides", "items": items}


def get_advanced_slides(db: Session, user_id: int):
    _require_scenario_approved(db, user_id)
    items = content_repo.get_active_items_by_key(db, "advanced-slides")
    content_repo.log_access(db, user_id=user_id, content_key="advanced-slides")
    return {"key": "advanced-slides", "items": items}
