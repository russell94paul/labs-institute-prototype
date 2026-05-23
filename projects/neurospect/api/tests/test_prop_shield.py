"""Tests for Prop Shield rule engine, lockout state machine, and distance-to-breach.

Tests are pure unit tests — no real database, no Stripe calls.
All DB interactions are mocked via AsyncMock following the pattern in test_singleton.py.
"""
from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")
os.environ.setdefault("BROKER_CRED_SECRET", "S3Jb5QZQK2UhMFHN4CjCiJMf3gqrJlpYktNbxFKHt1I=")

import pytest

from app.services.prop_rule_engine import (
    _compute_lockout_state,
    _distance,
    _is_in_forbidden_window,
    _pct_used,
)
from app.services.prop_lockout import apply_tilt_lockout, manual_reset, sync_lockout_state
from app.services.prop_presets import get_preset, list_presets
from app.schemas.prop_shield import RuleBreachStatus

USER_ID = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
CONFIG_ID = uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_config(
    daily_loss_limit=None,
    trailing_drawdown_limit=None,
    max_contracts=None,
    max_daily_trades=None,
    consistency_rule_pct=None,
    account_balance=Decimal("150000"),
    alert_threshold_pct=Decimal("80"),
    current_lockout_state="none",
    lockout_enabled=False,
) -> MagicMock:
    c = MagicMock()
    c.id = CONFIG_ID
    c.user_id = USER_ID
    c.account_label = "Test Account"
    c.account_balance = account_balance
    c.daily_loss_limit = daily_loss_limit
    c.trailing_drawdown_limit = trailing_drawdown_limit
    c.max_contracts = max_contracts
    c.max_daily_trades = max_daily_trades
    c.consistency_rule_pct = consistency_rule_pct
    c.forbidden_hours_start = None
    c.forbidden_hours_end = None
    c.alert_threshold_pct = alert_threshold_pct
    c.discord_webhook_url = None
    c.high_water_mark = account_balance
    c.lockout_enabled = lockout_enabled
    c.current_lockout_state = current_lockout_state
    return c


def _make_rule(rule: str, pct_used: Decimal, breached: bool, limit=Decimal("1000")) -> RuleBreachStatus:
    current = limit * pct_used / Decimal("100")
    return RuleBreachStatus(
        rule=rule,
        active=True,
        current_value=current,
        limit=limit,
        pct_used=pct_used,
        distance_to_breach=max(Decimal("0"), limit - current),
        breached=breached,
    )


def _make_db() -> AsyncMock:
    db = AsyncMock()
    db.add = MagicMock()
    return db


# ---------------------------------------------------------------------------
# _pct_used
# ---------------------------------------------------------------------------

class TestPctUsed:
    def test_zero_current(self):
        assert _pct_used(Decimal("0"), Decimal("3000")) == Decimal("0.00")

    def test_half(self):
        assert _pct_used(Decimal("1500"), Decimal("3000")) == Decimal("50.00")

    def test_at_limit(self):
        assert _pct_used(Decimal("3000"), Decimal("3000")) == Decimal("100.00")

    def test_over_limit(self):
        assert _pct_used(Decimal("4000"), Decimal("3000")) > Decimal("100")

    def test_zero_limit_returns_100(self):
        assert _pct_used(Decimal("1"), Decimal("0")) == Decimal("100")


# ---------------------------------------------------------------------------
# _distance
# ---------------------------------------------------------------------------

class TestDistance:
    def test_full_headroom(self):
        assert _distance(Decimal("0"), Decimal("3000")) == Decimal("3000")

    def test_partial(self):
        assert _distance(Decimal("1000"), Decimal("3000")) == Decimal("2000")

    def test_at_limit(self):
        assert _distance(Decimal("3000"), Decimal("3000")) == Decimal("0")

    def test_over_limit_floored_at_zero(self):
        assert _distance(Decimal("4000"), Decimal("3000")) == Decimal("0")


# ---------------------------------------------------------------------------
# _compute_lockout_state
# ---------------------------------------------------------------------------

