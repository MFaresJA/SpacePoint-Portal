from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import intern_repo


_ALLOWED_SUB_STATUSES = {"PENDING", "APPROVED", "REJECTED"}
_ALLOWED_TODO_STATUSES = {"TODO", "IN_PROGRESS", "DONE"}


def intern_submit_solution(
    db: Session,
    *,
    user_id: int,
    challenge_id: int,
    solution_url: str,
    notes: str | None,
):
    ch = intern_repo.get_challenge(db, challenge_id)
    if not ch or not ch.is_active:
        raise HTTPException(status_code=404, detail="Challenge not found or inactive")

    solution_url = solution_url.strip()
    if not solution_url:
        raise HTTPException(status_code=400, detail="solution_url is required")

    return intern_repo.create_submission(
        db,
        user_id=user_id,
        challenge_id=challenge_id,
        solution_url=solution_url,
        notes=notes.strip() if notes else None,
    )


def admin_create_challenge(
    db: Session,
    *,
    title: str,
    description: str,
    difficulty: str | None,
    due_date,
    is_active: bool,
):
    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    if not description or not description.strip():
        raise HTTPException(status_code=400, detail="description is required")

    return intern_repo.create_challenge(
        db,
        title=title,
        description=description.strip(),
        difficulty=difficulty.strip() if difficulty else None,
        due_date=due_date,
        is_active=is_active,
    )


def admin_review_submission(
    db: Session,
    *,
    reviewer_user_id: int,
    submission_id: int,
    decision: str,
    feedback: str | None,
):
    sub = intern_repo.get_submission(db, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    decision = decision.strip().upper()
    if decision not in {"APPROVED", "REJECTED"}:
        raise HTTPException(status_code=400, detail="decision must be APPROVED or REJECTED")

    intern_repo.create_review(
        db,
        submission_id=submission_id,
        reviewer_user_id=reviewer_user_id,
        decision=decision,
        feedback=feedback.strip() if feedback else None,
    )

    return intern_repo.set_submission_status(db, sub, status=decision)


def intern_create_todo(db: Session, *, user_id: int, title: str):
    title = title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    return intern_repo.create_todo(db, user_id=user_id, title=title)


def intern_update_todo(db: Session, *, user_id: int, todo_id: int, title: str | None, status: str | None):
    todo = intern_repo.get_todo(db, todo_id)
    if not todo or todo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")

    if status is not None:
        status = status.strip().upper()
        if status not in _ALLOWED_TODO_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid todo status: {status}")

    return intern_repo.update_todo(db, todo, title=title.strip() if title else None, status=status)


def intern_delete_todo(db: Session, *, user_id: int, todo_id: int):
    todo = intern_repo.get_todo(db, todo_id)
    if not todo or todo.user_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")
    intern_repo.delete_todo(db, todo)
    return {"ok": True}