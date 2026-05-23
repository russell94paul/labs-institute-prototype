---
tags: [concept, business-logic, ict, liquidity, neurospect]
aliases: [ICT Liquidity, Draw on Liquidity, DOL, BSL, SSL, Buy-Side Liquidity, Sell-Side Liquidity, BISI, SIBI]
sources:
  - sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-pt2-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-notes.md
  - sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md
created: 2026-04-18
updated: 2026-04-22
---

# ICT Liquidity

Liquidity and inefficiency are the **only two things that move the market**. Price always travels from liquidity to inefficiency or from inefficiency to liquidity. When it is doing neither, it is consolidating — engineering more liquidity for a future move.

## Buy-Side Liquidity (BSL)

Buy-side liquidity consists of buy stops resting **above swing highs**. Anyone who went short after a swing high forms uses that high to protect their short position (stop loss above the high). The algorithm targets these stops, so BSL is a reliable draw on liquidity.

- Found above the candle #2 high in a three-candle swing-high pattern
- BSL is above current market price
- One tick above the swing high is sufficient to collect the stops

## Sell-Side Liquidity (SSL)

Sell-side liquidity consists of sell stops resting **below swing lows**. Longs use swing lows to protect their positions, creating a pool of orders below those lows.

- Found below the candle #2 low in a three-candle swing-low pattern
- SSL is below current market price

## Swing Highs and Swing Lows

A swing high or swing low is a **three-candle pattern**:
- Swing high: candle 2 is the highest of the three
- Swing low: candle 2 is the lowest of the three

Larry Williams originally required five candles (fractals); Michael J. Huddleston (ICT) refined this to three. The **candle #2 price** is the exact level to mark — not a zone.

> "2 equal lows create a rejection block." — Class 1 Notes

## Draw on Liquidity (DOL)

The DOL is the specific liquidity pool that price is currently gravitating toward. Price behaves as a **daily magnet** — even on holidays, swing highs and swing lows are always forming so there is always a DOL.

- Primary timeframes for identifying the DOL: **1H and 15M** swing highs/lows
- The DOL is always a single price, not a zone
- Once a DOL is taken, look for the next DOL in the same direction, or a gap (inefficiency) before reversing

## Inefficiency (Fair Value Gap / FVG)

An inefficiency is left in price when the market **displaces** — moves rapidly in one direction. It is a void or gap in price action (not a zone).

- Also called: Fair Value Gap, FVG, void, hole in price action
- Three-candle pattern: candle 1's high does not touch candle 3's low (bullish) or candle 1's low does not touch candle 3's high (bearish)
- **Candle #2 creates the gap** — the market has only delivered in one direction through it

### Bullish FVG (BISI — Buy Side Imbalance, Sell Side Inefficiency)

Price has displaced higher, leaving a gap delivered only to the buy side. The gap is inefficient on the sell side. Price must return to this range to "deliver price efficiently." Entry is at or below the candle 3 low, one tick below.

### Bearish FVG (SIBI — Sell Side Imbalance, Buy Side Inefficiency)

Price has displaced lower, leaving a gap delivered only to the sell side. Price must return to deliver efficiently to the buy side.

### Mitigation Sufficiency

Price only needs to **tag or dip into** the FVG — often to candle 3's open/low/high — for the gap to be considered efficiently delivered. A full fill is not required before continuation to the target.

### IOFED (Institutional Order Flow Entry Drill)

The first FVG left by a displacement move. If price returns to the gap but **does not close below the CE** (50% / consequent encroachment), this is the IOFED — the highest-probability entry.

### BAG (Breakaway Gap)

If price does not return to the first FVG at all, the gap is classified as a breakaway gap. Market structure fractality (Vol 3) provides the framework for identifying when an FVG will be a BAG.

## Premium and Discount

After any expansion leg, split the range (swing low → swing high) at 50%:
- **Discount** (≤ 0.5): below the 50% — preferred entry zone for longs
- **Premium** (> 0.5): above the 50% — preferred entry zone for shorts

Valid PDA arrays (FVGs, order blocks) should be **at or below** the 50% when looking for longs, and at or above the 50% for shorts.

## Equal Highs / Equal Lows

Two equal highs or two equal lows represent **engineered liquidity** — the algorithm creates these specifically to collect stops from traders who see "support" or "resistance." Equal lows form a rejection block (RB) because after the sweep, price reacts and reverses.

## Liquidity Void

A liquidity void is a price range where **no delivery has occurred on either side** — price moved through the range entirely in one direction with no back-and-forth candle bodies inside it.

Distinct from an FVG: an FVG is a three-candle imbalance pattern; a liquidity void is a larger empty zone with zero trading in either direction.

- The algorithm is "in a hurry" to reprice toward a void — treats it as a magnet
- Do NOT fade price delivering into a liquidity void; do not short against one
- The void is only "done" (disregarded) when daily candles have closed both above AND below it on different days — confirming both buy-side and sell-side delivery has occurred inside the range
- Keep the void marked for at least one full trading week (5 days) before removing it
- Back-and-forth delivery many times inside the range = the algorithm efficiently rebalancing the void

**Contrast with BAG (Breakaway Gap):** A BAG is a FVG the market leaves unfilled during LRLR conditions; it may eventually fill. A liquidity void will always be rebalanced — it is not a BAG.

Source: `sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md`

## Liquidity vs. Inefficiency: Key Difference

| Property | Liquidity | Inefficiency |
|---|---|---|
| Always present? | Yes — always there | No — requires displacement |
| What creates it | Swing highs/lows | Displacement / expansion |
| Role in price delivery | Target (DOL) | Entry mechanism |
| Timeframes to look | 1H, 15M | 5M, 1M (for entries) |

## Application to Trade Setup

1. Identify HTF DOL on 1H / 15M (swing high = BSL, swing low = SSL)
2. Determine which side price is currently delivering toward
3. Wait for displacement in the direction of the DOL — this creates a FVG
4. Enter on a FVG (BISI for longs, SIBI for shorts) on the 5M–1M
5. Stop loss below candle #1 of the FVG (or below the swing that created it)
6. Target: the DOL (swing high or swing low on 1H/15M)

## See Also

- [[ict-market-structure]] — structure determines which liquidity side is targeted
- [[ict-narratives]] — Power of Three and daily bias context for the DOL
- [[ict-entry-models]] — FVG, order block, OTE entry mechanics
- [[ict-smt]] — intermarket divergence confirming liquidity-driven moves
- [[ict-deviations]] — measuring how far beyond a liquidity level price will run
- [[ict-live-commentary]] — live HOD/LOD calling using these liquidity concepts; liquidity void in practice
