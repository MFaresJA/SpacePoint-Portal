from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from app.db.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_suspended = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    onboarding_submissions = relationship("OnboardingSubmission", back_populates="user", cascade="all, delete-orphan")
    quiz_submissions = relationship("QuizSubmission", back_populates="user", cascade="all, delete-orphan")
    scenario_submissions = relationship("ScenarioSubmission", back_populates="user", cascade="all, delete-orphan")

