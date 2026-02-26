from sqlalchemy.orm import Session

from app.schemas.journey import JourneyProgressOut
from app.utils.enums import SubmissionStatus, JourneyStep
from app.repositories import submission_repo


def get_journey_progress(db: Session, user_id: int) -> JourneyProgressOut:
    completed: list[JourneyStep] = []
    locked: list[JourneyStep] = []
    reasons: dict[str, str] = {}

    onboarding = submission_repo.get_latest_onboarding(db=db, user_id=user_id)

    latest_quiz = submission_repo.get_latest_quiz(db=db, user_id=user_id)
    approved_quiz = submission_repo.get_latest_approved_quiz(db=db, user_id=user_id)

    latest_scenario = submission_repo.get_latest_scenario(db=db, user_id=user_id)
    approved_scenario = submission_repo.get_latest_approved_scenario(db=db, user_id=user_id)

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

    # No quiz attempt yet
    if latest_quiz is None:
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

    # Check if we have a NEWER (or equal) approved quiz relative to onboarding
    intro_unlocked = (
        approved_quiz is not None
        and approved_quiz.passed
        and approved_quiz.created_at >= onboarding.created_at
    )

    if not intro_unlocked:
        locked = [
            JourneyStep.INTRO_UNLOCKED,
            JourneyStep.SCENARIO_SUBMITTED_PENDING,
            JourneyStep.ADVANCED_UNLOCKED,
        ]

        # If user has an approved quiz but it's old (before latest onboarding) => force resubmit
        if approved_quiz and approved_quiz.created_at < onboarding.created_at:
            reasons["INTRO_UNLOCKED"] = "New onboarding submitted — please resubmit quiz"
        else:
            # Otherwise explain based on latest quiz attempt status
            if latest_quiz.status == SubmissionStatus.REJECTED:
                reasons["INTRO_UNLOCKED"] = "Quiz rejected — resubmit"
            elif latest_quiz.status == SubmissionStatus.APPROVED and not latest_quiz.passed:
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

    # Intro unlocked
    completed.append(JourneyStep.INTRO_UNLOCKED)

    # No scenario attempt
    if latest_scenario is None:
        locked = [JourneyStep.SCENARIO_SUBMITTED_PENDING, JourneyStep.ADVANCED_UNLOCKED]
        reasons["SCENARIO_SUBMITTED_PENDING"] = "Submit scenario first"
        reasons["ADVANCED_UNLOCKED"] = "Scenario must be approved first"

        return JourneyProgressOut(
            current_state=JourneyStep.INTRO_UNLOCKED,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    # Advanced unlock requires approved scenario newer/equal to approved quiz
    advanced_unlocked = (
        approved_scenario is not None
        and approved_scenario.created_at >= approved_quiz.created_at
    )

    if not advanced_unlocked:
        locked = [JourneyStep.ADVANCED_UNLOCKED]

        if approved_scenario and approved_scenario.created_at < approved_quiz.created_at:
            reasons["ADVANCED_UNLOCKED"] = "New quiz approved — please resubmit scenario"
        else:
            if latest_scenario.status == SubmissionStatus.REJECTED:
                reasons["ADVANCED_UNLOCKED"] = "Scenario rejected — resubmit"
            else:
                reasons["ADVANCED_UNLOCKED"] = "Waiting admin approval"

        return JourneyProgressOut(
            current_state=JourneyStep.SCENARIO_SUBMITTED_PENDING,
            completed_steps=completed,
            locked_steps=locked,
            locked_reasons=reasons,
        )

    completed.append(JourneyStep.ADVANCED_UNLOCKED)

    return JourneyProgressOut(
        current_state=JourneyStep.ADVANCED_UNLOCKED,
        completed_steps=completed,
        locked_steps=[],
        locked_reasons={},
    )
    