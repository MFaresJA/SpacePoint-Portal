from __future__ import annotations

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.utils.enums import SubmissionStatus, OnsiteLogStatus


class OnboardingSubmission(Base):
    __tablename__ = "onboarding_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable=False)

    reference_url: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="onboarding_submissions")


class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable=False)

    score: Mapped[float] = mapped_column(Float, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus, name="submission_status"),
        default=SubmissionStatus.PENDING,
        nullable=False,
    )

    attempt: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="quiz_submissions")


class ScenarioSubmission(Base):
    __tablename__ = "scenario_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable=False)

    scenario_url: Mapped[str] = mapped_column(String(500), nullable=False)

    status: Mapped[SubmissionStatus] = mapped_column(
        Enum(SubmissionStatus, name="submission_status"),
        default=SubmissionStatus.PENDING,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="scenario_submissions")


class OnsiteLog(Base):
    __tablename__ = "onsite_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable=False)

    session_type: Mapped[str] = mapped_column(String(30), nullable=False)  # TRAINEE / TRAINER
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_url: Mapped[str] = mapped_column(String(500), nullable=False)

    status: Mapped[OnsiteLogStatus] = mapped_column(
        Enum(OnsiteLogStatus, name="onsite_log_status"),
        default=OnsiteLogStatus.SUBMITTED,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="onsite_logs")