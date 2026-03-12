from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ContentAccessLogOut(BaseModel):
    id: int
    user_id: int
    content_key: str
    accessed_at: datetime

    class Config:
        from_attributes = True


class ContentAccessLogsResponse(BaseModel):
    total: int
    items: list[ContentAccessLogOut]