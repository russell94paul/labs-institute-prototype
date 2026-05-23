---
tags: [roadmap-idea, neurospect, next]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-26
horizon: next
status: in-progress
---

# Reduce Journaling Friction

Make journaling so cheap that it happens consistently: tab-based trade entry, fewer mandatory fields, sensible defaults, and eventually voice + auto-fill.

## Why it matters

Journal data is the substrate every later horizon depends on (profiler, edge detection, voice coach, action items). Inconsistent journaling = no data = nothing for AI to learn from. This is the highest-leverage friction reduction in the product.

## User feedback (2026-04-26)

Paul (primary user) after first real use:
- "Too many manual fields to enter"
- "The layout of when and how to enter the data doesn't flow as nicely as I would like"
- Wants the three phases (pre-trade, in-trade, post-trade) as **tabs**, not collapsible sections on one scrolling page

The form currently has 12 fields in the pre-trade collapsible section alone. The collapsible pattern buries complexity but doesn't remove it.

## Phase 1 — Tab redesign + field reduction (in-progress)

### Tab structure

Replace the three collapsible sections with three persistent tabs that map to the trade lifecycle status:

| Tab | Status gate | Purpose |
|---|---|---|
| **Pre-Trade** | Always accessible | Thesis capture before entry |
| **Entry** | Accessible once pre-trade saved | Execution capture at entry |
| **Post-Trade** | Accessible once active | Review after exit |

### Pre-Trade — minimal field set

Surface these prominently (no accordion):
- Trade Date (default: today)
- Instrument (default: NQ)
- Session + Kill Zone (side by side)
- HTF Bias (radio: Bullish / Bearish / Neutral)
- Setup Type (select)
- Narrative (textarea — "What do you see and why are you watching this?")

Move to an **Advanced** collapsible within the Pre-Trade tab:
- HTF FVG Low / High
- Draw on Liquidity + DOL Price Level
- Opening Price Position
- News flag

### Entry tab fields

- Entry Time (datetime-local, default: now)
- Entry Price
- Stop Price + Stop Logic
- Target Price + Target Logic
- Entry PDA, Displacement Quality, SMT Confirmation

### Post-Trade tab fields

- Exit Time + Exit Price
- Outcome, R-multiple (auto-calculated), MAE/MFE
- Target Reached, Plan Followed
- Quality Grade
- Mistake Tags
- Post-Trade Notes

### Default values

- Trade Date: today (removes the date-picker click for every entry)
- Instrument: "NQ" (most common; user overrides for other instruments)

## Phase 2 — AI Coach → journal pre-fill (future)

Coaching response (Layer 3) already contains `bias`, `valid_strategies`, and `narrative`. When a coaching event is marked complete, offer a one-click "Start Trade from Coach" button that pre-fills the pre-trade tab with:
- `htf_bias` ← `response_payload.bias`
- `setup_type` ← first `valid_strategies[0].strategy_id`
- `narrative` ← `response_payload.narrative`
- `session` / `kill_zone` ← derived from `alert_timestamp`

Tracked in [[concepts/architecture/tradingview-connector]] §8 Open items.

## Phase 3 — Voice + auto-populate (future)

- **Voice journaling** — speech-to-text into narrative / post-trade notes fields; reuses AI Coach pipeline.
- **Auto-populated trade data** — broker fills, instrument, session, kill zone prefilled (depends on [[concepts/roadmap/ideas/tradovate-integration]]).

## Dependencies

- Phase 1: no new dependencies — pure frontend refactor.
- Phase 2: coaching events pipeline (already built).
- Phase 3: Tradovate integration + AI Coach pipeline.

## Open questions

- Default templates per setup type (FVG entry vs. OTE vs. raid-on-stops) — derive from [[concepts/entry-models/README]]?
- Mobile capture path — is the Chrome extension enough, or do we need a thin mobile companion?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/trade-schema]]
- [[concepts/architecture/tradingview-connector]]
- [[concepts/roadmap/ideas/tradovate-integration]]
- [[concepts/roadmap/ideas/chrome-screenshot-extension]]
