---
tags: [course, module-1, foundations, fvg, bisi, sibi, iofed, bag, neurospect]
aliases: [Fair Value Gap Lesson, FVG Lesson, BISI SIBI Lesson]
sources:
  - sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-pt2-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-notes.md
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class2-notes.md
created: 2026-04-22
updated: 2026-04-22
---

# Module 1, Lesson 2: Fair Value Gaps

> **Vol 1, Class 1 (Part 2) + Class 2 notes — MrWitness + AXL**

You identified the FVG concept in Lesson 1. This lesson goes deeper: how to measure it precisely, which FVGs to prioritize, and the two special conditions (IOFED and BAG) that tell you the highest-probability entry scenario.

---

## Review: What Creates an FVG

An FVG requires **displacement** — a rapid, directional move that leaves a gap between candle 1's extreme and candle 3's extreme. Slow, overlapping price action does not create a valid FVG.

Three-candle pattern:

```
Bullish FVG:
  Candle 1 — last candle before the move (its HIGH is the bottom of the gap)
  Candle 2 — the gap itself (the void; no delivery on the sell side)
  Candle 3 — first candle of the expansion (its LOW is the top of the gap)

The gap = from Candle 1's high to Candle 3's low.
The entry = at or into Candle 3's low (the "top" of the gap), one tick below.
```

```
Bearish FVG:
  Candle 1 — last candle before the drop (its LOW is the top of the gap)
  Candle 2 — the gap (void; no buy-side delivery inside it)
  Candle 3 — first candle of the drop (its HIGH is the bottom of the gap)
```

---

## BISI vs. SIBI (Naming Convention)

These are the formal names for the two FVG directions:

**BISI — Buy Side Imbalance, Sell Side Inefficiency**
- A bullish FVG
- Price displaced higher → gap is efficient on the buy side, inefficient on the sell side
- Price must return to deliver the sell side → this is your long entry
- Target: BSL above

**SIBI — Sell Side Imbalance, Buy Side Inefficiency**
- A bearish FVG
- Price displaced lower → gap is efficient on the sell side, inefficient on the buy side
- Price must return to deliver the buy side → this is your short entry
- Target: SSL below

> From the notes: "When bullish, focus on a BISI left by the impulse that's headed toward the HTF liquidity; when bearish, use a SIBI."

---

## Entry Precision

Where exactly do you enter inside the FVG?

**For a bullish FVG (BISI):**
- Best entry zone: **at or below Candle 3's low** — this is the bottom of the gap's "top edge"
- One tick below Candle 3's low is the most precise entry
- Acceptable alternative: enter **at the CE** (consequent encroachment = 50% of the gap, from Candle 1's high to Candle 3's low)

**Do not** try to enter at the top 50% of the gap. You will miss trades where price only dips into the gap and immediately runs. Enter when price tags the lower/upper portion, not at the midpoint.

**Mitigation sufficiency rule:** Price only needs to **dip into** the gap, often to Candle 3's open, close, or low. It does not need to fill the gap all the way to Candle 1's high before continuing to the target.

---

## The 50% Level (Consequent Encroachment / CE)

The midpoint of the FVG (from Candle 1 extreme to Candle 3 extreme) is called the **CE (consequent encroachment)** or simply "the 50%."

The CE is important for two reasons:
1. **Entry threshold:** If price returns to the FVG but does NOT close below the CE → this is the IOFED condition (see below). Highest-probability continuation.
2. **Stop placement:** Your stop loss should not be placed at the CE. Place it below Candle 1 of the FVG (outside the entire gap).

---

## IOFED: The Highest-Probability Entry

**IOFED = Institutional Order Flow Entry Drill**

Condition: Price creates an FVG during a displacement move. Price then **retraces back to the gap** but does **not close below the CE** (50% of the FVG).

This is the signal that institutional order flow is using the FVG as support. The algorithm has noted the gap, returned to it, and is now ready to continue in the direction of the original displacement.

> From Class 2 notes: "The first gap that a market leaves can be an IOFED (if it goes back to the gap but does not go below the CE) — that's what you want to see when you long, for example."

**IOFED checklist:**
- [ ] Displacement created a FVG
- [ ] This is the first FVG of the move (not a subsequent one)
- [ ] Price returned to the FVG
- [ ] Price did NOT close below the CE (50%)
- [ ] This is your entry

---

## BAG: When Price Never Returns

**BAG = Breakaway Gap**

When price creates an FVG during a strong displacement and **never returns to it** — skipping it entirely and continuing to the target — that gap is classified as a BAG.

A BAG tells you the move was so strong (low-resistance, LRLR conditions) that the algorithm did not need to return to fill the gap before continuing.

**Trading implication:** Do not wait for a BAG to fill before taking the next FVG entry. The BAG confirms the move is strongly directional. Look for the next FVG on the continuation or enter on a retracement.

> From Class 2 notes: "If it does not touch the first gap, it's called BAG."

---

## Inversion FVG

When a **bearish FVG** (SIBI) — which originally signaled shorts — has price **close above** it, the FVG inverts. It is now a bullish support zone.

After inversion:
- When price returns to the former bearish FVG, it now acts as a bullish FVG
- Respect the 50% of the inverted zone for entries
- Stop is below the inverted FVG's range

This is a significant signal in the consolidation model — MrWitness demonstrated in Class 2 that closing above a bearish FVG that sits near the consolidation EQ creates a very strong bullish setup.

