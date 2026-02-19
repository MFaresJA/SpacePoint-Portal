from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.schemas.content import ContentResponse
from app.services.content_service import get_intro_slides, get_advanced_slides

router = APIRouter()


@router.get("/intro-slides", response_model=ContentResponse)
def intro_slides(
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_intro_slides(db=db, user_id=user.user_id)


@router.get("/advanced-slides", response_model=ContentResponse)
def advanced_slides(
    db: Session = Depends(get_db),
    user=Depends(require_roles("instructor", "admin")),
):
    return get_advanced_slides(db=db, user_id=user.user_id)
