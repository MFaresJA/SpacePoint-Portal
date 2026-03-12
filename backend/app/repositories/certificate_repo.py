from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.certificate import Certificate


def create_certificate(
    db: Session,
    *,
    user_id: int,
    title: str,
    certificate_url: str | None,
    issued_by_user_id: int | None,
) -> Certificate:
    obj = Certificate(
        user_id=user_id,
        title=title,
        certificate_url=certificate_url,
        issued_by_user_id=issued_by_user_id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_user_certificates(
    db: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
):
    q = db.query(Certificate).filter(Certificate.user_id == user_id)

    total = q.count()
    items = (
        q.order_by(Certificate.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items


def get_user_certificate_by_title(
    db: Session,
    *,
    user_id: int,
    title: str,
) -> Certificate | None:
    return (
        db.query(Certificate)
        .filter(Certificate.user_id == user_id, Certificate.title == title)
        .first()
    )