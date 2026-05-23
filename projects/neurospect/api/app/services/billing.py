"""Stripe billing service — Phase 3.

Mentor tier: monthly subscription
Trader tier: monthly subscription

Prices are configured via STRIPE_PRICE_MENTOR_ID and STRIPE_PRICE_TRADER_ID env vars.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.subscription import UserSubscription
from app.models.user import User

log = logging.getLogger(__name__)


def _get_stripe_client() -> stripe.StripeClient:
    return stripe.StripeClient(api_key=settings.stripe_secret_key)


def _price_id_for_tier(tier: str) -> str:
    if tier == "mentor":
        return settings.stripe_price_mentor_id
    if tier == "trader":
        return settings.stripe_price_trader_id
    raise ValueError(f"Unknown tier: {tier}")


async def get_or_create_subscription(
    user: User, db: AsyncSession
) -> UserSubscription:
    result = await db.execute(
        select(UserSubscription).where(UserSubscription.user_id == user.id)
    )
    sub = result.scalar_one_or_none()
    if sub is None:
        sub = UserSubscription(user_id=user.id, tier="free", status="none")
        db.add(sub)
        await db.flush()
    return sub


async def create_checkout_session(
    user: User,
    tier: str,
    success_url: str,
    cancel_url: str,
    db: AsyncSession,
) -> dict:
    """Create a Stripe Checkout session for the given tier.

    Returns {"checkout_url": ..., "session_id": ...}.
    """
    client = _get_stripe_client()
    sub = await get_or_create_subscription(user, db)

    # Create or reuse Stripe customer
    customer_id = sub.stripe_customer_id
    if not customer_id:
        customer = client.customers.create(
            params={
                "metadata": {"neurospect_user_id": str(user.id)},
                "description": f"Discord: {user.discord_username}",
            }
        )
        customer_id = customer.id
        sub.stripe_customer_id = customer_id
        await db.commit()

    session = client.checkout.sessions.create(
        params={
            "customer": customer_id,
            "mode": "subscription",
            "line_items": [{"price": _price_id_for_tier(tier), "quantity": 1}],
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": {
                "neurospect_user_id": str(user.id),
                "tier": tier,
            },
        }
    )
    return {"checkout_url": session.url, "session_id": session.id}


async def handle_webhook_event(payload: bytes, sig_header: str, db: AsyncSession) -> None:
    """Process a raw Stripe webhook payload.

    Handles:
    - checkout.session.completed → activate subscription
    - customer.subscription.updated → update tier/status
    - customer.subscription.deleted → cancel subscription
    """
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.stripe_webhook_secret,
        )
    except stripe.error.SignatureVerificationError:
        raise ValueError("Invalid Stripe webhook signature")

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        user_id_str = data.get("metadata", {}).get("neurospect_user_id")
        tier = data.get("metadata", {}).get("tier", "mentor")
        subscription_id = data.get("subscription")
        customer_id = data.get("customer")

        if not user_id_str:
            log.warning("checkout.session.completed missing neurospect_user_id")
            return

        user_id = uuid.UUID(user_id_str)
        result = await db.execute(
            select(UserSubscription).where(UserSubscription.user_id == user_id)
        )
        sub = result.scalar_one_or_none()
        if sub is None:
            sub = UserSubscription(user_id=user_id)
            db.add(sub)

        sub.stripe_customer_id = customer_id
        sub.stripe_subscription_id = subscription_id
        sub.tier = tier
        sub.status = "active"
        sub.updated_at = datetime.now(timezone.utc)
        await db.commit()

    elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
        customer_id = data.get("customer")
        status = data.get("status", "active")
        current_period_end_ts = data.get("current_period_end")
        result = await db.execute(
            select(UserSubscription).where(
                UserSubscription.stripe_customer_id == customer_id
            )
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = status
            sub.stripe_subscription_id = data.get("id")
            if current_period_end_ts:
                sub.current_period_end = datetime.fromtimestamp(
                    current_period_end_ts, tz=timezone.utc
                )
            sub.updated_at = datetime.now(timezone.utc)
            await db.commit()

    elif event_type == "customer.subscription.deleted":
        customer_id = data.get("customer")
        result = await db.execute(
            select(UserSubscription).where(
                UserSubscription.stripe_customer_id == customer_id
            )
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = "canceled"
            sub.tier = "free"
            sub.updated_at = datetime.now(timezone.utc)
            await db.commit()

    else:
        log.debug("Unhandled Stripe event type: %s", event_type)
