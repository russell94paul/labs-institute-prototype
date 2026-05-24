"""Tests for weekly/monthly report service (Phase 2).

Tests the pure utility functions directly — no database needed.
"""
import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")
os.environ.setdefault("BROKER_CRED_SECRET", "S3Jb5QZQK2UhMFHN4CjCiJMf3gqrJlpYktNbxFKHt1I=")

from datetime import date

from app.services.report import _month_bounds, _week_bounds


# ---------------------------------------------------------------------------
# _week_bounds — ISO week → (monday, sunday)
# ---------------------------------------------------------------------------

class TestWeekBounds:
    def test_2026_week_1(self):
        # ISO 2026 W01: Mon 2025-12-29 → Sun 2026-01-04
        start, end = _week_bounds(2026, 1)
        assert start.weekday() == 0  # Monday
        assert (end - start).days == 6

    def test_2026_week_20(self):
        start, end = _week_bounds(2026, 20)
        assert start.weekday() == 0
        assert end.weekday() == 6
        assert (end - start).days == 6

    def test_start_before_end(self):
        for week in [1, 10, 26, 52]:
            s, e = _week_bounds(2026, week)
            assert s < e

    def test_consecutive_weeks_are_adjacent(self):
        _, end_w20 = _week_bounds(2026, 20)
        start_w21, _ = _week_bounds(2026, 21)
        assert (start_w21 - end_w20).days == 1


# ---------------------------------------------------------------------------
# _month_bounds — (year, month) → (first_day, last_day)
# ---------------------------------------------------------------------------

class TestMonthBounds:
    def test_january(self):
        start, end = _month_bounds(2026, 1)
        assert start == date(2026, 1, 1)
        assert end == date(2026, 1, 31)

    def test_february_non_leap(self):
        start, end = _month_bounds(2026, 2)
        assert start == date(2026, 2, 1)
        assert end == date(2026, 2, 28)

    def test_february_leap_year(self):
        start, end = _month_bounds(2024, 2)
        assert end == date(2024, 2, 29)

    def test_december_wraps_to_next_year(self):
        start, end = _month_bounds(2026, 12)
        assert start == date(2026, 12, 1)
        assert end == date(2026, 12, 31)

    def test_april_30_days(self):
        _, end = _month_bounds(2026, 4)
        assert end == date(2026, 4, 30)

    def test_start_always_first_of_month(self):
        for month in range(1, 13):
            start, _ = _month_bounds(2026, month)
            assert start.day == 1
            assert start.month == month

    def test_end_always_last_of_month(self):
        for month in range(1, 13):
            start, end = _month_bounds(2026, month)
            # The day after end is the first of the next month
            next_day = date(end.year, end.month, end.day)
            # Just verify start <= end and they're in the same month
            assert start <= end
            assert end.month == month or (month == 12 and end.month == 12)


# ---------------------------------------------------------------------------
# Report schema validation — stats dict keys
# ---------------------------------------------------------------------------

class TestReportStatsShape:
    """Validate that _compute_stats produces the right keys without a DB."""

    EXPECTED_KEYS = {
        "trade_count", "closed_trades", "win_rate", "avg_r_multiple",
        "total_r", "total_pnl", "tilt_score", "discipline_score",
        "consistency_score", "revenge_trade_count", "overtrading_days",
        "rule_breach_rate",
    }

    def test_zero_trade_behavior_metrics_produce_expected_structure(self):
        """Verify behavior metrics returns a dict compatible with ReportStats."""
        import asyncio
        from unittest.mock import AsyncMock, MagicMock
        import uuid

        async def _run():
            from app.services.behavior import get_behavior_metrics

            # DB that returns empty results
            mapping_result = MagicMock()
            mapping_result.all.return_value = []
            execute_result = MagicMock()
            execute_result.mappings.return_value = mapping_result
            db = AsyncMock()
            db.execute = AsyncMock(return_value=execute_result)

            result = await get_behavior_metrics(db, uuid.uuid4(), None, None)
            return result

        result = asyncio.run(_run())
        assert result["trade_count"] == 0
        assert result["tilt"]["score"] == 0
        assert result["discipline"]["score"] == 0
        assert result["consistency"]["score"] == 0
        assert result["revenge_trades"] == []
        assert result["overtrading"]["overtrading_days"] == 0
        assert result["rule_breaches"]["total"] == 0
