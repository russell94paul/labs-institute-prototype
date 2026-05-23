"""Prop Shield rule engine — Phase 3.

Calculates real-time distance-to-breach for each configured rule.
Reads from the trades table (pnl_usd field) and current PropRuleConfig state.

All calculations are advisory only. See disclaimer in PropShieldStatus.
"""
from __future__ import annotations

import uuid
from datetime import date, datetime, time, timezone
from decimal import Decimal

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prop_shield import PropRuleConfig
from app.models.trade import Trade
from app.schemas.prop_shield import PropShieldStatus, RuleBreachStatus

_ZERO = Decimal("0")
_ONE_HUNDRED = Decimal("100")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _get_daily_pnl(
    db: AsyncSession, user_id: uuid.UUID, trade_date: date
) -> Decimal:
    """Sum of pnl_usd for all closed trades on trade_date. Returns 0 if none."""
    sql = text("""
        SELECT COALESCE(SUM(pnl_usd), 0)
        FROM trades
        WHERE user_id = :uid
          AND trade_date = :td
          AND status = 'closed'
          AND NOT is_deleted
          AND pnl_usd IS NOT NULL
    """)
    result = await db.execute(sql, {"uid": str(user_id), "td": trade_date})
    return Decimal(str(result.scalar() or 0))


async def _get_daily_trade_count(
    db: AsyncSession, user_id: uuid.UUID, trade_date: date
) -> int:
    """Count of closed trades on trade_date."""
    sql = text("""
        SELECT COUNT(*)
        FROM trades
        WHERE user_id = :uid
          AND trade_date = :td
          AND status = 'closed'
          AND NOT is_deleted
    """)
    result = await db.execute(sql, {"uid": str(user_id), "td": trade_date})
    return int(result.scalar() or 0)


async def _get_cumulative_pnl(
    db: AsyncSession, user_id: uuid.UUID
) -> Decimal:
    """Sum of pnl_usd across all closed trades (for consistency rule)."""
    sql = text("""
        SELECT COALESCE(SUM(pnl_usd), 0)
        FROM trades
        WHERE user_id = :uid
          AND status = 'closed'
          AND NOT is_deleted
          AND pnl_usd IS NOT NULL
    """)
    result = await db.execute(sql, {"uid": str(user_id)})
    return Decimal(str(result.scalar() or 0))


async def _get_current_position_size(
    db: AsyncSession, user_id: uuid.UUID
) -> int:
    """Max position_size from any currently active trade."""
    sql = text("""
        SELECT COALESCE(MAX(position_size), 0)
        FROM trades
        WHERE user_id = :uid
          AND status = 'active'
          AND NOT is_deleted
    """)
    result = await db.execute(sql, {"uid": str(user_id)})
    return int(result.scalar() or 0)


def _pct_used(current: Decimal, limit: Decimal) -> Decimal:
    """Percentage of a limit consumed. Handles zero limit."""
    if limit == _ZERO:
        return _ONE_HUNDRED
    return (current / limit * _ONE_HUNDRED).quantize(Decimal("0.01"))


def _distance(current: Decimal, limit: Decimal) -> Decimal:
    """Remaining headroom before limit is hit (floored at 0)."""
    return max(_ZERO, limit - current)


