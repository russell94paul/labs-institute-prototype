"""Tests for behavior metrics calculations (Phase 2).

Tests the pure calculation functions directly with mock trade dicts.
No database needed.
"""
import os
import uuid
from datetime import date, datetime, timezone

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")
os.environ.setdefault("BROKER_CRED_SECRET", "S3Jb5QZQK2UhMFHN4CjCiJMf3gqrJlpYktNbxFKHt1I=")

from app.services.behavior import (
    _calc_consistency,
    _calc_discipline,
    _calc_overtrading,
    _calc_rule_breaches,
    _calc_tilt_score,
    _detect_revenge_trades,
)


def _trade(
    outcome="win",
    instrument="NQ",
    trade_date=None,
    entry_time=None,
    exit_time=None,
    position_size=1,
    r_multiple=1.0,
    pnl_usd=None,
    htf_bias=None,
    plan_followed=True,
    mistake_tags=None,
    quality_grade=None,
    session=None,
):
    return {
        "id": uuid.uuid4(),
        "trade_date": trade_date or date(2026, 5, 20),
        "instrument": instrument,
        "outcome": outcome,
        "r_multiple": r_multiple,
        "pnl_usd": pnl_usd,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "position_size": position_size,
        "htf_bias": htf_bias,
        "plan_followed": plan_followed,
        "mistake_tags": mistake_tags,
        "quality_grade": quality_grade,
        "session": session,
    }


