"""
Raw SQL analytics queries.
All closed-trade queries filter: user_id = :user_id AND NOT is_deleted AND outcome IS NOT NULL.
"""
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

_DOW_NAMES = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
              4: "Thursday", 5: "Friday", 6: "Saturday"}

# R-distribution constants
_R_MIN = -10.0
_R_MAX = 10.0
_R_BINS = 40
_BIN_WIDTH = (_R_MAX - _R_MIN) / _R_BINS


async def get_summary(db: AsyncSession, user_id: uuid.UUID) -> dict:
    sql = text("""
        WITH closed AS (
            SELECT
                outcome,
                r_multiple,
                setup_type,
                trade_date,
                created_at,
                ROW_NUMBER() OVER (ORDER BY trade_date ASC, created_at ASC) AS rn
            FROM trades
            WHERE user_id       = :user_id
              AND NOT is_deleted
              AND status        = 'closed'
              AND outcome IS NOT NULL
        ),
        grouped AS (
            SELECT
                outcome,
                rn,
                rn - ROW_NUMBER() OVER (PARTITION BY outcome ORDER BY rn) AS grp
            FROM closed
        ),
        streak_lens AS (
            SELECT outcome, grp, COUNT(*) AS len
            FROM grouped
            GROUP BY outcome, grp
        ),
        current_grp AS (
            -- Group that contains the most recent trade
            SELECT g.outcome, g.grp
            FROM grouped g
            WHERE g.rn = (SELECT MAX(rn) FROM closed)
        ),
        setup_win_rates AS (
            SELECT
                setup_type::text                                          AS st,
                COUNT(*)                                                  AS total,
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)         AS wins
            FROM closed
            WHERE setup_type IS NOT NULL
            GROUP BY setup_type
            HAVING COUNT(*) >= 3
        )
        SELECT
            (
                SELECT COUNT(*)
                FROM trades
                WHERE user_id = :user_id AND NOT is_deleted
            )                                                             AS total_trades,
            COUNT(*)                                                      AS closed_trades,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                                             AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4)                           AS avg_r_multiple,
            (
                SELECT st FROM setup_win_rates
                ORDER BY wins::float / total DESC
                LIMIT 1
            )                                                             AS best_setup_type,
            COALESCE((
                SELECT sl.len
                FROM streak_lens sl
                JOIN current_grp cg ON sl.outcome = cg.outcome AND sl.grp = cg.grp
                WHERE sl.outcome = 'win'
            ), 0)                                                         AS current_win_streak,
            COALESCE((
                SELECT sl.len
                FROM streak_lens sl
                JOIN current_grp cg ON sl.outcome = cg.outcome AND sl.grp = cg.grp
                WHERE sl.outcome = 'loss'
            ), 0)                                                         AS current_loss_streak,
            COALESCE(
                (SELECT MAX(len) FROM streak_lens WHERE outcome = 'win'), 0
            )                                                             AS longest_win_streak,
            COALESCE(
                (SELECT MAX(len) FROM streak_lens WHERE outcome = 'loss'), 0
            )                                                             AS longest_loss_streak
        FROM closed
    """)
    row = (await db.execute(sql, {"user_id": str(user_id)})).mappings().one()
    return dict(row)


async def get_by_setup(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            setup_type::text                                              AS "group",
            COUNT(*)                                                      AS total,
            SUM(CASE WHEN outcome = 'win'       THEN 1 ELSE 0 END)       AS wins,
            SUM(CASE WHEN outcome = 'loss'      THEN 1 ELSE 0 END)       AS losses,
            SUM(CASE WHEN outcome = 'breakeven' THEN 1 ELSE 0 END)       AS breakevens,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                                             AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4)                           AS avg_r_multiple
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
          AND setup_type IS NOT NULL
        GROUP BY setup_type
        ORDER BY win_rate DESC NULLS LAST
    """)
    rows = (await db.execute(sql, {"user_id": str(user_id)})).mappings().all()
    return [dict(r) for r in rows]


async def get_by_session(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            session::text                                                 AS "group",
            COUNT(*)                                                      AS total,
            SUM(CASE WHEN outcome = 'win'       THEN 1 ELSE 0 END)       AS wins,
            SUM(CASE WHEN outcome = 'loss'      THEN 1 ELSE 0 END)       AS losses,
            SUM(CASE WHEN outcome = 'breakeven' THEN 1 ELSE 0 END)       AS breakevens,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                                             AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4)                           AS avg_r_multiple
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
          AND session IS NOT NULL
        GROUP BY session
        ORDER BY win_rate DESC NULLS LAST
    """)
    rows = (await db.execute(sql, {"user_id": str(user_id)})).mappings().all()
    return [dict(r) for r in rows]


async def get_by_instrument(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            instrument                                                    AS "group",
            COUNT(*)                                                      AS total,
            SUM(CASE WHEN outcome = 'win'       THEN 1 ELSE 0 END)       AS wins,
            SUM(CASE WHEN outcome = 'loss'      THEN 1 ELSE 0 END)       AS losses,
            SUM(CASE WHEN outcome = 'breakeven' THEN 1 ELSE 0 END)       AS breakevens,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                                             AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4)                           AS avg_r_multiple
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
        GROUP BY instrument
        ORDER BY win_rate DESC NULLS LAST
    """)
    rows = (await db.execute(sql, {"user_id": str(user_id)})).mappings().all()
    return [dict(r) for r in rows]


async def get_by_day_of_week(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            EXTRACT(DOW FROM trade_date)::int                             AS day_of_week,
            COUNT(*)                                                      AS total,
            SUM(CASE WHEN outcome = 'win'       THEN 1 ELSE 0 END)       AS wins,
            SUM(CASE WHEN outcome = 'loss'      THEN 1 ELSE 0 END)       AS losses,
            SUM(CASE WHEN outcome = 'breakeven' THEN 1 ELSE 0 END)       AS breakevens,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                                             AS win_rate,
            ROUND(AVG(r_multiple)::numeric, 4)                           AS avg_r_multiple
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
        GROUP BY day_of_week
        ORDER BY day_of_week ASC
    """)
    rows = (await db.execute(sql, {"user_id": str(user_id)})).mappings().all()
    return [
        {**dict(r), "day_name": _DOW_NAMES.get(r["day_of_week"], "Unknown")}
        for r in rows
    ]


