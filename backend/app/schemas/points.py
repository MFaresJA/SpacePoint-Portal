from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class PointsLedgerRow(BaseModel):
    id: int
    user_id: int
    points: int
    reason: str
    entity_type: str | None = None
    entity_id: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class PointsHistoryResponse(BaseModel):
    total: int
    items: list[PointsLedgerRow]