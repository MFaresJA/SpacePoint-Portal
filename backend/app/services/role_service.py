from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_role_by_name(db: Session, role_name: str) -> Role:
    role_name = role_name.lower().strip()
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


def list_user_roles(db: Session, user_id: int) -> list[str]:
    # ensure user exists
    get_user_by_id(db, user_id)

    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return [r[0] for r in rows]


def assign_role_to_user(db: Session, user_id: int, role_name: str) -> dict:
    user = get_user_by_id(db, user_id)
    role = get_role_by_name(db, role_name)

    existing = (
        db.query(UserRole)
        .filter(UserRole.user_id == user.user_id, UserRole.role_id == role.role_id)
        .first()
    )
    if existing:
        return {"message": "Role already assigned"}

    db.add(UserRole(user_id=user.user_id, role_id=role.role_id))
    db.commit()
    db.refresh(user)
    return {"message": f"Assigned role '{role.name}' to user {user.user_id}"}


def remove_role_from_user(db: Session, user_id: int, role_name: str) -> dict:
    user = get_user_by_id(db, user_id)
    role = get_role_by_name(db, role_name)

    row = (
        db.query(UserRole)
        .filter(UserRole.user_id == user.user_id, UserRole.role_id == role.role_id)
        .first()
    )
    if not row:
        return {"message": "Role not assigned"}

    db.delete(row)
    db.commit()
    return {"message": f"Removed role '{role.name}' from user {user.user_id}"}

def set_user_active(db: Session, user_id: int, active: bool) -> dict:
    user = get_user_by_id(db, user_id)
    user.is_active = active
    db.commit()
    return {
        "user_id": user.user_id,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_suspended": user.is_suspended,
    }


def set_user_verified(db: Session, user_id: int, verified: bool) -> dict:
    user = get_user_by_id(db, user_id)
    user.is_verified = verified
    db.commit()
    return {
        "user_id": user.user_id,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_suspended": user.is_suspended,
    }


def set_user_suspended(db: Session, user_id: int, suspended: bool) -> dict:
    user = get_user_by_id(db, user_id)
    user.is_suspended = suspended
    db.commit()
    return {
        "user_id": user.user_id,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_suspended": user.is_suspended,
    }
