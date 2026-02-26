"""add applications table

Revision ID: 92712166cf23
Revises: 9fccd3f102a8
Create Date: 2026-02-25 21:33:38.471230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "92712166cf23"
down_revision = "9fccd3f102a8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),

        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True),

        # why are they applying?
        sa.Column("track", sa.String(length=20), nullable=False),  # "intern" or "instructor"

        # basic info (as you listed)
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("phone_number", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("university", sa.String(length=255), nullable=False),
        sa.Column("highest_degree", sa.String(length=50), nullable=False),

        sa.Column("city_of_residence", sa.String(length=50), nullable=False),

        # store multi-select as JSON (simple + flexible)
        sa.Column("deliver_cities", sa.JSON(), nullable=False),     # e.g. ["Dubai","Abu Dhabi"]
        sa.Column("background_areas", sa.JSON(), nullable=False),   # e.g. ["Engineering","Science"]

        # summaries
        sa.Column("video1_summary", sa.Text(), nullable=False),
        sa.Column("video2_summary", sa.Text(), nullable=False),
        sa.Column("video3_summary", sa.Text(), nullable=False),

        # file paths on disk
        sa.Column("space_terms_pdf_path", sa.String(length=500), nullable=False),
        sa.Column("cv_pdf_path", sa.String(length=500), nullable=False),

        # review/admin
        sa.Column("status", sa.String(length=20), nullable=False, server_default="SUBMITTED"),  # SUBMITTED/UNDER_REVIEW/APPROVED/REJECTED
        sa.Column("admin_notes", sa.String(length=1000), nullable=True),

        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_applications_user_id_created_at", "applications", ["user_id", "created_at"])
    op.create_index("ix_applications_status", "applications", ["status"])


def downgrade():
    op.drop_index("ix_applications_status", table_name="applications")
    op.drop_index("ix_applications_user_id_created_at", table_name="applications")
    op.drop_table("applications")