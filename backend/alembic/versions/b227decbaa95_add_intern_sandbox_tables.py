"""add intern sandbox tables

Revision ID: b227decbaa95
Revises: 616fcb37dabf
Create Date: 2026-03-01 14:20:53.899377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b227decbaa95'
down_revision: Union[str, Sequence[str], None] = '616fcb37dabf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "challenges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(length=30), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_challenges_id", "challenges", ["id"])

    op.create_table(
        "challenge_submissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("challenge_id", sa.Integer(), sa.ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False),
        sa.Column("solution_url", sa.String(length=500), nullable=False),
        sa.Column("notes", sa.String(length=1000), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDING"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_challenge_submissions_id", "challenge_submissions", ["id"])
    op.create_index("ix_challenge_submissions_user_id", "challenge_submissions", ["user_id"])
    op.create_index("ix_challenge_submissions_challenge_id", "challenge_submissions", ["challenge_id"])
    op.create_index("ix_challenge_submissions_status", "challenge_submissions", ["status"])

    op.create_table(
        "submission_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("submission_id", sa.Integer(), sa.ForeignKey("challenge_submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("decision", sa.String(length=30), nullable=False),
        sa.Column("feedback", sa.String(length=2000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_submission_reviews_id", "submission_reviews", ["id"])
    op.create_index("ix_submission_reviews_submission_id", "submission_reviews", ["submission_id"])
    op.create_index("ix_submission_reviews_reviewer_user_id", "submission_reviews", ["reviewer_user_id"])

    op.create_table(
        "intern_todos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="TODO"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_intern_todos_id", "intern_todos", ["id"])
    op.create_index("ix_intern_todos_user_id", "intern_todos", ["user_id"])
    op.create_index("ix_intern_todos_status", "intern_todos", ["status"])


def downgrade() -> None:
    """Downgrade schema."""
    pass
