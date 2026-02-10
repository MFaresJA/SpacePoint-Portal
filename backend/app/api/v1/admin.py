from fastapi import APIRouter, Depends
from app.deps.roles import require_roles

from sqlalchemy.orm import Session

from app.deps.db import get_db


from app.schemas.roles import RolesListResponse, RoleActionResponse
from app.services.role_service import (
    list_user_roles,
    assign_role_to_user,
    remove_role_from_user,
)

router = APIRouter()

#@router.get("/ping")
#def admin_ping(user = Depends(require_roles("admin"))):
#    return {"ok": True, "msg": "admin access granted"}


@router.get("/ping")
def admin_ping(_: dict = Depends(require_roles("admin"))):
    return {"status": "ok", "role": "admin"}

@router.get("/users/{user_id}/roles", response_model=RolesListResponse)
def admin_list_roles(
    user_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    roles = list_user_roles(db, user_id)
    return {"user_id": user_id, "roles": roles}

@router.post("/users/{user_id}/roles/{role_name}", response_model=RoleActionResponse)
def admin_assign_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return assign_role_to_user(db, user_id, role_name)

@router.delete("/users/{user_id}/roles/{role_name}", response_model=RoleActionResponse)
def admin_remove_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    return remove_role_from_user(db, user_id, role_name)
