---
name: ns-phase1
description: NeuroSpect Phase 1 — Trading Data Foundation
---

You are working on **NeuroSpect Phase 1** (Trading Data Foundation).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\trade.py` — existing 100+ field trade model
4. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\enums.py` — 17 ICT-specific enums
5. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\broker_credential.py` — existing broker credential model
6. Read `C:\Users\PaulRussell\repos\neurospect\api\app\routers\tradovate.py` — existing Tradovate integration
7. Read `C:\Users\PaulRussell\repos\neurospect\api\app\services\tradovate.py` — Tradovate service layer
8. Read `C:\Users\PaulRussell\repos\neurospect\api\app\routers\trades.py` — trade CRUD

## Goal

Create the normalized, verified trading data foundation that every downstream feature depends on. Extend the existing trade and broker models with account types (sim/eval/funded/live), trade import pipelines, execution normalization, and data quality checks. This is the bedrock — risk engine, event detection, backtesting, AI review, and NeuroScore all read from this layer.

## Deliverables

1. **BrokerAccount model** — separate from BrokerCredential. Fields: account_type (sim/eval/funded/live), prop_firm_name, account_size, broker (tradovate/manual), verification_status, user_id FK
2. **Trade model extensions** — add account_id FK, verification_flag (broker_verified/self_reported), import_source (tradovate_sync/csv_import/manual)
3. **InstrumentMetadata model** — tick_size, contract_value, session_times, exchange, instrument_type for NQ/ES/YM/GC
4. **Trade import pipeline** — CSV import endpoint, Tradovate auto-sync improvements, manual entry validation
5. **Execution normalization** — map Tradovate fills to canonical trade format (entry/exit/stop/target/R-multiple)
6. **Data quality checks** — duplicate detection, gap detection, timezone normalization
7. **Alembic migrations** for all schema changes
8. **Tests** for import pipeline, normalization, and data quality checks
9. **API documentation** for new/modified endpoints

## Key Constraints

- Extend existing models — do NOT replace `trade.py` or `broker_credential.py`
- Keep changes backward-compatible with existing frontend
- Do not implement analytics, AI, or risk features yet — those are Phases 2-3
- Tradovate auto-sync should be idempotent (re-import doesn't create duplicates)
- All timestamps normalized to UTC

## Tasks

1. Inspect existing trade/account/schema code (boot procedure files)
2. Create `BrokerAccount` model and migration
3. Extend `Trade` model with account_id, verification, import_source fields + migration
4. Create `InstrumentMetadata` model and seed data for NQ, ES, YM
5. Build CSV import endpoint (`POST /api/trades/import`)
6. Improve Tradovate fill sync with normalization and dedup
7. Add data quality validation service
8. Add tests for all new models, import, and normalization
9. Update API docs

## Acceptance Criteria

- [ ] A user can have one or more broker accounts with type labels (sim/eval/funded/live)
- [ ] Trades are linked to a broker account
- [ ] Trades can be imported via CSV with validation
- [ ] Tradovate sync normalizes fills into canonical trade format
- [ ] Duplicate imports are detected and rejected
- [ ] InstrumentMetadata exists for NQ, ES, YM with correct tick sizes and session times
- [ ] All migrations run cleanly on existing database
- [ ] Tests pass for import pipeline, normalization, and data quality

## When done

Say: "Phase 1 complete — trading data foundation is in place. Run `/ns-phase2` in a new session for the Trader Workspace (journal + analytics + behavior metrics)."