def _dt(hour, minute=0):
    return datetime(2026, 5, 20, hour, minute, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Tilt score
# ---------------------------------------------------------------------------

class TestTiltScore:
    def test_empty_history(self):
        result = _calc_tilt_score([])
        assert result["score"] == 0
        assert result["consecutive_losses"] == 0

    def test_no_tilt_all_wins(self):
        trades = [_trade(outcome="win") for _ in range(5)]
        result = _calc_tilt_score(trades)
        assert result["score"] == 0
        assert result["consecutive_losses"] == 0

    def test_consecutive_losses_increase_score(self):
        trades = [_trade(outcome="loss") for _ in range(3)]
        result = _calc_tilt_score(trades)
        assert result["consecutive_losses"] == 3
        assert result["score"] == 45  # 3 * 15 = 45 (capped component)

    def test_win_breaks_loss_streak(self):
        trades = [
            _trade(outcome="loss"),
            _trade(outcome="loss"),
            _trade(outcome="win"),
            _trade(outcome="loss"),
        ]
        result = _calc_tilt_score(trades)
        assert result["consecutive_losses"] == 1

    def test_rapid_reentry_detected(self):
        trades = [
            _trade(outcome="loss", exit_time=_dt(10, 0)),
            _trade(outcome="win", entry_time=_dt(10, 15)),  # 15 min after loss
        ]
        result = _calc_tilt_score(trades)
        assert result["rapid_reentries"] == 1

    def test_no_rapid_reentry_after_win(self):
        trades = [
            _trade(outcome="win", exit_time=_dt(10, 0)),
            _trade(outcome="win", entry_time=_dt(10, 5)),
        ]
        result = _calc_tilt_score(trades)
        assert result["rapid_reentries"] == 0

    def test_position_escalation_after_loss(self):
        trades = [
            _trade(outcome="loss", position_size=2),
            _trade(outcome="win", position_size=4),  # 4 > 2 * 1.25 = 2.5
        ]
        result = _calc_tilt_score(trades)
        assert result["position_escalations"] == 1

    def test_no_escalation_within_threshold(self):
        trades = [
            _trade(outcome="loss", position_size=4),
            _trade(outcome="win", position_size=4),  # same size
        ]
        result = _calc_tilt_score(trades)
        assert result["position_escalations"] == 0

    def test_single_trade(self):
        result = _calc_tilt_score([_trade(outcome="loss")])
        assert result["consecutive_losses"] == 1
        assert result["rapid_reentries"] == 0
        assert result["position_escalations"] == 0

    def test_max_score_capped_at_100(self):
        trades = [
            _trade(outcome="loss", position_size=1, exit_time=_dt(10, i), entry_time=_dt(10, i))
            for i in range(20)
        ]
        for i in range(1, len(trades)):
            trades[i]["position_size"] = trades[i - 1]["position_size"] * 3
        result = _calc_tilt_score(trades)
        assert result["score"] <= 100


# ---------------------------------------------------------------------------
# Revenge trading detection
# ---------------------------------------------------------------------------

class TestRevengeTrades:
    def test_no_revenge_on_empty(self):
        assert _detect_revenge_trades([]) == []

    def test_detects_same_instrument_rapid_entry_after_loss(self):
        trades = [
            _trade(outcome="loss", instrument="NQ", exit_time=_dt(10, 0)),
            _trade(outcome="win", instrument="NQ", entry_time=_dt(10, 20)),
        ]
        flagged = _detect_revenge_trades(trades)
        assert len(flagged) == 1
        assert flagged[0]["instrument"] == "NQ"
        assert flagged[0]["minutes_after_loss"] == 20.0

    def test_no_revenge_different_instrument(self):
        trades = [
            _trade(outcome="loss", instrument="NQ", exit_time=_dt(10, 0)),
            _trade(outcome="win", instrument="ES", entry_time=_dt(10, 10)),
        ]
        assert _detect_revenge_trades(trades) == []

    def test_no_revenge_after_win(self):
        trades = [
            _trade(outcome="win", instrument="NQ", exit_time=_dt(10, 0)),
            _trade(outcome="loss", instrument="NQ", entry_time=_dt(10, 5)),
        ]
        assert _detect_revenge_trades(trades) == []

    def test_no_revenge_outside_window(self):
        trades = [
            _trade(outcome="loss", instrument="NQ", exit_time=_dt(10, 0)),
            _trade(outcome="win", instrument="NQ", entry_time=_dt(11, 0)),  # 60 min
        ]
        assert _detect_revenge_trades(trades) == []

    def test_against_bias_flagged(self):
        trades = [
            _trade(outcome="loss", instrument="NQ", exit_time=_dt(10, 0), htf_bias="bullish"),
            _trade(outcome="win", instrument="NQ", entry_time=_dt(10, 10), htf_bias="bearish"),
        ]
        flagged = _detect_revenge_trades(trades)
        assert len(flagged) == 1
        assert flagged[0]["against_bias"] is True

    def test_no_timestamps_skipped(self):
        trades = [
            _trade(outcome="loss", instrument="NQ", exit_time=None),
            _trade(outcome="win", instrument="NQ", entry_time=_dt(10, 5)),
        ]
        assert _detect_revenge_trades(trades) == []


# ---------------------------------------------------------------------------
# Overtrading
# ---------------------------------------------------------------------------

class TestOvertrading:
    def test_no_overtrading_under_limit(self):
        trades = [_trade(trade_date=date(2026, 5, 20)) for _ in range(5)]
        result = _calc_overtrading(trades)
        assert result["overtrading_days"] == 0

    def test_overtrading_detected(self):
        trades = [_trade(trade_date=date(2026, 5, 20)) for _ in range(8)]
        result = _calc_overtrading(trades)
        assert result["overtrading_days"] == 1
        assert result["total_excess_trades"] == 3
        assert result["worst_days"][0]["count"] == 8

    def test_empty_history(self):
        result = _calc_overtrading([])
        assert result["overtrading_days"] == 0

    def test_multiple_days(self):
        trades = (
            [_trade(trade_date=date(2026, 5, 20)) for _ in range(7)]
            + [_trade(trade_date=date(2026, 5, 21)) for _ in range(3)]
        )
        result = _calc_overtrading(trades)
        assert result["overtrading_days"] == 1  # only 5/20


# ---------------------------------------------------------------------------
# Rule breaches
# ---------------------------------------------------------------------------

class TestRuleBreaches:
    def test_empty_history(self):
        result = _calc_rule_breaches([])
        assert result["total"] == 0
        assert result["rate"] == 0.0

    def test_all_clean(self):
        trades = [_trade(plan_followed=True, mistake_tags=None) for _ in range(5)]
        result = _calc_rule_breaches(trades)
        assert result["total"] == 0

    def test_plan_not_followed(self):
        trades = [
            _trade(plan_followed=False),
            _trade(plan_followed=True),
        ]
        result = _calc_rule_breaches(trades)
        assert result["plan_not_followed"] == 1
        assert result["total"] == 1

    def test_with_mistakes(self):
        trades = [_trade(mistake_tags=["chased", "oversize"])]
        result = _calc_rule_breaches(trades)
        assert result["with_mistakes"] == 1

    def test_both_plan_and_mistakes_not_double_counted(self):
        trades = [_trade(plan_followed=False, mistake_tags=["chased"])]
        result = _calc_rule_breaches(trades)
        assert result["total"] == 1  # one unique trade
        assert result["plan_not_followed"] == 1
        assert result["with_mistakes"] == 1


# ---------------------------------------------------------------------------
# Consistency
# ---------------------------------------------------------------------------

class TestConsistency:
    def test_empty_history(self):
        result = _calc_consistency([])
        assert result["score"] == 0
        assert result["daily_return_stddev"] is None

    def test_single_trade(self):
        result = _calc_consistency([_trade()])
        assert result["score"] == 0

    def test_consistent_returns(self):
        trades = [
            _trade(trade_date=date(2026, 5, 20), r_multiple=1.0),
            _trade(trade_date=date(2026, 5, 21), r_multiple=1.0),
            _trade(trade_date=date(2026, 5, 22), r_multiple=1.0),
        ]
        result = _calc_consistency(trades)
        assert result["score"] == 100  # zero variance
        assert result["daily_return_stddev"] == 0.0

    def test_volatile_returns(self):
        trades = [
            _trade(trade_date=date(2026, 5, 20), r_multiple=5.0),
            _trade(trade_date=date(2026, 5, 21), r_multiple=-5.0),
        ]
        result = _calc_consistency(trades)
        assert result["score"] == 0  # stddev = 5.0 → score = max(0, 100 - 100) = 0

    def test_null_r_multiple_ignored(self):
        trades = [
            _trade(trade_date=date(2026, 5, 20), r_multiple=1.0),
            _trade(trade_date=date(2026, 5, 21), r_multiple=None),
            _trade(trade_date=date(2026, 5, 22), r_multiple=1.0),
        ]
        result = _calc_consistency(trades)
        assert result["trading_days"] == 2


# ---------------------------------------------------------------------------
# Discipline (composite)
# ---------------------------------------------------------------------------

class TestDiscipline:
    def test_empty_history(self):
        tilt = {"score": 0, "consecutive_losses": 0, "rapid_reentries": 0, "position_escalations": 0}
        breaches = {"total": 0, "plan_not_followed": 0, "with_mistakes": 0, "rate": 0.0}
        consistency = {"score": 0, "daily_return_stddev": None, "trading_days": 0}
        result = _calc_discipline(tilt, breaches, consistency, [])
        assert result["score"] == 0

    def test_perfect_discipline(self):
        tilt = {"score": 0, "consecutive_losses": 0, "rapid_reentries": 0, "position_escalations": 0}
        breaches = {"total": 0, "plan_not_followed": 0, "with_mistakes": 0, "rate": 0.0}
        consistency = {"score": 100, "daily_return_stddev": 0.0, "trading_days": 5}
        trades = [_trade() for _ in range(5)]
        result = _calc_discipline(tilt, breaches, consistency, trades)
        # rule_adherence=1.0*40 + tilt_control=100*0.35 + consistency=100*0.25 = 40+35+25 = 100
        assert result["score"] == 100

    def test_poor_discipline(self):
        tilt = {"score": 80, "consecutive_losses": 5, "rapid_reentries": 3, "position_escalations": 2}
        breaches = {"total": 4, "plan_not_followed": 3, "with_mistakes": 2, "rate": 0.8}
        consistency = {"score": 10, "daily_return_stddev": 4.5, "trading_days": 5}
        trades = [_trade() for _ in range(5)]
        result = _calc_discipline(tilt, breaches, consistency, trades)
        # rule_adherence=0.2*40=8, tilt_control=20*0.35=7, consistency=10*0.25=2.5 → 17
        assert result["score"] == 17

    def test_score_clamped_0_to_100(self):
        tilt = {"score": 100}
        breaches = {"rate": 1.0}
        consistency = {"score": 0}
        trades = [_trade()]
        result = _calc_discipline(tilt, breaches, consistency, trades)
        assert 0 <= result["score"] <= 100
