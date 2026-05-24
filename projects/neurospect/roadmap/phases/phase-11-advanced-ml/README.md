---
phase: 11
name: "Advanced ML Research"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Advanced ML research layer: NSLM evaluation, hybrid models, regime detection, NeuroQuant production serving, NeuroTrader shadow mode. Gated by Phase 5C null test."
deliverables:
  - "11A: NSLM prompt/model registries, structured output evaluation, dataset builder"
  - "11A: NSLM features for hybrid model input"
  - "11B: Pure quant baselines (LightGBM on quant features)"
  - "11B: ICT feature models (LightGBM on ICT features)"
  - "11B: Hybrid models (combined quant + ICT + NSLM features)"
  - "11B: HMM regime detector (4 states) with rule-based fallback"
  - "11B: Regime-conditional model selection and ensemble"
  - "11B: Confluence scorer (ICT gates + ML confidence + NSLM reasoning)"
  - "11C: NeuroQuant serving layer (load promoted models)"
  - "11C: NeuroTrader Agent shadow mode (scan → detect → evaluate → log)"
constraints:
  - "NSLM NOT run on every backtest bar — too expensive"
  - "No deep learning — boosted trees (LightGBM) for small datasets"
  - "No traditional indicators (RSI, MACD, Bollinger)"
  - "Null test is a hard gate — if Phase 5C failed, 11C does NOT proceed"
  - "RIA determination required before any live signal generation"
  - "Shadow mode only — never executes trades"
acceptance_criteria:
  - "11A: NSLM registries store versions; evaluation pipeline compares versions"
  - "11B: 3+ model types trained and compared; regime detector > 70% accuracy"
  - "11B: At least 1 model meets promotion criteria"
  - "11C: NeuroQuant loads and serves promoted models"
  - "11C: NeuroTrader shadow mode detects setups on live data"
  - "11C: Shadow signals logged with full reasoning; no real trades executed"
compliance_gate: "RIA determination before any live signal generation"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 11: Advanced ML Research (11A/11B/11C)

NSLM evaluation, hybrid models, regime detection, NeuroQuant, NeuroTrader shadow. Recommended: start in plan mode.

See `/ns-phase11` for full implementation guide.

## Deviations

_None yet._
