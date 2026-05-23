---
tags: [entry-model, consolidation, neurospect]
aliases: [Consolidation Model, Consolidation Range Entry, EQ Entry]
sources:
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class2-notes.md
  - sources/neurospect/2026-04-18-vol1-class1-notes.md
  - sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: Consolidation Model

The first and most fundamental entry model. Every price run starts with consolidation, and this model teaches you to recognize when the consolidation is ending and the expansion is beginning.

> "Consolidation is the origin of a price run. This is the first pillar, the first column, the base of the price action delivery." — MrWitness, Vol 1 Class 2

---

## What It Is

The market consolidates (ranges back and forth) to engineer liquidity on both sides. Above the range there is buy-side liquidity (BSL); below the range there is sell-side liquidity (SSL). The consolidation cannot expand until enough liquidity has been engineered on both sides.

The consolidation model captures the **beginning of the expansion** after the range has swept one side of its liquidity (intra-range sweep) and price returns to the EQ (50% of the range), giving you a PDA entry before the expansion to the opposite side.

---

## Setup Conditions

All conditions must be met. Check them in order — top to bottom.

### 1. Higher-Timeframe Context (4H / Daily)
- Price is inside a bullish or bearish HTF FVG **or** targeting the nearest external liquidity
- Opening price position is aligned: below the midnight open for longs, above for shorts
- This establishes *which direction* the consolidation will expand toward

### 2. Consolidation Range Identified (1M–5M)
- A range where candle **bodies** are encapsulated (wicks extend outside but bodies do not)
- The range has been active for enough time to engineer liquidity (typically Asia session overnight, or pre-market)
- BSL is above the range (swing highs / equal highs); SSL is below (swing lows / equal lows)
- The 50% (EQ) of the range is marked

### 3. Intra-Range Liquidity Sweep
- A swing low (for a bullish setup) or swing high (for a bearish setup) inside or at the edge of the range is swept
- This is the "manipulation" leg — price grabs the SSL (or BSL) before reversing
- The sweep must **reject off the low (or high) of the range** — a wick that goes below then immediately closes back above
- SMT divergence at this sweep = very high probability signal

### 4. Return to EQ
- After the sweep, price displaces back toward the 50% of the consolidation
- The displacement creates a FVG or leaves a PDA array below the EQ
- Price retraces back toward or into the EQ

### 5. PDA at or Below the EQ (for longs)
- The entry PDA must be **at or below the 50%** of the consolidation range
- Valid PDA types (in order of visual clarity):
  1. FVG (most common — the displacement after the sweep creates one)
  2. Inversion FVG (a prior bearish FVG that price closed above, now acting as support)
  3. Order block (down-close candle before the displacement higher)
  4. Rejection block (opening price of the sweep candle itself)
  5. Volume imbalance (treated like a FVG)
  6. Breaker block (invalidated OB that flipped to support)

### 6. Kill Zone Active
- Entry must occur inside an active kill zone
- Most common kill zone for this model: **London (2–5 AM Eastern)**
- Also valid: NY AM (8:30–11:30 AM), NY PM (1:30–4:00 PM)

---

## Step-by-Step Entry Process

**Step 1 — Higher Timeframe (15M or above):**
Find the main PDA of the consolidation — typically the EQ or the FVG left by the displacement. This is your anchor level.

**Step 2 — Lower Timeframe (15M or below):**
Find supporting confluences below the EQ — the FVG, OB, or rejection block that reinforces the HTF idea.

**Step 3 — Entry Timeframe (1M or 15s):**
Wait for a change of structure (COS) or confirmation. On a 1M chart, this means: price forms a swing low → displaces higher → closes above the swing high that began the last down leg. That is your green light to enter at the PDA.

**Entry:** At or into the PDA (FVG lower portion, or OB 50%) **while the PDA is at or below the consolidation EQ**.

---

## Stop Loss Logic

- **Standard:** Below the three candles that form the FVG (below Candle 1 of the FVG)
- **OB entry:** Below the body low of the order block (not the wick)
- **Rejection block entry:** Below the opening price of the sweep candle
- **Tightest (AXL sniper):** Stop below the candle that creates the COS on the 1M (the three-candle FVG on the entry timeframe)

> From AXL's Class 1 example: "This trade was 11 ticks stop loss. 1 risk, 36 reward."

---

## Target Logic

**Conservative (first partial):**
- The low end of the consolidation range (the SSL that was swept)
- Note: this is a quick target — you're targeting the opposite side of the range

**Standard:**
- The opposite side of the full consolidation range
- For a bullish setup: the BSL above the range (equal highs / swing high above)

**Best-case:**
- Previous day high/low (the algorithm frequently returns to PDH/PDL)
- The -1 to -2.5 Fibonacci deviation beyond the BSL swing high (see [[concepts/business-logic/ict-deviations]])

> "The algorithm will refer back to previous day highs and previous day lows. If you see a model which can allow you some space to target previous day lows or previous day highs from the consolidation — that is a very good target." — MrWitness, Vol 1 Class 2

> "The best case scenario is never necessary for you to make money." — MrWitness, Vol 1 Class 2

---

## Timeframe Summary

| Purpose | Timeframe |
|---------|-----------|
| HTF bias and FVG | 4H, Daily |
| Opening price anchor | Daily, 1H |
| Consolidation range | 1M–5M |
| PDA confluence | 15M–5M |
| Entry (COS / confirmation) | 1M, 15s, 5s |
| Stop / target precision | 1M |

---

## Worked Example (from Class 2 — Live NQ)

