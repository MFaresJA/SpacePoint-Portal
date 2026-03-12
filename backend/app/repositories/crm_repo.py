from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.crm import CRMLead


def create_lead(
    db: Session,
    *,
    instructor_user_id: int,
    organization_name: str,
    contact_name: str,
    contact_email: str,
    notes: str | None,
) -> CRMLead:
    obj = CRMLead(
        instructor_user_id=instructor_user_id,
        organization_name=organization_name,
        contact_name=contact_name,
        contact_email=contact_email,
        notes=notes,
        status="SUBMITTED",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_leads(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    instructor_user_id: int | None = None,
    status: str | None = None,
):
    q = db.query(CRMLead)

    if instructor_user_id is not None:
        q = q.filter(CRMLead.instructor_user_id == instructor_user_id)

    if status:
        q = q.filter(CRMLead.status == status)

    total = q.count()
    items = (
        q.order_by(CRMLead.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items


def get_lead(db: Session, lead_id: int) -> CRMLead | None:
    return db.query(CRMLead).filter(CRMLead.id == lead_id).first()


def update_lead_admin(
    db: Session,
    obj: CRMLead,
    *,
    status: str | None,
    admin_notes: str | None,
) -> CRMLead:
    if status is not None:
        obj.status = status
    if admin_notes is not None:
        obj.admin_notes = admin_notes

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj