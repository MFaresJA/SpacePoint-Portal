from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.models.user import User
from app.repositories import certificate_repo
from app.schemas.certificate import CertificatesListResponse

router = APIRouter()


@router.get("/me", response_model=CertificatesListResponse)
def my_certificates(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    if limit > 200:
        limit = 200
    if skip < 0:
        skip = 0

    total, items = certificate_repo.list_user_certificates(
        db,
        user_id=me.user_id,
        skip=skip,
        limit=limit,
    )
    return {"total": total, "items": items}