---

## Multiple FVGs on the Same Move

When a single displacement creates more than one FVG:
- The **first FVG** (closest to the candle that initiated the displacement) is the IOFED candidate — highest probability
- Enter on the first FVG and allow the stop to sit below the second FVG (the lower one)
- If the first FVG gets filled and the second FVG is tagged, that is still a valid entry — just one that experienced more drawdown

---

## Volume Imbalance vs. FVG

A **volume imbalance** is a related but distinct concept:
- FVG: gap between candle 1's high and candle 3's low (bodies touching or not)
- Volume imbalance: price moved through a range entirely in one direction with no back-and-forth volume inside it

In practice, AXL treats volume imbalances like FVGs for entry purposes. The 50% of a volume imbalance is a valid entry zone.

> AXL in Class 1: "Big wicks act like FVGs / volume imbalances — the market always comes back for the 50% of the wick."

---

## Rules

1. An FVG is a three-candle pattern only. Mark the exact range: Candle 1's extreme to Candle 3's extreme.
2. Enter at or into Candle 3's area (the top edge of a bullish FVG), not at the middle.
3. Stop goes below Candle 1 of the FVG (below the entire gap).
4. If price returns to the gap but does not close below the CE → IOFED → highest probability.
5. If price skips the FVG entirely → BAG → do not wait for it to fill; look for the next opportunity.
6. A bearish FVG that price closes above becomes a bullish entry zone (inversion FVG).
7. Multiple FVGs on one displacement: enter on the first; allow stop for the second.
8. Volume imbalances behave like FVGs — use the 50% of the imbalance for entry.

---

## Worked Example (Class 2 — MrWitness on NQ)

During the live example in Class 2, MrWitness identified the following sequence on the 1M NQ chart during London session:

1. Asia session created a consolidation range. The low of the consolidation = the SSL target for London.
2. London opened and took the Asia consolidation lows (swept the SSL).
3. At that exact moment, ES made a lower low while NQ **failed to make the same lower low** → SMT divergence signal.
4. The displacement higher created an **inversion FVG** just above the consolidation equilibrium (EQ). A prior bearish FVG that price closed above and treated as bullish support.
5. Price returned to this inversion FVG twice, respecting the 50%.
6. Third touch: price closed above the EQ of the consolidation simultaneously with the inversion FVG respect → the highest-probability long entry point.
7. Price expanded to previous day high.

**Key insight from MrWitness:** "When this candle closes above the bearish FVG AND above the consolidation equilibrium — it's killing two birds with one stone."

Source: `sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md`

---

## AXL's Trade Example (Class 1, Part 2)

AXL walked through an entry using the three-step framework:

1. **Step 1 (1H):** Identified a bullish FVG with a wick below it on the 1H chart. An FVG above a wick signals potential reversal or inversion inside the FVG.
2. **Step 2 (5M):** Inside the 1H FVG, found a **breaker block** — the last opposing candle before a significant move, now acting as support after being broken.
3. **Step 3 (15s):** Waited for price to give a lower high → lower high → change of structure (price closes above the breaker block's body 50%). Entered at the 50% of the breaker block.
4. Stop: above the breaker block high.
5. Target: the swing high with BSL — a cluster of equal highs.

> AXL: "In 15 seconds, I'm waiting for a change of structure inside the breaker block. I put my limit order at the 0.5% of the breaker block body. That's my sniper entry."

Source: `sources/neurospect/2026-04-18-vol1-class1-pt2-liquidity-and-inefficiency.md`

---

## Common Mistakes

- **Entering at the top 50% of the FVG:** AXL specifically warned against this — price frequently only dips to the lower portion (Candle 3 area) and immediately runs. Entering at the midpoint means missing the move.
- **Waiting for a full fill:** If the IOFED condition is met (returned but did not close below CE), the gap is "done." Waiting for a full fill means entering after the move has already begun.
- **Marking zones instead of precise candle levels:** "It is a void or gap in price action, not a zone." Mark the exact candle 1 high and candle 3 low.
- **Treating every displacement as a valid FVG:** The displacement must be real (rapid, directional). Slow, back-and-forth moves do not create valid FVGs.

---

## Vocabulary from Class 2 Notes

| Term | Meaning |
|------|---------|
| IOFED | Institutional Order Flow Entry Drill — first FVG, price returns but does not close below CE |
| BAG | Breakaway Gap — FVG price never returns to |
| BISI | Bullish FVG (buy-side imbalance, sell-side inefficiency) |
| SIBI | Bearish FVG (sell-side imbalance, buy-side inefficiency) |
| CE | Consequent Encroachment — 50% of the FVG |
| BOS | Break of Structure |
| LRLR | Low Resistance Liquidity Run |
| HRLR | High Resistance Liquidity Run |
| APD | Algorithmic Price Delivery |
| ORG | Opening Range Gap |

---

## See Also

- [[concepts/business-logic/ict-liquidity]] — full BISI/SIBI/IOFED/BAG reference
- [[concepts/business-logic/ict-entry-models]] — order blocks, rejection blocks, breakers — the other PDA types
- [[concepts/course/module-1-foundations/01-what-moves-the-market]] — previous lesson
- [[concepts/course/module-1-foundations/03-homework-and-practice]] — homework for this module
- [[concepts/course/module-2-price-delivery/02-consolidation-model]] — first full model using FVGs
