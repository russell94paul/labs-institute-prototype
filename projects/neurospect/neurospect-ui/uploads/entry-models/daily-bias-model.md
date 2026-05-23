---
tags: [entry-model, daily-bias, htf-fvg, opening-price, filter, neurospect]
aliases: [Daily Bias Model, HTF Bias Filter, Bias Confirmation Entry]
sources:
  - sources/neurospect/2026-04-18-vol2-class4-daily-bias-practice.md
  - sources/neurospect/2026-04-18-vol2-class4-notes.md
  - sources/neurospect/2026-04-18-vol2-class1-power-of-three.md
  - sources/neurospect/2026-04-18-vol2-class1-notes.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: Daily Bias (HTF FVG + Opening Price)

**Difficulty:** Foundational — this is the prerequisite filter for all other entry models  
**Role:** Not a standalone entry — it is the bias confirmation layer that gates all other models  
**Reference:** [[concepts/business-logic/ict-narratives|ICT Narratives KB]]

---

## What This Model Is

The daily bias model is the **prerequisite filter** applied before every other entry model. It answers two questions before a trade can be taken:

1. **What direction is the market biased for today?** (HTF FVG)
2. **Am I in the correct position relative to the opening price?** (AMD location)

Without this check, any entry model — no matter how perfect — is operating without a narrative. A model taken against the daily bias will have substantially lower probability.

> "What's required is the best narrative, the best in the right direction. That is all that is required." — MrWitness, Vol 2 Class 1

---

## Step 1: Establish HTF Bias (FVG Cycle)

**The rule:** Bias = Liquidity → Inefficiency → Liquidity (alternating cycle)

1. Open your 4H chart (or 1H if 4H has no clear FVG; 2H, 3H as intermediate steps)
2. Find the most dominant FVG — the one with clear displacement (not just a small gap)
3. Determine the current position:

| Market Position | Bias | Action |
|---|---|---|
| Price inside a bullish FVG | Bullish | Look for longs every session toward BSL above the FVG |
| Price inside a bearish FVG | Bearish | Look for shorts every session toward SSL below the FVG |
| Price above a bullish FVG (FVG filled) | Neutral/Targeting liquidity | Look for longs toward the swing high (BSL); no more FVG-based longs |
| Price closed below a bullish FVG | Bias reset | Re-evaluate; possible bearish shift |
| No clean FVG visible | Liquidity-driven | Target nearest external swing high or low |

**Timeframe hierarchy:** 4H is the primary. If 4H shows multiple FVGs, move to Daily. If Daily is clear, use that.

---

## Step 2: Opening Price Position (AMD Context)

Once bias direction is established, check the intraday AMD position:

**For a bullish bias:**
- Price below midnight open → valid for longs (accumulation phase)
- Price below 8:30 open → valid for longs
- Price below 9:30 open → valid for longs
- Price above ALL three opens → wait; distribution phase; smart money distributing to retail

**For a bearish bias:**
- Price above midnight open → valid for shorts
- Price above 8:30 open → valid for shorts  
- Price above 9:30 open → valid for shorts
- Price below ALL three opens → wait; accumulation phase; not a short setup

**Maximum confluence:** On a bullish bias day, price is below midnight + 8:30 + 9:30 opens simultaneously → highest-probability long window. Enter any valid model (consolidation, E&R, OTE, reversal) at this junction.

---

## What This Looks Like in Practice

**Pre-session routine:**

1. Open 4H chart; identify dominant FVG
2. Write one sentence: "I am inside a [bullish/bearish] 4H FVG. The target is [swing high/low]."
3. Open the 15M or 1M chart; mark midnight open (orange), 8:30, 9:30
4. Determine at session open: is price below (bullish) or above (bearish) the relevant opens?
5. If YES → bias is active; look for your entry model signal within the active kill zone
6. If NO → wait; no trades until price enters the correct opening price zone

---

## When to NOT Trade (Bias Override)

The bias model also governs when to **stand aside**:

