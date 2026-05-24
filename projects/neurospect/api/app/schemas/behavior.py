from pydantic import BaseModel


class TiltMetrics(BaseModel):
    score: int
    consecutive_losses: int
    rapid_reentries: int
    position_escalations: int


class RevengeTrade(BaseModel):
    trade_id: str
    instrument: str
    minutes_after_loss: float
    against_bias: bool


class OvertradingDay(BaseModel):
    date: str
    count: int


class OvertradingMetrics(BaseModel):
    daily_limit: int
    overtrading_days: int
    total_excess_trades: int
    worst_days: list[OvertradingDay]


class RuleBreachMetrics(BaseModel):
    total: int
    plan_not_followed: int
    with_mistakes: int
    rate: float


class ConsistencyMetrics(BaseModel):
    score: int
    daily_return_stddev: float | None
    trading_days: int


class DisciplineMetrics(BaseModel):
    score: int
    rule_adherence: float
    tilt_control: int
    consistency: int


class BehaviorMetricsResponse(BaseModel):
    trade_count: int
    date_start: str | None
    date_end: str | None
    tilt: TiltMetrics
    revenge_trades: list[RevengeTrade]
    overtrading: OvertradingMetrics
    rule_breaches: RuleBreachMetrics
    consistency: ConsistencyMetrics
    discipline: DisciplineMetrics


class EquityCurvePoint(BaseModel):
    date: str
    cumulative_r: float
    cumulative_pnl: float | None
    trade_count: int


class EquityCurveResponse(BaseModel):
    points: list[EquityCurvePoint]


class DrawdownPoint(BaseModel):
    date: str
    drawdown_r: float
    drawdown_pnl: float | None
    peak_r: float


class DrawdownResponse(BaseModel):
    max_drawdown_r: float
    max_drawdown_pnl: float | None
    current_drawdown_r: float
    points: list[DrawdownPoint]


class MonthlyCell(BaseModel):
    year: int
    month: int
    total_r: float
    total_pnl: float | None
    trade_count: int
    win_rate: float | None


class MonthlyHeatmapResponse(BaseModel):
    cells: list[MonthlyCell]
