"""Billing API — Phase 3 (Stripe).

Prefix: /api/billing
Auth: checkout + subscription GET require get_current_user.
      Stripe webhook is unauthenticated (verified by signature).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.billing import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    SubscriptionResponse,
)
from app.services import billing as billing_svc

router = APIRouter(prefix="/api/billing", tags=["billing"])


@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout(
    body: CheckoutSessionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CheckoutSessionResponse:
    """Create a Stripe Checkout session. Returns a redirect URL."""
    try:
        result = await billing_svc.create_checkout_session(
            user=user,
            tier=body.tier,
            success_url=body.success_url,
            cancel_url=body.cancel_url,
            db=db,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Stripe error: {exc}",
        )
    return CheckoutSessionResponse(**result)


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SubscriptionResponse:
    """Return the current user's subscription status."""
    sub = await billing_svc.get_or_create_subscription(user, db)
    await db.commit()
    return SubscriptionResponse.model_validate(sub)


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Stripe webhook endpoint. Verified via Stripe-Signature header."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        await billing_svc.handle_webhook_event(payload, sig_header, db)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing error: {exc}",
        )

    return {"received": True}