- Price is inside a bullish 4H FVG but is **above** all three opening prices → smart money distributing; don't chase longs
- Price is inside a bearish 4H FVG but is **below** all three opening prices → smart money accumulating from shorts; don't add shorts
- Small ORG (<50 handles NQ) + news week → HRLR; wait for OTE model conditions rather than 50% entries
- 4H FVG violated (closed below on a bullish FVG) → bias reset; no trades until re-evaluated
- Thursday or Friday of NFP week (unless Friday post-8:30) → stand aside regardless of bias

---

## Integration with Other Entry Models

The daily bias model is not an entry — it is a **gate**. Once bias is confirmed, apply one of these:

| Bias Status | Best Entry Models |
|---|---|
| Inside bullish 4H FVG + below midnight open | [[consolidation-model\|Consolidation]], [[expansion-retracement-model\|E&R]], [[reversal-raid-on-stops\|Reversal]] |
| HRLR + Model 2022 conditions | [[model-2022-ote\|Model 2022 + OTE]] |
| London session + Asia SSL swept | [[london-model\|London Model]] |
| SMT divergence at manipulation low | [[smt-confirmation-entry\|SMT Confirmation Entry]] |

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Checking bias on 15M only | Institutional bias lives on 4H and Daily; 15M is entry, not bias |
| Trading shorts inside a bullish 4H FVG | The FVG is an engine; shorts fight institutional positioning |
| Ignoring the opening price step | HTF bias gives direction; opening price gives the entry timing within that direction |
| Changing bias mid-session on small structures | 5M structures inside a 4H FVG are just AMD cycles; the 4H bias holds |
| Not checking ORG size | HRLR days need OTE model, not 50% entries — ORG size is a pre-session check |

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: daily-bias-model
strategy_name: Daily Bias (HTF FVG + Opening Price Filter)
version: 1
role: prerequisite_filter  # Not standalone — gates all other entry models

step_1_htf_bias:
  timeframes: [1H, 2H, 3H, 4H, Daily]
  primary_tf: 4H
  rule: Find the most dominant FVG; determine if price is inside bullish or bearish FVG
  cycle: Liquidity → FVG → Liquidity → FVG (alternating)
  states:
    inside_bullish_fvg: Look for longs toward BSL above
    inside_bearish_fvg: Look for shorts toward SSL below
    above_bullish_fvg: Look for longs toward next swing high; FVG no longer anchor
    no_clean_fvg: Target nearest external liquidity swing

step_2_opening_price:
  levels:
    - midnight_open: 00:00 Eastern
    - cme_open: 08:30 Eastern
    - rth_open: 09:30 Eastern
    - pm_open: 13:30 Eastern
  bullish_rule: Price below relevant opening price during KZ → valid for longs
  bearish_rule: Price above relevant opening price during KZ → valid for shorts
  max_confluence: Below all three AM opens (midnight + 8:30 + 9:30) simultaneously

checklist:
  - [ ] 4H FVG identified (bullish or bearish)
  - [ ] Current price position confirmed: inside FVG or above/below
  - [ ] Bias direction written out before session
  - [ ] Midnight open marked
  - [ ] 8:30 and 9:30 opens marked
  - [ ] 1:30 PM open marked (if trading PM session)
  - [ ] Opening price position checked at session start
  - [ ] ORG size noted (< 50 handles = HRLR → use OTE model)
  - [ ] Economic calendar checked (NFP Thu = avoid; FOMC AM only; etc.)
  - [ ] Active kill zone identified for the session

stand_aside_conditions:
  - HTF FVG violated (closed below bullish FVG on 4H candle)
  - Price above all three AM opens on bullish bias day (distributing)
  - Price below all three AM opens on bearish bias day (accumulating)
  - Thursday pre-NFP
  - CPI week Monday (no news)
  - Small ORG without confirming HRLR entry model available

opens_to_mark:
  - 00:00  # midnight — most important
  - 08:30  # CME open
  - 09:30  # RTH open
  - 13:30  # PM session open

timeframes:
  bias: [1H, 4H, Daily]
  confirmation: [15M, 5M]
  entry: [1M, 15s]  # Governed by the specific entry model, not this filter

integrates_with:
  - consolidation-model
  - expansion-retracement-model
  - reversal-raid-on-stops
  - london-model
  - model-2022-ote
  - smt-confirmation-entry
```
