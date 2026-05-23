---
tags: [concept, business-logic, ict, order-flow, htf-ltf, closing-basis, quadrants, neurospect]
aliases: [ICT Order Flow, HTF LTF Order Flow, Closing Basis, Quadrant Levels, LRLR, HRLR, Low Resistance, High Resistance]
sources:
  - sources/neurospect/2026-04-18-vol4-class1-htf-ltf-orderflow.md
created: 2026-04-18
updated: 2026-04-20
---

# ICT Order Flow (HTF/LTF)

Order flow in ICT does **not** require footprint charts, Level 2 data, or any paid subscription. It is determined by reading **closing prices of candles relative to PDA levels** and **quadrant analysis** of dealing ranges. Order flow tells you whether to trust the current move or stand aside.

> "Do you really think they're going to allow you to literally see what the big whales are entering at? You don't need anything like that. Just knowing where the swing highs and swing lows are is all you need." — Vol 4 Class 1

---

## HTF Order Flow — Reading Market Direction

### Candle Bodies vs. Wicks

- **Bodies tell the story** — closing prices confirm direction
- **Wicks engineer liquidity** — don't trade the wicks, trade the body reaction to them

### Closing Basis Analysis

Order flow is confirmed by **where candles are closing**, not just what price is touching:

| Observation | Signal |
|---|---|
| Bodies closing **above** a PDA level | Bullish — that level is now support |
| Bodies closing **below** a PDA level | Bearish — that level is now resistance |
| Close above a bearish CV / FVG | Inversion → bullish signal |
| Bodies not respecting either side | Chop → stand aside |
| Up-close candles not being respected as resistance | Order flow turning neutral or bullish |

**When to stop trading:** If up-close candles are no longer being respected as bearish order blocks (or down-close candles as bullish support), the order flow is indeterminate — exit or wait.

---

## Quadrant Levels

Divide any dealing range (significant swing low → swing high) into four equal levels:

| Level | Description |
|---|---|
| 0 (low end) | Bottom of the range |
| 0.25 (lower quadrant) | 25% level — PDA arrays form here in downtrends |
| 0.50 (midpoint / EQ) | 50% — key equilibrium; consolidation often forms here |
| 0.75 (upper quadrant) | 75% level — PDA arrays form here in uptrends |
| 1.0 (high end) | Top of the range |

> "PDA arrays are going to be formed around these specific levels." — Vol 4 Class 1

Useful for identifying where order blocks and FVGs will naturally form during a directional move — without guessing.

**Deviation from quadrants:** The -0.25 level below the range low is a common first target beyond the range, calculated the same way.

---

## Bullish Order Flow

Signs that order flow is bullish (look for entries in this environment):

1. **Down-close candles being supported** — up-close candles before the up move are respecting the opening price as support; bodies close above them
2. **FVGs staying unfilled** — bearish FVGs are left open, signaling price is not retracing
3. **Lower highs forming in the retracement** — steady pullback into discount with lower highs = "beautiful for long"
4. **Gap not filling on retracement** — LRLR conditions

> "Every single up-close candle, I need to see it supporting price lower [when bearish] and fair value gaps should stay unfilled. That is a characteristic of low-resistance liquidity run." — Vol 4 Class 1

---

## Bearish Order Flow

Signs that order flow is bearish (look for short entries):

1. **Up-close candles being respected as resistance** (bearish order blocks)
2. **FVGs staying unfilled above price** — price isn't coming back for them = LRLR down
3. **Bodies closing below key PDA levels** on multiple candles
4. **Swing lows being taken, swing highs being rejected** — structural confirmation

In LRLR bearish conditions: up-close candle before a down move = bearish OB → entry on breach of that opening price.

---

## LRLR vs. HRLR

| Condition | Full Name | Characteristics |
|---|---|---|
| **LRLR** | Low Resistance Liquidity Run | Fast, trending; FVGs stay unfilled; don't chase but entries are straightforward |
| **HRLR** | High Resistance Liquidity Run | Choppy, back-and-forth; bodies overlap; FVGs get filled; small ORG (<50 handles NQ) |

**How to identify:**
- HRLR: overlapping candle bodies, small opening range gap, news week (FOMC, NFP, CPI)
- LRLR: candles stacking in one direction, FVGs staying open, bodies respecting levels cleanly

In HRLR: use BPR (Balanced Price Range) logic; expect deep retracements; use OTE model.

---

## LTF Order Flow — 1M and Below

At the entry timeframe (1M, 15s, 5s):

**Order flow is bullish when:**
- Down-close candles (bullish OBs) are respected as support
- FVGs in the direction of the trend stay open (unfilled)
- Higher lows forming with each expansion

**Shift to bearish at LTF:**
- Up-close candles before the down move breach their opening price (CSD signal)
- Bodies now close below previously-respected PDA levels
- The FVG above price stays open — breakaway condition

---

## Range Quadrant Application (Step by Step)

1. Identify a significant dealing range (ITL → ITH swing)
2. Mark the 0, 0.25, 0.50, 0.75, 1.0 levels
3. In a bearish move from 1.0: look for PDA arrays at 0.75 and 0.50 (premium zone)
4. In a bullish retracement to 0.25: look for PDA arrays at 0.25 and 0.50 (discount zone)
5. Check closing basis: bodies must close in the direction of the trade before committing

---

## Holiday Liquidity

Levels created during holiday sessions (e.g., Thursday holiday close) are targeted **early the next trading day**:
- Holiday session creates thin liquidity at specific levels
- These get swept during the next day's London or NY AM session
- Do not use holiday session levels as "confluences" for trade direction — only as targets

---

## See Also

- [[ict-market-structure]] — ITH/ITL structure that defines the dealing ranges
- [[ict-liquidity]] — PDA arrays (FVG, OB) that form at quadrant levels
- [[ict-narratives]] — LRLR/HRLR conditions affect which delivery model applies
- [[ict-entry-models]] — order blocks and FVGs as order flow entry signals
- [[ict-smt]] — SMT divergence as an intermarket order flow signal
- [[ict-deviations]] — quadrant 0.25 extension as deviation target
