from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import ambassador_repo


_ALLOWED_STATUSES = {"PENDING", "APPROVED", "REJECTED", "UNDER_REVIEW"}


def submit_recruitment_entry(
    db: Session,
    *,
    ambassador_user_id: int,
    name: str,
    contact: str,
    notes: str | None,
):
    name = name.strip()
    contact = contact.strip()

    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    if not contact:
        raise HTTPException(status_code=400, detail="contact is required")

    return ambassador_repo.create_recruitment_entry(
        db,
        ambassador_user_id=ambassador_user_id,
        name=name,
        contact=contact,
        notes=notes.strip() if notes else None,
    )


def submit_impact_report(
    db: Session,
    *,
    ambassador_user_id: int,
    title: str,
    description: str,
    evidence_url: str,
    location: str,
    event_date,
    hours: int = 0,
    people_reached: int = 0,
):
    title = title.strip()
    location = location.strip()
    evidence_url = evidence_url.strip()

    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    if not description or not description.strip():
        raise HTTPException(status_code=400, detail="description is required")
    if not evidence_url:
        raise HTTPException(status_code=400, detail="evidence_url is required")
    if not location:
        raise HTTPException(status_code=400, detail="location is required")

    if hours < 0 or people_reached < 0:
        raise HTTPException(status_code=400, detail="hours/people_reached must be >= 0")

    return ambassador_repo.create_impact_report(
        db,
        ambassador_user_id=ambassador_user_id,
        title=title,
        description=description.strip(),
        evidence_url=evidence_url,
        location=location,
        event_date=event_date,
        hours=hours,
        people_reached=people_reached,
    )


# -------- Admin actions --------

def admin_update_recruitment(
    db: Session,
    *,
    entry_id: int,
    status: str | None,
    notes: str | None,
):
    entry = ambassador_repo.get_recruitment_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Recruitment entry not found")

    if status is not None:
        status = status.strip().upper()
        if status not in _ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    return ambassador_repo.update_recruitment_admin_fields(
        db, entry, status=status, notes=notes
    )


def admin_update_impact(
    db: Session,
    *,
    report_id: int,
    status: str | None,
):
    report = ambassador_repo.get_impact_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Impact report not found")

    if status is not None:
        status = status.strip().upper()
        if status not in _ALLOWED_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    return ambassador_repo.update_impact_admin_fields(db, report, status=status)