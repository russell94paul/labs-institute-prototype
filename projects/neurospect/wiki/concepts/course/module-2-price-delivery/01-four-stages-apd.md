---
tags: [course, module-2, apd, algorithmic-price-delivery, consolidation, expansion, retracement, reversal, neurospect]
aliases: [Four Stages APD, Algorithmic Price Delivery Lesson]
sources:
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class2-notes.md
  - sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md
  - sources/neurospect/2026-04-18-vol1-class3-notes.md
  - sources/neurospect/2026-04-18-vol1-class4-notes.md
created: 2026-04-22
updated: 2026-04-22
---

# Module 2, Lesson 1: The Four Stages of Algorithmic Price Delivery

> **Vol 1, Classes 2–4 — MrWitness**

In Module 1 you learned what price is targeting (liquidity) and where price enters from (inefficiency / FVG). This lesson answers the question of **how** price gets there — the four stages every price run follows, in order, every time.

> "The delivery of price is composed or formed by four stages. This is the only thing price is doing. The only thing the price will do. And the only thing you have to identify when we're trading." — MrWitness, Vol 1 Class 2

---

## The Four Stages

```
Consolidation → Expansion → Retracement → (back to Expansion OR Reversal)
```

These stages are **sequential and cyclical**. They are not random — the algorithm delivers price in this order always, with the only exception being manual intervention (rare).

### Two rules that reveal your stage read:

> "If you ever see a Retracement to a Reversal then it was not a Retracement." — Class 2 Notes

> "If you see a Consolidation to a Reversal then it wasn't a Consolidation." — Class 2 Notes

These rules let you self-correct in real-time. If what you labeled a "consolidation" became a reversal, you misidentified the stage — go back and re-read the structure.

---

## Stage 1: Consolidation

Consolidation is the **origin of every price run**. It is not a neutral phase. The algorithm is actively using this time to engineer liquidity on both sides of the range.

**What it looks like:**
- Candle bodies are encapsulated within a range (wicks extend outside, but bodies do not)
- BSL builds above the range (equal highs, swing highs)
- SSL builds below the range (equal lows, swing lows)
- Price ping-pongs inside the range, back and forth

**What it signals:**
- A significant expansion is coming
- The 50% (EQ) of the range is the most important level to mark
- Normal timing: Asia session (overnight), pre-market — when volatility is lowest

**What happens next:**
Consolidation always leads to expansion. There is no exception. If you believe price is consolidating but it then reverses without a proper expansion, you were not in a consolidation — you were in the third stage (reversal).

---

## Stage 2: Expansion

Expansion is when price **moves rapidly away from the equilibrium** (50%) of the previous range. It is a displacement move that reveals market maker intent — the direction price is heading.

**What it looks like:**
- Price breaks decisively out of the consolidation range
- Creates an FVG (displacement) — candles moving fast in one direction
- A swing high (or swing low) forms at the end of the expansion leg, capping it

**How to measure:**
- Draw a Fibonacci/box from the expansion's swing low to its swing high
- The 50% divides the expansion into discount (below) and premium (above)
- Valid PDA entries (for the next retracement) will be **at or below the 50%** for longs

**What it does for you:**
- Tells you the bias direction (bullish expansion higher = smart money buying)
- Creates the FVG or OB you will use for your entry on the retracement
- Begins the clock on the "real retracement" that must follow

---

## Stage 3: Retracement

The retracement is the corrective move after expansion. It has **two mandatory jobs**. Both must be completed for it to be a valid retracement.

| Job | Description |
|-----|-------------|
| **Job 1** | Fill the inefficiency — deliver price to the FVG or OB left by the expansion |
| **Job 2** | Reach discount — price must reach at or below the 50% of the expansion |

### Real Retracement vs. Fake Retracement

| Real Retracement | Fake Retracement |
|-----------------|-----------------|
| Fills FVG **and** reaches discount (≤ 50%) | Fills FVG but does **not** reach discount |
| Activates buy program → next expansion begins | Creates engineered sell-side liquidity → more retracement coming |
| Both checkmarks | Only one checkmark — danger |

