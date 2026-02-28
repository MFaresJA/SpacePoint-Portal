from app.db.base import Base  

# Import all models here so Alembic can detect them
from app.models.user import User  
from app.models.submissions import OnboardingSubmission, QuizSubmission, ScenarioSubmission  # noqa
from app.models.approvals import Approval  
from app.models.application import Application  
from app.models.ambassador import RecruitmentEntry, ImpactReport  # noqa

__all__ = ["Base"]