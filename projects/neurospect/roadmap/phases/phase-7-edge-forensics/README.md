---
phase: 7
name: "Edge Forensics"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Turn repeated losses and mistake patterns into testable improvement hypotheses. Connects analytics, events, backtesting, and AI review into a loss-diagnosis pipeline."
deliverables:
  - "Loss cluster detection (chi-squared/binomial test)"
  - "Structured mistake taxonomy (10 categories with auto-detection)"
  - "Pattern mining (loss-correlated factors with effect size)"
  - "Hypothesis generator (structured, testable, AI-enriched)"
  - "Promote-to-backtest workflow (hypothesis → EdgeLab experiment)"
  - "Forensics API (clusters, hypotheses, promote, improvement tracking)"
  - "Forensics dashboard (clusters, hypothesis cards, improvement timeline)"
  - "Tests for clustering, taxonomy, hypothesis generation"
constraints:
  - "Hypotheses are testable, not proven — no guaranteed improvement claims"
  - "Minimum sample sizes enforced (N >= 10 per cluster)"
  - "Effect sizes must be meaningful"
  - "Do not auto-execute hypothesis-modified strategies"
  - "Premium feature: Research tier ($199/mo) and above"
acceptance_criteria:
  - "Loss cluster detection identifies statistically significant patterns"
  - "Mistake taxonomy auto-detects 5+ categories"
  - "Pattern mining produces ranked factors with effect sizes"
  - "Hypothesis generator creates structured hypotheses with evidence"
  - "Promote-to-backtest creates EdgeLab experiment"
  - "Forensics dashboard shows clusters, hypotheses, improvement timeline"
  - "Minimum sample size enforced"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 7: Edge Forensics

Loss pattern mining → testable hypothesis generation → EdgeLab backtest promotion. Where NeuroSpect becomes uniquely defensible.

See `/ns-phase7` for full implementation guide.

## Deviations

_None yet._
