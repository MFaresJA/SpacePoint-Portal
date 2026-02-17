from pydantic import BaseModel, Field


class ApprovalDecisionIn(BaseModel):
    decision: str = Field(..., pattern="^(APPROVED|REJECTED)$")
    reason: str | None = None
