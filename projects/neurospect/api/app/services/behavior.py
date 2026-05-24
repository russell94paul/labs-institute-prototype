"""
Behavior metrics engine. Calculates tilt, revenge trading, overtrading,
discipline, and consistency scores from closed trade history.
"""
import uuid
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Tuning constants
REVENGE_WINDOW_MINUTES = 30
OVERTRADING_DAILY_LIMIT = 5
TILT_LOOKBACK_TRADES = 20
POSITION_ESCALATION_THRESHOLD = Decimal("1.25")


async def _fetch_closed_trades(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date | None = None,
    date_end: date | None = None,
) -> list[dict]:
    """Fetch closed trades ordered chronologically for behavior analysis."""
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
            id, trade_date, instrument, outcome, r_multiple, pnl_usd,
            entry_time, exit_time, position_size, htf_bias,
            plan_followed, mistake_tags, quality_grade, session
        FROM trades
        WHERE {where}
        ORDER BY trade_date ASC, COALESCE(entry_time, created_at) ASC
    """)
    rows = (await db.execute(sql, params)).mappings().all()
    return [dict(r) for r in rows]


def _calc_tilt_score(trades: list[dict]) -> dict:
    """
    Tilt score (0–100). Signals: consecutive losses, rapid re-entry after loss,
    position size escalation after losses. Uses the most recent TILT_LOOKBACK_TRADES.
    """
    if not trades:
        return {"score": 0, "consecutive_losses": 0,
                "rapid_reentries": 0, "position_escalations": 0}

    recent = trades[-TILT_LOOKBACK_TRADES:]
    consecutive_losses = 0
    for t in reversed(recent):
        if t["outcome"] == "loss":
            consecutive_losses += 1
        else:
            break

    rapid_reentries = 0
    position_escalations = 0

    for i in range(1, len(recent)):
        prev, curr = recent[i - 1], recent[i]

        if prev["outcome"] == "loss" and prev["exit_time"] and curr["entry_time"]:
            gap = curr["entry_time"] - prev["exit_time"]
            if gap.total_seconds() <= REVENGE_WINDOW_MINUTES * 60:
                rapid_reentries += 1

        if (prev["outcome"] == "loss"
                and prev["position_size"] and curr["position_size"]
                and curr["position_size"] > prev["position_size"] * float(POSITION_ESCALATION_THRESHOLD)):
            position_escalations += 1

    n = len(recent)
    loss_streak_component = min(consecutive_losses * 15, 45)
    reentry_component = min(rapid_reentries / max(n - 1, 1) * 100, 30)
    escalation_component = min(position_escalations / max(n - 1, 1) * 100, 25)

    score = int(min(loss_streak_component + reentry_component + escalation_component, 100))

    return {
        "score": score,
        "consecutive_losses": consecutive_losses,
        "rapid_reentries": rapid_reentries,
        "position_escalations": position_escalations,
    }


def _detect_revenge_trades(trades: list[dict]) -> list[dict]:
    """
    Flag trades that look like revenge entries: entered within REVENGE_WINDOW_MINUTES
    of a loss, on the same instrument.
    """
    flagged = []
    for i in range(1, len(trades)):
        prev, curr = trades[i - 1], trades[i]
        if prev["outcome"] != "loss":
            continue
        if prev["instrument"] != curr["instrument"]:
            continue
        if not prev["exit_time"] or not curr["entry_time"]:
            continue
        gap = curr["entry_time"] - prev["exit_time"]
        if gap.total_seconds() <= REVENGE_WINDOW_MINUTES * 60:
            against_bias = (
                prev.get("htf_bias") is not None
                and curr.get("htf_bias") is not None
                and prev["htf_bias"] != curr["htf_bias"]
            )
            flagged.append({
                "trade_id": str(curr["id"]),
                "instrument": curr["instrument"],
                "minutes_after_loss": round(gap.total_seconds() / 60, 1),
                "against_bias": against_bias,
            })
    return flagged


def _calc_overtrading(trades: list[dict]) -> dict:
    """Count days where trade count exceeds the daily limit."""
    daily_counts: dict[date, int] = {}
    for t in trades:
        d = t["trade_date"]
        daily_counts[d] = daily_counts.get(d, 0) + 1

    overtrading_days = [
        {"date": d.isoformat(), "count": c}
        for d, c in sorted(daily_counts.items())
        if c > OVERTRADING_DAILY_LIMIT
    ]
    return {
        "daily_limit": OVERTRADING_DAILY_LIMIT,
        "overtrading_days": len(overtrading_days),
        "total_excess_trades": sum(d["count"] - OVERTRADING_DAILY_LIMIT for d in overtrading_days),
        "worst_days": overtrading_days[:5],
    }


def _calc_rule_breaches(trades: list[dict]) -> dict:
    """Count trades where plan wasn't followed or mistake tags are present."""
    if not trades:
        return {"total": 0, "plan_not_followed": 0, "with_mistakes": 0, "rate": 0.0}

    plan_not_followed = sum(1 for t in trades if t["plan_followed"] is False)
    with_mistakes = sum(1 for t in trades if t["mistake_tags"])
    total = plan_not_followed + with_mistakes
    # Deduplicate: trades that have both
    unique_breach_trades = sum(
        1 for t in trades
        if t["plan_followed"] is False or (t["mistake_tags"] and len(t["mistake_tags"]) > 0)
    )

    return {
        "total": unique_breach_trades,
        "plan_not_followed": plan_not_followed,
        "with_mistakes": with_mistakes,
        "rate": round(unique_breach_trades / len(trades), 4) if trades else 0.0,
    }


