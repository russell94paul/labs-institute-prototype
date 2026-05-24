---
phase: 2
name: "Market Context & Trade Integration"
status: not_started
track: "A (Coaching)"
assigned: []
started: null
completed: null
tickets_total: 2
tickets_done: 0
created: 2026-05-09
updated: 2026-05-10
---

# Phase 2: Market Context & Trade Integration

Agent tools for personalized coaching, economic calendar, trade review, voice journaling prototype. Includes the real-time market data pipeline infrastructure that feeds Phases 7-9.

## Goals

_See `roadmap/plan.md` Phase 2 for detailed goals, plus the market data pipeline goals below._

## Market Data Pipeline (Added 2026-05-10)

Neither the v1 nor v2 plan specified data vendor contracts, costs, or latency requirements for market data. This is a critical dependency for Phase 2 (economic calendar, trade context) and becomes essential infrastructure for Phases 7-9 (EdgeLab, NeuroQuant, NeuroTrader).

### Deliverables

| Deliverable | Description | Gate? |
|---|---|---|
| Data vendor evaluation | Compare vendors: Polygon.io, Alpaca, IBKR, Databento, Tiingo. Evaluate cost, latency, instrument coverage, redistribution terms | Yes |
| Vendor contract(s) | Signed data agreements with selected vendor(s) covering redistribution rights | Yes |
| Market data ingestion pipeline | Scheduled pipeline: fetch OHLCV + economic calendar → PostgreSQL + R2 Parquet | Yes |
| Latency requirements doc | Define acceptable latency per use case: coaching (minutes OK), EdgeLab (end-of-day OK), NeuroTrader (sub-second required) | No |
| Redistribution compliance | Document what data can be shown to users, cached, or derived — per vendor ToS | No |
| Cost model | Monthly cost projection per vendor at each scale tier (MVP, 100 users, 1000 users) | No |

### Vendor Comparison (Preliminary)

| Vendor | OHLCV | Real-time | Cost (approx) | Redistribution | Notes |
|---|---|---|---|---|---|
| Polygon.io | Yes | WebSocket | $29-199/mo | Allowed with attribution | Good for MVP; futures coverage varies |
| Alpaca | Yes | WebSocket | Free-$99/mo | Allowed for display | Free tier for equities; futures limited |
| IBKR API | Yes | Streaming | $0 (with brokerage) | Display only | Best for live trading (Phase 9); complex API |
| Databento | Yes | TCP/WebSocket | Usage-based | Allowed | Best quality; expensive at scale |
| Tiingo | Yes | REST/WebSocket | $10-50/mo | Allowed | Budget option; limited futures |

### Latency Requirements by Phase

| Phase | Use Case | Acceptable Latency | Data Freshness |
|---|---|---|---|
| 2-3 (Coaching) | Economic calendar, session context | Minutes | End-of-day + intraday delayed |
| 7 (EdgeLab) | Backtesting, feature engineering | N/A (historical) | End-of-day batch |
| 8 (NeuroQuant) | Model scoring, regime detection | Seconds-minutes | Near real-time |
| 9 (NeuroTrader) | Trade execution, risk management | Sub-second | Real-time streaming |

### Exit Criteria (Market Data)

1. At least one data vendor contract signed
2. OHLCV ingestion pipeline operational for primary instruments (ES, NQ, GC)
3. Economic calendar integration functional
4. Redistribution compliance documented
5. Cost model validated against budget

## Exit Criteria (Original)

_See `roadmap/plan.md` Phase 2 for exit criteria._

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
