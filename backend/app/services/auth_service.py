from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, email: str, password: str) -> User:
    user = User(
        email=email,
        password_hash=hash_password(password),
        is_active=True,
        is_verified=False,
        is_suspended=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not user.is_active:
        return None
    if user.is_suspended:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def generate_token_pair(user: User) -> dict:
    return {
        "access_token": create_access_token({"sub": str(user.user_id)}),
        "refresh_token": create_refresh_token({"sub": str(user.user_id)}),
        "token_type": "bearer",
    }


def refresh_access_token(db: Session, refresh_token: str) -> str | None:
    payload = decode_refresh_token(refresh_token)
    if not payload or "sub" not in payload:
        return None

    user_id = int(payload["sub"])
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if not user.is_active or user.is_suspended:
        return None

    return create_access_token({"sub": str(user.user_id)})