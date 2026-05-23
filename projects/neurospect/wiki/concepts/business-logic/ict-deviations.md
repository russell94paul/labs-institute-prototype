---
tags: [concept, business-logic, ict, deviations, fibonacci, targets, neurospect]
aliases: [ICT Deviations, Fibonacci Deviations, HOD LOD Targeting, HPDL, High Probability Draw on Liquidity, Deviation Levels]
sources:
  - sources/neurospect/2026-04-18-vol2-class3-measuring-manipulation-deviations.md
  - sources/neurospect/2026-04-18-vol2-class3-notes.md
  - sources/neurospect/2026-04-18-vol3-class4-market-structure-deviations.md
created: 2026-04-18
updated: 2026-04-20
---

# ICT Deviations (Fibonacci Targeting)

Fibonacci deviations are used to **measure how far beyond a liquidity level** price will travel. The Fibonacci sequence is fractal — the same ratios that appear in nature appear in price delivery. Deviations allow you to set precise exit targets rather than closing at the obvious liquidity level and leaving money on the table.

> "The market already knows the high and low of the day from the midnight open. The algorithm's only job is to deliver price efficiently to those levels." — Vol 2 Class 3

---

## Core Concept

When price reaches a swing high or swing low (liquidity target), the **first deviation beyond that level** is often the real target — not the swing itself. The market frequently stops at -2 to -2.5 deviations for the HOD/LOD.

---

## Fibonacci Settings

MrWitness's deviation settings are available in the Discord under "notes and resources." Key levels to activate:
- 0 (origin / midnight open)
- -0.5
- -1
- -1.5
- -2
- -2.5
- -3, -4, -5, -7 (for extended moves)

---

## Anchoring the Deviations (Power of Three Context — Vol 2 Class 3)

**For a bullish day:**
1. Identify the midnight opening price (origin = 0)
2. Find the **last manipulation leg** before the reversal — the final swing low that breaks below the open, trapping retail shorts
3. Measure from that **swing low → swing high** (the high that initiated the breakout lower)
4. Project deviations upward from the swing high

**Timeframe for the swings:** 15M–1H for cleaner levels.

**Targets:**
- First deviation beyond the first liquidity level (swing high) = first partial take or hold level
- **-2 / -2.5 deviation**: ideal HOD/LOD zone, especially if it aligns with an HTF draw on liquidity

---

## High Probability Draw on Liquidity (HPDL)

When a **deviation level overlaps** a higher-timeframe liquidity level (daily FVG, weekly swing high, session high), this becomes the highest-probability target in the session.

> "Deviations overlapping liquidity = High-Probability Draw on Liquidity (HPDL). Treat it as a priority draw." — Vol 2 Class 3 Notes

---

## Market Structure Deviations (Vol 3 Class 4)

More advanced anchoring using **two sets of deviations** for precise intraday HOD/LOD identification:

### Set 1: Intermediate-Term Low Price Leg
- Anchor: from the **ITL** (intermediate-term low) to the swing high of the ITL's price leg (the "manipulation move" that created the ITL)
- This measures the dealing range
- First deviation beyond the first target swing: first exit zone

### Set 2: Short-Term Low Price Leg (Measuring Swing)
- Anchor: from the **STL to the right of the ITL** (the retracement leg back into the expansion) to the high
- This "measuring swing" provides the secondary set of deviation levels
- When both sets converge at similar levels → that zone is the HOD/LOD

**Convergence rule:** When Set 1 and Set 2 deviations print at similar levels (-2, -2.5, -3, -4, -5), that area is where price will reverse. The midpoint of two converging levels is the precise HOD/LOD.

---

## Practical Targets

| Deviation Level | Interpretation |
|---|---|
| -0.5 to -1 | First target beyond swing; good for partials |
| -1.5 | Secondary target; hold runner here |
| **-2 to -2.5** | **Ideal HOD/LOD zone** (most common daily extreme) |
| -3 to -4 | Extended target; use when inside HTF liquidity level |
| -5 to -7 | Extreme extension; rare but valid during strong sessions |

**Rule:** Do NOT exit at the obvious liquidity level. Always aim for **one deviation beyond** as your exit. On a bullish day: one deviation above the swing high is where you take the first partial.

---

## Timing Notes

- For a bullish day: HOD/LOD (the LOD in this case) is usually printed during the **London session** (2–5 AM) or the NY AM session
- For a bearish day: HOD is usually printed during London or NY AM
- The -2/-2.5 zone near the daily FVG (if present) = maximum confidence exit

---

## Application

1. Identify midnight open as origin (0)
2. Find the manipulation swing (last leg below open for bullish, last leg above for bearish)
3. Measure deviations from that swing
4. Mark -0.5, -1, -2, -2.5 levels
5. Check if any overlap with HTF liquidity → HPDL
6. Take partials at first deviation; run toward -2/-2.5 if inside HTF liquidity

---

## See Also

- [[ict-liquidity]] — liquidity levels that become deviation anchors
- [[ict-narratives]] — manipulation leg of Power of Three is the anchor for deviations
- [[ict-market-structure]] — ITL / STL identification for two-set deviation anchoring
- [[ict-entry-models]] — OTE deviations (-2 to -2.5 for OTE exits)
- [[ict-order-flow]] — daily range quadrant analysis complements deviation targeting
