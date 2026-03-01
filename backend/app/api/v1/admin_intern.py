from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import intern_repo
from app.schemas.intern import (
    AdminChallengeCreate,
    ChallengeOut,
    ChallengesListResponse,
    SubmissionsListResponse,
    SubmissionOut,
    AdminReviewSubmissionIn,
)
from app.services.intern_service import admin_create_challenge, admin_review_submission

router = APIRouter()


@router.post("/challenges", response_model=ChallengeOut)
def create_challenge(
    payload: AdminChallengeCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    return admin_create_challenge(
        db,
        title=payload.title,
        description=payload.description,
        difficulty=payload.difficulty,
        due_date=payload.due_date,
        is_active=payload.is_active,
    )


@router.get("/intern/submissions", response_model=SubmissionsListResponse)
def list_all_submissions(
    skip: int = 0,
    limit: int = 50,
    status: str | None = "PENDING",
    db: Session = Depends(get_db),
    _=Depends(require_roles("admin")),
):
    total, items = intern_repo.list_submissions(db, skip=skip, limit=limit, user_id=None, status=status.upper() if status else None)
    return {"total": total, "items": items}


@router.patch("/intern/submissions/{submission_id}", response_model=SubmissionOut)
def review_submission(
    submission_id: int,
    payload: AdminReviewSubmissionIn,
    db: Session = Depends(get_db),
    admin_user=Depends(require_roles("admin")),
):
    return admin_review_submission(
        db,
        reviewer_user_id=admin_user.user_id,
        submission_id=submission_id,
        decision=payload.decision,
        feedback=payload.feedback,
    )