async def get_mistakes(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            unnest(mistake_tags)  AS tag,
            COUNT(*)              AS count
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
          AND mistake_tags IS NOT NULL
        GROUP BY tag
        ORDER BY count DESC
    """)
    rows = (await db.execute(sql, {"user_id": str(user_id)})).mappings().all()
    return [dict(r) for r in rows]


async def get_r_distribution(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    sql = text("""
        SELECT
            WIDTH_BUCKET(r_multiple, :r_min, :r_max, :bins)  AS bucket,
            COUNT(*)                                          AS count
        FROM trades
        WHERE user_id       = :user_id
          AND NOT is_deleted
          AND outcome IS NOT NULL
          AND r_multiple IS NOT NULL
          AND r_multiple BETWEEN :r_min AND :r_max
        GROUP BY bucket
        ORDER BY bucket ASC
    """)
    rows = (await db.execute(sql, {
        "user_id": str(user_id),
        "r_min": _R_MIN,
        "r_max": _R_MAX,
        "bins": _R_BINS,
    })).mappings().all()

    return [
        {
            "bucket": r["bucket"],
            "r_low":  Decimal(str(round(_R_MIN + (r["bucket"] - 1) * _BIN_WIDTH, 4))),
            "r_high": Decimal(str(round(_R_MIN + r["bucket"] * _BIN_WIDTH, 4))),
            "count":  r["count"],
        }
        for r in rows
    ]


async def get_equity_curve(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date | None = None,
    date_end: date | None = None,
) -> list[dict]:
    clauses = [
        "user_id = :user_id",
        "NOT is_deleted",
        "status = 'closed'",
        "outcome IS NOT NULL",
    ]
    params: dict = {"user_id": str(user_id)}
    if date_start:
        clauses.append("trade_date >= :date_start")
        params["date_start"] = date_start.isoformat()
    if date_end:
        clauses.append("trade_date <= :date_end")
        params["date_end"] = date_end.isoformat()

    where = " AND ".join(clauses)
    sql = text(f"""
        SELECT
            trade_date,
            SUM(COALESCE(r_multiple, 0))::float  AS daily_r,
            SUM(COALESCE(pnl_usd, 0))::float     AS daily_pnl,
            COUNT(*)                              AS trade_count
        FROM trades
        WHERE {where}
        GROUP BY trade_date
        ORDER BY trade_date ASC
    """)
    rows = (await db.execute(sql, params)).mappings().all()

    cum_r = 0.0
    cum_pnl = 0.0
    points = []
    for r in rows:
        cum_r += r["daily_r"]
        cum_pnl += r["daily_pnl"]
        points.append({
            "date": r["trade_date"].isoformat(),
            "cumulative_r": round(cum_r, 4),
            "cumulative_pnl": round(cum_pnl, 2) if cum_pnl else None,
            "trade_count": r["trade_count"],
        })
    return points


async def get_drawdown(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date | None = None,
    date_end: date | None = None,
) -> dict:
    points = await get_equity_curve(db, user_id, date_start, date_end)
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
        cum_pnl = p["cumulative_pnl"] or 0.0

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


async def get_monthly_heatmap(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date | None = None,
    date_end: date | None = None,
) -> list[dict]:
    clauses = [
        "user_id = :user_id",
        "NOT is_deleted",
        "status = 'closed'",
        "outcome IS NOT NULL",
    ]
    params: dict = {"user_id": str(user_id)}
    if date_start:
        clauses.append("trade_date >= :date_start")
        params["date_start"] = date_start.isoformat()
    if date_end:
        clauses.append("trade_date <= :date_end")
        params["date_end"] = date_end.isoformat()

    where = " AND ".join(clauses)
    sql = text(f"""
        SELECT
            EXTRACT(YEAR FROM trade_date)::int    AS year,
            EXTRACT(MONTH FROM trade_date)::int   AS month,
            SUM(COALESCE(r_multiple, 0))::float   AS total_r,
            SUM(COALESCE(pnl_usd, 0))::float     AS total_pnl,
            COUNT(*)                              AS trade_count,
            ROUND(
                SUM(CASE WHEN outcome = 'win' THEN 1 ELSE 0 END)::numeric
                / NULLIF(COUNT(*), 0), 4
            )                                     AS win_rate
        FROM trades
        WHERE {where}
        GROUP BY year, month
        ORDER BY year ASC, month ASC
    """)
    rows = (await db.execute(sql, params)).mappings().all()
    return [
        {
            "year": r["year"],
            "month": r["month"],
            "total_r": round(r["total_r"], 4),
            "total_pnl": round(r["total_pnl"], 2) if r["total_pnl"] else None,
            "trade_count": r["trade_count"],
            "win_rate": float(r["win_rate"]) if r["win_rate"] is not None else None,
        }
        for r in rows
    ]
