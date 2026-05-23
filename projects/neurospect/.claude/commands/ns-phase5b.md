---
name: ns-phase5b
description: NeuroSpect Phase 5B — EdgeLab Core (Detectors + Stats + Features)
---

You are working on **NeuroSpect Phase 5B** (EdgeLab Core — Strategy Compiler + Statistical Validation + Feature Store). This is part 2 of 3 for EdgeLab.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read Phase 5A engine code — `api/app/edgelab/engine/` (all files)
4. Read Phase 5A strategy compiler — `api/app/edgelab/strategies/strategy_compiler.py`
5. Read all 7 entry model YAMLs in `wiki/concepts/entry-models/`
6. Read Phase 4 detector code — `api/app/edgelab/detectors/` (all files)

## Goal

Compile all 7 ICT entry models into backtestable strategies, add Monte Carlo simulation and walk-forward optimization for statistical rigor, build the feature store for quant + ICT features, and expose EdgeLab via REST API. After this phase, any strategy can be backtested with full statistical validation.

## Deliverables

1. **Strategy compiler for all 7 entry models**:
   - Expansion & Retracement (E&R)
   - Consolidation Model
   - Breaker Block
   - MMXM (Market Maker Model)
   - Silver Bullet (time-based)
   - Turtle Soup (liquidity sweep reversal)
   - Unicorn Model
2. **Monte Carlo simulation** (`api/app/edgelab/risk/monte_carlo.py`):
   - Permutation-based (shuffle trade sequence, 10K iterations)
   - Output: median return, P5/P95 returns, ruin probability, distribution
   - Target: 10K iterations in < 30 seconds
3. **Walk-forward optimization** (`api/app/edgelab/risk/walk_forward.py`):
   - Configurable window sizes (e.g., 3-month in-sample, 1-month out-of-sample)
   - Efficiency ratio (out-of-sample Sharpe / in-sample Sharpe)
   - Deflated Sharpe ratio (corrects for multiple testing)
   - Overfitting detection (efficiency < 0.5 = likely overfit)
4. **Risk metrics module** (`api/app/edgelab/risk/`):
   - VaR, CVaR (Expected Shortfall)
   - Maximum drawdown duration
   - Kelly criterion sizing
   - Calmar ratio
5. **Feature store** (`api/app/edgelab/features/`):
   - `registry.py` — feature catalog (name, category, computation source, version)
   - `quant_features.py` — mean price, Parkinson volatility, ATR, returns distribution, opening range gap
   - `ict_features.py` — FVG distance, OB proximity, session encoding, HTF bias, displacement z-score, premium/discount zone
   - `feature_ranker.py` — feature importance ranking via permutation importance
   - `feature_definitions` DB table — feature registry
   - `feature_snapshots` DB table — point-in-time feature values (metadata, values in Parquet)
6. **REST API endpoints** (`api/app/routers/edgelab.py`):
   - `POST /api/edgelab/experiments` — create experiment
   - `GET /api/edgelab/experiments` — list experiments
   - `GET /api/edgelab/experiments/{id}` — get experiment with runs
   - `POST /api/edgelab/experiments/{id}/run` — trigger a backtest run
   - `GET /api/edgelab/runs/{id}` — get run detail with trades and metrics
   - `GET /api/edgelab/features` — list registered features
   - `POST /api/edgelab/experiments/{id}/monte-carlo` — run Monte Carlo on experiment results
   - `GET /api/edgelab/experiments/{id}/walk-forward` — walk-forward results
7. **Tests** for all strategies, Monte Carlo, walk-forward, and feature calculations

## Key Constraints

- Every strategy must compile from its wiki YAML block — no hardcoded strategy logic
- Monte Carlo must be fast (10K iterations < 30s) — use vectorized operations via Polars/NumPy
- Walk-forward windows must be configurable, not hardcoded
- Feature snapshots are point-in-time — no leakage of future data into feature values
- Do not build the dashboard yet (Phase 5C)
- Do not add ML model training yet (Phase 11)

## Acceptance Criteria

- [ ] All 7 ICT strategies compile from YAML and produce backtest results
- [ ] Monte Carlo runs 10K iterations in < 30 seconds and produces distribution + ruin probability
- [ ] Walk-forward optimization produces efficiency ratio and deflated Sharpe
- [ ] Feature store registers quant + ICT features with point-in-time snapshots
- [ ] Feature importance ranking works via permutation importance
- [ ] All EdgeLab REST endpoints return correct data
- [ ] Tests cover each strategy on fixture data, Monte Carlo edge cases, and walk-forward window logic

## When done

Say: "Phase 5B complete — all 7 strategies backtestable with statistical validation. Run `/ns-phase5c` in a new session for the EdgeLab dashboard + null test."
