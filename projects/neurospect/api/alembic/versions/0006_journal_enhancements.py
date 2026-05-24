"""journal enhancements: emotion tags, checklist, review structure

Revision ID: 0005
Revises: 0004_broker_credentials
Create Date: 2026-05-23
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

revision = "0006_journal_enhancements"
down_revision = "0005_prop_shield"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE emotion_type AS ENUM (
            'confident', 'fearful', 'greedy', 'patient', 'impulsive', 'revenge'
        )
    """)

    op.add_column("trades", sa.Column("emotion_tags", ARRAY(sa.String()), nullable=True))
    op.add_column("trades", sa.Column("pre_trade_checklist", JSONB(), nullable=True))
    op.add_column("trades", sa.Column("setup_notes", sa.Text(), nullable=True))
    op.add_column("trades", sa.Column("execution_notes", sa.Text(), nullable=True))
    op.add_column("trades", sa.Column("risk_notes", sa.Text(), nullable=True))
    op.add_column("trades", sa.Column("psychology_notes", sa.Text(), nullable=True))
    op.add_column("trades", sa.Column("lesson_learned", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("trades", "lesson_learned")
    op.drop_column("trades", "psychology_notes")
    op.drop_column("trades", "risk_notes")
    op.drop_column("trades", "execution_notes")
    op.drop_column("trades", "setup_notes")
    op.drop_column("trades", "pre_trade_checklist")
    op.drop_column("trades", "emotion_tags")
    op.execute("DROP TYPE emotion_type")
