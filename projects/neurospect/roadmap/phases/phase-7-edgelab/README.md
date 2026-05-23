---
phase: 7
name: "NeuroSpect EdgeLab Foundation"
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

# Phase 7: NeuroSpect EdgeLab Foundation

Event-driven research, backtesting, quant feature engineering, NSLM prompt/model experimentation, and hybrid model evaluation engine. This is the foundation for everything in Phases 8-9.

## Goals

Build EdgeLab as the central experimentation platform where strategies, features, NSLM versions, and hybrid models are tested, compared, and validated before promotion to production.

Key deliverables:
- Custom event-driven backtest engine with anti-lookahead enforcement
- ICT pattern detector framework (8 detectors)
- Strategy compiler (YAML → StrategySpec)
- Quant feature store with registry and point-in-time snapshots
- Experiment registry (define, run, compare, reproduce)
- NSLM prompt/model version registries
- NSLM structured output evaluation pipeline
- Monte Carlo simulation + walk-forward optimization
- Market data ingestion pipeline
- Null test: ICT strategies vs random baseline

_See `roadmap/plan.md` §20 for detailed scope, sub-phases (7A-7D), and architecture._

## Exit Criteria

1. All 7 ICT strategies compiled from YAML and backtestable
2. Walk-forward efficiency ratio > 0.5 for at least 3 strategies
3. Monte Carlo simulation runs 10K iterations in < 30 seconds
4. NSLM prompt evaluation pipeline functional
5. Feature store contains quant + ICT + NSLM-derived features with snapshots
6. Null test completed and documented
7. Experiment registry tracks all runs with full reproducibility

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
