from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import opportunity_repo
from app.services.audit_service import log_action


def create_opportunity(
    db: Session,
    *,
    owner_user_id: int,
    title: str,
    description: str,
    link_url: str,
):
    title = title.strip()
    description = description.strip()
    link_url = link_url.strip()

    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    if not description:
        raise HTTPException(status_code=400, detail="description is required")
    if not link_url:
        raise HTTPException(status_code=400, detail="link_url is required")

    obj = opportunity_repo.create_opportunity(
        db,
        owner_user_id=owner_user_id,
        title=title,
        description=description,
        link_url=link_url,
    )

    log_action(
        db,
        actor_user_id=owner_user_id,
        action="opportunity_created",
        entity_type="opportunity",
        entity_id=obj.id,
    )
    return obj


def update_opportunity(
    db: Session,
    *,
    actor: User,
    opportunity_id: int,
    title: str | None,
    description: str | None,
    link_url: str | None,
    is_active: bool | None,
):
    obj = opportunity_repo.get_opportunity(db, opportunity_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    role_names = getattr(actor, "role_names", None)

    # fallback role check via attribute-less user object
    is_admin = False
    if role_names and "admin" in role_names:
        is_admin = True

    if actor.user_id != obj.owner_user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not allowed to update this opportunity")

    updated = opportunity_repo.update_opportunity(
        db,
        obj,
        title=title.strip() if title is not None else None,
        description=description.strip() if description is not None else None,
        link_url=link_url.strip() if link_url is not None else None,
        is_active=is_active,
    )

    log_action(
        db,
        actor_user_id=actor.user_id,
        action="opportunity_updated",
        entity_type="opportunity",
        entity_id=updated.id,
    )
    return updated


def delete_opportunity(
    db: Session,
    *,
    actor: User,
    opportunity_id: int,
):
    obj = opportunity_repo.get_opportunity(db, opportunity_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    role_names = getattr(actor, "role_names", None)

    is_admin = False
    if role_names and "admin" in role_names:
        is_admin = True

    if actor.user_id != obj.owner_user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not allowed to delete this opportunity")

    updated = opportunity_repo.update_opportunity(db, obj, is_active=False)

    log_action(
        db,
        actor_user_id=actor.user_id,
        action="opportunity_deactivated",
        entity_type="opportunity",
        entity_id=updated.id,
    )
    return updated