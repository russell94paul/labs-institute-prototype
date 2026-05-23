"""Prop Shield — PropRuleConfig, PropLockoutEvent, UserSubscription, pnl_usd on trades

Revision ID: 0005_prop_shield
Revises: 0004_broker_credentials
Create Date: 2026-05-15

Phase 3 deliverables:
- prop_account_type ENUM
- lockout_state ENUM
- subscription_tier ENUM
- subscription_status ENUM
- prop_rule_configs table
- prop_lockout_events table
- user_subscriptions table
- trades.pnl_usd column (nullable Numeric for dollar P&L from fills)
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0005_prop_shield"
down_revision = "0004_broker_credentials"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # -- ENUMs ---------------------------------------------------------------
    op.execute(
        "CREATE TYPE prop_account_type AS ENUM ('sim', 'eval', 'funded')"
    )
    op.execute(
        "CREATE TYPE lockout_state AS ENUM ('none', 'warning', 'soft_lock', 'hard_lock')"
    )
    op.execute(
        "CREATE TYPE subscription_tier AS ENUM ('free', 'mentor', 'trader')"
    )
    op.execute(
        "CREATE TYPE subscription_status AS ENUM "
        "('active', 'past_due', 'canceled', 'trialing', 'none')"
    )

    # -- prop_rule_configs ---------------------------------------------------
    op.create_table(
        "prop_rule_configs",
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
        sa.Column("account_label", sa.String(128), nullable=False),
        sa.Column(
            "account_type",
            postgresql.ENUM(
                "sim", "eval", "funded",
                name="prop_account_type",
                create_type=False,
            ),
            nullable=False,
            server_default="eval",
        ),
        sa.Column("preset", sa.String(64), nullable=True),
        sa.Column("account_balance", sa.Numeric(12, 2), nullable=False),

        # Rules
        sa.Column("daily_loss_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("trailing_drawdown_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("max_contracts", sa.Integer(), nullable=True),
        sa.Column("max_daily_trades", sa.Integer(), nullable=True),
        sa.Column("forbidden_hours_start", sa.String(5), nullable=True),
        sa.Column("forbidden_hours_end", sa.String(5), nullable=True),
        sa.Column("consistency_rule_pct", sa.Numeric(5, 2), nullable=True),

        # Alert
        sa.Column(
            "alert_threshold_pct",
            sa.Numeric(5, 2),
            nullable=False,
            server_default="80",
        ),
        sa.Column("discord_webhook_url", sa.Text(), nullable=True),

        # State
        sa.Column("high_water_mark", sa.Numeric(12, 2), nullable=False),
        sa.Column(
            "lockout_enabled",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.Column(
            "current_lockout_state",
            postgresql.ENUM(
                "none", "warning", "soft_lock", "hard_lock",
                name="lockout_state",
                create_type=False,
            ),
            nullable=False,
            server_default="none",
        ),

        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index("ix_prop_rule_configs_user_id", "prop_rule_configs", ["user_id"])

    # -- prop_lockout_events -------------------------------------------------
    op.create_table(
        "prop_lockout_events",
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
        sa.Column(
            "rule_config_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("prop_rule_configs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "from_state",
            postgresql.ENUM(
                "none", "warning", "soft_lock", "hard_lock",
                name="lockout_state",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "to_state",
            postgresql.ENUM(
                "none", "warning", "soft_lock", "hard_lock",
                name="lockout_state",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("trigger_rule", sa.String(64), nullable=True),
        sa.Column("trigger_value", sa.Numeric(14, 4), nullable=True),
        sa.Column("trigger_limit", sa.Numeric(14, 4), nullable=True),
        sa.Column(
            "reset_by_user",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    op.create_index(
        "ix_prop_lockout_events_config_id",
        "prop_lockout_events",
        ["rule_config_id"],
    )
    op.create_index(
        "ix_prop_lockout_events_user_id",
        "prop_lockout_events",
        ["user_id"],
    )

    # -- user_subscriptions --------------------------------------------------
    op.create_table(
        "user_subscriptions",
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
            unique=True,
        ),
        sa.Column("stripe_customer_id", sa.String(128), nullable=True, unique=True),
        sa.Column("stripe_subscription_id", sa.String(128), nullable=True, unique=True),
        sa.Column(
            "tier",
            postgresql.ENUM(
                "free", "mentor", "trader",
                name="subscription_tier",
                create_type=False,
            ),
            nullable=False,
            server_default="free",
        ),
        sa.Column(
            "status",
            postgresql.ENUM(
                "active", "past_due", "canceled", "trialing", "none",
                name="subscription_status",
                create_type=False,
            ),
            nullable=False,
            server_default="none",
        ),
        sa.Column("current_period_end", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    # -- trades.pnl_usd (dollar P&L from fill sync) -------------------------
    op.add_column(
        "trades",
        sa.Column("pnl_usd", sa.Numeric(12, 2), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("trades", "pnl_usd")
    op.drop_table("user_subscriptions")
    op.drop_index("ix_prop_lockout_events_user_id", table_name="prop_lockout_events")
    op.drop_index("ix_prop_lockout_events_config_id", table_name="prop_lockout_events")
    op.drop_table("prop_lockout_events")
    op.drop_index("ix_prop_rule_configs_user_id", table_name="prop_rule_configs")
    op.drop_table("prop_rule_configs")
    op.execute("DROP TYPE IF EXISTS subscription_status")
    op.execute("DROP TYPE IF EXISTS subscription_tier")
    op.execute("DROP TYPE IF EXISTS lockout_state")
    op.execute("DROP TYPE IF EXISTS prop_account_type")
