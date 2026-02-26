from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.repositories import application_repo

MAX_PDF_BYTES = 10 * 1024 * 1024  # 10MB
UPLOAD_ROOT = Path("/app/uploads/applications")


def _ensure_pdf(file: UploadFile):
    # Content-Type can be missing/incorrect sometimes, so we also trust extension check later.
    if file.content_type and file.content_type.lower() not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail=f"{file.filename}: must be a PDF")


def _save_pdf(user_id: int, kind: str, file: UploadFile) -> str:
    """
    Save PDF under: /app/uploads/applications/{user_id}/{kind}_{uuid}.pdf
    Return stored path (string).
    """
    _ensure_pdf(file)

    user_dir = UPLOAD_ROOT / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    safe_kind = kind.replace("/", "_")
    filename = f"{safe_kind}_{uuid4().hex}.pdf"
    dest_path = user_dir / filename

    total = 0
    with dest_path.open("wb") as f:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_PDF_BYTES:
                # cleanup partial file
                try:
                    dest_path.unlink(missing_ok=True)
                except Exception:
                    pass
                raise HTTPException(status_code=400, detail=f"{kind} file too large (max 10MB)")
            f.write(chunk)

    return str(dest_path)


def submit_application(
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
    space_terms_pdf: UploadFile,
    cv_pdf: UploadFile,
):
    track = track.lower().strip()
    if track not in {"intern", "instructor"}:
        raise HTTPException(status_code=400, detail="track must be 'intern' or 'instructor'")

    space_path = _save_pdf(user_id, "space_terms", space_terms_pdf)
    cv_path = _save_pdf(user_id, "cv", cv_pdf)

    return application_repo.create_application(
        db,
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
        space_terms_pdf_path=space_path,
        cv_pdf_path=cv_path,
    )