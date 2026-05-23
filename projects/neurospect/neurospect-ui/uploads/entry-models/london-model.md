---
tags: [entry-model, london, sessions, kill-zone, asia, neurospect]
aliases: [London Model, London Takes Asia Side]
sources:
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class2-notes.md
  - sources/neurospect/2026-04-18-vol2-class2-notes.md
  - sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: London Model

London takes one side of the Asia range (SSL or BSL) and delivers to the other. Occurs 1–3 times per week. Simple, high-probability, and one of the most profitable models once recognized consistently.

> "The model of London that takes one side of Asia and delivers to the other side of Asia — it's super simple, it is super easy, and it happens once, twice, sometimes three times a week. And it is everything you're going to need to start making money in the market." — MrWitness, Vol 1 Class 2

---

## What It Is

Asia session (roughly 8 PM – midnight Eastern) consolidates — engineering liquidity above (BSL) and below (SSL) the Asia range. The London session (2–5 AM Eastern) opens and takes one side — most commonly the sell side (sweeps the Asia lows) — then delivers price to the other side (the Asia highs / BSL above).

This is the consolidation model applied to a specific, recurring timing setup. The Asia range is the consolidation. The London session is the kill zone. The sweep of one side is the manipulation. The expansion to the other side is the distribution.

---

## Setup Conditions

1. **Asia range identified** — bodies of candles during Asia session (8 PM – midnight Eastern) define the range; mark the high, low, and 50% (EQ) of the Asia range
2. **BSL above** Asia range (Asia highs / equal highs) and **SSL below** (Asia lows / equal lows) clearly identified
3. **HTF bias aligned** — 4H/Daily FVG or nearest HTF liquidity level is consistent with the expected delivery direction (i.e., bullish HTF FVG = expect London to take SSL and deliver to BSL)
4. **Opening price position** — price below midnight open / 8:30 open for longs; above for shorts
5. **London session active** (2–5 AM Eastern)
6. **London takes Asia SSL** (for bullish setup) — a clear sweep of the Asia lows; wick extends below the Asia range low and closes back above
7. **Displacement higher** after the sweep — creates an FVG or inversion FVG near or above the Asia EQ
8. **PDA at or below Asia EQ** for the entry — FVG, inversion FVG, OB, or rejection block

---

## Entry Process

**Step 1 (HTF — 1H or above):** Mark the Asia range. Identify the HTF bias. Confirm that the expected sweep direction is consistent with the HTF DOL.

**Step 2 (5M–1M):** As London opens (2 AM), monitor for the sweep of the Asia low (SSL). Once the sweep occurs, watch for the displacement back above the Asia EQ.

**Step 3 (1M or 15s):** Look for the first PDA above the EQ — the inversion FVG, the FVG left by the displacement, or the OB from the move. Wait for a COS or candle body confirmation at the PDA. Enter below the EQ.

**Target:** The Asia high (BSL), then previous day high, then deviation targets.

---

## The SMT Confirmation Version (Highest Probability)

At the sweep of the Asia lows, check both correlated indices:
- If NQ takes the Asia low and ES does not (or ES takes it less deeply) → bullish SMT divergence → highest confidence version of this model
- MrWitness demonstrated this exact scenario in Vol 1 Class 2: "On ES, it was not taken. That is the first hint — this is what you should know as SMT."

SMT at the London sweep = strongest possible long signal on the London model.

---

## Worked Example (Vol 1 Class 2 — Live NQ)

**Setup:**
- FOMC week, high-resistance conditions; ORG ~41 handles (< 50 handles)
- Asia range: Sunday overnight to Monday pre-market
- HTF target: Wednesday's highs (pending business from prior week — 5 ticks short)

**London execution:**
- 3:20 AM: London swept the Asia lows (SSL)
- At that low: ES made a lower low; NQ did NOT → bullish SMT
- Immediate displacement higher → inversion FVG formed at the Asia EQ (prior bearish FVG closed above → inverted to bullish)
- Price returned to this inversion FVG three times
- Entry at ~4:14 AM, below the EQ, at the inversion FVG
- Expanded to PDH, then to Wednesday's highs

Source: `sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md`

---

## Frequency and Timing Notes

- Occurs 1–3 times per week
- Monday and Tuesday most consistent; avoid Sunday London (no algorithmic principle)
- Jackson Hole week / FOMC / NFP: expect the London move but with choppier delivery; do not over-trade
- CPI week Monday: very low probability; skip
- Do not hold through a news release inside the London window; exit before the release

---

## Stop Loss

- Below the rejection block (opening price of the sweep candle)
- Or below Candle 1 of the FVG entry
- Stops in the 10–15 handle range on NQ are typical for this model

---

## Target Logic

- **First target:** Asia high (BSL — opposite side of the range)
- **Standard target:** Previous day high
- **Extended target:** Weekly high or Fibonacci deviation beyond the prior swing high

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: london-model
name: London Model
description: >
  London takes one side of the Asia consolidation range (SSL for bullish,
  BSL for bearish), then delivers to the other side. Enter on the first PDA
  at or below the Asia EQ after the London sweep. Occurs 1–3 times per week.

conditions:
  - Asia range identified (bodies only; mark high, low, and 50% EQ)
  - HTF bias (4H/Daily FVG) aligned with the expected London delivery direction
  - Opening price position correct (below midnight/8:30 open for longs)
  - London kill zone active (02:00–05:00 Eastern)
  - Asia SSL swept (or BSL for bearish) — wick beyond Asia low and immediate close back above
  - Displacement after sweep creates FVG or PDA at or near the Asia EQ
  - PDA is at or below the Asia EQ

checklist:
  - "[ ] Asia range identified with bodies (not wicks) — high, low, and EQ marked"
  - "[ ] BSL above Asia range and SSL below Asia range clearly identified"
  - "[ ] HTF bias confirmed (4H/Daily bullish FVG for longs)"
  - "[ ] Opening price aligned (below midnight open and/or 8:30 open for longs)"
  - "[ ] London kill zone active (02:00–05:00 Eastern)"
  - "[ ] Asia SSL swept — wick below Asia low, closed back above"
  - "[ ] Sweep rejected immediately (did not close below Asia range low)"
  - "[ ] Displacement higher created FVG or identifiable PDA at or near EQ"
  - "[ ] PDA at or below Asia EQ confirmed"
  - "[ ] Kill zone still active at time of entry"
  - "[ ] SMT divergence at the sweep (optional — highest confidence add)"

timeframes:
  bias: [Daily, 4H, 1H]
  asia_range: [5M, 1M]
  entry: [1M, 15s]
  kill_zone: London (02:00–05:00 Eastern)

stop_logic: >
  Below the rejection block (opening price of the sweep candle).
  Or below Candle 1 of the FVG entry.
  Typical stop: 10–15 NQ handles.

target_logic: >
  Target 1: Asia high (BSL — opposite side of the range)
  Target 2: previous day high
  Target 3: weekly high or Fibonacci deviation beyond prior swing high

frequency: 1–3 times per week

avoid_conditions:
  - Sunday London session (no algorithmic delivery principle)
  - FOMC/CPI/NFP week before news release (choppy delivery; reduce size)
  - CPI week Monday (low probability; skip entirely)
  - Holding through news release within London window

smt_signal: >
  At the Asia SSL sweep: if ES fails to take the same lower low as NQ (or vice versa),
  this is bullish SMT divergence — highest confidence version of the London model.
  See consolidation-model YAML for full SMT entry logic.
```
