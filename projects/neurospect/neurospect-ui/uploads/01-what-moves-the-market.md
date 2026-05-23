---
tags: [course, module-1, foundations, liquidity, inefficiency, neurospect]
aliases: [What Moves the Market, Liquidity and Inefficiency Lesson]
sources:
  - sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-pt2-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-notes.md
created: 2026-04-22
updated: 2026-04-22
---

# Module 1, Lesson 1: What Moves the Market

> **Vol 1, Class 1 — MrWitness (primary) + AXL**

The answer that MrWitness is looking for when he asks "what makes the market move?" is not buyers and sellers, not supply and demand, not support and resistance. It is two things and only two things:

**1. Liquidity**
**2. Inefficiency**

Every price move, every day, is traveling from liquidity to inefficiency or from inefficiency to liquidity. When it is doing neither, it is consolidating — engineering more liquidity for a future move.

---

## Concept 1: Liquidity

Liquidity is always present. You do not need Level 2 data, an order flow subscription, or a paid tool to find it. You only need to read candlesticks.

Liquidity exists because of **stop orders**:

| Type | Where It Lives | Why It's There |
|------|---------------|----------------|
| **Buy-Side Liquidity (BSL)** | Above swing highs | Traders who went short after a swing high placed their stop loss there |
| **Sell-Side Liquidity (SSL)** | Below swing lows | Traders who went long after a swing low placed their stop loss there |

The algorithm targets these stops every single day. That makes swing highs and swing lows your **draw on liquidity (DOL)** — the daily price magnet.

### How to Identify a Swing High or Swing Low

A swing is a **three-candle pattern**:
- **Swing high:** Candle 2 is the highest of the three
- **Swing low:** Candle 2 is the lowest of the three

The exact level to mark is the **candle 2 price** — not a zone, not a range, a single price. One tick above (for BSL) or below (for SSL) is sufficient to collect the stops.

> **Origin:** Larry Williams originally required five candles (fractals). ICT refined this to three. The three-candle definition is what this curriculum uses exclusively.

> "2 equal lows create a rejection block." — Vol 1 Class 1 Notes

### Draw on Liquidity (DOL)

The DOL is the specific liquidity level that price is currently gravitating toward. Think of it as a daily magnet — price is always heading somewhere specific, and that somewhere is a swing high or swing low.

**Timeframes to use:** Mark your swing highs and lows on the **1H and 15M** charts. These are the primary timeframes for identifying the DOL.

**Key facts:**
- Even on holidays, there are always swing highs and swing lows, so there is always a DOL
- The DOL is a single price, not a zone
- Once a DOL is taken, immediately look for the next one

---

## Concept 2: Inefficiency (Fair Value Gap)

Unlike liquidity, inefficiency is **not always present**. It requires a specific condition: **displacement**.

**Displacement** = price moving rapidly (with force and energy) in one direction.

When displacement occurs, the market moves so fast that it leaves a gap — a price range where delivery only happened in one direction. This gap is the **Fair Value Gap (FVG)**, also called: void, hole in price action, imbalance.

### The Three-Candle FVG Pattern

Three candles form the gap:
- **Candle 1** — the last candle before the move
- **Candle 2** — the gap itself (the void)
- **Candle 3** — the first candle of the new move

**Bullish FVG:** Candle 1's high does NOT touch Candle 3's low → gap exists between them → Candle 2 is the void.

**Bearish FVG:** Candle 1's low does NOT touch Candle 3's high → gap exists between them.

### Why Price Returns to the FVG

The gap has only been delivered in one direction. For price to be "efficiently priced," it must return to this range and deliver in both directions. This is the mechanical reason the FVG works as an entry — the algorithm is designed to return.

