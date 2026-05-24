---
name: ns-phase11
description: NeuroSpect Phase 11 — Advanced ML Research (NSLM, Hybrid Models, NeuroQuant, NeuroTrader)
---

You are working on **NeuroSpect Phase 11** (Advanced ML Research). This is the final and largest phase — add frontier ML only after the data foundation is solid.

**Recommended:** Start this phase in plan mode (`/phase 11 plan`) to design the ML research roadmap before implementing.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\CLAUDE.md`
3. Read Phase 5 EdgeLab engine — `api/app/edgelab/engine/` (experiment runner, feature store)
4. Read Phase 5 null test results — `research/phase-5-edgelab/null-test-results.md` — **HARD GATE: if null test failed (p > 0.05), NeuroTrader is NOT viable**
5. Read Phase 6 NeuroCore — `api/app/coach/rag/` (retrieval for NSLM context)
6. Read Phase 5 feature store — `api/app/edgelab/features/` (quant + ICT features)
7. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\roadmap\plan.md` lines 1303-1475 — old Phase 8-10 + EdgeLab UI

## Goal

Build the advanced ML research layer: NSLM prompt/model versioning and evaluation, hybrid models (quant + ICT + NSLM features), regime detection, NeuroQuant production model layer, and NeuroTrader Agent (shadow mode). This phase converts EdgeLab from a backtesting tool into a full model development and evaluation platform.

## Sub-phases

| Sub-Phase | Scope | Effort | Prerequisite |
|---|---|---|---|
| **11A — NSLM Evaluation Framework** | Prompt/model registries, structured output evaluation, dataset builder | L | Phase 5 + 6 |
| **11B — Hybrid Models + Regime** | Quant baselines, ICT models, hybrid models, HMM regime detection, model ensembles | XL | Phase 11A |
| **11C — NeuroQuant + NeuroTrader Shadow** | Production model serving, confluence scorer, shadow mode agent | L | Phase 11B + null test pass |

## Deliverables

### 11A — NSLM Evaluation Framework

1. **NSLM prompt version registry** (`api/app/edgelab/nslm/prompt_registry.py`):
   - Version tag (v1, v2, ...), system prompt hash, changelog, is_default
   - `nslm_prompt_versions` DB table
2. **NSLM model version registry** (`api/app/edgelab/nslm/model_registry.py`):
   - Version tag, base model (claude-sonnet-4-6, etc.), fine_tune_id, training config
   - `nslm_model_versions` DB table
3. **Structured output schemas** (`api/app/edgelab/nslm/structured_output_schemas.py`):
   - Setup classification output (setup type, confidence, conditions met/unmet)
   - Feature extraction output (NSLM-derived features for hybrid models)
   - Reasoning quality assessment
4. **Evaluation pipeline** (`api/app/edgelab/nslm/evaluator.py`):
   - Replay historical setup windows through NSLM versions
   - Compare: classification accuracy, reasoning consistency, feature usefulness
   - A/B comparison: v(N) vs v(N-1) across all metrics
   - `nslm_evaluation_runs` and `nslm_structured_outputs` DB tables
5. **Dataset builder** (`api/app/edgelab/nslm/dataset_builder.py`):
   - Generate evaluation corpus from historical setups with known outcomes
   - Build training pairs for future fine-tuning (if instructor provides examples)
6. **NSLM features** (`api/app/edgelab/features/nslm_features.py`):
   - Extract NSLM structured outputs as features for hybrid models
   - setup_confidence, reasoning_coherence_score, conditions_met_count

### 11B — Hybrid Models + Regime Detection

7. **Pure quant baselines** — LightGBM on standard quant features only
8. **ICT feature models** — LightGBM on ICT-derived features only
9. **Hybrid models** — LightGBM/XGBoost on combined quant + ICT + NSLM features
10. **Market regime detector** (`api/app/neuroquant/regime/`):
    - HMM-based 4-state (trending-up, trending-down, ranging, volatile)
    - Rule-based fallback (LRLR/HRLR classification)
    - `regime_detector.py`, `regime_labeler.py`
