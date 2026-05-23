"""Prop Shield models — Phase 3.

PropRuleConfig: per-account rule configuration (daily loss, trailing DD, etc.)
PropLockoutEvent: audit log for every lockout state transition.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PropRuleConfig(Base):
    __tablename__ = "prop_rule_configs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Account metadata
    account_label: Mapped[str] = mapped_column(String(128), nullable=False)
    account_type: Mapped[str] = mapped_column(
        SAEnum("sim", "eval", "funded", name="prop_account_type", create_type=False),
        nullable=False,
        default="eval",
    )
    preset: Mapped[str | None] = mapped_column(String(64))  # e.g., "apex_150k"
    account_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )  # starting balance for % rule calculations

    # --- Rules (all optional; None = rule not active) ---

    # Daily loss limit
    daily_loss_limit: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    # Trailing drawdown from high-water mark
    trailing_drawdown_limit: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    # Position size
    max_contracts: Mapped[int | None] = mapped_column(Integer)

    # Trade frequency
    max_daily_trades: Mapped[int | None] = mapped_column(Integer)

    # Forbidden hours (UTC, "HH:MM" format)
    forbidden_hours_start: Mapped[str | None] = mapped_column(String(5))
    forbidden_hours_end: Mapped[str | None] = mapped_column(String(5))

    # Consistency rule: max single-day profit as % of cumulative profit (0-100)
    consistency_rule_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))

    # --- Alert settings ---
    alert_threshold_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("80")
    )
    discord_webhook_url: Mapped[str | None] = mapped_column(Text)

    # --- State ---
    # High-water mark for trailing drawdown (starts at account_balance, updated by rule engine)
    high_water_mark: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Feature flag: lockout UI warnings enabled
    lockout_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    # Current lockout state (cached; authoritative source = PropLockoutEvent)
    current_lockout_state: Mapped[str] = mapped_column(
        SAEnum("none", "warning", "soft_lock", "hard_lock", name="lockout_state", create_type=False),
        nullable=False,
        default="none",
        server_default="none",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class PropLockoutEvent(Base):
    """Immutable audit log of every lockout state transition.

    Every state change (including manual resets) is appended here.
    Never update or delete rows — append only.
    """

    __tablename__ = "prop_lockout_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    rule_config_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("prop_rule_configs.id", ondelete="CASCADE"),
        nullable=False,
    )

    from_state: Mapped[str] = mapped_column(
        SAEnum("none", "warning", "soft_lock", "hard_lock", name="lockout_state", create_type=False),
        nullable=False,
    )
    to_state: Mapped[str] = mapped_column(
        SAEnum("none", "warning", "soft_lock", "hard_lock", name="lockout_state", create_type=False),
        nullable=False,
    )

    # Which rule triggered the transition
    trigger_rule: Mapped[str | None] = mapped_column(String(64))
    # Current value and limit at transition time
    trigger_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))
    trigger_limit: Mapped[Decimal | None] = mapped_column(Numeric(14, 4))

    reset_by_user: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    note: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
