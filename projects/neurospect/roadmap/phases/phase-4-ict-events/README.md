---
phase: 4
name: "ICT Event Intelligence"
status: not_started
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
goal: "Convert ICT concepts into programmable, queryable market events. Foundation for backtesting, trade review context, and Edge Forensics."
deliverables:
  - "MarketEvent model (type, timestamp, instrument, timeframe, price levels, direction, confidence)"
  - "BaseDetector interface"
  - "Core detectors: FVG, Swing, Session, OpeningPrice, LiquiditySweep"
  - "Advanced detectors: OrderBlock, MarketStructure, Bias, SMT"
  - "Market data pipeline (FirstRate CSV → Bar model → multi-timeframe aggregation)"
  - "Fundamental event pipeline: economic calendar (FOMC, NFP, CPI, Fed Chair, PPI, retail sales, jobless claims), earnings reports, dividend dates, contract rollover, options expiry"
  - "FundamentalEvent model (event_type, scheduled_time, actual_vs_expected, surprise_magnitude, instrument_impact, source)"
  - "Event-trade association"
  - "Event API endpoints (query + detect)"
  - "Tests with fixture candle data"
constraints:
  - "Detectors must be deterministic — no ML in this phase"
  - "Events are detected market structures, not signals or recommendations"
  - "Anti-lookahead: detectors receive only bars up to current time"
  - "Keep detectors composable"
  - "Market data in PostgreSQL for now; Parquet migration in Phase 5A"
acceptance_criteria:
  - "MarketEvent model stores detected events with full metadata"
  - "All 5 core detectors correct on fixture data"
  - "At least 2 advanced detectors functional"
  - "Market data importable from FirstRate CSV"
  - "Multi-timeframe aggregation correct"
  - "Events queryable by type, instrument, timeframe, date range"
  - "Events associable with trades"
  - "Anti-lookahead enforced"
  - "Fundamental events ingested from economic calendar API"
  - "Earnings reports and key macro events queryable alongside ICT events"
  - "News blackout windows derivable from scheduled events"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 4: ICT Event Intelligence

Programmable ICT event detection — FVGs, sweeps, order blocks, market structure, sessions as queryable events. Also includes fundamental event pipeline: economic calendar (FOMC, NFP, CPI, etc.), earnings reports, contract rollover, options expiry. Both structural and fundamental events are unified under the MarketEvent model and feed into NeuroFusion signals (quant models, knowledge graph, causal discovery, regime detection, synthetic scenarios).

See `/ns-phase4` for full implementation guide.

## Deviations

_None yet._
