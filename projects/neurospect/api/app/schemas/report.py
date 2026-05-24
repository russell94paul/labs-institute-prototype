from pydantic import BaseModel


class ReportStats(BaseModel):
    trade_count: int
    closed_trades: int
    win_rate: float | None
    avg_r_multiple: float | None
    total_r: float
    total_pnl: float | None
    tilt_score: int
    discipline_score: int
    consistency_score: int
    revenge_trade_count: int
    overtrading_days: int
    rule_breach_rate: float


class UserReportResponse(BaseModel):
    id: str
    user_id: str
    period_type: str
    year: int
    period_number: int
    stats: ReportStats
    computed_at: str


class UserReportListResponse(BaseModel):
    items: list[UserReportResponse]
    total: int
