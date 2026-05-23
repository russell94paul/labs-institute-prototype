"""User subscription model — Phase 3 (Stripe billing).

Tracks the active Stripe subscription for each user.
One row per user; upserted when Stripe sends webhook events.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    stripe_customer_id: Mapped[str | None] = mapped_column(String(128), unique=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(128), unique=True)

    tier: Mapped[str] = mapped_column(
        SAEnum("free", "mentor", "trader", name="subscription_tier", create_type=False),
        nullable=False,
        default="free",
        server_default="free",
    )
    status: Mapped[str] = mapped_column(
        SAEnum(
            "active", "past_due", "canceled", "trialing", "none",
            name="subscription_status",
            create_type=False,
        ),
        nullable=False,
        default="none",
        server_default="none",
    )

    current_period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