class TestComputeLockoutState:
    def test_none_when_no_active_rules(self):
        rules = [
            RuleBreachStatus(rule="daily_loss", active=False, current_value=None,
                             limit=None, pct_used=None, distance_to_breach=None, breached=False)
        ]
        assert _compute_lockout_state(rules, Decimal("80")) == "none"

    def test_none_when_all_below_threshold(self):
        rules = [_make_rule("daily_loss", Decimal("50"), breached=False)]
        assert _compute_lockout_state(rules, Decimal("80")) == "none"

    def test_warning_at_threshold(self):
        rules = [_make_rule("daily_loss", Decimal("80"), breached=False)]
        assert _compute_lockout_state(rules, Decimal("80")) == "warning"

    def test_warning_above_threshold_not_breached(self):
        rules = [_make_rule("daily_loss", Decimal("95"), breached=False)]
        assert _compute_lockout_state(rules, Decimal("80")) == "warning"

    def test_soft_lock_when_breached(self):
        rules = [_make_rule("daily_loss", Decimal("100"), breached=True)]
        assert _compute_lockout_state(rules, Decimal("80")) == "soft_lock"

    def test_soft_lock_when_any_rule_breached(self):
        rules = [
            _make_rule("daily_loss", Decimal("50"), breached=False),
            _make_rule("trailing_drawdown", Decimal("100"), breached=True),
        ]
        assert _compute_lockout_state(rules, Decimal("80")) == "soft_lock"

    def test_warning_mixed_below_and_above_threshold(self):
        rules = [
            _make_rule("daily_loss", Decimal("30"), breached=False),
            _make_rule("trailing_drawdown", Decimal("85"), breached=False),
        ]
        assert _compute_lockout_state(rules, Decimal("80")) == "warning"


# ---------------------------------------------------------------------------
# Daily loss rule
# ---------------------------------------------------------------------------

class TestDailyLossRule:
    async def test_daily_loss_at_0_pct(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(daily_loss_limit=Decimal("3000"))

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("500"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=2)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("500"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=0)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        daily_rule = next(r for r in status.rules if r.rule == "daily_loss")
        assert daily_rule.active
        assert daily_rule.current_value == Decimal("0")  # profit day, no loss
        assert daily_rule.pct_used == Decimal("0.00")
        assert not daily_rule.breached

    async def test_daily_loss_at_80_pct(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(daily_loss_limit=Decimal("3000"))

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("-2400"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=3)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("-2400"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=0)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        daily_rule = next(r for r in status.rules if r.rule == "daily_loss")
        assert daily_rule.pct_used == Decimal("80.00")
        assert status.lockout_state == "warning"

    async def test_daily_loss_breached(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(daily_loss_limit=Decimal("3000"))

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("-3200"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=5)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("-3200"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=0)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        daily_rule = next(r for r in status.rules if r.rule == "daily_loss")
        assert daily_rule.breached
        assert daily_rule.distance_to_breach == Decimal("0")
        assert status.lockout_state == "soft_lock"


# ---------------------------------------------------------------------------
# Trailing drawdown
# ---------------------------------------------------------------------------

class TestTrailingDrawdown:
    async def test_trailing_dd_updates_high_water_mark(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(
            trailing_drawdown_limit=Decimal("5000"),
            account_balance=Decimal("150000"),
        )
        config.high_water_mark = Decimal("150000")

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=0)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("2000"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=0)),
        ):
            await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        # Equity = 150000 + 2000 = 152000; HWM should update
        assert config.high_water_mark == Decimal("152000")

    async def test_trailing_dd_breach(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(
            trailing_drawdown_limit=Decimal("5000"),
            account_balance=Decimal("150000"),
        )
        config.high_water_mark = Decimal("155000")  # peak was 155K

        # Current equity = 150K (DD from peak = 5K, exactly at limit)
        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=0)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=0)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        dd_rule = next(r for r in status.rules if r.rule == "trailing_drawdown")
        assert dd_rule.current_value == Decimal("5000")
        assert dd_rule.breached
        assert status.lockout_state == "soft_lock"


# ---------------------------------------------------------------------------
# Max position size
# ---------------------------------------------------------------------------

class TestMaxContracts:
    async def test_position_within_limit(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(max_contracts=10)

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=0)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=5)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        pos_rule = next(r for r in status.rules if r.rule == "max_contracts")
        assert pos_rule.pct_used == Decimal("50.00")
        assert not pos_rule.breached

    async def test_position_over_limit(self):
        from app.services.prop_rule_engine import evaluate_rules

        config = _make_config(max_contracts=10)

        with (
            patch("app.services.prop_rule_engine._get_daily_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_daily_trade_count", AsyncMock(return_value=0)),
            patch("app.services.prop_rule_engine._get_cumulative_pnl", AsyncMock(return_value=Decimal("0"))),
            patch("app.services.prop_rule_engine._get_current_position_size", AsyncMock(return_value=12)),
        ):
            status = await evaluate_rules(config, _make_db(), USER_ID, date(2026, 5, 15))

        pos_rule = next(r for r in status.rules if r.rule == "max_contracts")
        assert pos_rule.breached


# ---------------------------------------------------------------------------
# Tilt lockout
# ---------------------------------------------------------------------------

