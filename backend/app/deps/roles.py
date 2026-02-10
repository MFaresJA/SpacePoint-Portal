from typing import Callable, Iterable
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


def require_roles(*allowed_roles: str) -> Callable:
    allowed = set(allowed_roles)

    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        role_names = (
            db.query(Role.name)
            .join(UserRole, UserRole.role_id == Role.role_id)
            .filter(UserRole.user_id == current_user.user_id)
            .all()
        )
        role_names = {r[0] for r in role_names}

        if not (role_names & allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {sorted(allowed)}",
            )
        return current_user

    return dependency
