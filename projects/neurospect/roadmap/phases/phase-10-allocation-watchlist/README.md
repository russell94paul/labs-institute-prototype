---
phase: 10
name: "Allocation Watchlist"
status: in_progress
assigned: [paul]
started: 2026-05-15
completed: null
tickets_total: 0
tickets_done: 0
goal: "Internal workflow for identifying traders for challenge sponsorships, grants, or company-sponsored allocation consideration. Extends Phase 9 eligibility with deeper criteria."
deliverables:
  - "Allocation watchlist model (7-state status enum)"
  - "Qualification criteria (stricter than Phase 9: 100+ trades, NeuroScore >= 80, 60+ days, max DD < 8%)"
  - "Trader model card (risk profile, strategy summary, consistency evidence, NeuroScore history)"
  - "KYC/identity verification placeholder (status fields, no implementation)"
  - "Admin review workflow (watchlist view, comparison, notes, status transitions)"
  - "Allocation Watchlist API (admin-only list, model card, status transitions)"
  - "Trader-facing view (qualification progress, strategy submission)"
  - "Tests for qualification, status transitions, model card generation"
constraints:
  - "Same compliance rules as Phase 9 (APPROVED/FORBIDDEN language)"
  - "No promise of allocation"
  - "No managed account functionality"
  - "No letting users invest in traders"
  - "Admin discretion required — no automatic selection"
  - "KYC is placeholder only"
acceptance_criteria:
  - "Qualification criteria automatically evaluated"
  - "Trader model card generated with full profile"
  - "Watchlist status transitions with audit trail"
  - "Admin can compare traders side-by-side"
  - "Strategy submission form captures trader strategy"
  - "KYC status fields exist"
  - "All user-facing copy uses APPROVED language"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 10: Allocation Watchlist

Internal review workflow for challenge sponsorships and allocation consideration.

Code exists in session worktree branch (`session/phase-10-445fccd1`) but is not yet merged to main.

See `/ns-phase10` for full implementation guide.

## Deviations

_None yet._
