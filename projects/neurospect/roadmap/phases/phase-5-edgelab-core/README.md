---
phase: 5
name: "EdgeLab Core"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Event-driven backtesting engine with anti-lookahead, strategy compilation, Monte Carlo, walk-forward optimization, feature store, dashboard, and null test."
deliverables:
  - "5A: Backtest engine core (bar-by-bar replay, simulator, anti-lookahead)"
  - "5A: Market data pipeline (FirstRate CSV → Parquet on R2)"
  - "5A: Experiment registry MVP"
  - "5A: Strategy compiler (first strategy: Consolidation Model)"
  - "5B: All 7 ICT strategies compiled from YAML"
  - "5B: Monte Carlo simulation (10K iterations < 30s)"
  - "5B: Walk-forward optimization with deflated Sharpe"
  - "5B: Feature store (quant + ICT features, point-in-time snapshots)"
  - "5B: EdgeLab REST API"
  - "5C: Experiment dashboard, backtest detail, Monte Carlo viewer"
  - "5C: Null test (ICT vs random entries with same risk management)"
constraints:
  - "Anti-lookahead architecturally enforced — impossible to access future data"
  - "Every strategy must compile from wiki YAML — no hardcoded logic"
  - "Monte Carlo must be fast (vectorized Polars/NumPy)"
  - "Feature snapshots are point-in-time — no leakage"
  - "Null test is a hard gate for Phase 11 viability"
acceptance_criteria:
  - "Engine replays bars through strategies and produces trade records"
  - "Anti-lookahead proven by tests"
  - "All 7 strategies compile and produce backtest results"
  - "Monte Carlo runs 10K iterations in < 30s"
  - "Walk-forward produces efficiency ratio and deflated Sharpe"
  - "Feature store registers features with point-in-time snapshots"
  - "Null test run and results documented"
  - "Statistical significance test (p < 0.05)"
compliance_gate: "Backtesting disclaimers (past performance is not indicative...)"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 5: EdgeLab Core (5A/5B/5C)

Event-driven backtesting, quant feature engineering, strategy compilation, statistical validation. Three sub-phases. Research tier $199/mo.

See `/ns-phase5a`, `/ns-phase5b`, `/ns-phase5c` for full implementation guides.

## Deviations

_None yet._
