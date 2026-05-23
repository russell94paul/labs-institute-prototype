---
tags: [course, module-3, deviations, fibonacci, targets, hod-lod, neurospect]
aliases: [Deviations Lesson, Fibonacci Targeting, Module 3 Lesson 3]
sources:
  - sources/neurospect/2026-04-18-vol2-class3-measuring-manipulation-deviations.md
  - sources/neurospect/2026-04-18-vol2-class3-notes.md
created: 2026-04-22
updated: 2026-04-22
module: 3
lesson: 3
---

# Module 3, Lesson 3: Measuring Deviations (Fibonacci Targeting)

**Prerequisites:** [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]]  
**Reference:** [[concepts/business-logic/ict-deviations|ICT Deviations KB]]

---

## Concept

The high and low of every trading day are **engineered at the midnight open**. The algorithm's only job after that is delivering price efficiently to those levels. Fibonacci deviations allow you to measure exactly how far beyond an obvious liquidity level the market will travel — so you can exit at the real target instead of leaving money at the first swing.

> "The market already knows the high and low of the day from the midnight open. The algorithm's only job is to deliver price efficiently to those levels." — Vol 2 Class 3

This is not a tool for guessing. It is a measuring tool: once you know the manipulation leg (from Power of Three), you can quantify the delivery targets.

---

## Why Fibonacci?

The Fibonacci sequence is fractal — the same ratios that appear in plants, galaxies, and living organisms appear in price delivery. This is not coincidence; the market is an engineered system, and engineered systems obey mathematical laws.

> "As it's in big, it's going to be in small. Life is fractal." — Vol 2 Class 3

Practically speaking: whatever deviation level the market prints at on the weekly chart, the same ratio structure appears on the 5-minute chart. This is why Fibonacci works at all timeframes.

---

## Fibonacci Settings (Deviation Levels)

MrWitness's deviation settings are available in the Discord ("notes and resources" channel). Key levels to activate:

| Level | Label |
|---|---|
| 0 | Origin (midnight opening price) |
| -0.5 | First minor deviation |
| -1 | First major deviation beyond swing |
| -1.5 | Secondary target |
| -2 | **Ideal HOD/LOD zone (most common)** |
| -2.5 | **Ideal HOD/LOD zone (most common)** |
| -3, -4, -5, -7 | Extended targets (strong sessions) |

---

## How to Anchor the Deviations

**For a bullish day:**

1. Identify the **midnight opening price** — this is the origin (0)
2. Find the **last manipulation leg below the opening price** — the final swing low before the reversal
3. This swing low is where retail shorts are trapped; smart money is accumulating
4. From that swing low, find the **swing high that initiated the breakout lower** (the high that the manipulation broke through)
5. **Measure from the swing low → that swing high**, projecting deviations upward

**For a bearish day:** reverse — find the last manipulation high above the opening price; measure from swing high → swing low; project deviations downward.

**Timeframe for the swings:** Use 15M–1H candles for cleaner swing levels.

---

## What the Deviation Levels Mean

| Level | Use |
|---|---|
| -0.5 to -1 | First target beyond the obvious swing high/low; take partials here |
| -1.5 | Hold a partial runner toward this level |
| **-2 to -2.5** | **Ideal HOD/LOD zone** — most days end here |
| -3 to -4 | Extended target; use when inside an HTF draw on liquidity |
| -5 to -7 | Extreme extension; rare, but valid on high-momentum sessions |

**The key rule:** Do NOT exit at the obvious liquidity level (the swing high itself). Always aim for at least one deviation beyond it as your first partial exit.

---

## High-Probability Draw on Liquidity (HPDL)

When a **deviation level overlaps a higher-timeframe liquidity level** — a daily FVG, weekly swing high, or session extreme — this is the HPDL. It is the highest-priority exit target.

> "Deviations overlapping liquidity = High-Probability Draw on Liquidity (HPDL). Treat it as a priority draw." — Vol 2 Class 3 Notes

If the -2 to -2.5 zone aligns with a 4H or Daily FVG, that is the ideal final exit — hold your runner for that level.

---

