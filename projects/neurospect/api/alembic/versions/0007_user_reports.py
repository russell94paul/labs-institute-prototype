"""Create user_reports table for weekly/monthly analytics snapshots

Revision ID: 0007_user_reports
Revises: 0006_journal_enhancements
Create Date: 2026-05-24
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0007_user_reports"
down_revision = "0006_journal_enhancements"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_reports",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("period_type", sa.String(10), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("period_number", sa.Integer(), nullable=False),
        sa.Column("stats", postgresql.JSONB(), nullable=False),
        sa.Column(
            "computed_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.UniqueConstraint(
            "user_id", "period_type", "year", "period_number",
            name="uq_user_report_period",
        ),
    )
    op.create_index("ix_user_reports_user_id", "user_reports", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_user_reports_user_id", table_name="user_reports")
    op.drop_table("user_reports")
