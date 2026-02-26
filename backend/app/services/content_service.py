from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import content_repo, submission_repo


def _require_intro_unlocked(db: Session, user_id: int):
    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)
    if onboarding is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Intro slides are locked until you submit onboarding.",
        )

    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)
    if not approved_quiz or not approved_quiz.passed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Intro slides are locked until your quiz is approved and passed.",
        )

    if approved_quiz.created_at < onboarding.created_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Intro slides are locked: your approved quiz is older than your latest onboarding. Please resubmit quiz.",
        )


def _require_advanced_unlocked(db: Session, user_id: int):
    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)
    if not approved_quiz or not approved_quiz.passed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Advanced slides are locked until your quiz is approved and passed.",
        )

    approved_scenario = submission_repo.get_latest_approved_scenario(db=db, user_id=user_id)
    if not approved_scenario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Advanced slides are locked until your scenario is approved.",
        )

    if approved_scenario.created_at < approved_quiz.created_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Advanced slides are locked: your approved scenario is older than your latest approved quiz. Please resubmit scenario.",
        )


def get_intro_slides(db: Session, user_id: int):
    _require_intro_unlocked(db, user_id)
    items = content_repo.get_active_items_by_key(db, "intro-slides")
    content_repo.log_access(db, user_id=user_id, content_key="intro-slides")
    return {"key": "intro-slides", "items": items}


def get_advanced_slides(db: Session, user_id: int):
    _require_advanced_unlocked(db, user_id)
    items = content_repo.get_active_items_by_key(db, "advanced-slides")
    content_repo.log_access(db, user_id=user_id, content_key="advanced-slides")
    return {"key": "advanced-slides", "items": items}