from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.admin_approval_repo import list_pending_quiz, list_pending_scenario
from app.schemas.admin_approvals import PendingApprovalsResponse, PendingApprovalItem


def get_pending_approvals(db: Session, skip: int = 0, limit: int = 50) -> PendingApprovalsResponse:
    # We’ll split the limit roughly between quiz/scenario for now (simple + works).
    half = max(1, limit // 2)

    quiz_items = list_pending_quiz(db, skip=0, limit=half)
    scenario_items = list_pending_scenario(db, skip=0, limit=limit - half)

    items: list[PendingApprovalItem] = []

    for q in quiz_items:
        items.append(
            PendingApprovalItem(
                entity_type="quiz",
                entity_id=q.id,
                user_id=q.user_id,
                status=q.status,
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
                status=s.status,
                created_at=s.created_at,
                scenario_url=s.scenario_url,
                version=s.version,
            )
        )

    # sort combined list by created_at (oldest first)
    items.sort(key=lambda x: x.created_at)

    # apply skip/limit on the combined output
    sliced = items[skip : skip + limit]

    return PendingApprovalsResponse(total=len(items), items=sliced)
