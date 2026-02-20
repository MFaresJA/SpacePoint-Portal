from sqlalchemy.orm import Session

from app.schemas.journey import JourneyProgressOut
from app.utils.enums import SubmissionStatus, JourneyStep
from app.repositories import submission_repo


def get_journey_progress(db: Session, user_id: int) -> JourneyProgressOut:
    completed: list[JourneyStep] = []
    locked: list[JourneyStep] = []
    reasons: dict[str, str] = {}

    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)
    quiz = submission_repo.get_latest_quiz(db=db, user_id=user_id)
    scenario = submission_repo.get_latest_scenario(db=db, user_id=user_id)

    # No onboarding
    if onboarding is None:
        locked = [
            JourneyStep.ONBOARDING_SUBMITTED,
            JourneyStep.QUIZ_SUBMITTED_PENDING,
            JourneyStep.INTRO_UNLOCKED,
            JourneyStep.SCENARIO_SUBMITTED_PENDING,
            JourneyStep.ADVANCED_UNLOCKED,
        ]

        reasons["QUIZ_SUBMITTED_PENDING"] = "Submit onboarding first"
        reasons["INTRO_UNLOCKED"] = "Quiz must be approved first"
        reasons["SCENARIO_SUBMITTED_PENDING"] = "Quiz must be approved first"
        reasons["ADVANCED_UNLOCKED"] = "Scenario must be approved first"

        return JourneyProgressOut(
            current_state=JourneyStep.NOT_STARTED,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    completed.append(JourneyStep.ONBOARDING_SUBMITTED)

    # No quiz yet
    if quiz is None:
        locked = [
            JourneyStep.QUIZ_SUBMITTED_PENDING,
            JourneyStep.INTRO_UNLOCKED,
            JourneyStep.SCENARIO_SUBMITTED_PENDING,
            JourneyStep.ADVANCED_UNLOCKED,
        ]

        reasons["INTRO_UNLOCKED"] = "Submit quiz first"
        reasons["SCENARIO_SUBMITTED_PENDING"] = "Submit quiz first"
        reasons["ADVANCED_UNLOCKED"] = "Scenario must be approved first"

        return JourneyProgressOut(
            current_state=JourneyStep.ONBOARDING_SUBMITTED,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    # Quiz submitted but not approved
    if quiz.status != SubmissionStatus.APPROVED or not quiz.passed:
        locked = [
            JourneyStep.INTRO_UNLOCKED,
            JourneyStep.SCENARIO_SUBMITTED_PENDING,
            JourneyStep.ADVANCED_UNLOCKED,
        ]

        if quiz.status == SubmissionStatus.REJECTED:
            reasons["INTRO_UNLOCKED"] = "Quiz rejected — resubmit"
        elif quiz.status == SubmissionStatus.APPROVED and not quiz.passed:
            reasons["INTRO_UNLOCKED"] = "Quiz approved but failed — resubmit"
        else:
            reasons["INTRO_UNLOCKED"] = "Waiting admin approval"

        reasons["SCENARIO_SUBMITTED_PENDING"] = "Quiz must be approved first"
        reasons["ADVANCED_UNLOCKED"] = "Scenario must be approved first"

        return JourneyProgressOut(
            current_state=JourneyStep.QUIZ_SUBMITTED_PENDING,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    # Quiz approved & passed
    completed.append(JourneyStep.INTRO_UNLOCKED)

    # No scenario yet
    if scenario is None:
        locked = [
            JourneyStep.SCENARIO_SUBMITTED_PENDING,
            JourneyStep.ADVANCED_UNLOCKED,
        ]

        reasons["SCENARIO_SUBMITTED_PENDING"] = "Submit scenario first"
        reasons["ADVANCED_UNLOCKED"] = "Scenario must be approved first"

        return JourneyProgressOut(
            current_state=JourneyStep.INTRO_UNLOCKED,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    
    # Scenario submitted but not approved
    if scenario.status != SubmissionStatus.APPROVED:
        locked = [JourneyStep.ADVANCED_UNLOCKED]

        if scenario.status == SubmissionStatus.REJECTED:
            reasons["ADVANCED_UNLOCKED"] = "Scenario rejected — resubmit"
        else:
            reasons["ADVANCED_UNLOCKED"] = "Waiting admin approval"

        return JourneyProgressOut(
            current_state=JourneyStep.SCENARIO_SUBMITTED_PENDING,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    # ----------------------------
    # 7️⃣ Scenario approved
    # ----------------------------
    completed.append(JourneyStep.ADVANCED_UNLOCKED)

    return JourneyProgressOut(
        current_state=JourneyStep.ADVANCED_UNLOCKED,
        completed_steps=completed,
        locked_steps=[],
        locked_reasons={},
    )
