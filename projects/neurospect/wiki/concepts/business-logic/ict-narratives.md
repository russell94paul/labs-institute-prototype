---
tags: [concept, business-logic, ict, narratives, algorithmic-price-delivery, power-of-three, sessions, daily-bias, neurospect]
aliases: [ICT Narratives, Algorithmic Price Delivery, APD, Power of Three, AMD, Daily Bias, Kill Zones, Session Opens]
sources:
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class2-notes.md
  - sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md
  - sources/neurospect/2026-04-18-vol1-class3-notes.md
  - sources/neurospect/2026-04-18-vol1-class4-notes.md
  - sources/neurospect/2026-04-18-vol2-class1-power-of-three.md
  - sources/neurospect/2026-04-18-vol2-class1-notes.md
  - sources/neurospect/2026-04-18-vol2-class2-notes.md
  - sources/neurospect/2026-04-18-vol2-class4-daily-bias-practice.md
  - sources/neurospect/2026-04-18-vol2-class4-notes.md
  - sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md
  - sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md
created: 2026-04-18
updated: 2026-04-22
---

# ICT Narratives: Algorithmic Price Delivery & Daily Bias

A "narrative" is the contextual understanding of what the market is doing and why — combining higher-timeframe structure, the current draw on liquidity, session timing, and algorithmic delivery stages. Getting the narrative right is as important as the entry model.

## The Four Stages of Algorithmic Price Delivery

Every price run follows four sequential stages. The only exception is manual intervention (rare).

### 1. Consolidation (Origin / 1st Stage)

Consolidation is the **origin of every price run**. It is NOT a neutral/random phase — it is actively engineering liquidity on both sides of the range.

- Bodies of candles define the consolidation range (not wicks)
- Above the range: buy-side liquidity (BSL)
- Below the range: sell-side liquidity (SSL)
- The **50% / equilibrium** of the range is the most important level
- Normal timing: Asia session (overnight), pre-market

**Consolidation Model Entry:**
1. Find a consolidation on 1M–5M
2. Wait for an intra-range liquidity sweep (equal lows swept / swing low taken)
3. Wait for price to return to the EQ (50%)
4. Enter on a PDA below the EQ — FVG, order block, rejection block, or volume imbalance
5. Target: the opposite side of the range, then previous day high/low

> "Consolidation → always followed by expansion." — Vol 1 Class 2

### 2. Expansion (2nd Stage)

Expansion is when price **moves rapidly away from equilibrium**. It reveals market maker intent and bias direction.

- Begins at the 50% of the consolidation range
- Creates a fair value gap on the way to the target
- Entry: at the FVG below 50% of the expansion (discount zone)

**How to measure:**
- Draw a Fibonacci/box from the swing low (start of expansion) to the swing high (end of expansion)
- Everything below 50% = discount; above 50% = premium
- Valid PDA entries are **at or below** the 50% for longs

### 3. Retracement (3rd Stage)

A real retracement has **two jobs**. Both must be completed for the retracement to be valid and for the next expansion to begin:

1. **Fill the inefficiency** (FVG or order block from the expansion)
2. **Reach discount** (at or below 50% of the expansion)

| Real Retracement | Fake Retracement |
|---|---|
| Delivers to FVG AND reaches discount | Delivers to FVG but NOT discount |
| Activates buy program → next expansion | Engineered sell-side liquidity → price may continue retracing |

**Healthy vs. choppy retracement:**
- Healthy: steady series of lower highs into discount → strong continuation
- Choppy: messy return → slower, choppier delivery

### 4. Reversal (4th Stage)

A true reversal requires taking out the **origin swing** where the trend began. See [[ict-market-structure]] for the three reversal types (failure swing, raid on stops, accumulation of shorts/longs).

---

## Power of Three (AMD): Accumulation — Manipulation — Distribution

Power of Three is a **narrative framework**, not a picture-perfect pattern. It describes how the daily candle (and each session) delivers.

### Daily Candle Structure

Every daily candle (and session candle) has three phases relative to its **opening price**:

| Phase | What Happens | Who's Doing It |
|---|---|---|
| **Accumulation** | Price moves below the opening price | Smart money buys from retail sellers |
| **Manipulation** | Price breaks below the open, trapping retail shorts | Retail sees "weakness" and sells; SM accumulates |
| **Distribution** | Price rallies above the open and beyond | SM sells to retail breakout buyers |

The **opening price** is the daily anchor. The low of the daily candle (the wick below open) is the manipulation leg.

### Intraday Application

The AMD cycle repeats **four times per day** — once at each session open. On a bullish day:
- Look for longs **below** opening prices
- On a bearish day: look for shorts **above** opening prices

---

## Opening Prices (Session Killzone Anchors)

These are the key opening prices to mark on every chart:

| Open | Time (Eastern) | Notes |
|---|---|---|
| Midnight Open | 00:00 | Daily anchor; most important for full-day bias |
| 8:30 Open | 08:30 | CME futures open; often creates/targets one session side |
| 9:30 Open | 09:30 | RTH open; may continue or manipulate 8:30 move |
| 1:30 PM Open | 13:30 | PM session; frequently sets final high/low of day |

