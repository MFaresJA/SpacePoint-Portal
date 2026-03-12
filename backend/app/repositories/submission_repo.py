from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.submissions import OnboardingSubmission, QuizSubmission, ScenarioSubmission, OnsiteLog
from app.utils.enums import SubmissionStatus, OnsiteLogStatus


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


def get_latest_onsite_log(db: Session, user_id: int) -> OnsiteLog | None:
    return (
        db.query(OnsiteLog)
        .filter(OnsiteLog.user_id == user_id)
        .order_by(OnsiteLog.created_at.desc())
        .first()
    )


def get_latest_verified_onsite_log(db: Session, user_id: int) -> OnsiteLog | None:
    return (
        db.query(OnsiteLog)
        .filter(
            OnsiteLog.user_id == user_id,
            OnsiteLog.status == OnsiteLogStatus.VERIFIED,
        )
        .order_by(OnsiteLog.created_at.desc())
        .first()
    )


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


def create_onsite_log(
    db: Session,
    user_id: int,
    session_type: str,
    notes: str | None,
    evidence_url: str,
) -> OnsiteLog:
    obj = OnsiteLog(
        user_id=user_id,
        session_type=session_type,
        notes=notes,
        evidence_url=evidence_url,
        status=OnsiteLogStatus.SUBMITTED,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_onsite_log_status(
    db: Session,
    onsite_log: OnsiteLog,
    *,
    status: OnsiteLogStatus,
) -> OnsiteLog:
    onsite_log.status = status
    db.add(onsite_log)
    db.commit()
    db.refresh(onsite_log)
    return onsite_log


def get_onsite_log_by_id(db: Session, onsite_log_id: int) -> OnsiteLog | None:
    return db.query(OnsiteLog).filter(OnsiteLog.id == onsite_log_id).first()


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


def list_onsite_logs(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[OnsiteLog]:
    return (
        db.query(OnsiteLog)
        .filter(OnsiteLog.user_id == user_id)
        .order_by(OnsiteLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

