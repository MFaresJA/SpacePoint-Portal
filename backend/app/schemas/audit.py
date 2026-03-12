from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class AuditLogOut(BaseModel):
    id: int
    actor_user_id: int | None
    action: str
    entity_type: str
    entity_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogsResponse(BaseModel):
    total: int
    items: list[AuditLogOut]