---
tags: [course, module-5, order-flow, closing-basis, quadrants, lrlr, hrlr, neurospect]
aliases: [Order Flow Lesson, Closing Basis, HTF LTF Order Flow, Module 5 Lesson 1]
sources:
  - sources/neurospect/2026-04-18-vol4-class1-htf-ltf-orderflow.md
created: 2026-04-22
updated: 2026-04-22
module: 5
lesson: 1
---

# Module 5, Lesson 1: HTF/LTF Order Flow

**Prerequisites:** [[concepts/course/module-4-market-structure/01-swing-classification|Module 4, Lesson 1 — Swing Classification]], [[concepts/course/module-2-price-delivery/01-four-stages-apd|Module 2, Lesson 1 — Four Stages of APD]]  
**Reference:** [[concepts/business-logic/ict-order-flow|ICT Order Flow KB]]

---

## Concept

Order flow in this framework does **not** require footprint charts, level 2 data, or any paid subscription. It is read entirely from **closing prices of candles relative to PDA levels** and **quadrant analysis** of dealing ranges. These two tools tell you whether to trust the current move or stand aside.

> "Do you really think they're going to allow you to literally see what the big whales are entering at? You don't need anything like that. Just knowing where the swing highs and swing lows are is all you need." — MrWitness, Vol 4 Class 1

Order flow does not tell you where price is going — it tells you whether the move that has already started deserves your participation.

---

## Bodies vs. Wicks

The most fundamental order flow principle:

- **Bodies tell the story** — where candles **close** confirms direction
- **Wicks engineer liquidity** — the spike of a wick is for stops; the body is for direction

When analyzing order flow, look only at where bodies are **closing** relative to key levels:
- Bodies closing above a PDA → that PDA is acting as support → bullish order flow
- Bodies closing below a PDA → that PDA is acting as resistance → bearish order flow
- Bodies not respecting either side consistently → chop; stand aside

Wicks extending past PDAs are not disrespect — they are stop hunts. If the body **closes** through the PDA, that is genuine disrespect.

---

## Quadrant Levels

Divide any significant dealing range (ITL → ITH for bullish, ITH → ITL for bearish) into four equal levels:

| Level | Label | Significance |
|---|---|---|
| 0 (bottom) | Range low | Below here = below the dealing range |
| 0.25 | Lower quadrant | PDA arrays form here in downtrends; discount zone |
| 0.50 | Equilibrium (EQ) | Critical midpoint; consolidation forms here |
| 0.75 | Upper quadrant | PDA arrays form here in uptrends; premium zone |
| 1.0 (top) | Range high | Above here = above the dealing range |

> "PDA arrays are going to be formed around these specific levels." — Vol 4 Class 1

**How to use:**
- In a bearish move from 1.0: bearish OBs and FVGs form at the 0.75 and 0.50 levels → short entries
- In a bullish retracement to 0.25: bullish OBs and FVGs form at 0.25 and 0.50 → long entries
- Check closing basis: candles must close in the direction of the trade relative to these levels

**The -0.25 extension:** The level below the range (0 minus 25% of the range size) is a common first deviation target beyond the range. Measure the range, apply the same interval below zero.

---

## Closing Basis Rules (Bullish Order Flow)

Order flow is confirmed bullish when:

1. **Down-close candles are supported** — each bullish OB (down-close before an up move) holds when price returns; bodies close above them
2. **FVGs stay unfilled** — bearish FVGs above price are left open (price is not returning to fill them) = LRLR signature
3. **Lower highs in retracement** — steady series of lower highs into discount with bodies closing higher each time = "beautiful for longs"
4. **Bodies not closing below key levels** — if price wicks below a FVG but bodies stay above → the FVG is still respected

**When bullish order flow breaks:**
- Up-close candles before the down move are no longer being respected as bearish OBs
- Bodies close above previously-respected bearish PDAs
- FVGs above price start filling
- Step to the sidelines: "when up-close candles are not being respected as resistance, order flow is neutral or bullish"

---

## Closing Basis Rules (Bearish Order Flow)

Order flow is confirmed bearish when:

1. **Up-close candles respected as resistance** — each bearish OB (up-close before a down move) holds when price returns; bodies close below them
2. **FVGs stay unfilled above price** — bearish continuation signal; price is not coming back for them
3. **Swing lows being taken** and **swing highs being rejected** — structural sequence confirms bearish direction
4. **Bodies closing below previously-respected PDA levels**

**Entry signal:** When a bearish OB (up-close before down move) is in the upper quadrant of a dealing range, wait for price to touch the OB's opening price, confirm a close below, and enter.

---

## LRLR vs. HRLR Conditions

This is the most important environment distinction. Your entire entry model selection depends on it.

