---
phase: 8
name: "Hybrid Model Research + NeuroQuant Promotion"
status: not_started
track: "B (Trading Intelligence)"
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
created: 2026-05-09
updated: 2026-05-10
---

# Phase 8: Hybrid Model Research + NeuroQuant Promotion

Build hybrid models combining ICT features, quant features, and NSLM-derived features. Evaluate across market regimes. Establish formal promotion criteria from EdgeLab research to NeuroQuant production.

## Goals

Key deliverables:
- Pure quant baselines (logistic regression + LightGBM)
- ICT feature models
- NSLM-derived feature models
- Hybrid models (combined quant + ICT + NSLM features)
- Market regime detector (HMM-based + rule-based fallback)
- Regime-conditional model selection + ensemble
- Confidence calibration (Platt scaling)
- Formal promotion criteria (EdgeLab → NeuroQuant)
- Model cards for each promoted model
- NeuroQuant serving layer

_See `roadmap/plan.md` §21 for detailed scope, promotion criteria, and model card template._

## Exit Criteria

1. At least 3 model types trained and compared (pure quant, ICT, hybrid)
2. Regime detector classifies current market state with > 70% accuracy on labeled data
3. At least 1 model meets all promotion criteria and is deployed to NeuroQuant
4. Confluence scorer functional (ICT gates + ML + NSLM reasoning)
5. Model cards complete for all promoted models

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
