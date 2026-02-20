from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from app.utils.enums import SubmissionStatus


EntityType = Literal["quiz", "scenario"]


class PendingApprovalItem(BaseModel):
    entity_type: EntityType
    entity_id: int
    user_id: int
    status: SubmissionStatus
    created_at: datetime

    # quiz-only fields
    score: Optional[float] = None
    passed: Optional[bool] = None
    attempt: Optional[int] = None

    # scenario-only fields
    scenario_url: Optional[str] = None
    version: Optional[int] = None


class PendingApprovalsResponse(BaseModel):
    total: int
    items: list[PendingApprovalItem]
