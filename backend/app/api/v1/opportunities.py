from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import opportunity_repo
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityOut,
    OpportunitiesListResponse,
)
from app.services.opportunity_service import (
    create_opportunity,
    update_opportunity,
    delete_opportunity,
)

router = APIRouter()


@router.get("", response_model=OpportunitiesListResponse)
def list_opportunities(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = opportunity_repo.list_opportunities(db, skip=skip, limit=limit, active_only=True)
    return {"total": total, "items": items}


@router.post("", response_model=OpportunityOut)
def create_opportunity_route(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "instructor", "ambassador")),
):
    return create_opportunity(
        db,
        owner_user_id=user.user_id,
        title=payload.title,
        description=payload.description,
        link_url=payload.link_url,
    )


@router.patch("/{opportunity_id}", response_model=OpportunityOut)
def update_opportunity_route(
    opportunity_id: int,
    payload: OpportunityUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "instructor", "ambassador")),
):
    return update_opportunity(
        db,
        actor=user,
        opportunity_id=opportunity_id,
        title=payload.title,
        description=payload.description,
        link_url=payload.link_url,
        is_active=payload.is_active,
    )


@router.delete("/{opportunity_id}", response_model=OpportunityOut)
def delete_opportunity_route(
    opportunity_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin", "instructor", "ambassador")),
):
    return delete_opportunity(
        db,
        actor=user,
        opportunity_id=opportunity_id,
    )