from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel

from app.utils.enums import SubmissionStatus


class OnboardingHistoryItem(BaseModel):
    id: int
    reference_url: str
    created_at: datetime


class QuizHistoryItem(BaseModel):
    id: int
    score: float
    passed: bool
    status: SubmissionStatus
    attempt: int
    created_at: datetime


class ScenarioHistoryItem(BaseModel):
    id: int
    scenario_url: str
    status: SubmissionStatus
    version: int
    created_at: datetime


class OnboardingHistoryResponse(BaseModel):
    total: int
    items: list[OnboardingHistoryItem]


class QuizHistoryResponse(BaseModel):
    total: int
    items: list[QuizHistoryItem]


class ScenarioHistoryResponse(BaseModel):
    total: int
    items: list[ScenarioHistoryItem]
