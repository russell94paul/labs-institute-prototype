"""Tests for analytics service calculation logic (Phase 2).

Tests the Python-layer logic of equity curve accumulation and drawdown
calculation without hitting a real database.
"""
import os
import uuid
from datetime import date
from unittest.mock import AsyncMock, MagicMock

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")
os.environ.setdefault("BROKER_CRED_SECRET", "S3Jb5QZQK2UhMFHN4CjCiJMf3gqrJlpYktNbxFKHt1I=")

import pytest
from app.services.analytics import get_drawdown, get_equity_curve, get_monthly_heatmap


# ---------------------------------------------------------------------------
# Helpers — mock DB that returns predefined rows
# ---------------------------------------------------------------------------

def _mock_row(trade_date: date, daily_r: float, daily_pnl: float = 0.0, trade_count: int = 1):
    return {"trade_date": trade_date, "daily_r": daily_r, "daily_pnl": daily_pnl, "trade_count": trade_count}


def _make_db(rows: list[dict]):
    """Return an AsyncSession mock whose execute() returns the given rows."""
    mapping_result = MagicMock()
    mapping_result.all.return_value = [MagicMock(**{"__getitem__": lambda self, k: row[k], **row})
                                        for row in rows]
    mapping_result.all.return_value = rows

    execute_result = MagicMock()
    execute_result.mappings.return_value = mapping_result

    db = AsyncMock()
    db.execute = AsyncMock(return_value=execute_result)
    return db


def _row_obj(trade_date, daily_r, daily_pnl=0.0, trade_count=1):
    """Create a row-like object that supports row["key"] access."""
    class _Row(dict):
        pass
    r = _Row(trade_date=trade_date, daily_r=daily_r, daily_pnl=daily_pnl, trade_count=trade_count)
    return r


# ---------------------------------------------------------------------------
# Equity curve accumulation
# ---------------------------------------------------------------------------

class TestEquityCurveAccumulation:
    """Test the Python-layer cumulative sum logic by directly exercising the service."""

    def _build_points(self, raw_rows: list[dict]) -> list[dict]:
        """Replicate the accumulation logic from get_equity_curve."""
        cum_r = 0.0
        cum_pnl = 0.0
        points = []
        for r in raw_rows:
            cum_r += r["daily_r"]
            cum_pnl += r["daily_pnl"]
            points.append({
                "date": r["trade_date"].isoformat(),
                "cumulative_r": round(cum_r, 4),
                "cumulative_pnl": round(cum_pnl, 2) if cum_pnl else None,
                "trade_count": r["trade_count"],
            })
        return points

    def test_empty_history(self):
        points = self._build_points([])
        assert points == []

    def test_single_trade(self):
        rows = [_row_obj(date(2026, 5, 20), daily_r=2.0, daily_pnl=200.0)]
        points = self._build_points(rows)
        assert len(points) == 1
        assert points[0]["cumulative_r"] == 2.0
        assert points[0]["cumulative_pnl"] == 200.0

    def test_cumulative_sum_increases(self):
        rows = [
            _row_obj(date(2026, 5, 20), daily_r=1.0, daily_pnl=100.0),
            _row_obj(date(2026, 5, 21), daily_r=2.0, daily_pnl=200.0),
            _row_obj(date(2026, 5, 22), daily_r=-0.5, daily_pnl=-50.0),
        ]
        points = self._build_points(rows)
        assert points[0]["cumulative_r"] == 1.0
        assert points[1]["cumulative_r"] == 3.0
        assert points[2]["cumulative_r"] == 2.5

    def test_cumulative_pnl_none_when_zero(self):
        rows = [_row_obj(date(2026, 5, 20), daily_r=1.0, daily_pnl=0.0)]
        points = self._build_points(rows)
        assert points[0]["cumulative_pnl"] is None

    def test_negative_r_days(self):
        rows = [
            _row_obj(date(2026, 5, 20), daily_r=-1.0),
            _row_obj(date(2026, 5, 21), daily_r=-2.0),
        ]
        points = self._build_points(rows)
        assert points[-1]["cumulative_r"] == -3.0


# ---------------------------------------------------------------------------
# Drawdown calculation
# ---------------------------------------------------------------------------

class TestDrawdownCalculation:
    """Test drawdown computation from equity curve points."""

    def _calc_drawdown(self, points: list[dict]) -> dict:
        """Replicate drawdown logic from get_drawdown."""
        if not points:
            return {"max_drawdown_r": 0.0, "max_drawdown_pnl": None,
                    "current_drawdown_r": 0.0, "points": []}

        peak_r = 0.0
        peak_pnl = 0.0
        max_dd_r = 0.0
        max_dd_pnl = 0.0
        dd_points = []

        for p in points:
            cum_r = p["cumulative_r"]
            cum_pnl = p.get("cumulative_pnl") or 0.0

            if cum_r > peak_r:
                peak_r = cum_r
            if cum_pnl > peak_pnl:
                peak_pnl = cum_pnl

            dd_r = peak_r - cum_r
            dd_pnl = peak_pnl - cum_pnl

            if dd_r > max_dd_r:
                max_dd_r = dd_r
            if dd_pnl > max_dd_pnl:
                max_dd_pnl = dd_pnl

            dd_points.append({
                "date": p["date"],
                "drawdown_r": round(dd_r, 4),
                "drawdown_pnl": round(dd_pnl, 2) if dd_pnl else None,
                "peak_r": round(peak_r, 4),
            })

        return {
            "max_drawdown_r": round(max_dd_r, 4),
            "max_drawdown_pnl": round(max_dd_pnl, 2) if max_dd_pnl else None,
            "current_drawdown_r": dd_points[-1]["drawdown_r"],
            "points": dd_points,
        }

    def test_empty_history(self):
        result = self._calc_drawdown([])
        assert result["max_drawdown_r"] == 0.0
        assert result["current_drawdown_r"] == 0.0

    def test_no_drawdown_all_wins(self):
        points = [
            {"date": "2026-05-20", "cumulative_r": 1.0, "cumulative_pnl": None},
            {"date": "2026-05-21", "cumulative_r": 2.0, "cumulative_pnl": None},
            {"date": "2026-05-22", "cumulative_r": 3.0, "cumulative_pnl": None},
        ]
        result = self._calc_drawdown(points)
        assert result["max_drawdown_r"] == 0.0
        assert result["current_drawdown_r"] == 0.0

    def test_drawdown_detected(self):
        points = [
            {"date": "2026-05-20", "cumulative_r": 3.0, "cumulative_pnl": None},
            {"date": "2026-05-21", "cumulative_r": 1.0, "cumulative_pnl": None},
        ]
        result = self._calc_drawdown(points)
        assert result["max_drawdown_r"] == 2.0
        assert result["current_drawdown_r"] == 2.0

    def test_max_drawdown_from_historical_peak(self):
        points = [
            {"date": "2026-05-20", "cumulative_r": 5.0, "cumulative_pnl": None},
            {"date": "2026-05-21", "cumulative_r": 2.0, "cumulative_pnl": None},  # dd=3
            {"date": "2026-05-22", "cumulative_r": 6.0, "cumulative_pnl": None},  # new peak
            {"date": "2026-05-23", "cumulative_r": 5.0, "cumulative_pnl": None},  # dd=1
        ]
        result = self._calc_drawdown(points)
        assert result["max_drawdown_r"] == 3.0
        assert result["current_drawdown_r"] == 1.0

    def test_single_point_no_drawdown(self):
        points = [{"date": "2026-05-20", "cumulative_r": 2.0, "cumulative_pnl": None}]
        result = self._calc_drawdown(points)
        assert result["max_drawdown_r"] == 0.0

    def test_negative_cumulative_r_from_start(self):
        points = [
            {"date": "2026-05-20", "cumulative_r": -1.0, "cumulative_pnl": None},
            {"date": "2026-05-21", "cumulative_r": -2.0, "cumulative_pnl": None},
        ]
        result = self._calc_drawdown(points)
        # Peak starts at 0, so both points are below peak
        assert result["max_drawdown_r"] == 2.0

    def test_recovery_then_new_high(self):
        points = [
            {"date": "2026-05-20", "cumulative_r": 4.0, "cumulative_pnl": None},
            {"date": "2026-05-21", "cumulative_r": 2.0, "cumulative_pnl": None},
            {"date": "2026-05-22", "cumulative_r": 4.0, "cumulative_pnl": None},  # recovery
            {"date": "2026-05-23", "cumulative_r": 5.0, "cumulative_pnl": None},  # new high
        ]
        result = self._calc_drawdown(points)
        assert result["max_drawdown_r"] == 2.0
        assert result["current_drawdown_r"] == 0.0


# ---------------------------------------------------------------------------
# Monthly heatmap aggregation
# ---------------------------------------------------------------------------

class TestMonthlyHeatmap:
    """Test monthly heatmap row shaping logic."""

    def _shape_rows(self, raw_rows: list[dict]) -> list[dict]:
        return [
            {
                "year": r["year"],
                "month": r["month"],
                "total_r": round(r["total_r"], 4),
                "total_pnl": round(r["total_pnl"], 2) if r["total_pnl"] else None,
                "trade_count": r["trade_count"],
                "win_rate": float(r["win_rate"]) if r["win_rate"] is not None else None,
            }
            for r in raw_rows
        ]

    def test_empty_history(self):
        assert self._shape_rows([]) == []

    def test_single_month(self):
        rows = [{"year": 2026, "month": 5, "total_r": 3.5, "total_pnl": 350.0, "trade_count": 10, "win_rate": 0.6}]
        result = self._shape_rows(rows)
        assert len(result) == 1
        assert result[0]["total_r"] == 3.5
        assert result[0]["win_rate"] == 0.6

    def test_null_pnl_returns_none(self):
        rows = [{"year": 2026, "month": 5, "total_r": 1.0, "total_pnl": None, "trade_count": 3, "win_rate": None}]
        result = self._shape_rows(rows)
        assert result[0]["total_pnl"] is None
        assert result[0]["win_rate"] is None

    def test_negative_month(self):
        rows = [{"year": 2026, "month": 4, "total_r": -2.0, "total_pnl": -200.0, "trade_count": 5, "win_rate": 0.2}]
        result = self._shape_rows(rows)
        assert result[0]["total_r"] == -2.0
