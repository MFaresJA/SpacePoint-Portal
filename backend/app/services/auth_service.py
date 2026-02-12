from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


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


def generate_access_token(user: User) -> str:
    return create_access_token(
        data={"sub": str(user.user_id)}
    )
