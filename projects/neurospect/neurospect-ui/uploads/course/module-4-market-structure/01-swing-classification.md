---
tags: [course, module-4, market-structure, swing-classification, itl, ith, fractality, neurospect]
aliases: [Swing Classification Lesson, STH ITH LTH, Module 4 Lesson 1]
sources:
  - sources/neurospect/2026-04-18-vol3-class2-market-structure-fractality.md
  - sources/neurospect/2026-04-18-vol3-class4-market-structure-deviations.md
created: 2026-04-22
updated: 2026-04-22
module: 4
lesson: 1
---

# Module 4, Lesson 1: Swing Classification (STH/ITH/LTH)

**Prerequisites:** [[concepts/course/module-2-price-delivery/01-four-stages-apd|Module 2, Lesson 1 — Four Stages of APD]], [[concepts/course/module-1-foundations/01-what-moves-the-market|Module 1, Lesson 1 — What Moves the Market]]  
**Reference:** [[concepts/business-logic/ict-market-structure|ICT Market Structure KB]]

---

## Concept

Not every swing high or swing low is equal. Three orders of swings exist, each with different probability of holding and different roles in your analysis. Misclassifying a short-term high as intermediate-term is one of the most common ways traders take premature entries and get stopped through.

The classification is objective: it is determined by whether the price leg creating the swing **fills a gap** or **creates a gap**. No subjectivity required.

---

## The Three Swing Types

| Label | Abbreviation | Classification Rule |
|---|---|---|
| **Short-Term High/Low** | STH / STL | Three-candle swing; the price leg that creates it does NOT fill a gap and does NOT create one |
| **Intermediate-Term High/Low** | ITH / ITL | The price leg that creates or fills a fair value gap |
| **Long-Term High/Low** | LTH / LTL | An intermediate-term high/low that gets subsequently taken out by a new price leg |

**The key rule:** An ITH or ITL is identified by its **price leg** — the move from the previous swing to the new swing. If that price leg creates a FVG (leaves an imbalance) OR fills a pre-existing FVG on its way, the resulting swing is intermediate-term.

---

## Why STLs Are "Suspect"

A short-term low has NOT proved itself. By definition, its price leg showed no gap creation or gap fill — which means there is no structural evidence that it will hold.

> "You can have a high probability intermediate term low that is not going to be broken through... once it fills a gap or creates a gap, that is the one you want to protect." — Vol 3 Class 5

Practical implication: **Never stop a long position below a STL.** Stop below the ITL — the one that created or filled a gap. The ITL has earned protection; the STL has not.

The market confirms a STL is also an ITL when the price leg **after** the STL creates a gap on the way up (or down). Once that gap is created, you know the low is intermediate-term and will likely hold.

---

## How Price Legs Qualify Swings

**For a bullish ITL:**
1. Price comes down in a sustained price leg
2. That price leg **creates a fair value gap** (displacement) or **fills a pre-existing bullish FVG** completely
3. When the price leg does either, the resulting low = ITL (high probability, protected)

**For a bearish ITH:**
1. Price rallies in a sustained price leg
2. That price leg creates a bearish FVG (displacement upward) or fills a pre-existing bearish FVG
3. The resulting high = ITH

**Becomes a long-term swing when:**
- A subsequent ITL takes out the prior ITL → prior ITL becomes LTL
- A subsequent ITH takes out the prior ITH → prior ITH becomes LTH

---

## Market Structure Shift (MSS)

A valid MSS occurs when:
1. An ITL forms (the price leg creates/fills a gap)
2. Price **breaks above the high** that initiated that ITL price leg downward

This break confirms the trend has shifted higher. After a bullish MSS:
- The ITL must not be broken (stop logic lives here)
- Expect a retracement into the expansion leg
- Look for a PDA (FVG, OB) in the discount zone (below 50%) of the expansion
- Target: the buy-side liquidity from the ITH side

**IMPORTANT:** The MSS requires breaking the **initiating high** — not just any nearby high. The initiating high is the high that price turned from before creating the ITL price leg.

---

## The Three-Swing Pattern in Practice

The market builds a bullish structure in a predictable fractal:

```
STL (suspect) → STL taken → ITL created (gap fills/creates)
   → STL to the right of ITL (fails to take out ITL)
      → MSS (price breaks initiating high)
         → Retracement to PDA in discount
            → Expansion toward target (ITH)
```

**What makes the STL to the right of ITL important:** This second STL is the "measuring swing" used in deviation anchoring (covered in [[concepts/course/module-4-market-structure/03-structure-deviations|Lesson 3]]). It is the pullback into the expansion range — the most important retracement candle for deviation measurement.

---

## Worked Example: Daily Chart ITL (Vol 3 Class 2)

MrWitness walks through a multi-day price structure on a 1H chart:

1. **First low forms:** three-candle STL — no gap, no fill; classified as suspect STL
2. **Price takes out the STL:** This creates an ITL — the price leg lower fills a bullish 1H FVG on its way down
3. **Another STL forms to the right:** price retraces; this STL fails to take out the ITL
4. **MSS fires:** price breaks above the high that started the ITL leg
5. **Entry:** at the bullish order block in the discount of the expansion (body only, 50% entry)
6. **Result:** 9.41% move from the ITL to the HTF target (prior day high / session high)

The key observation: "You have short-term low, intermediate-term low, short-term low. Once you put this intermediate expansion and close this swing low, you can enter on a trade and hold it toward these highs." — Vol 3 Class 2

---

## Fractal Application (Same Pattern at All Timeframes)

The STH/ITH/LTH pattern nests inside itself at every timeframe:
- The ITL on a 1M chart is the STL on the 15M chart
- The ITL on the 15M chart is the STL on the 1H chart
- The ITL on the Daily chart is the STL on the Weekly chart

This is why higher-timeframe context is always required before interpreting lower-timeframe structure. A 1M MSS that occurs inside a 4H bearish FVG is an AMD manipulation leg, not a trend reversal.

See [[concepts/course/module-4-market-structure/02-fractality|Lesson 2 — Fractality]] for the full fractal model.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Placing stop below a STL | STL is unproven; price will take it out and continue lower before the ITL holds |
| Calling a swing ITL just because it looks big | Classification requires a gap — not candle size, not look, not importance |
| Initiating a trade at the first STL without a gap | No structural confirmation that it holds; low probability |
| Treating every break of a recent high as an MSS | MSS requires breaking the specific **initiating high** that started the ITL price leg |

---

## Homework

1. Open any NQ or ES 15M chart for the past 5 trading days.
2. Mark every swing low (down candle + candle to the left and right that are higher).
3. Classify each: **STL** (no gap) or **ITL** (gap created or filled on the price leg).
4. Draw the pattern: STL → ITL → STL (to the right) → MSS for each complete structure.
5. Record in your journal: how many times did the STL to the right of the ITL hold? How many times was the ITL taken out (→ new ITL)?

---

## See Also

- [[concepts/course/module-4-market-structure/02-fractality|Lesson 2 — Fractality]] — the same pattern at every timeframe
- [[concepts/course/module-4-market-structure/03-structure-deviations|Lesson 3 — Structure Deviations]] — using ITL + STL to anchor deviation targets
- [[concepts/course/module-4-market-structure/04-model-2022-ote-csd|Lesson 4 — Model 2022 + OTE]] — MSS as the trigger for deep OTE retracement entries
- [[concepts/business-logic/ict-market-structure|ICT Market Structure KB]] — full reference including BOS vs. MSS, CSD, internal/external liquidity
