---
phase: 9
name: "NeuroFund Elite Rewards"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Create NeuroFund Elite rewards MVP as premium opt-in eligibility and rewards program. Company-sponsored, funded from revenue. NOT a fund, NOT pooled capital."
deliverables:
  - "Elite eligibility flag and status on user model"
  - "Activation threshold (50 verified eligible members)"
  - "Eligibility criteria (Quant tier, NeuroScore >= 75, 90+ trades, 60+ days, no lockout breaches, funded/live)"
  - "Reward eligibility state machine (6 states)"
  - "Monthly leaderboard seasons"
  - "Challenge sponsorship eligibility"
  - "Admin review workflow with audit trail"
  - "Elite dashboard (eligibility progress, criteria checklist)"
  - "Public marketing copy with APPROVED language only"
  - "Tests for eligibility, state transitions, activation threshold"
constraints:
  - "No pooled user capital"
  - "No return promises — use 'may be eligible for'"
  - "No managed account functionality"
  - "No automatic payout — admin review required"
  - "COMPLIANCE_TODO tags wherever reward language appears"
  - "Legal counsel review before marketing copy goes live"
  - "Feature flag entire system for gradual rollout"
acceptance_criteria:
  - "Users flagged as Elite eligible based on criteria"
  - "Activation threshold enforced"
  - "State machine transitions correctly through 6 states"
  - "Admin can review and transition trader status"
  - "Audit trail for every state transition"
  - "All user-facing copy uses APPROVED language only"
  - "No FORBIDDEN language anywhere in codebase"
  - "Monthly seasons snapshot correctly"
compliance_gate: "Full compliance review. Approved/forbidden language audit. Legal counsel review"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 9: NeuroFund Elite Rewards — COMPLIANCE-CRITICAL

Company-sponsored rewards program. NOT pooled capital, NOT an investment vehicle.

See `/ns-phase9` for full implementation guide.

## Deviations

_None yet._
