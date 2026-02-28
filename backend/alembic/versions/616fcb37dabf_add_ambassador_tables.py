"""add ambassador tables

Revision ID: 616fcb37dabf
Revises: 92712166cf23
Create Date: 2026-02-28 11:14:21.289478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '616fcb37dabf'
down_revision: Union[str, Sequence[str], None] = '92712166cf23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "recruitment_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ambassador_user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("contact", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDING"),
        sa.Column("notes", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_recruitment_entries_id", "recruitment_entries", ["id"])
    op.create_index("ix_recruitment_entries_ambassador_user_id", "recruitment_entries", ["ambassador_user_id"])
    op.create_index("ix_recruitment_entries_status", "recruitment_entries", ["status"])

    op.create_table(
        "impact_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ambassador_user_id", sa.Integer(), sa.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_url", sa.String(length=500), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="PENDING"),
        sa.Column("hours", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("people_reached", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_impact_reports_id", "impact_reports", ["id"])
    op.create_index("ix_impact_reports_ambassador_user_id", "impact_reports", ["ambassador_user_id"])
    op.create_index("ix_impact_reports_status", "impact_reports", ["status"])


def downgrade() -> None:
    op.drop_index("ix_impact_reports_status", table_name="impact_reports")
    op.drop_index("ix_impact_reports_ambassador_user_id", table_name="impact_reports")
    op.drop_index("ix_impact_reports_id", table_name="impact_reports")
    op.drop_table("impact_reports")

    op.drop_index("ix_recruitment_entries_status", table_name="recruitment_entries")
    op.drop_index("ix_recruitment_entries_ambassador_user_id", table_name="recruitment_entries")
    op.drop_index("ix_recruitment_entries_id", table_name="recruitment_entries")
    op.drop_table("recruitment_entries")