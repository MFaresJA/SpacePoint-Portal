from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, hash_password
from app.repositories import user_repo
from app.services.audit_service import log_action


def update_my_profile(
    db: Session,
    *,
    user_id: int,
    new_email: str,
):
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    normalized_email = new_email.strip().lower()

    existing = user_repo.get_user_by_email(db, normalized_email)
    if existing and existing.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already in use",
        )

    updated = user_repo.update_user_email(db, user, email=normalized_email)

    log_action(
        db,
        actor_user_id=user_id,
        action="profile_updated",
        entity_type="user",
        entity_id=user_id,
    )

    roles = user_repo.get_user_role_names(db, user_id)
    return {
        "user_id": updated.user_id,
        "email": updated.email,
        "is_active": updated.is_active,
        "is_verified": updated.is_verified,
        "is_suspended": updated.is_suspended,
        "roles": roles,
    }


def change_my_password(
    db: Session,
    *,
    user_id: int,
    current_password: str,
    new_password: str,
):
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if current_password == new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    user_repo.update_user_password_hash(
        db,
        user,
        password_hash=hash_password(new_password),
    )

    log_action(
        db,
        actor_user_id=user_id,
        action="password_changed",
        entity_type="user",
        entity_id=user_id,
    )

    return {"message": "Password changed successfully"}