MrWitness walked through the following trade during Vol 1, Class 2:

**Context:**
- FOMC week: high-resistance, back-and-forth price action expected until Wednesday 2:30 PM
- Opening range gap: ~41 handles (< 50 → HRLR conditions)
- Wednesday's highs were "pending business" from the prior week — a known BSL target

**Consolidation:**
- Asia session (Sunday overnight to Monday pre-market)
- Consolidation range formed on 1M chart with bodies encapsulated
- SSL: Asia lows (equal lows at the bottom of the range)
- BSL: Asia highs / Wednesday's highs from the prior week

**Sweep and SMT:**
- London session (2–5 AM): took the Asia lows (swept the SSL)
- At that same level: ES made a lower low; NQ **did not** → SMT divergence (bullish signal)
- The non-confirmation by NQ signaled accumulation at the lows

**PDA and Entry:**
- Post-sweep displacement created an inversion FVG just above the consolidation EQ
- A prior bearish FVG was closed above → became a bullish inversion FVG
- Price accumulated at this inversion FVG / consolidation EQ three times
- Entry: approximately 4:14 AM, at the inversion FVG, below the EQ
- PDA: inversion FVG + order block respecting the EQ

**Result:**
- Price expanded to previous day high (PDH) → then to Wednesday's highs (pending business)
- MrWitness closed partial at PDH, second contract at Wednesday's highs

Source: `sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md`

---

## Common Mistakes

| Mistake | Correction |
|---------|-----------|
| Using wick extremes to define the range | Use **body** extremes only for the consolidation range |
| Entering above the EQ | The PDA must be **at or below** the 50%. Premium entries are low probability |
| Entering before the intra-range sweep | Wait for the sweep. Without it, the SSL (or BSL) is still outstanding — price may still go there |
| Entering without a kill zone | Outside kill zones, the model's probability drops significantly |
| Targeting the best case only | Always have a conservative target (opposite side of range). Don't require PDH to make the trade worthwhile |
| Consolidating on Sundays | MrWitness: "You should not be trying this on a Sunday. There's no algorithmic principle on Sunday." |

---

## Related Models

- [[concepts/entry-models/expansion-retracement-model]] — what happens after the consolidation expands
- [[concepts/entry-models/london-model]] — the London-takes-Asia-side variant of this model
- [[concepts/entry-models/smt-confirmation-entry]] — SMT divergence at the sweep as an additional signal

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: consolidation-model
name: Consolidation Model
description: >
  Enter at a PDA at or below the 50% (EQ) of a consolidation range, after
  intra-range liquidity has been swept and price has returned toward the EQ.
  Target: opposite side of the range, then previous day high/low.

conditions:
  - HTF FVG (4H/Daily) bias confirmed in direction of intended trade
  - Opening price position aligned (below midnight/8:30 open for longs; above for shorts)
  - Consolidation range identified on 1M–5M (bodies define range, not wicks)
  - Intra-range liquidity sweep completed (swing low swept for bullish; swing high swept for bearish)
  - Price has returned toward the 50% (EQ) of the consolidation
  - PDA present at or below the EQ (FVG, OB, inversion FVG, rejection block, or volume imbalance)
  - Kill zone active (London preferred; NY AM and NY PM also valid)

checklist:
  - "[ ] HTF FVG (4H or Daily) confirmed — price inside bullish FVG for longs"
  - "[ ] Opening price position correct — below midnight open and/or 8:30 open for longs"
  - "[ ] Consolidation range bodies defined (not wicks) — high and low marked"
  - "[ ] EQ (50%) of consolidation identified"
  - "[ ] Intra-range liquidity swept (SSL taken for bullish setup)"
  - "[ ] Sweep rejected — price did not close below the range low (rejection at the sweep)"
  - "[ ] Displacement after sweep created an FVG or identifiable PDA"
  - "[ ] PDA is at or below the EQ"
  - "[ ] Kill zone active at time of entry"
  - "[ ] 1M (or 15s) COS or confirmation present before entry"
  - "[ ] SMT divergence at sweep (optional but adds significant confluence)"

timeframes:
  bias: [Daily, 4H, 1H]
  range_identification: [5M, 1M]
  pda_confluence: [15M, 5M]
  entry: [1M, 15s, 5s]

stop_logic: >
  Below the PDA used for entry:
  - FVG entry: below Candle 1 of the FVG (below the three candles that form the gap)
  - OB entry: below the body low of the order block
  - Rejection block: below the opening price of the sweep candle

target_logic: >
  Target 1 (conservative): opposite side of the consolidation range
  Target 2 (standard): BSL above the range (equal highs / swing high)
  Target 3 (best case): previous day high/low
  Target 4 (extended): -1 to -2.5 Fibonacci deviation beyond the first liquidity sweep

kill_zones:
  primary: London (02:00–05:00 Eastern)
  secondary: [NY AM (08:30–11:30 Eastern), NY PM (13:30–16:00 Eastern)]

avoid_conditions:
  - Sunday consolidation ranges (no algorithmic delivery principle)
  - FOMC/NFP/CPI week before the news release (HRLR; use only for experienced traders)
  - Opening range gap < 50 handles NQ (HRLR — wider stops required)
  - Entry above the EQ (premium zone — low probability for longs)

smt_signal: >
  Optional but high-confidence add: At the intra-range SSL sweep, if ES fails to
  make the same lower low as NQ (or vice versa) — that is bullish SMT divergence.
  Treat this as the highest-probability version of the consolidation model.
```