11. **Regime-conditional model selection** — different models for different regimes
12. **Model ensemble** — regime-aware, calibrated via Platt scaling
13. **Confluence scorer** (`api/app/neuroquant/confluence.py`):
    - ICT gates (binary pass/fail)
    - ML confidence (probability)
    - NSLM reasoning (narrative coherence check)
14. **Model promotion criteria** (EdgeLab → NeuroQuant):
    - Walk-forward efficiency > 0.6
    - Out-of-sample Sharpe > 0.5
    - Confidence calibration error < 0.1
    - Positive in 2+ of 4 regime states
    - Feature importance stable across windows
    - Monte Carlo median positive at 95% CI
    - Complete model card

### 11C — NeuroQuant + NeuroTrader Shadow

15. **NeuroQuant serving layer** (`api/app/neuroquant/`):
    - Load promoted models for live/paper scoring
    - `models/baseline.py`, `models/lgbm_model.py`, `models/ensemble.py`
    - Model card storage and retrieval
16. **NeuroTrader Agent shadow mode** (`api/app/agent/`):
    - Agent state machine: IDLE → SCANNING → SETUP_DETECTED → EVALUATING → LOGGING
    - Market monitor (read-only WebSocket for live bars)
    - Signal logging (hypothetical decisions to `agent_signals` table)
    - Discord webhook notifications for detected setups
    - **Shadow only** — no real trades, no paper trades in this phase

## Key Constraints

- **NSLM is NOT run on every backtest bar** — too expensive. Use for: live/paper decisions (~5-20 calls/day), post-hoc analysis, borderline setups (0.55-0.75 confidence)
- **No deep learning** — boosted trees (LightGBM) outperform on small datasets
- **No traditional indicators** (RSI, MACD, Bollinger) — ICT methodology doesn't use them
- **Null test is a hard gate** — if Phase 5C null test failed, NeuroTrader (11C) does NOT proceed
- **RIA determination required** before any live signal generation — legal review
- Every model must have: backtest, walk-forward, leakage checks
- New Python dependencies: `scikit-learn`, `lightgbm`, `hmmlearn`
- Shadow mode generates "what-if" signals only — never executes trades

## Acceptance Criteria

### 11A
- [ ] NSLM prompt/model registries store versions with metadata
- [ ] Evaluation pipeline compares two NSLM versions on historical data
- [ ] Dataset builder generates evaluation corpus from historical setups
- [ ] NSLM features extractable for hybrid model input

### 11B
- [ ] At least 3 model types trained and compared (pure quant, ICT, hybrid)
- [ ] Regime detector classifies market state with > 70% accuracy on labeled data
- [ ] At least 1 model meets all promotion criteria
- [ ] Confluence scorer combines ICT gates + ML confidence + NSLM reasoning
- [ ] Model cards complete for all promoted models

### 11C
- [ ] NeuroQuant loads and serves promoted models
- [ ] NeuroTrader shadow mode detects setups on live data
- [ ] Shadow signals logged with full reasoning
- [ ] Discord notifications fire for detected setups
- [ ] No real or paper trades executed

## NeuroFusion-13 Research Context

Before implementation, read ALL SIHRE research reports — this is where NeuroFusion-13 comes together:
- `research/neurofusion/data/prompt-1-ensemble-architecture.md` — 13-signal heterogeneous ensemble architecture and signal fusion design for NeuroQuant
- `research/neurofusion/data/prompt-2-dslm-quant-hybrid.md` — DSLM design, ICT-aware model family architecture, and quant-hybrid model patterns for NSLM
- `research/neurofusion/data/prompt-3-knowledge-graph.md` — temporal knowledge graph integration, confidence decay, and GNN patterns relevant to NeuroGraph feeding NeuroQuant
- `research/neurofusion/data/prompt-4-quant-trading-tech.md` — Monte Carlo, walk-forward, anti-lookahead, and feature engineering for the full ML pipeline
- `research/neurofusion/data/prompt-5-extended-signals.md` — extended signal types, fundamental data, and regime-conditional model selection for NeuroQuant

## When done

Say: "Phase 11 complete — NSLM evaluation, hybrid models, and NeuroTrader shadow mode are operational. The core NeuroSpect platform is feature-complete. Future work: paper trading (requires null test + RIA), live trading (requires 30+ days profitable paper + explicit approval), and advanced ML research."