class TestTiltLockout:
    async def test_loss_streak_triggers_warning(self):
        config = _make_config(current_lockout_state="none")
        db = _make_db()

        new_state = await apply_tilt_lockout(config, loss_streak=3, revenge_detected=False, db=db)

        assert new_state == "warning"
        assert config.current_lockout_state == "warning"
        db.add.assert_called_once()

    async def test_revenge_triggers_soft_lock(self):
        config = _make_config(current_lockout_state="none")
        db = _make_db()

        new_state = await apply_tilt_lockout(config, loss_streak=1, revenge_detected=True, db=db)

        assert new_state == "soft_lock"
        assert config.current_lockout_state == "soft_lock"

    async def test_less_than_3_losses_no_tilt(self):
        config = _make_config(current_lockout_state="none")
        db = _make_db()

        result = await apply_tilt_lockout(config, loss_streak=2, revenge_detected=False, db=db)

        assert result is None
        assert config.current_lockout_state == "none"
        db.add.assert_not_called()

    async def test_hard_lock_blocks_tilt_warning(self):
        config = _make_config(current_lockout_state="hard_lock")
        db = _make_db()

        # Loss streak with hard_lock — not "none" so tilt warning won't fire
        result = await apply_tilt_lockout(config, loss_streak=5, revenge_detected=False, db=db)

        assert result is None
        assert config.current_lockout_state == "hard_lock"


# ---------------------------------------------------------------------------
# Lockout state machine — sync and manual reset
# ---------------------------------------------------------------------------

class TestLockoutStateMachine:
    async def test_manual_reset_from_hard_lock(self):
        config = _make_config(current_lockout_state="hard_lock")
        db = _make_db()

        new_state = await manual_reset(config, db, note="Reviewed — resuming")

        assert new_state == "none"
        assert config.current_lockout_state == "none"
        db.add.assert_called_once()
        event = db.add.call_args[0][0]
        assert event.reset_by_user is True
        assert event.from_state == "hard_lock"
        assert event.to_state == "none"

    async def test_hard_lock_cannot_auto_resolve(self):
        from app.schemas.prop_shield import PropShieldStatus

        config = _make_config(current_lockout_state="hard_lock")
        db = _make_db()

        # Even if rules are now "none", hard_lock must not auto-exit
        status = PropShieldStatus(
            rule_config_id=CONFIG_ID,
            account_label="Test",
            lockout_state="none",  # computed state is "none"
            lockout_enabled=True,
            rules=[],
            evaluated_at=datetime.now(timezone.utc),
        )

        result = await sync_lockout_state(config, status, db)

        # Must stay hard_lock (auto-exit blocked)
        assert result == "hard_lock"
        assert config.current_lockout_state == "hard_lock"

    async def test_none_to_warning_transition(self):
        from app.schemas.prop_shield import PropShieldStatus

        config = _make_config(current_lockout_state="none")
        db = _make_db()

        status = PropShieldStatus(
            rule_config_id=CONFIG_ID,
            account_label="Test",
            lockout_state="warning",
            lockout_enabled=True,
            rules=[_make_rule("daily_loss", Decimal("85"), breached=False)],
            evaluated_at=datetime.now(timezone.utc),
        )

        result = await sync_lockout_state(config, status, db)

        assert result == "warning"
        assert config.current_lockout_state == "warning"
        db.add.assert_called_once()

    async def test_no_event_when_state_unchanged(self):
        from app.schemas.prop_shield import PropShieldStatus

        config = _make_config(current_lockout_state="warning")
        db = _make_db()

        status = PropShieldStatus(
            rule_config_id=CONFIG_ID,
            account_label="Test",
            lockout_state="warning",
            lockout_enabled=True,
            rules=[],
            evaluated_at=datetime.now(timezone.utc),
        )

        result = await sync_lockout_state(config, status, db)

        assert result == "warning"
        db.add.assert_not_called()


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

class TestPresets:
    def test_all_required_firms_present(self):
        presets = {p.preset_id for p in list_presets()}
        for expected in ["apex_150k", "apex_100k", "apex_50k", "topstep_150k",
                         "ftmo_100k", "earn2trade_100k", "mff_100k"]:
            assert expected in presets, f"Missing preset: {expected}"

    def test_apex_150k_rules(self):
        p = get_preset("apex_150k")
        assert p is not None
        assert p.daily_loss_limit == Decimal("3000")
        assert p.trailing_drawdown_limit == Decimal("5000")
        assert p.max_contracts == 20

    def test_topstep_has_consistency_rule(self):
        p = get_preset("topstep_150k")
        assert p is not None
        assert p.consistency_rule_pct is not None
        assert p.consistency_rule_pct == Decimal("30")

    def test_ftmo_no_max_contracts(self):
        p = get_preset("ftmo_100k")
        assert p is not None
        assert p.max_contracts is None

    def test_unknown_preset_returns_none(self):
        assert get_preset("nonexistent_firm_xyz") is None
