"""add points ledger

Revision ID: 999c4285367e
Revises: b227decbaa95
Create Date: 2026-03-02 01:26:28.095042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '999c4285367e'
down_revision: Union[str, Sequence[str], None] = 'b227decbaa95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "points_ledger",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=200), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_points_ledger_id"), "points_ledger", ["id"], unique=False)
    op.create_index(op.f("ix_points_ledger_user_id"), "points_ledger", ["user_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_points_ledger_user_id"), table_name="points_ledger")
    op.drop_index(op.f("ix_points_ledger_id"), table_name="points_ledger")
    op.drop_table("points_ledger")