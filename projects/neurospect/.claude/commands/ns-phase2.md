---
name: ns-phase2
description: NeuroSpect Phase 2 — Trader Workspace (Journal + Analytics + Behavior Metrics)
---

You are working on **NeuroSpect Phase 2** (Trader Workspace).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\services\analytics.py` — existing 7 analytics endpoints
4. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\routers\analytics.py` — analytics router
5. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\routers\trades.py` — trade CRUD
6. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\models\trade.py` — trade model (extended in Phase 1)
7. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\app\CLAUDE.md` — frontend context

## Goal

Make the journal and analytics production-quality for daily trader use. Add behavior metrics (tilt detection, discipline scoring, consistency tracking) that become inputs for NeuroScore in Phase 8. The Trader Workspace is the "free tier" engagement layer that hooks users before paid features (Prop Shield, EdgeLab).

## Deliverables

1. **Behavior metrics engine** — service that calculates from trade history:
   - Tilt score (consecutive losses, rapid re-entry patterns, increasing position size after losses)
   - Revenge trading detection (entry within N minutes of a loss, same instrument, against bias)
   - Overtrading count (trades exceeding daily/weekly plan)
   - Rule breach count (configurable per-user trading rules)
   - Discipline score (composite: rule adherence + tilt control + consistency)
   - Consistency score (variance of daily returns, streak analysis)
2. **Enhanced analytics endpoints**:
   - Equity curve data (`GET /api/analytics/equity-curve`)
   - Drawdown series (`GET /api/analytics/drawdown`)
   - Monthly PnL heatmap (`GET /api/analytics/monthly-heatmap`)
   - Best/worst session, instrument, setup breakdowns
3. **Journal enhancements**:
   - Emotion tags on trades (confident, fearful, greedy, patient, impulsive, revenge)
   - Pre-trade checklist model (configurable per-user)
   - Post-trade review structure (setup, execution, risk mgmt, psychology, lesson learned)
4. **Dashboard homepage** — daily summary: open P&L, today's trades, behavior alerts, recent coaching
5. **Weekly/monthly report data model** — aggregated stats for report generation
6. **Frontend**: equity curve chart, drawdown chart, behavior alerts, journal form improvements
7. **Tests** for behavior metrics calculations and analytics endpoints

## Metrics Calculated

| Category | Metrics |
|---|---|
| Performance | Net PnL, win rate, loss rate, avg win, avg loss, expectancy, profit factor, max drawdown, avg R/R, avg hold time |
| Session | Best/worst session, best/worst instrument, best/worst setup |
| Behavior | Tilt events, overtrading count, revenge trading flags, rule breach count |
| Composite | Consistency score, discipline score |

## Key Constraints

- Extend existing analytics service — do NOT replace it
- Behavior metrics must be calculable from existing trade data (no new data collection requirements)
- Keep analytics educational and performance-review focused — no financial advice
- Support both manual entries and imported trades
- Do not implement NeuroScore yet (Phase 8) — just build the data inputs it will consume
- Do not implement AI-powered trade review yet (Phase 6)

## Acceptance Criteria

- [ ] Behavior metrics endpoint returns tilt, revenge, overtrading, discipline, consistency scores
- [ ] Equity curve and drawdown endpoints return time-series data
- [ ] Trades can have emotion tags and journal notes
- [ ] Dashboard homepage shows daily summary with behavior alerts
- [ ] Analytics can be filtered by date range, instrument, session, setup, and account type
- [ ] Weekly/monthly report data model stores aggregated stats
- [ ] Tests cover behavior metric calculations for edge cases (empty history, single trade, long streaks)

## When done

Say: "Phase 2 complete — Trader Workspace is production-ready with behavior metrics. Run `/ns-phase3` in a new session for Prop Shield (the first paid feature)."
