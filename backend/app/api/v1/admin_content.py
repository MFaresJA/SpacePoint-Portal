from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import content_repo
from app.schemas.admin_content import (
    AdminContentCreateIn,
    AdminContentUpdateIn,
    AdminContentOut,
    AdminContentListResponse,
)
from app.services.admin_content_service import (
    admin_create_content,
    admin_update_content,
    admin_delete_content,
)

router = APIRouter()


@router.post("/content", response_model=AdminContentOut)
def create_content(
    payload: AdminContentCreateIn,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    return admin_create_content(
        db,
        admin_user_id=admin.user_id,
        key=payload.key,
        title=payload.title,
        url=payload.url,
        is_active=payload.is_active,
    )


@router.get("/content", response_model=AdminContentListResponse)
def list_content(
    limit: int = 50,
    offset: int = 0,
    key: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0

    total, items = content_repo.list_content_items(
        db,
        limit=limit,
        offset=offset,
        key=key,
        is_active=is_active,
    )
    return {"total": total, "items": items}


@router.patch("/content/{content_id}", response_model=AdminContentOut)
def update_content(
    content_id: int,
    payload: AdminContentUpdateIn,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    return admin_update_content(
        db,
        admin_user_id=admin.user_id,
        content_id=content_id,
        key=payload.key,
        title=payload.title,
        url=payload.url,
        is_active=payload.is_active,
    )


@router.delete("/content/{content_id}", response_model=AdminContentOut)
def delete_content(
    content_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_roles("admin")),
):
    return admin_delete_content(
        db,
        admin_user_id=admin.user_id,
        content_id=content_id,
    )