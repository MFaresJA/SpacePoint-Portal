from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.application import Application


def create_application(
    db: Session,
    *,
    user_id: int,
    track: str,
    full_name: str,
    phone_number: str,
    email: str,
    university: str,
    highest_degree: str,
    city_of_residence: str,
    deliver_cities: list[str],
    background_areas: list[str],
    video1_summary: str,
    video2_summary: str,
    video3_summary: str,
    space_terms_pdf_path: str,
    cv_pdf_path: str,
) -> Application:
    obj = Application(
        user_id=user_id,
        track=track,
        full_name=full_name,
        phone_number=phone_number,
        email=email,
        university=university,
        highest_degree=highest_degree,
        city_of_residence=city_of_residence,
        deliver_cities=deliver_cities,
        background_areas=background_areas,
        video1_summary=video1_summary,
        video2_summary=video2_summary,
        video3_summary=video3_summary,
        space_terms_pdf_path=space_terms_pdf_path,
        cv_pdf_path=cv_pdf_path,
        status="SUBMITTED",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_latest_by_user(db: Session, user_id: int) -> Application | None:
    return (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
        .first()
    )


def list_applications(db: Session, skip: int = 0, limit: int = 50, status: str | None = None):
    q = db.query(Application)
    if status:
        q = q.filter(Application.status == status)

    total = q.count()
    items = q.order_by(Application.created_at.desc()).offset(skip).limit(limit).all()
    return total, items


def get_by_id(db: Session, app_id: int) -> Application | None:
    return db.query(Application).filter(Application.id == app_id).first()


def update_admin_fields(db: Session, app_obj: Application, *, status: str | None, admin_notes: str | None) -> Application:
    if status is not None:
        app_obj.status = status
    if admin_notes is not None:
        app_obj.admin_notes = admin_notes

    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj