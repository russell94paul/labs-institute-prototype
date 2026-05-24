---
phase: 2
name: "Trader Workspace"
status: in_progress
assigned: [paul]
started: 2026-05-10
completed: null
tickets_total: 0
tickets_done: 0
goal: "Build daily-use trader workspace: full journal, analytics dashboard, behavior metrics (tilt, discipline, consistency)."
deliverables:
  - "Behavior metrics engine (tilt, revenge trading, overtrading, discipline, consistency)"
  - "Enhanced analytics (equity curve, drawdown, monthly heatmap)"
  - "Journal enhancements (emotion tags, pre-trade checklist, post-trade review)"
  - "Dashboard homepage (daily summary, behavior alerts)"
  - "Weekly/monthly report data model"
  - "Frontend charts and journal form improvements"
  - "Tests for behavior metrics and analytics"
constraints:
  - "Extend existing analytics service — do NOT replace"
  - "Behavior metrics calculable from existing trade data"
  - "Keep analytics educational — no financial advice"
  - "Do not implement NeuroScore yet (Phase 8)"
  - "Do not implement AI trade review yet (Phase 6)"
acceptance_criteria:
  - "Behavior metrics endpoint returns tilt, revenge, overtrading, discipline, consistency scores"
  - "Equity curve and drawdown endpoints return time-series data"
  - "Trades can have emotion tags and journal notes"
  - "Dashboard shows daily summary with behavior alerts"
  - "Analytics filterable by date range, instrument, session, setup, account type"
  - "Tests cover edge cases (empty history, single trade, long streaks)"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 2: Trader Workspace

Journal, analytics, behavior metrics. The "free tier" engagement layer that hooks users before paid features.

Partially implemented: analytics backend + dashboard/trades pages exist. Full journal and behavior metrics dashboard not yet built.

See `/ns-phase2` for full implementation guide.

## Deviations

_None yet._
