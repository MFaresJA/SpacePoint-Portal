from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import intern_repo
from app.schemas.intern import (
    ChallengesListResponse,
    ChallengeOut,
    SubmissionCreate,
    SubmissionOut,
    SubmissionsListResponse,
    TodoCreate,
    TodoUpdate,
    TodoOut,
    TodosListResponse,
    InternProgressOut,
)
from app.services.intern_service import (
    intern_submit_solution,
    intern_create_todo,
    intern_update_todo,
    intern_delete_todo,
)

router = APIRouter()


@router.get("/ping")
def intern_ping(_=Depends(require_roles("intern", "admin"))):
    return {"ok": True, "msg": "intern access granted"}


@router.get("/challenges", response_model=ChallengesListResponse)
def list_challenges(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    _=Depends(require_roles("intern")),
):
    total, items = intern_repo.list_challenges(db, skip=skip, limit=limit, active_only=True)
    return {"total": total, "items": items}


@router.post("/submissions", response_model=SubmissionOut)
def submit_solution(
    payload: SubmissionCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    return intern_submit_solution(
        db,
        user_id=user.user_id,
        challenge_id=payload.challenge_id,
        solution_url=payload.solution_url,
        notes=payload.notes,
    )


@router.get("/submissions", response_model=SubmissionsListResponse)
def my_submissions(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    total, items = intern_repo.list_submissions(
        db,
        skip=skip,
        limit=limit,
        user_id=user.user_id,
        status=status.upper() if status else None,
    )
    return {"total": total, "items": items}


@router.get("/progress", response_model=InternProgressOut)
def my_progress(
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    return intern_repo.get_intern_progress(db, user_id=user.user_id)


@router.post("/todos", response_model=TodoOut)
def create_todo(
    payload: TodoCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    return intern_create_todo(db, user_id=user.user_id, title=payload.title)


@router.get("/todos", response_model=TodosListResponse)
def list_todos(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    total, items = intern_repo.list_todos(db, skip=skip, limit=limit, user_id=user.user_id)
    return {"total": total, "items": items}


@router.patch("/todos/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    return intern_update_todo(db, user_id=user.user_id, todo_id=todo_id, title=payload.title, status=payload.status)


@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("intern")),
):
    return intern_delete_todo(db, user_id=user.user_id, todo_id=todo_id)