"""Billing schemas — Phase 3 (Stripe)."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class CheckoutSessionCreate(BaseModel):
    tier: Literal["mentor", "trader"]
    success_url: str
    cancel_url: str


class CheckoutSessionResponse(BaseModel):
    checkout_url: str
    session_id: str


class SubscriptionResponse(BaseModel):
    tier: str          # "free" | "mentor" | "trader"
    status: str        # "active" | "past_due" | "canceled" | "trialing" | "none"
    current_period_end: datetime | None
    stripe_customer_id: str | None

    model_config = {"from_attributes": True}
