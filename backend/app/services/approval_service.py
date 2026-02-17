from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.approvals import Approval
from app.models.submissions import QuizSubmission, ScenarioSubmission
from app.utils.enums import SubmissionStatus


def _require_reason_if_rejected(decision: str, reason: str | None):
    if decision == "REJECTED" and (reason is None or reason.strip() == ""):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rejection reason is required when decision is REJECTED.",
        )


def decide_quiz(db: Session, admin_user_id: int, quiz_id: int, decision: str, reason: str | None):
    _require_reason_if_rejected(decision, reason)

    quiz = db.query(QuizSubmission).filter(QuizSubmission.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz submission not found.")

    # update quiz status
    if decision == "APPROVED":
        quiz.status = SubmissionStatus.APPROVED
        # Optional: you can also enforce quiz.passed == True here if you want
    else:
        quiz.status = SubmissionStatus.REJECTED

    approval = Approval(
        entity_type="quiz",
        entity_id=quiz_id,
        decision=decision,
        reason=reason,
        approved_by_user_id=admin_user_id,
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return {
        "entity_type": "quiz",
        "entity_id": quiz_id,
        "decision": decision,
        "reason": reason,
    }


def decide_scenario(db: Session, admin_user_id: int, scenario_id: int, decision: str, reason: str | None):
    _require_reason_if_rejected(decision, reason)

    scenario = db.query(ScenarioSubmission).filter(ScenarioSubmission.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario submission not found.")

    # update scenario status
    if decision == "APPROVED":
        scenario.status = SubmissionStatus.APPROVED
    else:
        scenario.status = SubmissionStatus.REJECTED

    approval = Approval(
        entity_type="scenario",
        entity_id=scenario_id,
        decision=decision,
        reason=reason,
        approved_by_user_id=admin_user_id,
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    return {
        "entity_type": "scenario",
        "entity_id": scenario_id,
        "decision": decision,
        "reason": reason,
    }