> "The correct retracement is calling it a real retracement. It's not like you're going to see these in books. I call it that way just to explain it." — MrWitness, Class 3

**What happens when a fake retracement occurs:**
The market fills the FVG near the 50% but turns back up without reaching discount. This is the algorithm engineering buy-side stops on the way down, trapping traders into shorts. The real bottom has not been formed yet — expect more downside before the next expansion.

### Healthy vs. Choppy Retracement

**Healthy retracement:** Price makes a steady series of lower highs as it descends into discount. Each lower high builds more sell-side liquidity. This is "beautiful for longs" — the lower highs mean smart money is systematically engineering liquidity that will fuel the next expansion.

**Choppy retracement:** Price moves sideways, irregularly, sometimes making equal highs. Delivery toward discount is slower. The next expansion will likely be slower and choppier as well.

### The Buy Program at the 50%

Once price reaches discount AND fills the inefficiency, the buy program activates. This is the mechanical reason the expansion resumes from the 50% level — the algorithm has now completed the delivery cycle and is ready to push toward the DOL.

---

## Stage 4: Reversal

A true reversal is distinct from a retracement. A reversal takes out the **origin swing** — the swing high or swing low where the current trend began.

**Key definitions:**
- **Reversal**: price must reach and take out the origin of the current trend
- **Retracement**: price corrects within the current trend without taking out the origin swing

The three types of reversals are covered fully in [[concepts/course/module-2-price-delivery/04-reversals]].

---

## The Cycle

After Stage 3 (real retracement), the cycle returns to Stage 2 (expansion). It continues expanding → retracing → expanding until the trend's origin swing is finally taken out (Stage 4, reversal) — at which point the cycle begins again on the opposite side.

```
Consolidation
    ↓
Expansion (1)
    ↓
Real Retracement → back to Expansion (2) → Expansion (2) continues to DOL
    ↓ (or, eventually)
Reversal (origin swing taken out)
    ↓
New Consolidation on the other side
```

---

## Skipping the Retracement: BPR Conditions

In one specific scenario, the market skips the retracement phase entirely and continues expanding without returning to discount:

**Balanced Price Range (BPR):** When everything below the 50% has already been efficiently delivered — meaning price has already visited and filled those levels — the market does not need to retrace. It continues expanding.

> From the Class 3 Q&A: "In the case that you see something like that, it's because the market is going to be under the pretense of either a balanced price range or a breaker blow. In the time that everything under the 50% has already been efficiently delivered, you do not need to see another comeback to discount."

This is an advanced concept. For now, if the market skips the retracement: do not chase it into premium. Wait for the next setup.

---

## Rules

1. The four stages are sequential: Consolidation → Expansion → Retracement → (Expansion or Reversal).
2. A real retracement requires **both** jobs: fills inefficiency AND reaches discount (≤ 50%).
3. If only the inefficiency is filled (not discount) → fake retracement → expect more downside.
4. If a "consolidation" leads to a reversal → it was not a consolidation. Re-read the structure.
5. Healthy retracements (lower highs) → stronger continuation. Choppy retracements → weaker continuation.
6. Never chase expansion in premium. Wait for the retracement to discount.
7. If price skips the retracement (BPR conditions) → do not chase. Wait for the next opportunity.

---

## See Also

- [[concepts/course/module-2-price-delivery/02-consolidation-model]] — Stage 1 in depth
- [[concepts/course/module-2-price-delivery/03-expansion-retracement]] — Stages 2 & 3 in depth with worked examples
- [[concepts/course/module-2-price-delivery/04-reversals]] — Stage 4 in depth
- [[concepts/business-logic/ict-narratives]] — reference KB for APD stages
- [[concepts/entry-models/consolidation-model]] — entry model checklist for Stage 1 entry
- [[concepts/entry-models/expansion-retracement-model]] — entry model checklist for Stage 3 entry
