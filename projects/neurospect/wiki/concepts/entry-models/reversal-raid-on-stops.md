---
tags: [entry-model, reversal, raid-on-stops, liquidity-sweep, neurospect]
aliases: [Raid on Stops, Reversal Model, 80% Reversal]
sources:
  - sources/neurospect/2026-04-18-vol1-class4-notes.md
  - sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md
  - sources/neurospect/2026-04-18-vol3-class2-market-structure-fractality.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: Reversal — Raid on Stops

The most common reversal pattern (~80% of reversals). Price sweeps a major liquidity pool, collects stops, and immediately rejects. Enter on the first FVG or rejection block formed on the retracement.

> "Market runs the liquidity (e.g., highs), then rejects. Classic 'get in, get out' behavior — quick sweep then reversal." — Class 4 Notes

---

## What It Is

At a major BSL or SSL level, the algorithm makes a decisive sweep — running stops above the swing high (BSL) or below the swing low (SSL) — then immediately reverses. The sweep trap both directional traders (shorts selling resistance get their stops triggered; longs buying the breakout get trapped at the high).

The reversal entry is taken on the first PDA the market leaves after the sweep, as price begins the expansion in the opposite direction.

---

## Setup Conditions

1. **Major liquidity pool identified** — weekly high/low, daily high/low, or session high/low with multiple stacked swing points (layered liquidity = highest probability)
2. **HTF bias shift** — the HTF narrative (4H/Daily FVG) is pointing toward this liquidity level being swept and reversed (not continued through)
3. **Sweep occurs** — price takes out the swing high(s) or swing low(s) clearly, with a spike/wick beyond the level
4. **Immediate rejection** — the sweep candle closes back below the swept level (for BSL sweeps) or back above the swept level (for SSL sweeps) within the same session
5. **First PDA formed** on the expansion lower — FVG, rejection block, or OB left by the initial displacement down from the sweep
6. **MSS or CSD on entry timeframe** — a change of structure or change in state of delivery confirms the reversal direction
7. **Kill zone active** at the time of the sweep and entry

---

## Entry Process

**Step 1 (HTF — 4H/Daily):** Confirm that the major liquidity pool has been swept. The sweep level is now "done" — price should not need to return above it (for BSL sweeps going bearish).

**Step 2 (15M–5M):** Find the first FVG or OB left by the expansion after the sweep. This is your entry zone. For a bearish reversal after a BSL sweep: find the first bearish FVG (SIBI) or a bearish OB (up-close candle before the expansion lower).

**Step 3 (1M or 15s):** Wait for price to retrace up into the PDA. Look for a CSD (change in state of delivery) or change of structure confirming bearish delivery. Enter at the PDA (at the opening price of the OB, or into the upper portion of the bearish FVG).

**Rejection block entry (most precise):**
The opening price of the candle that made the sweep is the rejection block level. After the MSS, this level acts as resistance. A clean return to the rejection block opening price = sniper entry.

---

## Stop Loss

- **FVG entry (bearish):** Above the three candles that form the FVG (above Candle 1 of the bearish FVG)
- **OB entry:** Above the body high of the bearish OB
- **Rejection block entry:** Above the wick high of the sweep candle (one tick above the sweep extreme)

---

## Target Logic

- **First target:** The origin swing where the uptrend began (a true reversal must take out the origin swing)
- **Standard target:** Previous day low / session low / nearest SSL below
- **Extended target:** Deviation levels below the swept SSL (see [[concepts/business-logic/ict-deviations]])

---

## Layered Liquidity (Highest Probability Version)

When multiple swing highs (or lows) are stacked at the same level — equal highs, prior swing high, weekly high all within the same price zone — the raid-on-stops reversal at this level carries the highest probability.

> "Best probability reversals happen when layered liquidity pools (multiple highs/lows stacked)." — Class 4 Notes

The more layers, the more stops collected, the more fuel for the reversal.

---

## What to Watch For (Not a Reversal)

The raid pattern can deceive if:
- Price sweeps the level and **does not close back below it** within a few candles → the breakout may be genuine
- The origin swing is not taken out → may be a deep retracement, not a true reversal
- Price sweeps the level but the HTF FVG is bullish → more likely a retracement buy opportunity, not a reversal short

When uncertain: take partials at the rejection block and let the market confirm with a full MSS before adding.

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: reversal-raid-on-stops
name: Reversal — Raid on Stops (80% Reversal)
description: >
  Enter on the first FVG or rejection block after a major liquidity pool
  (BSL or SSL) is swept and price immediately rejects. Target: origin swing
  of the trend, then previous day high/low.

conditions:
  - Major liquidity pool identified at weekly/daily/session high or low
  - Layered liquidity present (multiple stacked swing points = highest probability)
  - HTF bias (4H/Daily) indicates this level will be swept and reversed (not extended through)
  - Sweep occurs — price takes out the swing high(s) or swing low(s) clearly
  - Sweep candle closes back below the swept level (for BSL sweeps) within the same session
  - First PDA (FVG or OB) formed on the initial expansion in reversal direction
  - CSD or MSS on 1M/15s confirms reversal direction
  - Kill zone active

checklist:
  - "[ ] Major liquidity pool identified (daily/weekly/session high or low)"
  - "[ ] Layered liquidity present (multiple stacked levels)"
  - "[ ] HTF FVG or narrative points to this level being swept and reversed"
  - "[ ] Sweep occurred — spike above BSL (or below SSL) and immediate close back through"
  - "[ ] Sweep candle closed back below the swept level (BSL sweep) or above (SSL sweep)"
  - "[ ] First bearish FVG or OB identified below the sweep (for BSL reversal)"
  - "[ ] Opening price position confirms reversal (above opens for shorts; below for longs)"
  - "[ ] Kill zone active"
  - "[ ] CSD or MSS on 1M/15s confirms reversal direction"
  - "[ ] SMT divergence at the sweep (optional — very high confidence add)"

timeframes:
  liquidity_identification: [Daily, 4H, 1H]
  sweep_confirmation: [15M, 5M]
  entry: [1M, 15s]

stop_logic: >
  FVG entry: above Candle 1 of the bearish FVG (above all three candles).
  OB entry: above the body high of the bearish OB.
  Rejection block entry: above the wick high of the sweep candle.

target_logic: >
  Target 1: origin swing of the trend (first intermediate-term swing that started the up move)
  Target 2: previous day low / nearest session SSL
  Target 3: Fibonacci deviation below the origin swing

probability: "~80% of reversals"

false_positive_signals:
  - Sweep candle does not close back through the level — possible genuine breakout
  - HTF FVG is still bullish — likely a retracement, not a reversal
  - Origin swing not subsequently taken out — reclassify as deep retracement

partial_exit_rule: >
  Always take partials at the rejection block (opening price of the sweep candle).
  This protects against type 1 failure swings masquerading as type 2.
```
