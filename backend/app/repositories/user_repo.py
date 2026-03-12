from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_roles(db: Session, user_id: int) -> list[Role]:
    """
    Returns Role objects for the user.
    """
    return (
        db.query(Role)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user_id)
        .order_by(Role.name.asc())
        .all()
    )


def get_user_role_names(db: Session, user_id: int) -> list[str]:
    """
    Convenience helper: returns ["admin", "instructor", ...]
    """
    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user_id)
        .order_by(Role.name.asc())
        .all()
    )
    return [r[0] for r in rows]


def update_user_email(db: Session, user: User, *, email: str) -> User:
    user.email = email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_password_hash(db: Session, user: User, *, password_hash: str) -> User:
    user.password_hash = password_hash
    db.add(user)
    db.commit()
    db.refresh(user)
    return user