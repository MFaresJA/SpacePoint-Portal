from collections import defaultdict
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole


from fastapi import HTTPException, status



def list_users_with_roles(db: Session, skip: int = 0, limit: int = 50) -> tuple[int, list[dict]]:
    # total users count (for pagination)
    total = db.query(User).count()

    # get users page
    users = (
        db.query(User)
        .order_by(User.user_id.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not users:
        return total, []

    user_ids = [u.user_id for u in users]

    # get roles for all users in this page in ONE query
    rows = (
        db.query(UserRole.user_id, Role.name)
        .join(Role, Role.role_id == UserRole.role_id)
        .filter(UserRole.user_id.in_(user_ids))
        .all()
    )

    roles_map: dict[int, list[str]] = defaultdict(list)
    for uid, role_name in rows:
        roles_map[uid].append(role_name)

    # build response items
    items = []
    for u in users:
        items.append({
            "user_id": u.user_id,
            "email": u.email,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "is_suspended": u.is_suspended,
            "roles": sorted(roles_map.get(u.user_id, [])),
        })

    return total, items

def get_user_detail(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    roles = [r[0] for r in rows]

    return {
        "user_id": user.user_id,
        "email": user.email,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "is_suspended": user.is_suspended,
        "roles": roles,
    }