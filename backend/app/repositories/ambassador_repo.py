from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.ambassador import ImpactReport, RecruitmentEntry


# -------- Recruitment --------

def create_recruitment_entry(
    db: Session,
    *,
    ambassador_user_id: int,
    name: str,
    contact: str,
    notes: str | None,
) -> RecruitmentEntry:
    obj = RecruitmentEntry(
        ambassador_user_id=ambassador_user_id,
        name=name,
        contact=contact,
        notes=notes,
        status="PENDING",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_recruitment_entries(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    ambassador_user_id: int | None = None,
):
    q = db.query(RecruitmentEntry)
    if status:
        q = q.filter(RecruitmentEntry.status == status)
    if ambassador_user_id is not None:
        q = q.filter(RecruitmentEntry.ambassador_user_id == ambassador_user_id)

    total = q.count()
    items = q.order_by(RecruitmentEntry.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_recruitment_by_id(db: Session, entry_id: int) -> RecruitmentEntry | None:
    return db.query(RecruitmentEntry).filter(RecruitmentEntry.id == entry_id).first()


def update_recruitment_admin_fields(
    db: Session,
    entry: RecruitmentEntry,
    *,
    status: str | None,
    notes: str | None,
) -> RecruitmentEntry:
    if status is not None:
        entry.status = status
    if notes is not None:
        entry.notes = notes

    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


# -------- Impact Reports --------

def create_impact_report(
    db: Session,
    *,
    ambassador_user_id: int,
    title: str,
    description: str,
    evidence_url: str,
    location: str,
    event_date,
    hours: int,
    people_reached: int,
) -> ImpactReport:
    obj = ImpactReport(
        ambassador_user_id=ambassador_user_id,
        title=title,
        description=description,
        evidence_url=evidence_url,
        location=location,
        event_date=event_date,
        status="PENDING",
        hours=hours,
        people_reached=people_reached,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_impact_reports(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    ambassador_user_id: int | None = None,
):
    q = db.query(ImpactReport)
    if status:
        q = q.filter(ImpactReport.status == status)
    if ambassador_user_id is not None:
        q = q.filter(ImpactReport.ambassador_user_id == ambassador_user_id)

    total = q.count()
    items = q.order_by(ImpactReport.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_impact_by_id(db: Session, report_id: int) -> ImpactReport | None:
    return db.query(ImpactReport).filter(ImpactReport.id == report_id).first()


def update_impact_admin_fields(
    db: Session,
    report: ImpactReport,
    *,
    status: str | None,
) -> ImpactReport:
    if status is not None:
        report.status = status

    db.add(report)
    db.commit()
    db.refresh(report)
    return report