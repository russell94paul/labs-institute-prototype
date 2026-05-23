---
name: ns-phase4
description: NeuroSpect Phase 4 — ICT Event Intelligence
---

You are working on **NeuroSpect Phase 4** (ICT Event Intelligence).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\neurospect\wiki\CLAUDE.md`
4. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\enums.py` — 17 ICT-specific enums
5. Read all files in `C:\Users\PaulRussell\repos\neurospect\wiki\concepts\entry-models\` — 7 strategies with YAML blocks
6. Read all files in `C:\Users\PaulRussell\repos\neurospect\wiki\concepts\business-logic\` — 8 ICT concept docs
7. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\trade.py` — trade model for event-trade association

## Goal

Convert ICT concepts (FVGs, liquidity sweeps, order blocks, sessions, market structure) into programmable, queryable market events. Events become the foundation for backtesting (Phase 5), trade review context enrichment (Phase 6), and Edge Forensics (Phase 7). This is the ICT Event Engine component.

## Deliverables

1. **MarketEvent model** — canonical event representation:
   - type (fvg, sweep, order_block, bos, mss, choch, session_open, session_close, displacement, smt_divergence)
   - timestamp, instrument, timeframe
   - price_levels (high, low, midpoint as applicable)
   - direction (bullish/bearish)
   - confidence (0-1 for qualitative events like displacement)
   - metadata (JSONB — detector-specific details)
   - status (active/mitigated/invalidated)
2. **BaseDetector interface** — abstract class with `detect(bars: list[Bar]) -> list[MarketEvent]`
3. **Core detectors** (deterministic, rule-based):
   - `FVGDetector` — 3-candle gap detection (BISI/SIBI), with IOFED classification
   - `SwingDetector` — STH/ITH/LTH, STL/ITL/LTL identification via pivot logic
   - `SessionDetector` — kill zone boundaries, session open/close events (Asia, London, NY AM, NY PM)
   - `OpeningPriceDetector` — midnight open, session opens, weekly open
   - `LiquiditySweepDetector` — equal highs/lows taken, BSL/SSL sweep events
4. **Advanced detectors** (higher complexity):
   - `OrderBlockDetector` — last opposing candle before displacement (requires displacement judgment)
   - `MarketStructureDetector` — BOS, MSS, CHoCH detection using swing points
   - `BiasDetector` — HTF bias from FVG + opening price + session context
   - `SMTDetector` — cross-instrument divergence (NQ vs ES)
5. **Market data pipeline**:
   - CSV importer for FirstRate Data (1-min NQ/ES OHLCV)
   - Bar model (timestamp, open, high, low, close, volume, instrument, timeframe)
   - Multi-timeframe aggregation (1m → 5m → 15m → 1H → 4H → Daily)
6. **Event-trade association** — link detected events to nearby trades (configurable proximity window)
7. **Event API endpoints**:
   - `GET /api/events` — query by instrument, timeframe, type, date range
   - `POST /api/events/detect` — run detectors on a date range
8. **Tests** with fixture candle data for each detector

## Key Constraints

- Detectors must be deterministic first — no ML in this phase
- Events are "detected market structures" not "signals" or "recommendations"
- Anti-lookahead: detectors receive only bars up to current time
- Keep detectors composable — MarketStructureDetector uses SwingDetector output
- OrderBlock and displacement detection are the hardest — start with conservative rules, iterate
- Do not create strategy claims or backtest results yet (Phase 5)
- Market data storage: keep in PostgreSQL for now. Parquet migration happens in Phase 5A.

## Detector Complexity Guide

| Detector | Difficulty | Notes |
|---|---|---|
| FVGDetector | Low | 3-candle pattern, purely structural |
| SwingDetector | Medium | Requires lookback window for pivot confirmation |
| SessionDetector | None | Fixed time windows, deterministic |
| OpeningPriceDetector | None | Lookup by timestamp |
| LiquiditySweepDetector | Low | Price level identification against swing highs/lows |
| OrderBlockDetector | HIGH | "Displacement" judgment is qualitative — use z-score threshold |
| MarketStructureDetector | Medium | Depends on SwingDetector quality |
| BiasDetector | Medium | Multi-timeframe, combines FVG + opening price |
| SMTDetector | Medium | Cross-instrument comparison |

## Acceptance Criteria

- [ ] MarketEvent model stores detected events with full metadata
- [ ] All 5 core detectors produce correct events on fixture candle data
- [ ] At least 2 advanced detectors (OrderBlock, MarketStructure) functional
- [ ] Market data can be imported from FirstRate CSV
- [ ] Multi-timeframe aggregation produces correct higher-timeframe bars
- [ ] Events can be queried by type, instrument, timeframe, date range
- [ ] Events can be associated with trades (nearest events to entry/exit)
- [ ] Tests prove detector behavior on fixture data with known expected events
- [ ] Anti-lookahead enforced — detectors never access future bars

## When done

Say: "Phase 4 complete — ICT Event Engine is operational with 7+ detectors. Run `/ns-phase5a` in a new session for EdgeLab Core (backtest engine + data pipeline)."
