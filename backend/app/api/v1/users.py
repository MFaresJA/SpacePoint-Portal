from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.models.user import User
from app.repositories import user_repo
from app.schemas.profile import UpdateMyProfileIn, ChangePasswordIn, MyProfileOut
from app.services.profile_service import update_my_profile, change_my_password

router = APIRouter()


@router.get("/me", response_model=MyProfileOut)
def get_my_profile(
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    roles = user_repo.get_user_role_names(db, me.user_id)
    return {
        "user_id": me.user_id,
        "email": me.email,
        "is_active": me.is_active,
        "is_verified": me.is_verified,
        "is_suspended": me.is_suspended,
        "roles": roles,
    }


@router.patch("/me", response_model=MyProfileOut)
def patch_my_profile(
    payload: UpdateMyProfileIn,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return update_my_profile(
        db,
        user_id=me.user_id,
        new_email=payload.email,
    )


@router.post("/change-password")
def post_change_password(
    payload: ChangePasswordIn,
    db: Session = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return change_my_password(
        db,
        user_id=me.user_id,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )