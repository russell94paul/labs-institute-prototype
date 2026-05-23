---
name: ns-phase5a
description: NeuroSpect Phase 5A — EdgeLab Core (Engine + Data Pipeline)
---

You are working on **NeuroSpect Phase 5A** (EdgeLab Core — Engine + Data Pipeline). This is part 1 of 3 for EdgeLab, the largest phase in the roadmap.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read Phase 4 detector code — `api/app/edgelab/detectors/` (all detector files)
4. Read Phase 4 market data code — `api/app/edgelab/data/` (bar model, import pipeline)
5. Read `C:\Users\PaulRussell\repos\neurospect\wiki\concepts\entry-models\` — all 7 strategy YAMLs
6. Read `C:\Users\PaulRussell\repos\neurospect\roadmap\plan.md` lines 1209-1290 — Phase 7 (old numbering) deliverables and architecture

## Goal

Build the core backtest engine with anti-lookahead enforcement, Parquet-based market data storage, and the experiment registry. This engine replays historical bars through ICT strategies, tracks positions, and records every trade. It is the foundation for statistical validation (5B) and the dashboard (5C).

## Deliverables

1. **Backtest engine core** (`api/app/edgelab/engine/`):
   - `event_engine.py` — bar-by-bar replay loop with detector integration
   - `simulator.py` — position management (entry, stop, target, partial fills)
   - `execution_model.py` — realistic execution modeling (slippage, commission)
   - `anti_lookahead.py` — enforcement layer: strategy receives only `bars[:current_idx+1]`
2. **Market data pipeline** (`api/app/edgelab/data/`):
   - `parquet_store.py` — read/write OHLCV Parquet files on Cloudflare R2
   - `market_data_pipeline.py` — FirstRate CSV → cleaned → aggregated → Parquet
   - `replay_loader.py` — load Parquet data for a date range, instrument, timeframe
3. **Database schema** (new tables):
   - `edgelab_experiments` — experiment lifecycle (id, name, type, status, parameters JSONB, created_by)
   - `edgelab_runs` — individual runs within experiment (id, experiment_id, run_number, status, metrics JSONB, config JSONB)
   - `edgelab_run_trades` — per-trade records (entry/exit time, price, direction, stop, target, R-multiple, strategy, detections JSONB)
   - `backtest_metrics` — aggregate metrics per run (total_trades, win_rate, avg_r, max_drawdown, sharpe, sortino, profit_factor, expectancy)
4. **Experiment registry MVP** (`api/app/edgelab/experiments/`):
   - `experiment_registry.py` — create, list, get, update experiments
   - `experiment_runner.py` — orchestrate: load data → run detectors → apply strategy → record trades → compute metrics
5. **Strategy compiler (first strategy)**:
   - `strategy_compiler.py` — parse YAML strategy block into executable `StrategySpec`
   - `strategy_spec.py` — dataclass with entry conditions, exit rules, risk parameters
   - Compile and run the **Consolidation Model** as the first strategy
6. **Alembic migrations** for all EdgeLab tables
7. **Tests** for engine, anti-lookahead, and experiment lifecycle

## Key Constraints

- Anti-lookahead is **architecturally enforced** — the strategy function signature only accepts bars up to current index. This is not just a convention; the engine must make it impossible to access future data.
- Parquet files on R2 — use PyArrow for read/write, Polars for analysis
- Keep the engine synchronous for now — background task orchestration comes later
- The first strategy must be fully functional end-to-end before adding more strategies (that's Phase 5B)
- Do not build the dashboard yet (Phase 5C)
- New Python dependencies: `polars`, `pyarrow`

## Architecture

```
Market Data (FirstRate CSV → Parquet on R2)
    ↓
Replay Loader (date range, instrument, timeframe)
    ↓
Event Engine (bar-by-bar replay)
    ├── ICT Detectors (from Phase 4)
    ├── Strategy Spec (compiled from YAML)
    └── Anti-Lookahead Enforcement
    ↓
Simulator (position management, execution modeling)
    ↓
Trade Records → PostgreSQL (experiments, runs, trades, metrics)
```

## Acceptance Criteria

- [ ] Backtest engine replays bars through a strategy and produces trade records
- [ ] Anti-lookahead is enforced — tests prove strategy cannot access future bars
- [ ] Parquet store reads/writes OHLCV data to R2
- [ ] FirstRate CSV can be imported, cleaned, aggregated, and stored as Parquet
- [ ] Experiment registry creates, tracks, and completes experiments
- [ ] Consolidation Model strategy compiles from YAML and produces trades on historical data
- [ ] Backtest metrics (win rate, avg R, drawdown, Sharpe, expectancy) calculated correctly
- [ ] All EdgeLab tables created via Alembic migration
- [ ] Tests pass for engine, anti-lookahead, Parquet I/O, and experiment lifecycle

## When done

Say: "Phase 5A complete — EdgeLab engine runs backtests with anti-lookahead enforcement. Run `/ns-phase5b` in a new session for strategy compiler (all 7 models) + statistical validation."
