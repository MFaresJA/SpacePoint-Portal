from __future__ import annotations

from pydantic import BaseModel

from app.schemas.user import UserOut
from app.schemas.journey import JourneyProgressOut
from app.schemas.submission_history import (
    OnboardingHistoryResponse,
    QuizHistoryResponse,
    ScenarioHistoryResponse,
)


class AdminUserReviewResponse(BaseModel):
    user: UserOut
    roles: list[str]
    journey: JourneyProgressOut
    onboarding: OnboardingHistoryResponse
    quizzes: QuizHistoryResponse
    scenarios: ScenarioHistoryResponse