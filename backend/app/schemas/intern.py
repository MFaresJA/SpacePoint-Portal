from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, Field


# -------- Challenges --------

class ChallengeOut(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str | None
    due_date: date | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChallengesListResponse(BaseModel):
    total: int
    items: list[ChallengeOut]


class AdminChallengeCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str
    difficulty: str | None = Field(None, max_length=30)
    due_date: date | None = None
    is_active: bool = True


# -------- Submissions --------

class SubmissionCreate(BaseModel):
    challenge_id: int
    solution_url: str = Field(..., max_length=500)
    notes: str | None = Field(None, max_length=1000)


class SubmissionOut(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    solution_url: str
    notes: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubmissionsListResponse(BaseModel):
    total: int
    items: list[SubmissionOut]


class AdminReviewSubmissionIn(BaseModel):
    decision: str  # APPROVED / REJECTED
    feedback: str | None = Field(None, max_length=2000)


# -------- Todos --------

class TodoCreate(BaseModel):
    title: str = Field(..., max_length=300)


class TodoUpdate(BaseModel):
    title: str | None = Field(None, max_length=300)
    status: str | None = Field(None, max_length=30)  # TODO/IN_PROGRESS/DONE


class TodoOut(BaseModel):
    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodosListResponse(BaseModel):
    total: int
    items: list[TodoOut]


# -------- Progress --------

class InternProgressOut(BaseModel):
    total_submissions: int
    pending: int
    approved: int
    rejected: int
    todos_total: int
    todos_done: int