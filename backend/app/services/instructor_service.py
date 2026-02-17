from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import submission_repo


def submit_onboarding(db: Session, user_id: int, reference_url: str):
    # No gating for onboarding
    return submission_repo.create_onboarding(db=db, user_id=user_id, reference_url=reference_url)


def submit_quiz(db: Session, user_id: int, score: float, passed: bool):
    # Gate: must have onboarding submitted
    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)
    if onboarding is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding must be submitted before quiz.",
        )

    latest_quiz = submission_repo.get_latest_quiz(db=db, user_id=user_id)
    next_attempt = 1 if latest_quiz is None else (latest_quiz.attempt + 1)

    return submission_repo.create_quiz(
        db=db,
        user_id=user_id,
        score=score,
        passed=passed,
        attempt=next_attempt,
    )


def submit_scenario(db: Session, user_id: int, scenario_url: str):
    # Gate: must have an APPROVED quiz
    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)
    if approved_quiz is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz must be approved before submitting scenario.",
        )

    latest_scenario = submission_repo.get_latest_scenario(db=db, user_id=user_id)
    next_version = 1 if latest_scenario is None else (latest_scenario.version + 1)

    return submission_repo.create_scenario(
        db=db,
        user_id=user_id,
        scenario_url=scenario_url,
        version=next_version,
    )
