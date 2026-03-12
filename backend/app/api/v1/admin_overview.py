from __future__ import annotations

from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.models.user import User
from app.models.application import Application
from app.models.ambassador import RecruitmentEntry, ImpactReport
from app.models.intern import ChallengeSubmission

router = APIRouter()


@router.get("/overview")
def admin_overview(
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    total_users = db.query(func.count(User.user_id)).scalar() or 0
    verified_users = db.query(func.count(User.user_id)).filter(User.is_verified.is_(True)).scalar() or 0
    suspended_users = db.query(func.count(User.user_id)).filter(User.is_suspended.is_(True)).scalar() or 0

    pending_applications = db.query(func.count(Application.id)).filter(Application.status == "SUBMITTED").scalar() or 0
    pending_recruitment = db.query(func.count(RecruitmentEntry.id)).filter(RecruitmentEntry.status == "PENDING").scalar() or 0
    pending_impact = db.query(func.count(ImpactReport.id)).filter(ImpactReport.status == "PENDING").scalar() or 0
    pending_intern_submissions = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.status == "PENDING").scalar() or 0

    return {
        "users": {
            "total": int(total_users),
            "verified": int(verified_users),
            "suspended": int(suspended_users),
        },
        "pending": {
            "applications": int(pending_applications),
            "recruitment": int(pending_recruitment),
            "impact_reports": int(pending_impact),
            "intern_submissions": int(pending_intern_submissions),
        },
    }