## Worked Example 1: London LOD — Bullish Day (Vol 2 Class 3 Live)

**Setup:** Monday, bullish day; market was manipulating lower during London (2–5 AM). Opening price marked.

1. London session creates the final swing low below the midnight open
2. Swing low to swing high measured (the swing high that began the breakdown below open)
3. Deviation levels projected upward

**Targets achieved:**
- First swing high = first exit level → take partials here
- -1 deviation above the first swing high = +8 points extra (covers commissions and more)
- Second swing high (another level up) → -2 deviation above that swing = +11 points extra
- Once price surpassed -2/-2.5 → it ran to -4 deviation
- -4 deviation ran to -7 deviation → **high of the day**, printed ~3 ticks from the -7

> "By taking something off here, you can take something off at the -4, run toward the -7 which is the high of this day." — Vol 2 Class 3 Transcript

---

## Worked Example 2: PM Short — Bearish Day (Vol 2 Class 3 Live)

**Setup:** Manipulation occurred above the 8:00 AM opening price; then delivery turned lower.

1. Find the opening price for this day's manipulation leg (8 AM open in this example)
2. Swing high to swing low measured
3. Deviation levels projected downward

**First target:** First 15M swing low below the manipulation → take first partial at -0.5 to -1 deviation
**Running target:** -1.5 → secondary partial  
**LOD zone:** -2 to -2.5 deviation was printed as part of Asia (next session's beginning), confirming this as the turn

---

## Step-by-Step Application

1. **Identify** the midnight opening price (origin = 0)
2. **Find** the manipulation swing: the last swing low (bullish) or swing high (bearish) before the reversal, below (bullish) or above (bearish) the opening price
3. **Find** the swing high (bullish) or swing low (bearish) that initiated that manipulation leg
4. **Measure** from manipulation extreme → initiating swing, projecting deviations in the direction of delivery
5. **Mark** -0.5, -1, -1.5, -2, -2.5 on the chart
6. **Check** if any deviation level overlaps an HTF liquidity level → HPDL if so
7. **Execute:** partials at -1; runner toward -2/-2.5; hold if inside an HTF FVG boundary

---

## Manual Intervention Exception

The only exception to the "HOD/LOD is engineered at midnight" rule is **manual intervention**. When it occurs:
1. Price makes an unusual forced move in one direction
2. Price makes a strong move in the **opposite direction** immediately after

Deviations anchored from manual intervention moves are not reliable for the same day. Identify manual intervention first (unusual speed, unusual size, no kill zone context) before applying deviations.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Exiting at the obvious swing level | The -1 deviation adds 8–20 extra points; leaving the full position at the swing leaves money behind |
| Anchoring from the wrong swing | Must use the **last** manipulation leg, not any swing below the opening price |
| Expecting -7 every day | -2/-2.5 is the most common HOD/LOD zone; -4 to -7 happens in strong sessions |
| Ignoring HPDL alignment | When -2 aligns with a daily FVG, that is the maximum-confidence exit — don't close too early |
| Using intraday swings for anchoring | Use 15M–1H swings; 1M swings produce noisy deviation levels |

---

## Homework

Back-test deviations for 10 trading days (do not post to the homework channel — keep in your personal journal):

1. Mark the midnight opening price for each day
2. Identify the manipulation leg below the open (bullish) or above the open (bearish)
3. Anchor your deviation Fibonacci from the correct swings
4. Record where the HOD/LOD printed in relation to the deviation levels
5. Note any HPDL alignment (deviation + daily FVG)

> "Please remember to do your homework. Do back testing of this. Don't post in the homework channel. Just keep it for you in your own journals." — MrWitness, Vol 2 Class 3

---

## See Also

- [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]] — manipulation leg identification
- [[concepts/business-logic/ict-deviations|ICT Deviations KB]] — two-set deviation anchoring (ITL/STL method from Vol 3)
- [[concepts/business-logic/ict-narratives|ICT Narratives KB]] — daily bias and opening price context
- [[concepts/entry-models/model-2022-ote|Model 2022 + OTE Entry Model]] — OTE and deviation exits used together
