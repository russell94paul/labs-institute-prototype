from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.report import UserReportListResponse, UserReportResponse
from app.services import report as svc

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _serialize(r) -> UserReportResponse:
    return UserReportResponse(
        id=str(r.id),
        user_id=str(r.user_id),
        period_type=r.period_type,
        year=r.year,
        period_number=r.period_number,
        stats=r.stats,
        computed_at=r.computed_at.isoformat(),
    )


@router.get("/weekly", response_model=UserReportResponse)
async def get_weekly_report(
    year: int = Query(...),
    week: int = Query(..., ge=1, le=53),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return (and cache) the weekly report for the given ISO year/week."""
    report = await svc.upsert_weekly_report(db, current_user.id, year, week)
    await db.commit()
    return _serialize(report)


@router.get("/monthly", response_model=UserReportResponse)
async def get_monthly_report(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return (and cache) the monthly report for the given year/month."""
    report = await svc.upsert_monthly_report(db, current_user.id, year, month)
    await db.commit()
    return _serialize(report)


@router.get("/history", response_model=UserReportListResponse)
async def list_reports(
    period_type: str | None = Query(None, pattern="^(weekly|monthly)$"),
    limit: int = Query(24, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List stored reports, newest first."""
    reports = await svc.list_reports(db, current_user.id, period_type, limit)
    return UserReportListResponse(
        items=[_serialize(r) for r in reports],
        total=len(reports),
    )


@router.post("/this-week", response_model=UserReportResponse)
async def refresh_this_week(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Force-refresh the current week's report."""
    today = date.today()
    year, week, _ = today.isocalendar()
    report = await svc.upsert_weekly_report(db, current_user.id, year, week)
    await db.commit()
    return _serialize(report)


@router.post("/this-month", response_model=UserReportResponse)
async def refresh_this_month(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Force-refresh the current month's report."""
    today = date.today()
    report = await svc.upsert_monthly_report(db, current_user.id, today.year, today.month)
    await db.commit()
    return _serialize(report)
