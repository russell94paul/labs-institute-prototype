"""Prop Shield alert service — Phase 3.

Fires Discord webhook alerts when a rule approaches or reaches its limit.
Designed to be called after evaluate_rules() + sync_lockout_state().
"""
from __future__ import annotations

import logging

import httpx

from app.models.prop_shield import PropRuleConfig
from app.schemas.prop_shield import PropShieldStatus, RuleBreachStatus

log = logging.getLogger(__name__)

# Discord embed colors
_COLOR_WARNING = 0xFFA500   # orange
_COLOR_SOFT_LOCK = 0xFF4500  # red-orange
_COLOR_HARD_LOCK = 0xFF0000  # red


def _rule_label(rule: str) -> str:
    return {
        "daily_loss": "Daily Loss",
        "trailing_drawdown": "Trailing Drawdown",
        "max_contracts": "Position Size",
        "max_daily_trades": "Daily Trade Count",
        "forbidden_hours": "Forbidden Trading Hours",
        "consistency": "Consistency Rule",
        "tilt_loss_streak": "Loss Streak (Tilt)",
        "tilt_revenge": "Revenge Trading (Tilt)",
    }.get(rule, rule.replace("_", " ").title())


def _build_embed(
    config: PropRuleConfig,
    status: PropShieldStatus,
    prev_state: str,
) -> dict:
    state = status.lockout_state
    color = {
        "warning": _COLOR_WARNING,
        "soft_lock": _COLOR_SOFT_LOCK,
        "hard_lock": _COLOR_HARD_LOCK,
    }.get(state, _COLOR_WARNING)

    state_label = {
        "warning": "WARNING",
        "soft_lock": "SOFT LOCK",
        "hard_lock": "HARD LOCK",
    }.get(state, state.upper())

    fields = []
    for rule in status.rules:
        if not rule.active or rule.pct_used is None:
            continue
        if rule.pct_used < config.alert_threshold_pct and not rule.breached:
            continue  # Only include rules at/above threshold
        fields.append({
            "name": _rule_label(rule.rule),
            "value": (
                f"**{float(rule.pct_used):.1f}%** of limit used\n"
                f"Current: {rule.current_value} | Limit: {rule.limit}"
                + (f"\nHeadroom: {rule.distance_to_breach}" if rule.distance_to_breach is not None else "")
                + (" ⛔ BREACHED" if rule.breached else "")
            ),
            "inline": False,
        })

    return {
        "embeds": [{
            "title": f"Prop Shield — {state_label}",
            "description": (
                f"Account: **{config.account_label}**\n"
                f"State changed: `{prev_state}` → `{state}`\n\n"
                "⚠️ *Advisory only — verify with your prop firm's dashboard.*"
            ),
            "color": color,
            "fields": fields,
            "footer": {"text": "NeuroSpect Prop Shield"},
        }]
    }


async def fire_alert(
    config: PropRuleConfig,
    status: PropShieldStatus,
    prev_state: str,
) -> None:
    """Send a Discord webhook alert if the state changed and a webhook is configured."""
    if not config.discord_webhook_url:
        return
    if status.lockout_state == prev_state:
        return  # No state change — no alert
    if status.lockout_state == "none":
        return  # Resolved state — no alert (avoid spam)

    payload = _build_embed(config, status, prev_state)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(config.discord_webhook_url, json=payload)
            if resp.status_code not in (200, 204):
                log.warning(
                    "Discord webhook returned %s for rule_config %s",
                    resp.status_code,
                    config.id,
                )
    except Exception as exc:
        # Alert failures are non-fatal
        log.warning("Discord alert failed for rule_config %s: %s", config.id, exc)
