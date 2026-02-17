from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

from app.utils.enums import SubmissionStatus, JourneyStep


class OnboardingSubmitIn(BaseModel):
    reference_url: HttpUrl


class QuizSubmitIn(BaseModel):
    score: float = Field(..., ge=0)
    passed: bool


class ScenarioSubmitIn(BaseModel):
    scenario_url: HttpUrl


class SubmissionOut(BaseModel):
    id: int
    status: SubmissionStatus
    created_at: datetime


class JourneyProgressOut(BaseModel):
    current_state: JourneyStep
    completed_steps: list[JourneyStep]
    locked_steps: list[JourneyStep]
    locked_reasons: dict[str, str]
