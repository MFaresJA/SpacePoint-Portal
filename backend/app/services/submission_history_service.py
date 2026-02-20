from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import submission_repo
from app.schemas.submission_history import (
    OnboardingHistoryResponse,
    QuizHistoryResponse,
    ScenarioHistoryResponse,
    OnboardingHistoryItem,
    QuizHistoryItem,
    ScenarioHistoryItem,
)


def get_onboarding_history(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> OnboardingHistoryResponse:
    items = submission_repo.list_onboarding(db=db, user_id=user_id, skip=skip, limit=limit)
    return OnboardingHistoryResponse(
        total=len(items),
        items=[
            OnboardingHistoryItem(id=i.id, reference_url=i.reference_url, created_at=i.created_at)
            for i in items
        ],
    )


def get_quiz_history(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> QuizHistoryResponse:
    items = submission_repo.list_quizzes(db=db, user_id=user_id, skip=skip, limit=limit)
    return QuizHistoryResponse(
        total=len(items),
        items=[
            QuizHistoryItem(
                id=i.id,
                score=i.score,
                passed=i.passed,
                status=i.status,
                attempt=i.attempt,
                created_at=i.created_at,
            )
            for i in items
        ],
    )


def get_scenario_history(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> ScenarioHistoryResponse:
    items = submission_repo.list_scenarios(db=db, user_id=user_id, skip=skip, limit=limit)
    return ScenarioHistoryResponse(
        total=len(items),
        items=[
            ScenarioHistoryItem(
                id=i.id,
                scenario_url=i.scenario_url,
                status=i.status,
                version=i.version,
                created_at=i.created_at,
            )
            for i in items
        ],
    )
