---
phase: 8
name: "NeuroScore + Leaderboard"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Build verified, risk-adjusted trader ranking. Performance (40%) + drawdown discipline (20%) + rule adherence (15%) + consistency (15%) + tilt control (10%). Prerequisite for NeuroFund Elite."
deliverables:
  - "NeuroScore calculation engine (5 weighted components, 0-100 range)"
  - "Verification requirements (broker-verified trades only)"
  - "Account type labeling (sim/eval/funded/live)"
  - "NeuroScore history model (weekly snapshots)"
  - "Leaderboard API (top traders, rank, history)"
  - "Leaderboard UI (sortable table, score breakdown, percentile ranking)"
  - "Peer comparison within account-type cohort"
  - "Tests for scoring edge cases"
constraints:
  - "Do NOT rank by profit alone — holistic assessment"
  - "No screenshot-based verification"
  - "Account types clearly labeled"
  - "No implication that high score equals future profitability"
  - "Leaderboard visible on free tier; details require Quant tier"
  - "Minimum 50 verified trades to appear"
  - "Do NOT implement rewards yet (Phase 9)"
acceptance_criteria:
  - "NeuroScore calculated from 5 weighted components"
  - "Only broker-verified trades count"
  - "Minimum requirements enforced (50 trades, 30 days)"
  - "Account types labeled on leaderboard"
  - "Filterable by account type, instrument, time period"
  - "Score history tracked weekly"
  - "Percentile ranking within cohort"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 8: NeuroScore + Leaderboard

Risk-adjusted trader ranking. Broker-verified trades only. Quant tier $349/mo.

See `/ns-phase8` for full implementation guide.

## Deviations

_None yet._
