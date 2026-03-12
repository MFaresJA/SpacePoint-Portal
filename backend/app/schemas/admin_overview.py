from __future__ import annotations

from pydantic import BaseModel


class OverviewUsersBlock(BaseModel):
    total: int
    verified: int
    suspended: int


class OverviewPendingBlock(BaseModel):
    quizzes: int
    scenarios: int
    onsite_logs: int
    crm_leads: int
    crm_proposals: int
    recruitment: int
    impact_reports: int
    intern_submissions: int


class OverviewRecognitionBlock(BaseModel):
    certificates: int
    badges: int


class OverviewEngagementBlock(BaseModel):
    opportunities_total: int
    opportunities_active: int
    content_access_logs: int


class OverviewLeaderboardItem(BaseModel):
    user_id: int
    email: str
    total_points: int


class OverviewLeaderboardBlock(BaseModel):
    top_users: list[OverviewLeaderboardItem]


class AdminOverviewResponse(BaseModel):
    users: OverviewUsersBlock
    pending: OverviewPendingBlock
    recognition: OverviewRecognitionBlock
    engagement: OverviewEngagementBlock
    leaderboard: OverviewLeaderboardBlock