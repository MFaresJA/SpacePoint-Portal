from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity


def create_opportunity(
    db: Session,
    *,
    owner_user_id: int,
    title: str,
    description: str,
    link_url: str,
) -> Opportunity:
    obj = Opportunity(
        owner_user_id=owner_user_id,
        title=title,
        description=description,
        link_url=link_url,
        is_active=True,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_opportunities(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
):
    q = db.query(Opportunity)

    if active_only:
        q = q.filter(Opportunity.is_active.is_(True))

    total = q.count()
    items = (
        q.order_by(Opportunity.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items


def get_opportunity(db: Session, opportunity_id: int) -> Opportunity | None:
    return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()


def update_opportunity(
    db: Session,
    obj: Opportunity,
    *,
    title: str | None = None,
    description: str | None = None,
    link_url: str | None = None,
    is_active: bool | None = None,
) -> Opportunity:
    if title is not None:
        obj.title = title
    if description is not None:
        obj.description = description
    if link_url is not None:
        obj.link_url = link_url
    if is_active is not None:
        obj.is_active = is_active

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj