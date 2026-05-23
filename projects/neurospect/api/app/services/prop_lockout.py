"""Prop Shield lockout state machine — Phase 3.

Handles state transitions, tilt integration, and audit logging.
Every state change appends a PropLockoutEvent row (append-only).

State machine:
  none → warning → soft_lock → hard_lock
  hard_lock → none (manual reset only)
  soft_lock → none (manual reset)
  any → none (manual reset)

Tilt integration (from Phase 2 behavior metrics):
  3+ consecutive losses → tilt warning appended to lockout events
  Revenge trading detected → soft_lock suggestion
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prop_shield import PropLockoutEvent, PropRuleConfig
from app.schemas.prop_shield import PropShieldStatus, RuleBreachStatus

# Valid state transitions (from → allowed tos)
_ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "none":      {"warning", "soft_lock", "hard_lock"},
    "warning":   {"none", "soft_lock", "hard_lock"},
    "soft_lock": {"none", "warning", "hard_lock"},
    "hard_lock": {"none"},
}

# State severity order (higher = worse)
_SEVERITY: dict[str, int] = {
    "none": 0,
    "warning": 1,
    "soft_lock": 2,
    "hard_lock": 3,
}


def _most_severe_rule(rules: list[RuleBreachStatus]) -> RuleBreachStatus | None:
    """Return the rule with the highest pct_used."""
    active = [r for r in rules if r.active and r.pct_used is not None]
    if not active:
        return None
    return max(active, key=lambda r: r.pct_used or Decimal("0"))


async def sync_lockout_state(
    config: PropRuleConfig,
    status: PropShieldStatus,
    db: AsyncSession,
) -> str:
    """Reconcile the computed lockout state against the stored state.

    If state changed, appends a PropLockoutEvent and updates config.current_lockout_state.
    Returns the new state (which may be same as before if no change).

    Caller must commit after this call.
    """
    computed_state = status.lockout_state
    previous_state = config.current_lockout_state

    if computed_state == previous_state:
        return previous_state

    # Enforce: hard_lock can only exit via manual reset
    if previous_state == "hard_lock" and computed_state != "hard_lock":
        # Do not auto-transition out of hard_lock; return hard_lock
        return "hard_lock"

    # Log the transition
    worst_rule = _most_severe_rule(status.rules)
    event = PropLockoutEvent(
        user_id=config.user_id,
        rule_config_id=config.id,
        from_state=previous_state,
        to_state=computed_state,
        trigger_rule=worst_rule.rule if worst_rule else None,
        trigger_value=worst_rule.current_value if worst_rule else None,
        trigger_limit=worst_rule.limit if worst_rule else None,
        reset_by_user=False,
    )
    db.add(event)

    config.current_lockout_state = computed_state
    config.updated_at = datetime.now(timezone.utc)

    # Escalate soft_lock → hard_lock if already in soft_lock and still breached
    if previous_state == "soft_lock" and computed_state == "soft_lock":
        # Already in soft_lock — escalate to hard_lock
        hard_event = PropLockoutEvent(
            user_id=config.user_id,
            rule_config_id=config.id,
            from_state="soft_lock",
            to_state="hard_lock",
            trigger_rule=worst_rule.rule if worst_rule else None,
            trigger_value=worst_rule.current_value if worst_rule else None,
            trigger_limit=worst_rule.limit if worst_rule else None,
            reset_by_user=False,
            note="Auto-escalated: rule breach persisted while in soft_lock.",
        )
        db.add(hard_event)
        config.current_lockout_state = "hard_lock"
        return "hard_lock"

    return computed_state


async def manual_reset(
    config: PropRuleConfig,
    db: AsyncSession,
    note: str | None = None,
) -> str:
    """User manually acknowledges and resets the lockout state to 'none'.

    Always allowed regardless of current state.
    Appends a PropLockoutEvent with reset_by_user=True.
    Caller must commit after this call.
    """
    previous_state = config.current_lockout_state

    event = PropLockoutEvent(
        user_id=config.user_id,
        rule_config_id=config.id,
        from_state=previous_state,
        to_state="none",
        trigger_rule=None,
        trigger_value=None,
        trigger_limit=None,
        reset_by_user=True,
        note=note,
    )
    db.add(event)

    config.current_lockout_state = "none"
    config.updated_at = datetime.now(timezone.utc)

    return "none"


async def apply_tilt_lockout(
    config: PropRuleConfig,
    loss_streak: int,
    revenge_detected: bool,
    db: AsyncSession,
) -> str | None:
    """Integrate Phase 2 tilt signals into the lockout state.

    Returns the new lockout state if it changed, else None.
    Caller must commit after this call.

    Tilt rules:
    - 3+ consecutive losses → warning (if currently none)
    - Revenge trading detected → soft_lock suggestion (if currently warning or none)
    """
    current = config.current_lockout_state
    new_state: str | None = None

    if revenge_detected and current in ("none", "warning"):
        new_state = "soft_lock"
        trigger_rule = "tilt_revenge"
        note = "Revenge trading pattern detected — suggested cooldown."
    elif loss_streak >= 3 and current == "none":
        new_state = "warning"
        trigger_rule = "tilt_loss_streak"
        note = f"{loss_streak} consecutive losses — tilt warning."
    else:
        return None

    event = PropLockoutEvent(
        user_id=config.user_id,
        rule_config_id=config.id,
        from_state=current,
        to_state=new_state,
        trigger_rule=trigger_rule,
        trigger_value=Decimal(str(loss_streak)),
        trigger_limit=Decimal("3"),
        reset_by_user=False,
        note=note,
    )
    db.add(event)

    config.current_lockout_state = new_state
    config.updated_at = datetime.now(timezone.utc)

    return new_state


async def get_lockout_history(
    config_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession,
    limit: int = 50,
) -> list[PropLockoutEvent]:
    result = await db.execute(
        select(PropLockoutEvent)
        .where(
            PropLockoutEvent.rule_config_id == config_id,
            PropLockoutEvent.user_id == user_id,
        )
        .order_by(PropLockoutEvent.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
