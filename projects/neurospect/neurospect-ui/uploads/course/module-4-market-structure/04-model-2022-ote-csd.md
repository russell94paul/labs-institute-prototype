---
tags: [course, module-4, model-2022, ote, csd, market-structure, neurospect]
aliases: [Model 2022 Course Lesson, OTE Lesson, CSD Lesson, Module 4 Lesson 4]
sources:
  - sources/neurospect/2026-04-18-vol3-class5-model-2022-ote-csd.md
created: 2026-04-22
updated: 2026-04-22
module: 4
lesson: 4
---

# Module 4, Lesson 4: Model 2022 + OTE + CSD

**Prerequisites:** [[concepts/course/module-4-market-structure/01-swing-classification|Lesson 1 — Swing Classification]], [[concepts/course/module-2-price-delivery/03-expansion-retracement|Module 2, Lesson 3 — Expansion & Retracement]]  
**Entry Model:** [[concepts/entry-models/model-2022-ote|Model 2022 + OTE Entry Model]] — full checklist and YAML  
**Reference:** [[concepts/business-logic/ict-entry-models|ICT Entry Models KB]], [[concepts/business-logic/ict-market-structure|ICT Market Structure KB]]

---

## Concept

Module 2's expansion-retracement model has one entry condition: price retraces to the 50% discount zone (or below) of the expansion leg, where a FVG or OB is present. But the market does not always offer a 50% retracement. In **high-resistance conditions**, price retraces all the way to the 62–79% Fibonacci zone before continuing. This deeper retracement is called the **Optimal Trade Entry (OTE)**, and the setup that predicts it is called **Model 2022**.

> "Whenever you just break through this high [the MSS level] and come all the way back lower, you use expansion retracement. But what precisely am I looking at inside of expansion retracement? This golden pocket right here — the Optimal Trade Entry." — MrWitness, Vol 3 Class 5

Understanding when to use OTE instead of the standard 50% entry is the key skill this lesson teaches. The signal is the market's own failure to reach 50% — when the expansion leg stops short of giving you the E&R entry, it is telling you Model 2022 conditions are in effect.

---

## The OTE Zone: 62–79% Fibonacci

The OTE zone is the "golden pocket" — the 62% to 79% Fibonacci retracement of the expansion leg. Within this zone:

- **62% level:** First point of the zone; price sometimes turns here
- **0.705 (70.5%):** The midpoint between 62 and 79; the most precise level
- **79% level:** Deepest point; price sometimes reaches here, especially in HRLR

The 0.705 is the target level for stop entry. The **OTE block** (the order block at or near the 0.705) is what you enter at.

This has many retail names ("golden pocket," "golden zone") but the precision comes from combining the Fibonacci level with the order block at that level — what MrWitness calls the "OTE block."

---

## When to Expect Model 2022 (vs. Standard E&R)

| Condition | Entry Model |
|---|---|
| After MSS, price retraces to 50% discount + PDA present | Standard expansion-retracement |
| After MSS, price does NOT reach 50% discount before reversing | **Model 2022 — expect OTE (62–79%)** |
| HRLR conditions (small ORG, overlapping bodies, news week) | **Model 2022 — OTE rather than 50%** |
| High-resistance run after a weaker-than-expected sweep | Model 2022 |

The diagnostic: if price had a clean MSS and you were looking for a 50% retracement entry but price only bounced to 30% and then dropped again — Model 2022 is in effect. Price will come back to the OTE zone.

---

## Identifying the OTE Block

The OTE block is the order block in the 62–79% zone. Selecting the correct one is the most critical skill:

**Rule 1: Highest body open wins.**  
Find all down-close candles in the OTE zone. The OTE block is the one with the **highest body open price** — not the last one, not the largest one, the one with the highest opening price.

> "We are looking at the candle with the highest down-close, with the highest body for the down-close candle." — Vol 3 Class 5

**Rule 2: Prefer the propulsion block.**  
If two down-close candles exist in the zone and the second one **trades into the body of the first** (overlaps), the second one is the **propulsion block**. The propulsion block has more institutional force.

> "The order block that trades to the previous order block is called the propulsion block. And this candle — the job of this candle is to propel price higher." — Vol 3 Class 5

