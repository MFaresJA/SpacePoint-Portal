from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.services.journey_service import get_journey_progress
from app.services.submission_history_service import (
    get_onboarding_history,
    get_quiz_history,
    get_scenario_history,
)


def get_admin_user_review(db: Session, user_id: int):
    user = user_repo.get_user_by_id(db, user_id)
    roles = user_repo.get_user_roles(db, user_id)

    journey = get_journey_progress(db, user_id)
    onboarding = get_onboarding_history(db, user_id)
    quizzes = get_quiz_history(db, user_id)
    scenarios = get_scenario_history(db, user_id)

    role_names: list[str] = []
    for r in roles:
        role_names.append(getattr(r, "name", r))

    return {
        "user": user,
        "roles": role_names,
        "journey": journey,
        "onboarding": onboarding,
        "quizzes": quizzes,
        "scenarios": scenarios,
    }