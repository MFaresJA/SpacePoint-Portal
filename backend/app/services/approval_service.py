from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.approvals import Approval
from app.models.submissions import QuizSubmission, ScenarioSubmission, OnsiteLog
from app.utils.enums import SubmissionStatus, OnsiteLogStatus

from app.services.points_service import award_points
from app.utils.points_rules import QUIZ_APPROVED_POINTS, SCENARIO_APPROVED_POINTS

from app.services.audit_service import log_action

from app.services.certificate_service import auto_issue_journey_completion_certificate

from app.services.badge_service import auto_issue_journey_completion_badge

def _require_reason_if_rejected(decision: str, reason: str | None):
    if decision == "REJECTED" and (reason is None or reason.strip() == ""):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Rejection reason is required when decision is REJECTED.",
        )


def decide_quiz(db: Session, admin_user_id: int, quiz_id: int, decision: str, reason: str | None):
    decision = decision.strip().upper()
    _require_reason_if_rejected(decision, reason)

    quiz = db.query(QuizSubmission).filter(QuizSubmission.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz submission not found.")

    was_approved = (quiz.status == SubmissionStatus.APPROVED)

    if decision == "APPROVED":
        quiz.status = SubmissionStatus.APPROVED

        # award only on first transition to approved
        if not was_approved:
            award_points(
                db,
                user_id=quiz.user_id,
                points=QUIZ_APPROVED_POINTS,
                reason="quiz_approved",         
                entity_type="quiz",
                entity_id=quiz_id,
            )
    elif decision == "REJECTED":
        quiz.status = SubmissionStatus.REJECTED
    else:
        raise HTTPException(status_code=400, detail="decision must be APPROVED or REJECTED")

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

    log_action(
        db,
        actor_user_id=admin_user_id,
        action=f"quiz_{decision.lower()}",
        entity_type="quiz",
        entity_id=quiz_id,
    )

    return {
        "entity_type": "quiz",
        "entity_id": quiz_id,
        "decision": decision,
        "reason": reason,
    }


def decide_scenario(db: Session, admin_user_id: int, scenario_id: int, decision: str, reason: str | None):
    decision = decision.strip().upper()
    _require_reason_if_rejected(decision, reason)

    scenario = db.query(ScenarioSubmission).filter(ScenarioSubmission.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario submission not found.")

    was_approved = (scenario.status == SubmissionStatus.APPROVED)

    if decision == "APPROVED":
        scenario.status = SubmissionStatus.APPROVED

        if not was_approved:
            award_points(
                db,
                user_id=scenario.user_id,
                points=SCENARIO_APPROVED_POINTS,
                reason="scenario_approved",     
                entity_type="scenario",
                entity_id=scenario_id,
            )
    elif decision == "REJECTED":
        scenario.status = SubmissionStatus.REJECTED
    else:
        raise HTTPException(status_code=400, detail="decision must be APPROVED or REJECTED")

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
    
    log_action(
        db,
        actor_user_id=admin_user_id,
        action=f"scenario_{decision.lower()}",
        entity_type="scenario",
        entity_id=scenario_id,
    )
    return {
        "entity_type": "scenario",
        "entity_id": scenario_id,
        "decision": decision,
        "reason": reason,
    }

def decide_onsite_log(db: Session, admin_user_id: int, onsite_log_id: int, decision: str, reason: str | None):
    decision = decision.strip().upper()
    _require_reason_if_rejected(decision, reason)

    onsite_log = db.query(OnsiteLog).filter(OnsiteLog.id == onsite_log_id).first()
    if not onsite_log:
        raise HTTPException(status_code=404, detail="Onsite log not found.")

    if decision == "APPROVED":
        onsite_log.status = OnsiteLogStatus.VERIFIED
        
        auto_issue_journey_completion_certificate(
            db,
            user_id=onsite_log.user_id,
            issued_by_user_id=admin_user_id,
        )
        
        auto_issue_journey_completion_badge(
            db,
            user_id=onsite_log.user_id,
            issued_by_user_id=admin_user_id,
        )
        
    elif decision == "REJECTED":
        onsite_log.status = OnsiteLogStatus.REJECTED
    else:
        raise HTTPException(status_code=400, detail="decision must be APPROVED or REJECTED")

    approval = Approval(
        entity_type="onsite_log",
        entity_id=onsite_log_id,
        decision=decision,
        reason=reason,
        approved_by_user_id=admin_user_id,
    )

    db.add(approval)
    db.commit()
    db.refresh(approval)

    log_action(
        db,
        actor_user_id=admin_user_id,
        action=f"onsite_log_{decision.lower()}",
        entity_type="onsite_log",
        entity_id=onsite_log_id,
    )

    return {
        "entity_type": "onsite_log",
        "entity_id": onsite_log_id,
        "decision": decision,
        "reason": reason,
    }