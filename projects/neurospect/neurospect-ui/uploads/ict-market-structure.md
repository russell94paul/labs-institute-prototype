---
tags: [concept, business-logic, ict, market-structure, neurospect]
aliases: [ICT Market Structure, MSS, BOS, Market Structure Shift, CSD, STH, STL, ITH, ITL, LTH, LTL, Market Structure Fractality]
sources:
  - sources/neurospect/2026-04-18-vol3-class2-market-structure-fractality.md
  - sources/neurospect/2026-04-18-vol3-class4-market-structure-deviations.md
  - sources/neurospect/2026-04-18-vol3-class5-model-2022-ote-csd.md
  - sources/neurospect/2026-04-18-vol4-class1-htf-ltf-orderflow.md
  - sources/neurospect/2026-04-18-vol1-class4-notes.md
created: 2026-04-18
updated: 2026-04-20
---

# ICT Market Structure

Market structure is the framework for reading direction and identifying the precise points where price behavior changes. All entries and trade narratives are filtered through a multi-timeframe structure read. The same fractal patterns repeat from seconds charts to weekly charts.

## Short-Term, Intermediate-Term, and Long-Term Swings

Price creates three orders of swing highs and swing lows. Each level requires specific conditions to qualify:

| Label | Abbreviation | Qualification |
|---|---|---|
| Short-Term High/Low | STH / STL | Three-candle swing that does not fill a gap or create one |
| Intermediate-Term High/Low | ITH / ITL | The swing that fills OR creates a fair value gap on its price leg |
| Long-Term High/Low | LTH / LTL | Intermediate-term high/low taken out by a subsequent move |

**Key rule:** A STL is **suspect** — you cannot assume it will hold. Only once a STL has been violated and the resulting price leg fills or creates a gap does it become an ITL. The ITL is the price you must protect in your trade.

## Market Structure Fractality

Whatever pattern appears on the 1-minute chart also appears on the daily chart. The three-swing fractal (STH → ITH → LTH or STL → ITL → LTL) nests inside itself at every timeframe.

- FVGs inside a range invite liquidity into the gap → a swing high/low forms inside the gap
- That engineered swing creates a high-probability target: the algorithm will return to take that liquidity later
- The swing that fills a gap on a higher timeframe is the higher-timeframe ITH/ITL — use it for swing trades

> "As it's in big, it's going to be in small. Life is fractal." — Vol 3 Class 3

## Market Structure Shift (MSS)

A valid MSS occurs when:
1. An ITL (or ITH) is formed — price leg creates or fills a FVG
2. Price then **breaks above the high** (for bullish MSS) that initiated the ITL price leg lower

After a bullish MSS:
- Expect a retracement back into the expansion range
- Look for PDA arrays (OB, FVG) in the **discount** (below 50%) of the expansion
- Target: the buy-side liquidity that the ITL was reaching for

## Change in State of Delivery (CSD)

CSD is the **precursor** to a full MSS — it signals the direction has changed before structure confirms it.

- CSD identified by: a group of **down-close candles** (for bullish) or **up-close candles** (for bearish) whose **opening price gets breached** by price
- When price closes through the opening price of those candles, the state of delivery has changed
- A CSD is pre-MSS: you don't need a full market structure shift to use it as confluence
- Frequently used with the Model 2022 + OTE entry (see [[ict-entry-models]])

## Internal vs. External Structure

- **External liquidity**: highs/lows that are visible on the current timeframe as clear swing points
- **Internal liquidity**: smaller highs/lows created inside a larger price leg or range (sub-structure)

When the market takes **external AND internal liquidity** before the entry signal, that adds meaningful confluence. Internal liquidity sweeps signal the market is gathering energy for the next expansion.

## Break of Structure (BOS) vs. MSS

| BOS | MSS |
|---|---|
| Price closes above/below a swing point | Price closes above/below the high that started the opposing price leg |
| Continuation signal | Reversal signal |
| Lower timeframe — common | Higher timeframe — more significant |

## Multi-Timeframe Confluence

- Use 1H–4H–Daily for HTF bias (finding the main ITH/ITL)
- Use 15M–1M for entry structure (STH/STL, CSD)
- When the same swing level exists on multiple timeframes, probability is higher

## Reversal Types (Vol 1 Class 4)

Three ways a market trend reverses:

1. **Failure Swing (~10%)**: Market fails to reach the liquidity target. Turns at a rejection block or CE. Looks like a retracement but isn't (doesn't tap an OB/FVG at 50%). Take partials at rejection blocks — no one knows if it will fail or complete.

2. **Raid on Stops (~80%)**: Market runs the liquidity (sweeps highs/lows) then immediately rejects. Classic "get in, get out." Traps both shorts selling resistance and longs buying the breakout. Most common reversal pattern.

3. **Accumulation of Shorts/Longs (~10%)**: Smart money builds positions at extremes near liquidity. Retail interprets this as a consolidation (continuation), but it is accumulation at extremes (reversal). Difference: consolidation is within a range before a target; accumulation is at extremes, around liquidity.

**Best probability reversals**: layered liquidity pools (multiple highs/lows stacked).

## Application to Trade Setup

1. Identify the HTF bias using ITH/ITL on 1H–4H–Daily
2. Drop to 15M–1M to find a CSD or MSS in the direction of HTF bias
3. After the MSS, measure the expansion leg (swing low → swing high for bullish)
4. Find a PDA (FVG or OB) in the discount zone (below 50%) of the expansion
5. Enter there, stop below the ITL
6. Target: external HTF liquidity (BSL for longs, SSL for shorts)

## See Also

- [[ict-liquidity]] — liquidity targets that follow from structure
- [[ict-narratives]] — algorithmic price delivery stages that include structure concepts
- [[ict-entry-models]] — MSS and CSD as entry triggers (Model 2022 + OTE)
- [[ict-smt]] — intermarket confirmation of structural moves
- [[ict-deviations]] — measuring targets beyond the obvious liquidity level
