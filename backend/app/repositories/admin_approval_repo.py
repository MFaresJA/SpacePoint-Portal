from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.submissions import QuizSubmission, ScenarioSubmission
from app.utils.enums import SubmissionStatus


def list_pending_quiz(db: Session, skip: int = 0, limit: int = 50) -> list[QuizSubmission]:
    return (
        db.query(QuizSubmission)
        .filter(QuizSubmission.status == SubmissionStatus.PENDING)
        .order_by(QuizSubmission.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_pending_scenario(db: Session, skip: int = 0, limit: int = 50) -> list[ScenarioSubmission]:
    return (
        db.query(ScenarioSubmission)
        .filter(ScenarioSubmission.status == SubmissionStatus.PENDING)
        .order_by(ScenarioSubmission.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