**Rule:** If bullish → look for longs below these opens. If bearish → look for shorts above these opens.  
**Best longs:** below all three AM opens (midnight, 8:30, 9:30) simultaneously.  
**Best shorts:** above all three AM opens simultaneously.

---

## Session Killzones

One of the four killzones typically sets the **high or low of the day**.

| Session | Time (Eastern) | Notes |
|---|---|---|
| Asia | ~8:00 PM – 12:00 AM | Often consolidation; use session open as anchor |
| London | 2:00 AM – 5:00 AM | Takes one side of Asia and delivers to the other; 2022 model common |
| NY AM | 8:30 AM – 11:30 AM | 8:30 sets a side; 9:30 may continue or manipulate it |
| Lunch | ~11:30 AM – 1:30 PM | Lower energy; transition into PM |
| NY PM | 1:30 PM – 4:00 PM | 1:30 open is the anchor; frequently sets final high/low |

The **London model**: London takes the Asia low, delivers to the Asia high (or vice versa). Occurs 1–3 times per week. Simple and highly profitable once recognized.

---

## Daily Bias (Vol 2 Class 4)

Daily bias is the trader's assessment of whether the next trading day will be bullish or bearish, with ~80% assurance. Two steps:

### Step 1: Find the HTF Inefficiency

- Look for the cleanest FVG on 1H → 4H → Daily (higher TF if multiple overlaps)
- **As long as price remains inside a bullish FVG** → look for longs; inside a bearish FVG → look for shorts
- If no clean FVG: target nearest external liquidity instead
- The 4H timeframe is the most reliable for finding the "main" bias FVG
- Cycle: Liquidity → FVG → Liquidity → FVG (alternating)

### Step 2: Check Opening Price Position

- Align the HTF bias with intraday position:
  - Bullish day + price below midnight open = best long condition
  - Bearish day + price above midnight open = best short condition
- If price is below 8:30 AND 9:30 AND midnight open on a bullish day → highest probability

> "Bias = Liquidity → Inefficiency → Liquidity. Market is always going toward one of these — never both simultaneously." — Vol 2 Class 4 Notes

---

## Economic Calendar Framing

High-impact news weeks change the delivery character:

- **FOMC / CPI / NFP weeks**: expect high-resistance, back-and-forth price action until after the release
- Jackson Hole week: Thursday-like conditions throughout (slow, choppy, picky)
- **Small Opening Range Gap** (<50 handles on NQ): expect choppy, overlapping bodies — HRLR conditions
- **Large Opening Range Gap**: more trending, lower resistance delivery
- **Fed Chair Testifies (Powell):** avoid NY PM same day and next day; lunch session is best window; same-day AM is tradeable with caution
- **ISM / PMI / JOLTS at 10 AM:** wait for the 10 AM print; best entry conditions for the day often appear immediately after news
- **CPI week Monday (no news):** very low probability; market is engineering liquidity for Wednesday; watch only

Opening Range Gap (ORG): gap between previous RTH close (~4:00 PM) and today's 9:30 open.

## Weekly Opening Price

The weekly opening price (Sunday electronic open) is the directional "compass" for Tuesday and Wednesday.

**Rule (live stream + YouTube weekly review):**
- Below weekly opening price on **Tuesday or Wednesday** → high probability longs toward buy-side
- Above weekly opening price on **Tuesday or Wednesday** → high probability shorts toward sell-side

This holds in both trending AND range/choppy conditions. The further below (or above) the weekly OP at the start of Tuesday or Wednesday, the higher the probability.

**Maximum probability condition:** Price is simultaneously below the weekly OP, midnight OP, and 8:30 OP on Tuesday or Wednesday.

**Monday's role:**
- Monday does NOT set the trend — it engineers liquidity for Tuesday/Wednesday to consume
- If Monday delivers bullish → Tuesday will likely sweep Monday's sell-side before continuing higher or forming the high of the week
- If Monday delivers bearish (when you expected bullish) → "the paradigm has changed"; only buy-side targets remain for the week; Tuesday/Wednesday take Monday's sell-side lows and rally
- When the market does NOT take the sell-side liquidity pool on Monday (the one you were watching) → interpret this as confirmation that the whole week has shifted to buy-side delivery

Sources: `sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md`, `sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md`

## Manual Intervention

Rare but impactful. When manual intervention occurs, expect:
1. Forced move in one direction (unusual speed/magnitude)
2. Strong move in the **opposite direction** immediately after

The HOD/LOD is decided at the midnight open under normal (non-manual) conditions.

## See Also

- [[ict-market-structure]] — MSS and CSD that confirm narrative direction
- [[ict-liquidity]] — DOL and FVG targets that the narrative aims at
- [[ict-entry-models]] — entry models for each delivery stage (consolidation, E&R, reversal)
- [[ict-smt]] — SMT divergence confirming the manipulation leg of Power of Three
- [[ict-deviations]] — measuring targets beyond the obvious liquidity level
- [[ict-live-commentary]] — live application of these frameworks: day-of-week protocol, HOD/LOD calling, weekly opening price in practice
