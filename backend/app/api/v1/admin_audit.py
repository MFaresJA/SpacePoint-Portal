from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.roles import require_roles
from app.repositories import audit_repo
from app.schemas.audit import AuditLogsResponse

router = APIRouter()


@router.get("/audit-logs", response_model=AuditLogsResponse)
def admin_list_audit_logs(
    limit: int = 50,
    offset: int = 0,
    action: str | None = None,
    entity_type: str | None = None,
    db: Session = Depends(get_db),
    _: dict = Depends(require_roles("admin")),
):
    if limit > 200:
        limit = 200
    if offset < 0:
        offset = 0

    total, items = audit_repo.list_audit_logs(
        db,
        limit=limit,
        offset=offset,
        action=action,
        entity_type=entity_type,
    )
    return {"total": total, "items": items}