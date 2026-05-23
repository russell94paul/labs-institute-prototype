---
tags: [entry-model, expansion, retracement, e-and-r, neurospect]
aliases: [Expansion Retracement Model, E&R Model]
sources:
  - sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md
  - sources/neurospect/2026-04-18-vol1-class3-notes.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: Expansion & Retracement (E&R)

Enter at a FVG or OB **at or below the 50%** of a completed expansion leg, after a real retracement (fills inefficiency AND reaches discount) has begun.

> "Look for an OB / FVG that was left at or below the EQ of the Expansion. Enter on that PDA." — Vol 1 Class 3 Notes

---

## What It Is

After a strong expansion leg, the market retraces to fill the inefficiency it left behind. The retracement must reach the discount zone (≤ 50%). Once price enters the discount zone and taps the FVG or OB, the buy program activates — this is your entry for the continuation to the original target.

---

## Setup Conditions

1. **Expansion leg identified** on 1M–5M with a clear swing low and swing high
2. **50% measured** on the expansion leg — discount zone defined
3. **FVG or OB present at or below the 50%** of the expansion
4. **HTF bias aligned** — the expansion direction matches the 4H/Daily FVG bias
5. **Real retracement in progress** — price is making lower highs back toward discount (not a fake retracement)
6. **Retracement reaches discount** (price trades at or through the 50% line) before entry
7. **PDA at or below 50%** is the entry point — not above it
8. **Kill zone active** at the time of entry

---

## Entry Process

**Step 1 (HTF — 15M or above):** Find the FVG or OB left by the expansion that is at or below the 50% of the expansion leg. This is the main PDA.

**Step 2 (Mid-TF — 5M):** Look for additional confluence confirming the PDA — a second FVG or OB that reinforces the entry level.

**Step 3 (Entry TF — 1M or 15s):** Wait for a candle body to close at or above the FVG boundary (bullish FVG confirmation signature). Enter as the next candle opens. Or wait for a COS (change of structure) inside the PDA.

**Algorithmic signature:** Bodies closing above the FVG = the algorithm is respecting the gap. Enter on the open of the next candle after this confirmation.

---

## Stop Loss

- **FVG entry:** Below the three candles that form the FVG (below Candle 1 of the gap)
- **OB entry:** Below the body low of the order block
- **Trail option:** Trail below the three candles forming the FVG once price is moving in your favor

---

## Target Logic

- **First target:** The swing high (BSL) that capped the original expansion leg
- **Extended target:** Previous day high/low if the expansion swing high doesn't provide enough R:R
- **Deviation target:** One Fibonacci deviation beyond the swing high (see [[concepts/business-logic/ict-deviations]])

---

## Timeframes

| Purpose | Timeframe |
|---------|-----------|
| HTF bias | Daily, 4H |
| Expansion measurement | 5M, 1M |
| PDA identification | 5M, 15M |
| Entry confirmation | 1M, 15s |

---

## When to Skip the Trade

- Price fills the FVG but it is **above** the 50% → not in discount → skip or wait
- Fake retracement in progress (price turned up before reaching discount) → wait for a new leg down
- BPR conditions: everything below 50% already efficiently delivered → market may skip the retracement entirely (do not chase; wait for the next expansion leg)
- HRLR / news week: retracement will be choppier; use OTE model instead (see [[concepts/entry-models/model-2022-ote]])

---

## Related Models

- [[concepts/entry-models/consolidation-model]] — the Stage 1 version (entering from a range EQ)
- [[concepts/entry-models/model-2022-ote]] — deep OTE retracement variant for HRLR conditions

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: expansion-retracement-model
name: Expansion & Retracement (E&R) Model
description: >
  Enter at a FVG or OB at or below the 50% of a completed expansion leg,
  after the retracement has filled the inefficiency AND reached discount.
  Target: the swing high (BSL) that capped the expansion, then PDH/PDL.

conditions:
  - Expansion leg identified (swing low to swing high, 1M–5M)
  - 50% of expansion measured (discount = at or below 50%)
  - FVG or OB present at or below the 50% of the expansion leg
  - HTF bias aligned (4H/Daily inside bullish FVG or targeting BSL)
  - Retracement in progress making lower highs (healthy) or irregular (choppy)
  - Retracement has reached or is entering the discount zone (at or below 50%)
  - Kill zone active

checklist:
  - "[ ] HTF bias confirmed (4H/Daily inside bullish FVG for longs)"
  - "[ ] Opening price position aligned (below midnight/8:30 open for longs)"
  - "[ ] Expansion leg identified and 50% measured"
  - "[ ] FVG or OB exists AT OR BELOW the 50% of the expansion"
  - "[ ] Retracement has reached discount (price at or below 50%)"
  - "[ ] Not a fake retracement (discount reached, not just FVG filled)"
  - "[ ] PDA (FVG/OB) in discount confirmed"
  - "[ ] Kill zone active"
  - "[ ] Algorithmic signature: body closing above/at FVG boundary (or COS on 1M/15s)"
  - "[ ] OB+FVG alignment at 50% present (optional — highest confluence)"

timeframes:
  bias: [Daily, 4H]
  expansion_measurement: [5M, 1M]
  pda_identification: [15M, 5M]
  entry: [1M, 15s]

stop_logic: >
  FVG entry: below Candle 1 of the FVG (below all three candles that form the gap).
  OB entry: below the body low of the order block.
  Trail option: trail below the three candles forming the FVG entry.

target_logic: >
  Target 1: swing high (BSL) that capped the expansion
  Target 2: previous day high/low
  Target 3: one Fibonacci deviation beyond the first BSL

retracement_quality:
  healthy: steady lower highs into discount → LRLR continuation expected
  choppy: irregular back-and-forth into discount → slower/choppier continuation; use OTE model

avoid_conditions:
  - FVG or OB above the 50% — do not enter in premium
  - Fake retracement (FVG filled but discount not reached) — wait for more downside
  - BPR conditions — do not chase if market skips the retracement
  - HRLR / news week before news release — use OTE model instead
```