def _calc_consistency(trades: list[dict]) -> dict:
    """
    Consistency score (0–100). Low variance in daily returns = high consistency.
    Also tracks streak patterns.
    """
    if len(trades) < 2:
        return {"score": 0, "daily_return_stddev": None, "trading_days": len(trades)}

    daily_r: dict[date, list[float]] = {}
    for t in trades:
        if t["r_multiple"] is not None:
            d = t["trade_date"]
            daily_r.setdefault(d, []).append(float(t["r_multiple"]))

    if len(daily_r) < 2:
        return {"score": 0, "daily_return_stddev": None, "trading_days": len(daily_r)}

    daily_totals = [sum(rs) for rs in daily_r.values()]
    mean = sum(daily_totals) / len(daily_totals)
    variance = sum((x - mean) ** 2 for x in daily_totals) / len(daily_totals)
    stddev = variance ** 0.5

    # Score: lower stddev = higher consistency. Calibrated so stddev=0 → 100, stddev≥5R → 0
    score = int(max(0, min(100, 100 - stddev * 20)))

    return {
        "score": score,
        "daily_return_stddev": round(stddev, 4),
        "trading_days": len(daily_r),
    }


def _calc_discipline(
    tilt: dict, rule_breaches: dict, consistency: dict, trades: list[dict]
) -> dict:
    """
    Discipline score (0–100). Composite of rule adherence, tilt control, consistency.
    Weights: rule adherence 40%, tilt control 35%, consistency 25%.
    """
    if not trades:
        return {"score": 0, "rule_adherence": 0.0, "tilt_control": 0, "consistency": 0}

    rule_adherence = 1.0 - rule_breaches["rate"]
    tilt_control = max(0, 100 - tilt["score"])
    consistency_score = consistency["score"]

    score = int(
        rule_adherence * 100 * 0.40
        + tilt_control * 0.35
        + consistency_score * 0.25
    )
    score = max(0, min(100, score))

    return {
        "score": score,
        "rule_adherence": round(rule_adherence, 4),
        "tilt_control": tilt_control,
        "consistency": consistency_score,
    }


async def get_behavior_metrics(
    db: AsyncSession,
    user_id: uuid.UUID,
    date_start: date | None = None,
    date_end: date | None = None,
) -> dict:
    trades = await _fetch_closed_trades(db, user_id, date_start, date_end)

    tilt = _calc_tilt_score(trades)
    revenge_trades = _detect_revenge_trades(trades)
    overtrading = _calc_overtrading(trades)
    rule_breaches = _calc_rule_breaches(trades)
    consistency = _calc_consistency(trades)
    discipline = _calc_discipline(tilt, rule_breaches, consistency, trades)

    return {
        "trade_count": len(trades),
        "date_start": date_start.isoformat() if date_start else None,
        "date_end": date_end.isoformat() if date_end else None,
        "tilt": tilt,
        "revenge_trades": revenge_trades,
        "overtrading": overtrading,
        "rule_breaches": rule_breaches,
        "consistency": consistency,
        "discipline": discipline,
    }
