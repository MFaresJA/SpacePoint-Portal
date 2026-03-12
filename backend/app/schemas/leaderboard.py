from __future__ import annotations

from pydantic import BaseModel, EmailStr


class LeaderboardRow(BaseModel):
    user_id: int
    email: EmailStr
    total_points: int


class LeaderboardResponse(BaseModel):
    total: int
    items: list[LeaderboardRow]


class MyLeaderboardResponse(BaseModel):
    user_id: int
    email: EmailStr
    total_points: int
    rank: int | None