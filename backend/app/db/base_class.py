from app.db.base import Base  

# Import all models here so Alembic can detect them
from app.models.user import User  
from app.models.submissions import OnboardingSubmission, QuizSubmission, ScenarioSubmission  # noqa
from app.models.approvals import Approval  
from app.models.application import Application  

__all__ = ["Base"]