**Mitigation sufficiency:** Price only needs to **tag or dip into** the FVG (often to Candle 3's open/close area) for it to be considered efficiently delivered. A full fill all the way to Candle 1 is not required before price continues to the target.

---

## Concept 3: Liquidity vs. Inefficiency

| Property | Liquidity (BSL/SSL) | Inefficiency (FVG) |
|---|---|---|
| Always present? | Yes | No — requires displacement |
| What creates it | Swing highs / swing lows | Rapid price movement |
| Role | Target (DOL) | Entry signal |
| Timeframes to identify | 1H, 15M | 5M, 1M (entry timeframes) |

**The daily cycle:** Identify the HTF DOL (1H/15M swing high or swing low) → price displaces in that direction and creates an FVG → enter at the FVG → ride to the DOL.

---

## BISI and SIBI

Two formal names for the two FVG types:

**BISI (Buy Side Imbalance, Sell Side Inefficiency):**
- Price displaced higher, creating a gap
- Delivered on the buy side only
- Inefficient on the sell side → price must return to deliver sell-side
- **Used for long entries** — you enter at or into this gap, targeting the BSL above

**SIBI (Sell Side Imbalance, Buy Side Inefficiency):**
- Price displaced lower, creating a gap
- Delivered on the sell side only
- Inefficient on the buy side → price must return to deliver buy-side
- **Used for short entries** — targeting the SSL below

---

## Rules

1. Above swing highs = BSL. Below swing lows = SSL. These are your daily targets.
2. A swing is exactly three candles. Mark candle 2's price level, not a zone.
3. One tick beyond the swing high/low is sufficient to collect the stops.
4. An FVG requires displacement. A slow-moving range does not create a valid FVG.
5. Price only needs to dip into the FVG — it does not need to fully fill it before continuing.
6. When bullish: find a BISI. When bearish: find a SIBI.
7. Mark swing highs/lows for the DOL on 1H and 15M. Find your FVG entry on 5M–1M.

---

## Worked Example (from Class 1 — AXL's trade walk-through)

AXL demonstrated the following sequence on a live NQ chart:

1. On the 1M chart, he identified equal lows — two swing lows at the same level. Equal lows = a **rejection block** (the algorithm engineered those equal lows to collect stops below them).
2. The market swept those equal lows (took SSL), then immediately reacted and displaced higher.
3. The displacement created a **volume imbalance** (treated like a FVG) below the equilibrium of the range.
4. AXL entered at the volume imbalance, with stop loss below the swing that created the sweep.
5. Result: 1 risk, 36 reward. "Pretty simple, pretty easy."

The key sequence: **equal lows swept → displacement → FVG/volume imbalance near EQ → entry → run to target**.

Source: `sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md`

---

## Common Mistakes (from the Transcript)

- **Using zones instead of prices:** The swing high/low is a single price level (candle 2), not a zone. Entries at "around" the level lose precision.
- **Waiting for a full FVG fill:** Mitigation sufficiency means a tag is enough. Waiting for a full fill will cause missed entries.
- **Trading without a DOL:** An FVG entry without a target is gambling. Always identify your HTF DOL before entering.
- **Ignoring timeframe alignment:** FVGs exist on every timeframe. Only use 5M–1M FVGs for entries when the HTF (1H/15M) DOL is aligned.

---

## Homework (assigned in class)

> Assigned by MrWitness at the end of Vol 1 Class 1.

**Task:** Back-test this idea using historical price — do not take live or demo trades.

**Step 1:** On the **1H and 15M** charts, identify swing highs and swing lows. These are your liquidity levels (draw on liquidity).

**Step 2:** On the **5M, 4M, 3M, 2M, or 1M** charts, find a fair value gap (BISI for bullish setups) that was created by a displacement move in the direction of the 1H/15M DOL.

**Step 3:** Mark the ideal entry, stop loss, and target on the chart:
- Entry: at the FVG (specifically the upper portion of a bullish FVG — Candle 3's area)
- Stop loss: below the three candles that create the gap (below Candle 1 of the FVG)
- Target: the swing high (BSL) on the 1H/15M that is the DOL

**Step 4:** Take a screenshot. The screenshot must include the time of entry. Add the economic calendar if possible.

**Deliverable:** Post 1–5 examples in the Discord homework channel. No live trades. This is analysis only.

---

## See Also

- [[concepts/business-logic/ict-liquidity]] — full reference KB for BSL/SSL, DOL, FVG
- [[concepts/course/module-1-foundations/02-fair-value-gaps]] — next lesson: FVG mechanics in depth
- [[concepts/entry-models/consolidation-model]] — first entry model that applies these concepts
