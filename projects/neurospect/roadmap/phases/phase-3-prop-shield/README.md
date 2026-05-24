---
phase: 3
name: "Prop Shield"
status: complete
assigned: [paul]
started: 2026-05-10
completed: 2026-05-13
tickets_total: 0
tickets_done: 0
goal: "Build the paid wedge that generates first revenue. Prop Shield monitors accounts against prop firm rules, tracks trailing drawdown, detects tilt, issues lockout warnings."
deliverables:
  - "PropRuleConfig model (daily loss, trailing DD, max contracts, max trades, forbidden hours, consistency)"
  - "Rule engine service (real-time distance-to-breach calculations)"
  - "Lockout state machine (warning → soft_lock → hard_lock → manual_reset)"
  - "Tilt lockout integration from behavior metrics"
  - "Risk dashboard UI (rule gauges, lockout history)"
  - "Multi-account support"
  - "Alert system (Discord webhook, email)"
  - "Prop firm presets (Apex, TopStep, FTMO, Earn2Trade, MyFundedFutures)"
  - "Stripe billing (Mentor $29/mo, Trader $99/mo)"
  - "Tests for rule engine, lockout state machine, distance-to-breach"
constraints:
  - "Lockouts are advisory only — cannot prevent order execution"
  - "Required disclaimer on risk dashboard"
  - "Read-only monitoring — do not execute or modify orders"
  - "Feature flags for lockout during rollout"
  - "Every state transition logged with timestamp and trigger"
acceptance_criteria:
  - "User can configure prop rules per account or select presets"
  - "Rule engine calculates distance-to-breach in real-time"
  - "Lockout state machine transitions correctly"
  - "Risk dashboard shows all rule statuses with visual meters"
  - "Tilt detection integrates with soft lockout"
  - "Prop firm presets load correct rules"
  - "Stripe accepts Mentor and Trader subscriptions"
  - "Tests cover daily loss, trailing DD, max position, tilt lockout"
  - "Advisory disclaimer displayed"
compliance_gate: "Advisory lockout disclaimer reviewed by counsel"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 3: Prop Shield — FIRST REVENUE

Prop firm rule tracking, trailing drawdown monitoring, tilt lockouts, advisory alerts, Stripe billing.

**Status: COMPLETE** (2026-05-10 → 2026-05-13). Deliverables: rule engine, lockout state machine, presets, billing, frontend.

See `/ns-phase3` for full implementation guide.

## Deviations

_None yet._
