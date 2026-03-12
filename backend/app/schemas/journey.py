from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

from app.utils.enums import SubmissionStatus, JourneyStep, OnsiteLogStatus


class OnboardingSubmitIn(BaseModel):
    reference_url: HttpUrl


class QuizSubmitIn(BaseModel):
    score: float = Field(..., ge=0)
    passed: bool


class ScenarioSubmitIn(BaseModel):
    scenario_url: HttpUrl


class OnsiteLogSubmitIn(BaseModel):
    session_type: str = Field(..., max_length=30)
    notes: str | None = None
    evidence_url: HttpUrl


class SubmissionOut(BaseModel):
    id: int
    status: SubmissionStatus
    created_at: datetime


class OnsiteLogOut(BaseModel):
    id: int
    session_type: str
    notes: str | None
    evidence_url: str
    status: OnsiteLogStatus
    created_at: datetime

    class Config:
        from_attributes = True


class JourneyProgressOut(BaseModel):
    current_state: JourneyStep
    completed_steps: list[JourneyStep]
    locked_steps: list[JourneyStep]
    locked_reasons: dict[str, str]