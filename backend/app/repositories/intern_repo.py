from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.intern import Challenge, ChallengeSubmission, SubmissionReview, InternTodo


# -------- Challenges --------

def list_challenges(db: Session, *, skip: int = 0, limit: int = 50, active_only: bool = True):
    q = db.query(Challenge)
    if active_only:
        q = q.filter(Challenge.is_active.is_(True))

    total = q.count()
    items = q.order_by(Challenge.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def create_challenge(db: Session, *, title: str, description: str, difficulty: str | None, due_date, is_active: bool):
    obj = Challenge(
        title=title,
        description=description,
        difficulty=difficulty,
        due_date=due_date,
        is_active=is_active,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_challenge(db: Session, challenge_id: int) -> Challenge | None:
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()


# -------- Submissions --------

def create_submission(
    db: Session,
    *,
    user_id: int,
    challenge_id: int,
    solution_url: str,
    notes: str | None,
):
    obj = ChallengeSubmission(
        user_id=user_id,
        challenge_id=challenge_id,
        solution_url=solution_url,
        notes=notes,
        status="PENDING",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_submissions(db: Session, *, skip: int = 0, limit: int = 50, user_id: int | None = None, status: str | None = None):
    q = db.query(ChallengeSubmission)
    if user_id is not None:
        q = q.filter(ChallengeSubmission.user_id == user_id)
    if status:
        q = q.filter(ChallengeSubmission.status == status)

    total = q.count()
    items = q.order_by(ChallengeSubmission.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_submission(db: Session, submission_id: int) -> ChallengeSubmission | None:
    return db.query(ChallengeSubmission).filter(ChallengeSubmission.id == submission_id).first()


def set_submission_status(db: Session, submission: ChallengeSubmission, *, status: str):
    submission.status = status
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def create_review(db: Session, *, submission_id: int, reviewer_user_id: int, decision: str, feedback: str | None):
    obj = SubmissionReview(
        submission_id=submission_id,
        reviewer_user_id=reviewer_user_id,
        decision=decision,
        feedback=feedback,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# -------- Todos --------

def create_todo(db: Session, *, user_id: int, title: str):
    obj = InternTodo(user_id=user_id, title=title, status="TODO")
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_todos(db: Session, *, skip: int = 0, limit: int = 50, user_id: int):
    q = db.query(InternTodo).filter(InternTodo.user_id == user_id)
    total = q.count()
    items = q.order_by(InternTodo.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_todo(db: Session, todo_id: int) -> InternTodo | None:
    return db.query(InternTodo).filter(InternTodo.id == todo_id).first()


def update_todo(db: Session, todo: InternTodo, *, title: str | None, status: str | None):
    if title is not None:
        todo.title = title
    if status is not None:
        todo.status = status
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: InternTodo):
    db.delete(todo)
    db.commit()


# -------- Progress --------

def get_intern_progress(db: Session, *, user_id: int):
    total_sub = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.user_id == user_id).scalar() or 0
    pending = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.user_id == user_id, ChallengeSubmission.status == "PENDING").scalar() or 0
    approved = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.user_id == user_id, ChallengeSubmission.status == "APPROVED").scalar() or 0
    rejected = db.query(func.count(ChallengeSubmission.id)).filter(ChallengeSubmission.user_id == user_id, ChallengeSubmission.status == "REJECTED").scalar() or 0

    todos_total = db.query(func.count(InternTodo.id)).filter(InternTodo.user_id == user_id).scalar() or 0
    todos_done = db.query(func.count(InternTodo.id)).filter(InternTodo.user_id == user_id, InternTodo.status == "DONE").scalar() or 0

    return {
        "total_submissions": total_sub,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "todos_total": todos_total,
        "todos_done": todos_done,
    }