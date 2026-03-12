from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.crm_proposal import CRMProposal


def create_proposal(
    db: Session,
    *,
    lead_id: int,
    instructor_user_id: int,
    proposal_url: str,
    notes: str | None,
) -> CRMProposal:
    obj = CRMProposal(
        lead_id=lead_id,
        instructor_user_id=instructor_user_id,
        proposal_url=proposal_url,
        notes=notes,
        status="SUBMITTED",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_proposals(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    instructor_user_id: int | None = None,
    status: str | None = None,
):
    q = db.query(CRMProposal)

    if instructor_user_id is not None:
        q = q.filter(CRMProposal.instructor_user_id == instructor_user_id)

    if status:
        q = q.filter(CRMProposal.status == status)

    total = q.count()
    items = (
        q.order_by(CRMProposal.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items


def get_proposal(db: Session, proposal_id: int) -> CRMProposal | None:
    return db.query(CRMProposal).filter(CRMProposal.id == proposal_id).first()


def update_proposal_admin(
    db: Session,
    obj: CRMProposal,
    *,
    status: str | None,
    admin_notes: str | None,
) -> CRMProposal:
    if status is not None:
        obj.status = status
    if admin_notes is not None:
        obj.admin_notes = admin_notes

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj