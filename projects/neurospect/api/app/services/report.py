"""
Weekly/monthly report service. Computes aggregated stats from existing analytics
and behavior services and persists them as snapshots in user_reports.
"""
import uuid
from datetime import date, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import UserReport
from app.services.analytics import get_equity_curve, get_monthly_heatmap
from app.services.behavior import get_behavior_metrics


def _week_bounds(year: int, week: int) -> tuple[date, date]:
    """ISO week → (monday, sunday)."""
    jan4 = date(year, 1, 4)
    week_start = jan4 + timedelta(weeks=week - 1) - timedelta(days=jan4.weekday())
    return week_start, week_start + timedelta(days=6)


def _month_bounds(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


async def _compute_stats(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date,
    date_end: date,
) -> dict:
    """Run analytics + behavior queries for the given date range."""
    closed_sql = text("""
        SELECT
            COUNT(*) AS closed,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            ) AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4) AS avg_r,
            COALESCE(SUM(r_multiple::float), 0) AS total_r,
            SUM(pnl_usd::float) AS total_pnl
        FROM trades
        WHERE user_id = :uid
          AND NOT is_deleted
          AND status = 'closed'
          AND outcome IS NOT NULL
          AND trade_date BETWEEN :ds AND :de
    """)
    row = (await db.execute(closed_sql, {"uid": str(user_id),
                                         "ds": date_start.isoformat(),
                                         "de": date_end.isoformat()})).mappings().one()

    behavior = await get_behavior_metrics(db, user_id, date_start, date_end)

    return {
        "trade_count": (row["closed"] or 0),
        "closed_trades": (row["closed"] or 0),
        "win_rate": float(row["win_rate"]) if row["win_rate"] is not None else None,
        "avg_r_multiple": float(row["avg_r"]) if row["avg_r"] is not None else None,
        "total_r": round(float(row["total_r"] or 0), 4),
        "total_pnl": round(float(row["total_pnl"]), 2) if row["total_pnl"] is not None else None,
        "tilt_score": behavior["tilt"]["score"],
        "discipline_score": behavior["discipline"]["score"],
        "consistency_score": behavior["consistency"]["score"],
        "revenge_trade_count": len(behavior["revenge_trades"]),
        "overtrading_days": behavior["overtrading"]["overtrading_days"],
        "rule_breach_rate": behavior["rule_breaches"]["rate"],
    }


async def upsert_weekly_report(
    db: AsyncSession, user_id: uuid.UUID, year: int, week: int
) -> UserReport:
    date_start, date_end = _week_bounds(year, week)
    stats = await _compute_stats(db, user_id, date_start, date_end)

    result = await db.execute(
        select(UserReport).where(
            UserReport.user_id == user_id,
            UserReport.period_type == "weekly",
            UserReport.year == year,
            UserReport.period_number == week,
        )
    )
    report = result.scalar_one_or_none()
    if report:
        report.stats = stats
    else:
        report = UserReport(
            user_id=user_id,
            period_type="weekly",
            year=year,
            period_number=week,
            stats=stats,
        )
        db.add(report)
    await db.flush()
    return report


async def upsert_monthly_report(
    db: AsyncSession, user_id: uuid.UUID, year: int, month: int
) -> UserReport:
    date_start, date_end = _month_bounds(year, month)
    stats = await _compute_stats(db, user_id, date_start, date_end)

    result = await db.execute(
        select(UserReport).where(
            UserReport.user_id == user_id,
            UserReport.period_type == "monthly",
            UserReport.year == year,
            UserReport.period_number == month,
        )
    )
    report = result.scalar_one_or_none()
    if report:
        report.stats = stats
    else:
        report = UserReport(
            user_id=user_id,
            period_type="monthly",
            year=year,
            period_number=month,
            stats=stats,
        )
        db.add(report)
    await db.flush()
    return report


async def list_reports(
    db: AsyncSession,
    user_id: uuid.UUID,
    period_type: str | None = None,
    limit: int = 24,
) -> list[UserReport]:
    q = select(UserReport).where(UserReport.user_id == user_id)
    if period_type:
        q = q.where(UserReport.period_type == period_type)
    q = q.order_by(UserReport.year.desc(), UserReport.period_number.desc()).limit(limit)
    result = await db.execute(q)
    return list(result.scalars().all())
