---
tags: [entry-model, model-2022, ote, csd, market-structure, neurospect]
aliases: [Model 2022, OTE Entry, Optimal Trade Entry, CSD Entry, Model 2022 + OTE]
sources:
  - sources/neurospect/2026-04-18-vol3-class5-model-2022-ote-csd.md
  - sources/neurospect/2026-04-18-vol2-class3-measuring-manipulation-deviations.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: Model 2022 + OTE (Optimal Trade Entry)

**Difficulty:** Advanced — requires understanding of market structure (ITL/ITH), HRLR conditions, and CSD  
**Frequency:** 2–4 setups per week on NQ; most common during London and NY AM kill zones  
**Reference:** [[concepts/business-logic/ict-entry-models|ICT Entry Models KB]], [[concepts/business-logic/ict-market-structure|ICT Market Structure KB]]

---

## What This Model Is

Model 2022 + OTE is the entry model for **deep retracement** conditions. When a market structure shift occurs but price fails to retrace to the standard 50% discount zone (which is the normal expansion-retracement entry), the market signals that a deeper retracement to the **Optimal Trade Entry zone (62–79%)** is coming.

This model is also the entry framework for **high-resistance liquidity run (HRLR) conditions** — when the market is choppy and overlapping, deep retracements to the OTE zone are more common than shallow 50% entries.

> "My favorite PDA for this reason. When you know how to use them, it's just beautiful." — MrWitness on OTE blocks, Vol 3 Class 5

---

## When to Expect This Model (Trigger Conditions)

**Primary trigger (Model 2022):**
1. A market structure shift (MSS) occurs: price takes out an intermediate-term low (ITL), then breaks above the high that initiated the ITL price leg lower
2. After the MSS, price expands higher but **does NOT retrace to 50% discount** of the expansion leg
3. This failure to reach 50% signals deep OTE retracement is coming

**Secondary trigger (HRLR conditions):**
- Opening range gap (ORG) less than 50 handles on NQ
- Overlapping candle bodies; FVGs filling rather than staying open
- News week (FOMC, CPI, NFP)
- In HRLR: skip the standard 50% E&R model; wait for OTE

**CSD trigger (pre-MSS entry — see below):**
- Down-close candles in the discount zone
- Price breaches the **opening price** of those down-close candles → CSD confirmed
- Can enter on CSD without waiting for the full MSS

---

## Setup Conditions

Before entering, all of these must be true:

- [ ] HTF FVG bias confirmed on 4H (inside bullish FVG for long entry)
- [ ] Opening price position correct (price below midnight/8:30/9:30 opens for longs)
- [ ] MSS has occurred OR CSD has been confirmed (see CSD section)
- [ ] Price is in the OTE zone (62–79% retracement of the expansion leg)
- [ ] OTE block identified in the zone (highest down-close candle by body, or propulsion block)
- [ ] Kill zone active (London, NY AM, or NY PM)
- [ ] No major news release within the next 30 minutes

---

## Entry: Selecting the OTE Block

The OTE block is the order block that coincides with the 62–79% Fibonacci zone. Selecting the correct OTE block is the most critical skill in this model.

**Rules for identifying the OTE block:**

1. **Highest down-close candle wins.** Measure the expansion leg (ITL → swing high for bullish). In the 62–79% zone, find the down-close candle with the **highest body open** — that is the OTE block. Not the last down-close candle; the one with the highest open.

2. **Prefer the propulsion block.** If two down-close candles exist in the OTE zone and the second one trades into the body of the first → the second is the **propulsion block**. It has more force than the original OB. Enter on the propulsion block.

3. **Prefer concert with levels.** The ideal OTE block is at or very near the 0.705 level (the midpoint between 0.62 and 0.79). Check: is the block's body in concert with the 0.705?

4. **Use the 50% of the OTE block as entry.** Enter at or above the midpoint (50%) of the OTE block's body for longs. The opening price of the OTE block is the defining level.

**Stop loss:** Below the closing price of the OTE block (the lowest body level of the down-close candle). A true order block will not see its closing price touched after entry — if it does, the analysis is wrong.

> "Because remember, a true order block won't see the closing price being reached." — Vol 3 Class 5

---

## Change in State of Delivery (CSD) — The Pre-MSS Signal

CSD is the signal that direction has changed **before** a full market structure shift confirms it. Using CSD allows earlier entries at better prices.

**How to identify CSD:**
1. Price is in discount (below 50% of a dealing range)
2. There is a group of **down-close candles** in that discount
3. Price **breaches the opening price** of those down-close candles (closes above, for bullish)
4. → CSD confirmed: the state of delivery has changed; longs are now valid

**CSD vs. MSS:**
- CSD: earlier signal; opening price of down-close candles is breached (pre-MSS)
- MSS: later confirmation; price closes above the high that started the ITL leg lower

> "Down-close candles right here in the discount get breached. Why does it leave you also a fair value gap? And price goes to that before continuing higher. So you already know that this low is not going to be taken out. This is your change in the state of delivery." — Vol 3 Class 5

**In practice:** Take the CSD entry and let the MSS be a **post-entry confirmation**. CSD entry + MSS confirms = highest quality.

---

## Step-by-Step Entry Process

