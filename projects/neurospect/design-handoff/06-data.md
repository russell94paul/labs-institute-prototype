# NeuroSpect Marketing Site — Data Models & Mock Data

All visualizations use illustrative (not real) data. This document describes the data shapes and key values so the designer understands what drives each visualization.

---

## Tier System (shared across all visualizations)

| Tier ID | Name | Short | Color | Hex |
|---|---|---|---|---|
| tier1 | Discretionary ICT Trader | Discretionary | Slate | #64748b |
| tier2 | Quant Trader | Quant | Purple | #8b5cf6 |
| tier3 | Hybrid Trader | Hybrid | Cyan/Brand | #06b6d4 |
| tier4 | S-Tier Trader | S-Tier | Emerald | #10b981 |

The tier system tells a **progression story**: each tier adds more NeuroSpect capability. Tier 1 is baseline (manual ICT trader), Tier 4 is the end state (automated with safety gates). Visualizations should reinforce this progression — Tier 4 always outperforms, but Tier 1 shows the most improvement potential.

---

## Equity Curves

**Shape:** Array of `{ date: string, equity: number }` per tier

**Parameters:**
- Instrument: NQ (Nasdaq 100 Futures)
- Period: May 2026, 20 trading days
- Starting equity: $25,000 per tier
- End equity (approximate): Tier 1 ~$23,800 | Tier 2 ~$27,200 | Tier 3 ~$29,500 | Tier 4 ~$31,000

**Key characteristics:**
- Tier 1: volatile, some recovery but net negative. Biggest drawdowns on tilt days.
- Tier 2: steady positive, fewer but higher-quality trades. Statistical approach reduces volatility.
- Tier 3: best of both worlds. Uses quant signals to filter discretionary entries.
- Tier 4: smoothest curve, highest Sharpe. Automated execution removes emotional decisions.

---

## Trade Markers

**Shape:** 8 annotated events on specific dates

Each marker includes:
- `date`, `title`, `symbol` (NQ), `session`, `setupType`, `marketContext`
- `tierOutcomes`: per-tier object with `action` (entered/skipped), `result` (win/loss/BE/no_trade), `pnl`, `explanation[]`, `mistakes[]` (Tier 1 only)
- `tier1Solution`: what Tier 1 needed from NeuroSpect to avoid the mistake

**Purpose:** When a trader clicks a marker, they see the same market event handled differently by each tier. This is the core "aha moment" — showing that the difference isn't the market, it's the trader's tools and process.

---

## KPI Summary (per tier)

| Metric | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Net P&L | -$1,200 | +$2,200 | +$4,500 | +$6,000 |
| Win Rate | ~45% | ~55% | ~62% | ~68% |
| Profit Factor | ~0.85 | ~1.8 | ~2.3 | ~3.1 |
| Total Trades | ~42 | ~25 | ~30 | ~22 |
| Avg R | -0.15 | +0.45 | +0.72 | +1.1 |
| Max Drawdown | ~$3,200 | ~$1,800 | ~$1,200 | ~$800 |
| Sharpe Ratio | ~0.3 | ~1.2 | ~1.8 | ~2.4 |
| Execution Grade | C | B+ | A- | A+ |

*(Exact values are in `site/src/data/tier-kpis.ts`)*

---

## Day-of-Week Performance

| Day | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Monday | Negative | Flat | Positive | Positive |
| Tuesday | Mixed | Positive | Positive | Positive |
| Wednesday | Most negative (tilt) | Positive | Most positive | Positive |
| Thursday | Flat | Best day | Positive | Best day |
| Friday | Slight positive | Flat (reduced size) | Flat | Small positive |

**Story:** Tier 1 loses most on Wednesdays (mid-week tilt after Monday/Tuesday losses). Higher tiers handle mid-week drawdowns better due to risk limits and coaching.

---

## Session Performance

5 sessions: Asia, London, New York AM, New York Lunch, New York PM

**Key insight:** NY AM is the best session across all tiers (Silver Bullet + London Close alignment). Tier 1 overtrades in NY Lunch and PM. Higher tiers skip low-probability sessions.

---

## Setup Performance

7 ICT setups tracked:
1. Liquidity Sweep + Displacement + FVG
2. Market Structure Shift
3. HTF Bias + LTF Entry
4. Order Block Continuation
5. Breaker Retest
6. Session Range Expansion
7. Failed FVG Continuation

**Key insight:** Setup #1 (Liq Sweep + Displacement + FVG) is the highest-expectancy setup for all tiers. Tier 1 doesn't filter enough and takes setups #6 and #7 which have negative expectancy.

---

## Mistakes (per tier)

| Tier | Top Mistakes | Total Count |
|---|---|---|
| Tier 1 | Overtrading, poor stop placement, ignoring HTF bias, revenge trading, trading low-probability sessions | ~18 |
| Tier 2 | Over-optimization, ignoring discretionary signals, small sample size | ~6 |
| Tier 3 | Occasional override of model signals, position sizing errors | ~4 |
| Tier 4 | Parameter drift, insufficient retraining window | ~2 |

---

## Risk Metrics (per tier)

Includes: max drawdown, max DD duration, largest win, largest loss, consecutive losses, consistency score (/100), recovery factor, Calmar ratio, return volatility.

---

## Capability Matrix (Compare Page)

14 capabilities compared across 7 tools. NeuroSpect is "yes" on all 14. Best competitor column maxes out at ~3 partial and 0 full.

---

## Subscription Stack (Compare Page)

8 tools with cost ranges summing to $125-$710/mo vs NeuroSpect at $29-$349/mo.

---

## Data File Locations (in codebase)

| File | Contains |
|---|---|
| `site/src/data/tier-colors.ts` | Tier color definitions, chart colors |
| `site/src/data/equity-curves.ts` | 20-day equity curve arrays + 8 trade markers |
| `site/src/data/tier-kpis.ts` | Full KPI breakdown per tier |
| `site/src/data/performance-analytics.ts` | Day-of-week, session, setup, mistake, risk data |
| `site/src/data/competitors.ts` | Capability matrix, subscription stack, workflow, questions |
