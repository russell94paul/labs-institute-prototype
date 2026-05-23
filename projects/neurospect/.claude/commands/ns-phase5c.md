---
name: ns-phase5c
description: NeuroSpect Phase 5C — EdgeLab Core (Dashboard + Null Test)
---

You are working on **NeuroSpect Phase 5C** (EdgeLab Core — Dashboard + Null Test). This is part 3 of 3 for EdgeLab.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\app\CLAUDE.md`
3. Read Phase 5A/5B EdgeLab API — `api/app/routers/edgelab.py` (all endpoints)
4. Read Phase 5A engine — `api/app/edgelab/engine/` (data flow for dashboard)
5. Read Phase 5B risk modules — `api/app/edgelab/risk/` (Monte Carlo, walk-forward)
6. Read `C:\Users\PaulRussell\repos\neurospect\roadmap\plan.md` lines 1454-1481 — EdgeLab UI/product implications

## Goal

Build the EdgeLab frontend dashboard (experiment list, backtest detail, charts, feature browser) and run the null test: ICT strategies vs random entries with the same risk management. The null test is a hard gate — if ICT strategies don't show statistically significant edge (p < 0.05), Phase 11's NeuroTrader Agent is NOT viable.

## Deliverables

### Dashboard Pages

1. **Experiment Dashboard** (`app/src/pages/edgelab/experiments.tsx`):
   - List of experiments with status, type, parameters, summary metrics
   - Filter by type (backtest/feature_eval)
   - "New Experiment" button → experiment creation form
2. **Backtest Run Detail** (`app/src/pages/edgelab/backtest-detail.tsx`):
   - Equity curve chart (cumulative P&L over time)
   - Drawdown chart (drawdown % over time)
   - R-distribution histogram
   - Monthly returns heatmap
   - Trade log table (sortable, filterable)
   - MAE/MFE scatter plot (maximum adverse/favorable excursion)
   - Summary metrics cards (win rate, avg R, Sharpe, expectancy, profit factor, max DD)
3. **Monte Carlo Viewer** (component within backtest detail):
   - Fan chart with P5/P25/P50/P75/P95 confidence bands
   - Ruin probability display
   - Distribution histogram of terminal equity
4. **Walk-Forward Results** (component within backtest detail):
   - Efficiency bars (in-sample vs out-of-sample per window)
   - Deflated Sharpe ratio
   - Overfitting indicator (green/yellow/red based on efficiency ratio)
5. **Feature Library** (`app/src/pages/edgelab/features.tsx`):
   - Browse registered features by category (quant/ICT)
   - Feature importance rankings from latest runs
   - Feature distribution charts

### Null Test

6. **Null test execution**:
   - Run all 7 ICT strategies against 2+ years of NQ data
   - Run random entry strategies with identical risk management (same stop size, target, position size)
   - Compare ICT vs random on: expectancy, Sharpe, win rate, profit factor
   - Statistical significance test (p < 0.05 via permutation test or bootstrap)
7. **Null test dashboard** (`app/src/pages/edgelab/null-test.tsx`):
   - ICT vs baseline comparison table
   - Statistical significance visualization
   - Go/no-go gate indicator

### Charting

8. Use **Recharts** for analytics charts (React-native, works with shadcn)
9. Use **TradingView Lightweight Charts** if candlestick display needed in replay review

## Key Constraints

- Charts must handle 1000+ data points smoothly (use data decimation for equity curves)
- Null test results must be documented in `research/phase-5-edgelab/null-test-results.md`
- If null test fails (p > 0.05 for all strategies), document this clearly — it changes the entire downstream roadmap
- Tier access: Trader tier sees backtest detail (read-only). Research tier sees full EdgeLab dashboard.
- Do not implement NSLM evaluation or model training (Phase 11)

## Acceptance Criteria

- [ ] Experiment dashboard lists experiments with correct status and metrics
- [ ] Backtest detail page shows equity curve, drawdown, R-distribution, trade log, MAE/MFE
- [ ] Monte Carlo fan chart renders with confidence bands
- [ ] Walk-forward efficiency bars display correctly
- [ ] Feature library shows registered features with importance rankings
- [ ] Null test has been run for all 7 strategies vs random baseline
- [ ] Statistical significance documented (p-value for each strategy)
- [ ] Null test results written to `research/phase-5-edgelab/null-test-results.md`
- [ ] Go/no-go gate clearly communicated for Phase 11 viability

## When done

If null test passes (any strategy p < 0.05):
Say: "Phase 5C complete — EdgeLab dashboard is live and null test shows statistical edge for [strategies]. Run `/ns-phase6` in a new session for AI Trade Review + RAG."

If null test fails:
Say: "Phase 5C complete — EdgeLab dashboard is live but null test shows NO statistical edge (p > 0.05). Phase 11 (NeuroTrader Agent) is NOT viable. The platform pivots to coaching and analytics only. Run `/ns-phase6` to proceed with AI Trade Review."
