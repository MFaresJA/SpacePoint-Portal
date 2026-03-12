from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import content_repo
from app.services.audit_service import log_action


def admin_create_content(
    db: Session,
    *,
    admin_user_id: int,
    key: str,
    title: str,
    url: str,
    is_active: bool,
):
    key = key.strip()
    title = title.strip()
    url = url.strip()

    if not key:
        raise HTTPException(status_code=400, detail="key is required")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    if not url:
        raise HTTPException(status_code=400, detail="url is required")

    created = content_repo.create_content_item(
        db,
        key=key,
        title=title,
        url=url,
        is_active=is_active,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="content_created",
        entity_type="content_item",
        entity_id=created.id,
    )

    return created


def admin_update_content(
    db: Session,
    *,
    admin_user_id: int,
    content_id: int,
    key: str | None,
    title: str | None,
    url: str | None,
    is_active: bool | None,
):
    item = content_repo.get_content_item_by_id(db, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")

    updated = content_repo.update_content_item(
        db,
        item,
        key=key.strip() if key is not None else None,
        title=title.strip() if title is not None else None,
        url=url.strip() if url is not None else None,
        is_active=is_active,
    )

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="content_updated",
        entity_type="content_item",
        entity_id=updated.id,
    )

    return updated


def admin_delete_content(
    db: Session,
    *,
    admin_user_id: int,
    content_id: int,
):
    item = content_repo.get_content_item_by_id(db, content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")

    updated = content_repo.update_content_item(db, item, is_active=False)

    log_action(
        db,
        actor_user_id=admin_user_id,
        action="content_deactivated",
        entity_type="content_item",
        entity_id=updated.id,
    )

    return updated