def _is_in_forbidden_window(start_str: str, end_str: str) -> bool:
    """Return True if current UTC time is within the forbidden window."""
    now_utc = datetime.now(timezone.utc).time().replace(tzinfo=None)
    start = time.fromisoformat(start_str)
    end = time.fromisoformat(end_str)
    if start <= end:
        return start <= now_utc <= end
    # Wraps midnight
    return now_utc >= start or now_utc <= end


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def evaluate_rules(
    config: PropRuleConfig,
    db: AsyncSession,
    user_id: uuid.UUID,
    today: date | None = None,
) -> PropShieldStatus:
    """Evaluate all rules for a PropRuleConfig and return a status snapshot.

    Updates config.high_water_mark if account equity has risen (caller must commit).
    """
    if today is None:
        today = datetime.now(timezone.utc).date()

    rules: list[RuleBreachStatus] = []

    daily_pnl = await _get_daily_pnl(db, user_id, today)
    daily_trade_count = await _get_daily_trade_count(db, user_id, today)
    cumulative_pnl = await _get_cumulative_pnl(db, user_id)
    current_position_size = await _get_current_position_size(db, user_id)

    # --- 1. Daily loss limit ---
    if config.daily_loss_limit is not None:
        daily_loss = max(_ZERO, -daily_pnl)  # convert to positive loss amount
        pct = _pct_used(daily_loss, config.daily_loss_limit)
        rules.append(RuleBreachStatus(
            rule="daily_loss",
            active=True,
            current_value=daily_loss,
            limit=config.daily_loss_limit,
            pct_used=pct,
            distance_to_breach=_distance(daily_loss, config.daily_loss_limit),
            breached=pct >= _ONE_HUNDRED,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="daily_loss", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- 2. Trailing drawdown ---
    if config.trailing_drawdown_limit is not None:
        # Update high-water mark if current equity is higher
        current_equity = config.account_balance + cumulative_pnl
        if current_equity > config.high_water_mark:
            config.high_water_mark = current_equity
            config.updated_at = datetime.now(timezone.utc)

        drawdown = max(_ZERO, config.high_water_mark - current_equity)
        pct = _pct_used(drawdown, config.trailing_drawdown_limit)
        rules.append(RuleBreachStatus(
            rule="trailing_drawdown",
            active=True,
            current_value=drawdown,
            limit=config.trailing_drawdown_limit,
            pct_used=pct,
            distance_to_breach=_distance(drawdown, config.trailing_drawdown_limit),
            breached=pct >= _ONE_HUNDRED,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="trailing_drawdown", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- 3. Max contracts (position size) ---
    if config.max_contracts is not None:
        pos = Decimal(str(current_position_size))
        limit = Decimal(str(config.max_contracts))
        pct = _pct_used(pos, limit)
        rules.append(RuleBreachStatus(
            rule="max_contracts",
            active=True,
            current_value=pos,
            limit=limit,
            pct_used=pct,
            distance_to_breach=_distance(pos, limit),
            breached=pos > limit,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="max_contracts", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- 4. Max daily trades ---
    if config.max_daily_trades is not None:
        cnt = Decimal(str(daily_trade_count))
        limit = Decimal(str(config.max_daily_trades))
        pct = _pct_used(cnt, limit)
        rules.append(RuleBreachStatus(
            rule="max_daily_trades",
            active=True,
            current_value=cnt,
            limit=limit,
            pct_used=pct,
            distance_to_breach=_distance(cnt, limit),
            breached=cnt >= limit,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="max_daily_trades", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- 5. Forbidden trading hours ---
    if config.forbidden_hours_start and config.forbidden_hours_end:
        in_window = _is_in_forbidden_window(
            config.forbidden_hours_start, config.forbidden_hours_end
        )
        rules.append(RuleBreachStatus(
            rule="forbidden_hours",
            active=True,
            current_value=Decimal("1") if in_window else _ZERO,
            limit=Decimal("0"),  # 0 = must not be in window
            pct_used=_ONE_HUNDRED if in_window else _ZERO,
            distance_to_breach=_ZERO if in_window else None,
            breached=in_window,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="forbidden_hours", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- 6. Consistency rule ---
    if config.consistency_rule_pct is not None and cumulative_pnl > _ZERO:
        max_allowed_day = cumulative_pnl * (config.consistency_rule_pct / _ONE_HUNDRED)
        today_profit = max(_ZERO, daily_pnl)
        pct = _pct_used(today_profit, max_allowed_day) if max_allowed_day > _ZERO else _ZERO
        rules.append(RuleBreachStatus(
            rule="consistency",
            active=True,
            current_value=today_profit,
            limit=max_allowed_day.quantize(Decimal("0.01")),
            pct_used=pct,
            distance_to_breach=_distance(today_profit, max_allowed_day),
            breached=pct >= _ONE_HUNDRED,
        ))
    else:
        rules.append(RuleBreachStatus(
            rule="consistency", active=False,
            current_value=None, limit=None, pct_used=None,
            distance_to_breach=None, breached=False,
        ))

    # --- Compute overall lockout state ---
    lockout_state = _compute_lockout_state(rules, config.alert_threshold_pct)

    return PropShieldStatus(
        rule_config_id=config.id,
        account_label=config.account_label,
        lockout_state=lockout_state,
        lockout_enabled=config.lockout_enabled,
        rules=rules,
        evaluated_at=datetime.now(timezone.utc),
    )


def _compute_lockout_state(
    rules: list[RuleBreachStatus],
    alert_threshold_pct: Decimal,
) -> str:
    """Derive lockout state from rule statuses.

    none      — all rules below alert threshold
    warning   — any rule >= alert_threshold_pct, none breached
    soft_lock — any rule breached (first breach)
    hard_lock — not set here; only set by manual escalation or persistent breach
    """
    active_rules = [r for r in rules if r.active]
    if not active_rules:
        return "none"

    any_breached = any(r.breached for r in active_rules)
    if any_breached:
        return "soft_lock"

    any_warning = any(
        r.pct_used is not None and r.pct_used >= alert_threshold_pct
        for r in active_rules
    )
    if any_warning:
        return "warning"

    return "none"