| Condition | Full Name | Candle Signature | Entry Approach |
|---|---|---|---|
| **LRLR** | Low Resistance Liquidity Run | Bodies stacking cleanly in one direction; FVGs staying open; minimal overlap | Enter near the OB/FVG at 50% or quadrant; targets clean and fast |
| **HRLR** | High Resistance Liquidity Run | Overlapping bodies; FVGs filling frequently; back-and-forth price | Wait for OTE (62–79%); smaller size; expect deep retracements |

**How to identify before trading:**
- **LRLR:** Small ORG (<50 handles NQ) is an early HRLR signal; candles stacking confirms LRLR once the session starts
- **HRLR:** Large ORG suggests LRLR conditions; overlapping bodies day-of confirms HRLR regardless

> "Every single up-close candle, I need to see it supporting price lower [when bearish] and fair value gaps should stay unfilled. That is a characteristic of low-resistance liquidity run." — Vol 4 Class 1

**Critical rule:** Do not use market structure fractality entries in HRLR. Deep retracements will reverse your fractals repeatedly. Use OTE model instead.

---

## LTF Order Flow (1M and Below)

At the entry timeframe, order flow is bullish when:
- Down-close candles (bullish OBs) hold on the first return
- FVGs in the direction of the trade stay open after entry
- Higher lows forming with each mini-expansion

**Shift to bearish at LTF:**
- Up-close candles before the down move breach their opening price (CSD at LTF)
- Bodies start closing below previously-respected PDA levels
- The FVG above price stays open = breakaway condition; do not expect a return fill

---

## Balanced Price Range (BPR) Behavior

A BPR is a range where both buy-side and sell-side have been delivered — both directions of candle body delivery have occurred inside the range.

**Key property:** Price entering a BPR will chop. Do NOT expect:
- A clean 2022 model from a BPR
- An OTE model from a BPR
- LRLR conditions from a BPR

Do expect:
- Back-and-forth body delivery
- The BPR's midpoint (50%) to act as the consolidation anchor
- An expansion from the BPR's low end (consolidation model applies)

**Identifying BPR:** If you see many wicks at a level (bodies going up and down, back and forth) — you are in a BPR. Switch to watching the BPR midpoint and look for a consolidation model break.

---

## Worked Example: Five-Minute Bearish Flow (Vol 4 Class 1 Live)

MrWitness walks through a bearish intraday session on ES, 5-minute chart:

**Reading the quadrants:**
1. Price is in the upper quadrant (0.75–1.0) of the dealing range → premium zone → looking for bearish order flow
2. Long-term high formed (ITH takes out prior ITH) → intermediate-term high confirmed
3. Bodies close below the 0.75 level → bearish order flow established

**Following the flow:**
- First up-close candle after the CSD → bearish OB candidate
- Price returns to that candle's opening price → entry signal
- Bodies close below → LRLR confirmation; FVGs left open above
- Next up-close candle (at 0.50 level) → another bearish OB → another entry
- BPR forms at the 0.50 equilibrium → consolidation phase → wait
- After BPR, next expansion lower → bearish OB at 0.25 → final entry before target

**Key lesson:** "When the order flow is bearish like this and up-close candles are being respected as bearish order blocks, it doesn't matter — you just want to wait for another bearish OB, and that's going to be your entry. You will not be fearful of the retracement because you're not going to have the retracements." — Vol 4 Class 1

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Using the wick as the disrespect signal | Wicks are stop hunts; body closes are direction signals |
| Looking for LRLR entries in HRLR conditions | Shallow entries get stopped through deep retracements |
| Entering at 50% in a BPR | BPR chops; the 50% is just consolidation, not a clean OTE or E&R |
| Abandoning a bearish trade when an up-close OB is tapped | If the body closes BELOW the OB, order flow is still bearish |
| Entering during chop (bodies not respecting either side) | No order flow confirmation = no edge; wait for clarity |

---

## Homework

Practice for one week on 5-minute ES or NQ charts:

1. Each day, mark the quadrant levels of the intraday dealing range (session low to session high)
2. Watch where the first bearish (or bullish) OB appears after an LTH (or LTL)
3. Track: does the OB hold on the first return? Second return?
4. Note when LRLR conditions are present (clean candle stack, no FVG filling) vs. HRLR
5. Record how many entries per session the order flow gave you vs. how many you could have taken

---

## See Also

- [[concepts/course/module-5-order-flow-and-smt/02-smt-divergence|Lesson 2 — SMT Divergence]] — intermarket order flow confirmation
- [[concepts/business-logic/ict-order-flow|ICT Order Flow KB]] — full reference including holiday liquidity and LTF specific rules
- [[concepts/entry-models/model-2022-ote|Model 2022 + OTE]] — used in HRLR conditions instead of standard 50% entry
- [[concepts/business-logic/ict-narratives|ICT Narratives KB]] — LRLR/HRLR framing in economic calendar context
