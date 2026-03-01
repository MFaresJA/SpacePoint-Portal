from __future__ import annotations

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # optional helpful fields
    difficulty: Mapped[str | None] = mapped_column(String(30), nullable=True)  # BEGINNER/MID/ADV
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    challenge_id: Mapped[int] = mapped_column(
        ForeignKey("challenges.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    solution_url: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default="PENDING")  # PENDING/APPROVED/REJECTED

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SubmissionReview(Base):
    __tablename__ = "submission_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    submission_id: Mapped[int] = mapped_column(
        ForeignKey("challenge_submissions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    reviewer_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(String(30), nullable=False)  # APPROVED/REJECTED
    feedback: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class InternTodo(Base):
    __tablename__ = "intern_todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String(300), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, server_default="TODO")  # TODO/IN_PROGRESS/DONE

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)