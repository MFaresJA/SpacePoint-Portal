from app.db.base import Base  

# Import all models here so Alembic can detect them
from app.models.user import User  
from app.models.submissions import OnboardingSubmission, QuizSubmission, ScenarioSubmission, OnsiteLog
from app.models.approvals import Approval  
from app.models.application import Application  
from app.models.ambassador import RecruitmentEntry, ImpactReport  
from app.models.intern import Challenge, ChallengeSubmission, SubmissionReview, InternTodo  
from app.models.points import PointsLedger
from app.models.audit import AuditLog
from app.models.opportunity import Opportunity
from app.models.certificate import Certificate
from app.models.crm import CRMLead
from app.models.crm_proposal import CRMProposal
from app.models.badge import Badge
__all__ = ["Base"]