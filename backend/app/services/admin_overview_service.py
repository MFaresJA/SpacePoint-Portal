from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.submissions import QuizSubmission, ScenarioSubmission, OnsiteLog
from app.models.ambassador import RecruitmentEntry, ImpactReport
from app.models.intern import ChallengeSubmission
from app.models.certificate import Certificate
from app.models.badge import Badge
from app.models.opportunity import Opportunity
from app.models.content import ContentAccessLog
from app.models.crm import CRMLead
from app.models.crm_proposal import CRMProposal
from app.models.points import PointsLedger
from app.schemas.admin_overview import (
    AdminOverviewResponse,
    OverviewUsersBlock,
    OverviewPendingBlock,
    OverviewRecognitionBlock,
    OverviewEngagementBlock,
    OverviewLeaderboardBlock,
    OverviewLeaderboardItem,
)


def get_admin_overview(db: Session) -> AdminOverviewResponse:
    users_total = db.query(func.count(User.user_id)).scalar() or 0
    users_verified = db.query(func.count(User.user_id)).filter(User.is_verified.is_(True)).scalar() or 0
    users_suspended = db.query(func.count(User.user_id)).filter(User.is_suspended.is_(True)).scalar() or 0

    pending_quizzes = db.query(func.count(QuizSubmission.id)).filter(QuizSubmission.status == "PENDING").scalar() or 0
    pending_scenarios = db.query(func.count(ScenarioSubmission.id)).filter(ScenarioSubmission.status == "PENDING").scalar() or 0
    pending_onsite_logs = db.query(func.count(OnsiteLog.id)).filter(OnsiteLog.status == "SUBMITTED").scalar() or 0
    pending_crm_leads = db.query(func.count(CRMLead.id)).filter(CRMLead.status == "SUBMITTED").scalar() or 0
    pending_crm_proposals = db.query(func.count(CRMProposal.id)).filter(CRMProposal.status == "SUBMITTED").scalar() or 0
    pending_recruitment = db.query(func.count(RecruitmentEntry.id)).filter(RecruitmentEntry.status == "PENDING").scalar() or 0
    pending_impact_reports = db.query(func.count(ImpactReport.id)).filter(ImpactReport.status == "PENDING").scalar() or 0
    pending_intern_submissions = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.status == "PENDING").scalar() or 0

    total_certificates = db.query(func.count(Certificate.id)).scalar() or 0
    total_badges = db.query(func.count(Badge.id)).scalar() or 0

    total_opportunities = db.query(func.count(Opportunity.id)).scalar() or 0
    active_opportunities = db.query(func.count(Opportunity.id)).filter(Opportunity.is_active.is_(True)).scalar() or 0
    total_content_access_logs = db.query(func.count(ContentAccessLog.id)).scalar() or 0

    leaderboard_rows = (
        db.query(
            PointsLedger.user_id,
            func.coalesce(func.sum(PointsLedger.points), 0).label("total_points"),
            User.email,
        )
        .join(User, User.user_id == PointsLedger.user_id)
        .group_by(PointsLedger.user_id, User.email)
        .order_by(func.coalesce(func.sum(PointsLedger.points), 0).desc())
        .limit(3)
        .all()
    )

    top_users = [
        OverviewLeaderboardItem(
            user_id=int(row.user_id),
            email=row.email,
            total_points=int(row.total_points or 0),
        )
        for row in leaderboard_rows
    ]

    return AdminOverviewResponse(
        users=OverviewUsersBlock(
            total=int(users_total),
            verified=int(users_verified),
            suspended=int(users_suspended),
        ),
        pending=OverviewPendingBlock(
            quizzes=int(pending_quizzes),
            scenarios=int(pending_scenarios),
            onsite_logs=int(pending_onsite_logs),
            crm_leads=int(pending_crm_leads),
            crm_proposals=int(pending_crm_proposals),
            recruitment=int(pending_recruitment),
            impact_reports=int(pending_impact_reports),
            intern_submissions=int(pending_intern_submissions),
        ),
        recognition=OverviewRecognitionBlock(
            certificates=int(total_certificates),
            badges=int(total_badges),
        ),
        engagement=OverviewEngagementBlock(
            opportunities_total=int(total_opportunities),
            opportunities_active=int(active_opportunities),
            content_access_logs=int(total_content_access_logs),
        ),
        leaderboard=OverviewLeaderboardBlock(
            top_users=top_users,
        ),
    )