**Rule 3: Prefer OB in concert with 0.705.**  
The ideal OTE block has its body at or very near the 0.705 level. When the order block and the Fibonacci level are at the same price → highest precision entry.

**Entry:** 50% of the OTE block's body  
**Stop:** Below the OTE block's closing price (the body low; a true OB's closing price should not be touched after entry)

---

## Change in State of Delivery (CSD)

CSD is a pre-MSS signal. You don't need to wait for a full MSS to confirm direction — CSD tells you the move has already started.

**How to identify CSD:**
1. Price is in discount (below 50% of the dealing range, or below the opening price)
2. A group of **down-close candles** exists in that discount
3. Price **closes through the opening price** of those down-close candles

That breach = CSD. The state of delivery has changed. Longs are valid.

> "As soon as this opening price gets breached, now the market structure has changed higher. This opening price is enough. Now you're going to keep looking for higher prices." — Vol 3 Class 5

**CSD vs. MSS timing:**
- CSD fires first — entering on CSD gets you earlier at better price
- MSS fires after — the MSS then becomes your post-entry confirmation
- Both together = maximum confidence

**In live trading:** When MrWitness says "I want to see price trade above this opening price," he is looking for the CSD — the breach of the down-close candles' opening price in discount, before the full MSS.

---

## Full Sequence (Model 2022 + OTE + CSD)

```
1. HTF FVG bias confirmed (bullish 4H FVG)
2. Opening price position correct (below midnight open)
3. Price creates an ITL (price leg creates/fills a FVG)
4. MSS fires: price breaks above the initiating high
5. DIAGNOSTIC: Does price retrace to 50%? 
   → YES → Use standard E&R entry
   → NO → Model 2022 active; wait for OTE zone
6. In the OTE zone: identify down-close candles
7. Look for CSD: down-close candles' opening price gets breached → enter
   (Optional: wait for full OTE block tap if CSD is not clear enough)
8. Enter at 50% of OTE/propulsion block
9. Stop: below OTE block closing price
10. Target: first deviation above initiating high → runner to -2/-2.5 convergence zone
```

---

## Worked Example: Vol 3 Class 5 Live Trade

**Session:** NY AM, bullish day

**Structure reading:**
- Pre-market sweeps the sell-side → creates the ITL
- ITL price leg fills a bullish FVG → confirmed ITL
- Price expands higher (MSS fires)
- Price pulls back but does NOT reach 50% discount → Model 2022 confirmed

**OTE setup:**
- Measure expansion leg: ITL → swing high
- 62–79% zone lands in the prior IOFED area (a pre-existing FVG that was never fully filled)
- In that zone: two down-close candles; the second trades into the first → propulsion block
- Propulsion block is in concert with 0.705

**CSD:**
- The two down-close candles in discount are the CSD candidates
- Price breaches their opening prices → CSD confirmed
- Enter at 50% of the propulsion block

**Stop:** Below the propulsion block's closing price (6 handles risk)  
**Target:** -2 deviation of the dealing range = high of the day

**Confirmation after entry:** MSS fires as price closes above the initiating high.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Using E&R entry when price doesn't reach 50% | 50% entry won't fill; waiting leaves you in confusion as price runs away |
| Choosing the last OB in the OTE zone instead of highest open | The last candle often does not have the highest authority level |
| Entering at the 62% expecting price to run immediately | Sometimes price dips to 79% first; the propulsion block may be at 79% |
| Setting stop below the swing low instead of below OTE block | Massively oversized risk relative to the precision of the OTE block stop |
| Using OTE/CSD without HTF FVG bias | CSD is a confirmation signal, not a standalone trigger |

---

## See Also

- [[concepts/entry-models/model-2022-ote|Model 2022 + OTE Entry Model]] — full checklist, YAML machine-readable block
- [[concepts/course/module-2-price-delivery/03-expansion-retracement|Module 2, Lesson 3 — Expansion & Retracement]] — the standard 50% entry that Model 2022 replaces in HRLR conditions
- [[concepts/course/module-4-market-structure/03-structure-deviations|Lesson 3 — Structure Deviations]] — deviation targets for OTE trade exits
- [[concepts/business-logic/ict-entry-models|ICT Entry Models KB]] — OTE block, propulsion block, CSD reference
- [[concepts/business-logic/ict-market-structure|ICT Market Structure KB]] — MSS and CSD definitions