1. **Confirm HTF bias** (4H bullish FVG + price below midnight open)
2. **Identify the MSS:** Find the ITL; find the high that initiated the ITL price leg; price must break above that high
3. **Measure the expansion leg:** From ITL to the swing high of the expansion after the MSS
4. **Plot Fibonacci 62–79%** on the expansion leg
5. **Find the OTE block** in the 62–79% zone: highest down-close candle (or propulsion block)
6. **Set limit order** at 50% of the OTE block's body
7. **Set stop loss** below the OTE block's body (below the closing price of the candle)
8. **Target:** HTF draw on liquidity (swing high, daily BSL, session high)

**CSD early entry variant:**
- Instead of waiting for price to retrace into the OTE zone, identify the down-close candles in discount
- Enter when price breaches their opening price
- Stop: below the ITL (the low that must hold)

---

## Stop and Target Logic

| | Level |
|---|---|
| **Stop loss** | Below the OTE block body's closing price (not below the wick) |
| **First target** | The first deviation beyond the swing high target (use Fibonacci deviations) |
| **Ideal exit** | -2 to -2.5 deviation, especially if aligned with an HTF FVG boundary (HPDL) |

---

## Worked Example: Vol 3 Class 5 Live Trade Review

**Session:** NY AM, bullish day

**Structure:**
- Pre-market sweeps the sell-side (creates the ITL)
- Price expands higher — this is the MSS price leg
- Price fails to reach 50% discount → Model 2022 confirmed

**Setup:**
- Measure the expansion leg: ITL to swing high
- 62–79% Fibonacci zone lands in the prior fair value gap (IOFED area)
- In that zone: two down-close candles; second is the propulsion block (trades into the first)
- Propulsion block is in concert with the 0.705 level

**Entry:** Limit order at 50% of the propulsion block body  
**Stop:** Below the propulsion block's closing price (6 handles risk in the example)  
**Target:** -2 deviation of the dealing range = HOD  

Result: Clean delivery from the OTE zone to the deviation target.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Entering at 50% discount when HRLR conditions exist | HRLR means deep retracement; 50% E&R entry will be stopped through |
| Choosing the last down-close candle instead of highest open | The OTE block is always the highest body open in the zone, not the last |
| Ignoring the propulsion block | The propulsion block has more institutional force than the base OB |
| Setting stop below the swing low instead of below the OTE block | Oversized stop; risk:reward deteriorates |
| Entering on CSD without any HTF bias | CSD is a confirmation signal, not a standalone trigger |

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: model-2022-ote
strategy_name: Model 2022 + OTE (Optimal Trade Entry)
version: 1
direction: long  # Also applicable for shorts (reverse all conditions)

trigger_conditions:
  primary:
    - Market structure shift (MSS) confirmed — ITL taken, then break above initiating high
    - Price fails to retrace to 50% discount after MSS expansion → Model 2022 active
  secondary:
    - HRLR conditions (ORG < 50 handles NQ, overlapping bodies, news week)
  csd_early_entry:
    - Group of down-close candles in discount
    - Price breaches opening price of those candles (CSD)

setup_conditions:
  - HTF FVG bias confirmed on 4H (bullish FVG for long)
  - Opening price position: price below midnight/8:30/9:30 opens
  - MSS or CSD confirmed
  - OTE block identified in 62–79% Fibonacci zone (highest down-close body)
  - Propulsion block preferred over base OB
  - Kill zone active

entry:
  zone: 62–79% Fibonacci retracement of the MSS expansion leg
  block_selection: Highest down-close candle body in OTE zone; prefer propulsion block
  trigger: Limit order at 50% of OTE block body (at or above opening price)
  csd_variant: Enter on breach of down-close candle opening prices in discount

stop_logic: Below the OTE block body's closing price (not below wick)

target_logic:
  first_target: First deviation beyond swing high target (-1 deviation)
  runner_target: -2 to -2.5 deviation, especially if aligned with HTF FVG (HPDL)

checklist:
  - [ ] 4H bullish FVG confirmed; price inside it
  - [ ] Opening price: price below midnight open (ideal: below 8:30 and 9:30 also)
  - [ ] MSS confirmed OR CSD confirmed
  - [ ] OTE zone (62–79%) mapped from ITL to expansion swing high
  - [ ] OTE block identified — highest down-close body in zone
  - [ ] Propulsion block check: is second OB inside first OB? Use propulsion block if yes
  - [ ] Block in concert with 0.705 Fibonacci level (preferred)
  - [ ] Kill zone active
  - [ ] No major news in next 30 minutes
  - [ ] Stop set below OTE block closing price
  - [ ] Deviation targets (-1 partial, -2/-2.5 runner) pre-marked

timeframes:
  bias: [1H, 4H, Daily]
  structure: [15M, 1H]
  entry: [1M, 5M, 15s]

avoid_conditions:
  - Pre-MSS without CSD (don't enter on a suspect STL only)
  - 50% of expansion is filled — E&R model applies, not OTE
  - HRLR with no clear OTE block in the zone
  - Entering from OTE when HTF FVG is violated

related_models:
  - expansion-retracement-model  # Standard 50% entry — use when MSS retraces to 50%
  - daily-bias-model             # Prerequisite for HTF FVG bias confirmation
```
