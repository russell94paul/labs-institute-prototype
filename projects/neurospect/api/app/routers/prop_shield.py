"""Prop Shield API — Phase 3.

Prefix: /api/prop-shield
Auth: all endpoints require get_current_user.

Disclaimer: Prop Shield monitors trading data and alerts users to rule status,
but cannot guarantee prevention of rule violations.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, get_db
from app.models.prop_shield import PropRuleConfig
from app.models.user import User
from app.schemas.prop_shield import (
    LockoutResetRequest,
    PropFirmPreset,
    PropLockoutEventResponse,
    PropRuleConfigCreate,
    PropRuleConfigResponse,
    PropRuleConfigUpdate,
    PropShieldStatus,
)
from app.services import prop_alerts, prop_lockout, prop_rule_engine
from app.services.prop_presets import apply_preset_to_create_data, get_preset, list_presets

router = APIRouter(prefix="/api/prop-shield", tags=["prop-shield"])


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

@router.get("/presets", response_model=list[PropFirmPreset])
async def get_presets() -> list[PropFirmPreset]:
    """Return all available prop firm presets."""
    return list_presets()


# ---------------------------------------------------------------------------
# Rule config CRUD
# ---------------------------------------------------------------------------

@router.get("/configs", response_model=list[PropRuleConfigResponse])
async def list_configs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[PropRuleConfigResponse]:
    result = await db.execute(
        select(PropRuleConfig)
        .where(PropRuleConfig.user_id == user.id)
        .order_by(PropRuleConfig.created_at.asc())
    )
    return [PropRuleConfigResponse.model_validate(c) for c in result.scalars().all()]


@router.post("/configs", response_model=PropRuleConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_config(
    body: PropRuleConfigCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropRuleConfigResponse:
    """Create a new prop rule config. If preset is set, merges preset defaults."""
    data = body.model_dump()

    # Apply preset fields if specified and fields not explicitly set
    if body.preset:
        preset = get_preset(body.preset)
        if preset is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown preset: {body.preset}",
            )
        preset_data = apply_preset_to_create_data(body.preset)
        for field, value in preset_data.items():
            if data.get(field) is None:
                data[field] = value

    config = PropRuleConfig(
        user_id=user.id,
        high_water_mark=body.account_balance,  # starts at account balance
        **{k: v for k, v in data.items() if k != "account_balance"},
        account_balance=body.account_balance,
    )
    db.add(config)
    await db.commit()
    await db.refresh(config)
    return PropRuleConfigResponse.model_validate(config)


@router.get("/configs/{config_id}", response_model=PropRuleConfigResponse)
async def get_config(
    config_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropRuleConfigResponse:
    config = await _get_config_or_404(config_id, user.id, db)
    return PropRuleConfigResponse.model_validate(config)


@router.patch("/configs/{config_id}", response_model=PropRuleConfigResponse)
async def update_config(
    config_id: uuid.UUID,
    body: PropRuleConfigUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropRuleConfigResponse:
    config = await _get_config_or_404(config_id, user.id, db)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    config.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(config)
    return PropRuleConfigResponse.model_validate(config)


@router.delete("/configs/{config_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_config(
    config_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    config = await _get_config_or_404(config_id, user.id, db)
    await db.delete(config)
    await db.commit()


# ---------------------------------------------------------------------------
# Status (computed, not stored)
# ---------------------------------------------------------------------------

@router.get("/configs/{config_id}/status", response_model=PropShieldStatus)
async def get_status(
    config_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropShieldStatus:
    """Evaluate all rules and return current distance-to-breach for each."""
    config = await _get_config_or_404(config_id, user.id, db)
    prev_state = config.current_lockout_state

    status_snapshot = await prop_rule_engine.evaluate_rules(config, db, user.id)

    # Sync lockout state (may update config.current_lockout_state + append audit event)
    new_state = await prop_lockout.sync_lockout_state(config, status_snapshot, db)
    status_snapshot = status_snapshot.model_copy(update={"lockout_state": new_state})

    await db.commit()

    # Fire alert if state changed
    if config.lockout_enabled and new_state != prev_state:
        await prop_alerts.fire_alert(config, status_snapshot, prev_state)

    return status_snapshot


# ---------------------------------------------------------------------------
# Lockout management
# ---------------------------------------------------------------------------

@router.post("/configs/{config_id}/reset-lockout", response_model=PropRuleConfigResponse)
async def reset_lockout(
    config_id: uuid.UUID,
    body: LockoutResetRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropRuleConfigResponse:
    """Manually reset the lockout state to 'none' after user review."""
    config = await _get_config_or_404(config_id, user.id, db)
    await prop_lockout.manual_reset(config, db, note=body.note)
    await db.commit()
    await db.refresh(config)
    return PropRuleConfigResponse.model_validate(config)


@router.get("/configs/{config_id}/lockout-history", response_model=list[PropLockoutEventResponse])
async def get_lockout_history(
    config_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=200),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[PropLockoutEventResponse]:
    """Return the lockout event audit log for a config, newest first."""
    await _get_config_or_404(config_id, user.id, db)  # ownership check
    events = await prop_lockout.get_lockout_history(config_id, user.id, db, limit=limit)
    return [PropLockoutEventResponse.model_validate(e) for e in events]


# ---------------------------------------------------------------------------
# Tilt integration endpoint
# ---------------------------------------------------------------------------

@router.post("/configs/{config_id}/apply-tilt", response_model=PropRuleConfigResponse)
async def apply_tilt(
    config_id: uuid.UUID,
    loss_streak: int = Query(0, ge=0),
    revenge_detected: bool = Query(False),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PropRuleConfigResponse:
    """Apply tilt signals from Phase 2 behavior metrics to the lockout state machine."""
    config = await _get_config_or_404(config_id, user.id, db)
    await prop_lockout.apply_tilt_lockout(config, loss_streak, revenge_detected, db)
    await db.commit()
    await db.refresh(config)
    return PropRuleConfigResponse.model_validate(config)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _get_config_or_404(
    config_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession
) -> PropRuleConfig:
    result = await db.execute(
        select(PropRuleConfig).where(
            PropRuleConfig.id == config_id,
            PropRuleConfig.user_id == user_id,
        )
    )
    config = result.scalar_one_or_none()
    if config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule config not found")
    return config
