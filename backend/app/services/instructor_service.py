from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import submission_repo
from app.services.audit_service import log_action


def submit_onboarding(db: Session, user_id: int, reference_url: str):
    obj = submission_repo.create_onboarding(db=db, user_id=user_id, reference_url=reference_url)

    log_action(
        db,
        actor_user_id=user_id,
        action="onboarding_submitted",
        entity_type="onboarding",
        entity_id=obj.id,
    )
    return obj


def submit_quiz(db: Session, user_id: int, score: float, passed: bool):
    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)
    if onboarding is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding must be submitted before quiz.",
        )

    latest_quiz = submission_repo.get_latest_quiz(db=db, user_id=user_id)
    next_attempt = 1 if latest_quiz is None else (latest_quiz.attempt + 1)

    obj = submission_repo.create_quiz(
        db=db,
        user_id=user_id,
        score=score,
        passed=passed,
        attempt=next_attempt,
    )

    log_action(
        db,
        actor_user_id=user_id,
        action="quiz_submitted",
        entity_type="quiz",
        entity_id=obj.id,
    )
    return obj


def submit_scenario(db: Session, user_id: int, scenario_url: str):
    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)
    if approved_quiz is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz must be approved before submitting scenario.",
        )

    latest_scenario = submission_repo.get_latest_scenario(db=db, user_id=user_id)
    next_version = 1 if latest_scenario is None else (latest_scenario.version + 1)

    obj = submission_repo.create_scenario(
        db=db,
        user_id=user_id,
        scenario_url=scenario_url,
        version=next_version,
    )

    log_action(
        db,
        actor_user_id=user_id,
        action="scenario_submitted",
        entity_type="scenario",
        entity_id=obj.id,
    )
    return obj


def submit_onsite_log(
    db: Session,
    *,
    user_id: int,
    session_type: str,
    notes: str | None,
    evidence_url: str,
):
    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)
    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)
    approved_scenario = submission_repo.get_latest_approved_scenario(db=db, user_id=user_id)

    if onboarding is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding must be submitted first.",
        )

    if approved_quiz is None or not approved_quiz.passed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz must be approved and passed before submitting onsite logs.",
        )

    if approved_quiz.created_at < onboarding.created_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your approved quiz is older than your latest onboarding. Please resubmit quiz first.",
        )

    if approved_scenario is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Scenario must be approved before submitting onsite logs.",
        )

    if approved_scenario.created_at < approved_quiz.created_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your approved scenario is older than your latest approved quiz. Please resubmit scenario first.",
        )

    session_type = session_type.strip().upper()
    if session_type not in {"TRAINEE", "TRAINER"}:
        raise HTTPException(status_code=400, detail="session_type must be TRAINEE or TRAINER")

    evidence_url = evidence_url.strip()
    if not evidence_url:
        raise HTTPException(status_code=400, detail="evidence_url is required")

    obj = submission_repo.create_onsite_log(
        db=db,
        user_id=user_id,
        session_type=session_type,
        notes=notes.strip() if notes else None,
        evidence_url=evidence_url,
    )

    log_action(
        db,
        actor_user_id=user_id,
        action="onsite_log_submitted",
        entity_type="onsite_log",
        entity_id=obj.id,
    )
    return obj