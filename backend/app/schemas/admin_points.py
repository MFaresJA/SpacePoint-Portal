from pydantic import BaseModel, Field


class AdminPointsAdjustIn(BaseModel):
    user_id: int
    points: int = Field(..., description="Positive to grant, negative to deduct")
    reason: str = Field(..., min_length=1, max_length=200)


class AdminPointsAdjustOut(BaseModel):
    message: str
    user_id: int
    points: int
    reason: str