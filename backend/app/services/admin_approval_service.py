from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.admin_approval_repo import (
    list_pending_quiz,
    list_pending_scenario,
    list_pending_onsite_logs,
)
from app.schemas.admin_approvals import PendingApprovalsResponse, PendingApprovalItem


def get_pending_approvals(db: Session, skip: int = 0, limit: int = 50) -> PendingApprovalsResponse:
    third = max(1, limit // 3)

    quiz_items = list_pending_quiz(db, skip=0, limit=third)
    scenario_items = list_pending_scenario(db, skip=0, limit=third)
    onsite_items = list_pending_onsite_logs(db, skip=0, limit=limit - (2 * third))

    items: list[PendingApprovalItem] = []

    for q in quiz_items:
        items.append(
            PendingApprovalItem(
                entity_type="quiz",
                entity_id=q.id,
                user_id=q.user_id,
                status=q.status.value if hasattr(q.status, "value") else str(q.status),
                created_at=q.created_at,
                score=q.score,
                passed=q.passed,
                attempt=q.attempt,
            )
        )

    for s in scenario_items:
        items.append(
            PendingApprovalItem(
                entity_type="scenario",
                entity_id=s.id,
                user_id=s.user_id,
                status=s.status.value if hasattr(s.status, "value") else str(s.status),
                created_at=s.created_at,
                scenario_url=s.scenario_url,
                version=s.version,
            )
        )

    for o in onsite_items:
        items.append(
            PendingApprovalItem(
                entity_type="onsite_log",
                entity_id=o.id,
                user_id=o.user_id,
                status=o.status,
                created_at=o.created_at,
                session_type=o.session_type,
                notes=o.notes,
                evidence_url=o.evidence_url,
            )
        )

    items.sort(key=lambda x: x.created_at)
    sliced = items[skip : skip + limit]

    return PendingApprovalsResponse(total=len(items), items=sliced)