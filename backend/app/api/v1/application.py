from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.schemas.application import ApplicationOut
from app.services.application_service import submit_application

router = APIRouter()


@router.post("/submit", response_model=ApplicationOut)
async def application_submit(
    track: str = Form(...),  # "INTERN" or "INSTRUCTOR"
    full_name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    university: str = Form(...),
    highest_degree: str = Form(...),
    city_of_residence: str = Form(...),

    deliver_cities: str = Form(...),      # comma-separated from UI
    background_areas: str = Form(...),    # comma-separated from UI

    video1_summary: str = Form(...),
    video2_summary: str = Form(...),
    video3_summary: str = Form(...),

    space_terms_pdf: UploadFile = File(...),
    cv_pdf: UploadFile = File(...),

    db: Session = Depends(get_db),
    # TEMP: allow any logged-in role; later we’ll switch to "any authenticated user"
    user=Depends(require_roles("admin", "intern", "instructor", "ambassador")),
):
    deliver_list = [x.strip() for x in deliver_cities.split(",") if x.strip()]
    background_list = [x.strip() for x in background_areas.split(",") if x.strip()]

    app_obj = submit_application(
        db=db,
        user_id=user.user_id,
        track=track,
        full_name=full_name,
        phone_number=phone_number,
        email=email,
        university=university,
        highest_degree=highest_degree,
        city_of_residence=city_of_residence,
        deliver_cities=deliver_list,         # service will store as JSON
        background_areas=background_list,    # service will store as JSON
        video1_summary=video1_summary,
        video2_summary=video2_summary,
        video3_summary=video3_summary,
        space_terms_pdf=space_terms_pdf,
        cv_pdf=cv_pdf,
    )

    # If ApplicationOut matches DB fields, we can return ORM directly.
    return app_obj