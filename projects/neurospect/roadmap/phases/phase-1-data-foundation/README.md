---
phase: 1
name: "Trading Data Foundation"
status: complete
assigned: [paul]
started: 2026-05-10
completed: 2026-05-13
tickets_total: 0
tickets_done: 0
goal: "Create the normalized, verified trading data foundation that every downstream feature depends on."
deliverables:
  - "BrokerAccount model (account types: sim/eval/funded/live)"
  - "Trade model extensions (account_id FK, verification_flag, import_source)"
  - "InstrumentMetadata model (tick_size, contract_value, session_times)"
  - "Trade import pipeline (CSV import, Tradovate sync improvements)"
  - "Execution normalization (Tradovate fills to canonical format)"
  - "Data quality checks (dedup, gap detection, timezone normalization)"
  - "Alembic migrations for all schema changes"
  - "Tests for import, normalization, and data quality"
constraints:
  - "Extend existing models — do NOT replace trade.py or broker_credential.py"
  - "Keep backward-compatible with existing frontend"
  - "Do not implement analytics, AI, or risk features yet"
  - "Tradovate auto-sync must be idempotent"
acceptance_criteria:
  - "User can have multiple broker accounts with type labels"
  - "Trades linked to broker accounts"
  - "CSV import with validation"
  - "Tradovate sync normalizes fills into canonical format"
  - "Duplicate imports detected and rejected"
  - "InstrumentMetadata for NQ, ES, YM"
  - "All migrations run cleanly"
  - "Tests pass for import, normalization, data quality"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 1: Trading Data Foundation

Normalized, verified trading data layer — the bedrock for risk engine, events, backtesting, AI review, and NeuroScore.

**Status: COMPLETE** (2026-05-10 → 2026-05-13). Deliverables: ORM, CRUD, bulk import, analytics service.

See `/ns-phase1` for full implementation guide.

## Deviations

_None yet._
