from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import application_repo
from app.schemas.application import ApplicationOut, ApplicationsListResponse, AdminUpdateApplicationIn

UPLOAD_ROOT = Path("/app/uploads/applications").resolve()

router = APIRouter()


@router.get("/applications", response_model=ApplicationsListResponse)
def admin_list_applications(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = application_repo.list_applications(db, skip=skip, limit=limit, status=status)
    return {"total": total, "items": items}


@router.get("/applications/{app_id}", response_model=ApplicationOut)
def admin_get_application(
    app_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    obj = application_repo.get_by_id(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj


@router.patch("/applications/{app_id}", response_model=ApplicationOut)
def admin_update_application(
    app_id: int,
    payload: AdminUpdateApplicationIn,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    obj = application_repo.get_by_id(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return application_repo.update_admin_fields(db, obj, status=payload.status, admin_notes=payload.admin_notes)


@router.get("/applications/{app_id}/files/{kind}")
def admin_download_application_file(
    app_id: int,
    kind: str,  # "cv" or "space_terms"
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    obj = application_repo.get_by_id(db, app_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Application not found")

    if kind == "cv":
        path = Path(obj.cv_pdf_path)
    elif kind == "space_terms":
        path = Path(obj.space_terms_pdf_path)
    else:
        raise HTTPException(status_code=400, detail="kind must be 'cv' or 'space_terms'")

    resolved = path.resolve()
    if not str(resolved).startswith(str(UPLOAD_ROOT)):
        raise HTTPException(status_code=400, detail="Invalid file path")

    if not resolved.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(resolved), media_type="application/pdf", filename=resolved.name)