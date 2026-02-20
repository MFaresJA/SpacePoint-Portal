from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.submissions import OnboardingSubmission, QuizSubmission, ScenarioSubmission
from app.utils.enums import SubmissionStatus


# ---------- Read helpers (latest records) ----------

def get_latest_onboarding(db: Session, user_id: int) -> OnboardingSubmission | None:
    return (
        db.query(OnboardingSubmission)
        .filter(OnboardingSubmission.user_id == user_id)
        .order_by(OnboardingSubmission.created_at.desc())
        .first()
    )


def get_latest_quiz(db: Session, user_id: int) -> QuizSubmission | None:
    return (
        db.query(QuizSubmission)
        .filter(QuizSubmission.user_id == user_id)
        .order_by(QuizSubmission.created_at.desc())
        .first()
    )


def get_latest_approved_quiz(db: Session, user_id: int) -> QuizSubmission | None:
    return (
        db.query(QuizSubmission)
        .filter(
            QuizSubmission.user_id == user_id,
            QuizSubmission.status == SubmissionStatus.APPROVED,
        )
        .order_by(QuizSubmission.created_at.desc())
        .first()
    )


def get_latest_scenario(db: Session, user_id: int) -> ScenarioSubmission | None:
    return (
        db.query(ScenarioSubmission)
        .filter(ScenarioSubmission.user_id == user_id)
        .order_by(ScenarioSubmission.created_at.desc())
        .first()
    )


def get_latest_approved_scenario(db: Session, user_id: int) -> ScenarioSubmission | None:
    return (
        db.query(ScenarioSubmission)
        .filter(
            ScenarioSubmission.user_id == user_id,
            ScenarioSubmission.status == SubmissionStatus.APPROVED,
        )
        .order_by(ScenarioSubmission.created_at.desc())
        .first()
    )


# ---------- Create helpers (new submissions) ----------

def create_onboarding(db: Session, user_id: int, reference_url: str) -> OnboardingSubmission:
    obj = OnboardingSubmission(user_id=user_id, reference_url=reference_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_quiz(db: Session, user_id: int, score: float, passed: bool, attempt: int) -> QuizSubmission:
    obj = QuizSubmission(
        user_id=user_id,
        score=score,
        passed=passed,
        status=SubmissionStatus.PENDING,
        attempt=attempt,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_scenario(db: Session, user_id: int, scenario_url: str, version: int) -> ScenarioSubmission:
    obj = ScenarioSubmission(
        user_id=user_id,
        scenario_url=scenario_url,
        status=SubmissionStatus.PENDING,
        version=version,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_onboarding(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[OnboardingSubmission]:
    return (
        db.query(OnboardingSubmission)
        .filter(OnboardingSubmission.user_id == user_id)
        .order_by(OnboardingSubmission.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_quizzes(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[QuizSubmission]:
    return (
        db.query(QuizSubmission)
        .filter(QuizSubmission.user_id == user_id)
        .order_by(QuizSubmission.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_scenarios(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[ScenarioSubmission]:
    return (
        db.query(ScenarioSubmission)
        .filter(ScenarioSubmission.user_id == user_id)
        .order_by(ScenarioSubmission.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
