---
tags: [entry-model, smt, intermarket, divergence, confirmation, neurospect]
aliases: [SMT Entry, SMT Divergence Entry, Cracking Correlation Entry, SMT Confirmation]
sources:
  - sources/neurospect/2026-04-18-vol4-class2-smt-divergence.md
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md
created: 2026-04-22
updated: 2026-04-22
---

# Entry Model: SMT Confirmation Entry

**Difficulty:** Intermediate — requires multi-instrument charting setup and pre-existing bias  
**Frequency:** 1–3 times per week on the cleanest setups; present almost daily but not always actionable  
**Reference:** [[concepts/business-logic/ict-smt|ICT SMT Divergence KB]]

---

## What This Model Is

SMT (Smart Money Technique / Smart Money Tool) confirmation entry uses **intermarket divergence** between NQ, ES, and YM to confirm the manipulation leg of Power of Three has completed. It is the highest-confidence signal that a reversal is occurring — not a standalone entry, but the strongest possible confluence when combined with a pre-existing bias and a PDA.

> "How do you know to trust a buy program? The market has taken a big sell-side pool. Or at least a minor one. Once that happens, whatever model you use — even a breakout model — is going to work." — MrWitness, YouTube: +1000 Points NQ (2026-03-04)

The three indices (NQ, ES, YM) run on the same algorithmic source code but with independent sub-algorithms. They normally move in tandem. When one breaks correlation at an important liquidity level, it signals institutional accumulation (bullish) or distribution (bearish).

---

## The Triad

| Index | Ticker | Character |
|---|---|---|
| Nasdaq 100 | NQ | Most volatile; fastest moves; execution must be quick |
| S&P 500 | ES | Most stable; preferred by MrWitness for standard setups |
| Dow Jones 30 | YM | Special character; diverges differently; often the confirming index |

---

## SMT Signal Types

### Bullish SMT (Accumulation)

**Condition:** At a major sell-side liquidity level (swing low):
- NQ makes a **lower low** (takes the level)
- ES makes a **higher low** (fails to take the same level)
- OR: ES makes the lower low while YM fails → ES is the confirming divergence

**Signal:** Smart money is accumulating long positions. The index that does NOT make the lower low "recorded" the level as hit in the source code — it doesn't need to go back.

**Entry:** After the SMT signal at the manipulation low, look for an inversion FVG, rejection block, or OTE block at the reversal zone. Enter with a LTF change of structure confirming the reversal.

### Bearish SMT (Distribution)

**Condition:** At a major buy-side liquidity level (swing high):
- ES makes a **higher high** (takes the level)
- NQ makes a **lower high** (fails to take the same level)
- NQ's inability to make new highs while ES does = distribution signal

**Signal:** Smart money is distributing (selling) as retail buys the breakout. Enter short with PDA confirmation.

---

## Context Requirements (Non-Negotiable)

This model has strict prerequisites — without them, any correlation divergence is random noise:

1. **Pre-existing HTF bias** (from [[concepts/entry-models/daily-bias-model|Daily Bias Model]]). SMT is a confirmation of an existing bias, not a reason to create one.

2. **SMT at the manipulation leg.** Power of Three's manipulation leg is where SMT most frequently appears. Price sweeps below the midnight open (bullish day), one index makes a lower low, another doesn't — that is the classic setup.

3. **Correct session timing.** SMT at the London kill zone or NY AM kill zone is highest probability. SMT during lunch or pre-market outside kill zones is much lower probability.

4. **Combine with a PDA entry.** After identifying the SMT signal, wait for the entry signal in the entry timeframe: an inversion FVG, a rejection block, an OTE block, or a CSD at the reversal zone.

---

## Price SMT vs. PDR SMT

| Type | Description | Use |
|---|---|---|
| **Price SMT** | One index makes a lower low at a price level while another makes a higher low at that same level | Classic confirmation of manipulation completion at a price swing |
| **PDR SMT** | One index fails to tap the same PDA (OB, FVG) at the same time as the others | More granular; used when indices share a PDA level but one doesn't react |

**PDR SMT example:** NQ and YM both bounce from a shared bullish breaker block. ES does not tap it at the same time. That crack in the PDR reaction is the SMT. Enter on an inversion FVG or the next LTF signal.

---

## Setup Conditions

- [ ] HTF FVG bias confirmed (4H bullish FVG for longs; 4H bearish FVG for shorts)
- [ ] Opening price position correct (price below midnight open for longs)
- [ ] Price at a major liquidity level (swing high or swing low — at least 15M magnitude)
- [ ] SMT divergence confirmed: one index makes new extreme; another fails to (at the same level, same timeframe)
- [ ] Kill zone active (London or NY AM for highest probability)
- [ ] No manual intervention signals (unusual speed / magnitude in one direction before the SMT)
- [ ] Contract rollover not in effect (check futures contract volume — use the fresher contract)

---

## Entry Process (Step by Step)

1. **Set up charts** — three panels or overlaid charts: ES | NQ | YM. Use the current front-month contract for each.
2. **Confirm HTF bias** (4H FVG direction + opening price position)
3. **Identify the manipulation leg** — price sweeping below (bullish) or above (bearish) an important level during the KZ
4. **Watch for SMT:** At the sweep level, does one index make the new extreme while another fails?
5. **Confirm the SMT:** The failing index is the signal — it "already recorded" the level
6. **Switch to entry TF (1M–5M):** Look for the first LTF entry signal at the reversal zone:
   - Inversion FVG (bearish FVG that price has closed above → now bullish)
   - Rejection block (opening price of the sweep candle)
   - OTE block (if deep enough retracement)
   - CSD (group of down-close candles whose opening price is breached)
7. **Enter** on the LTF signal with stop below the sweep low (or above sweep high for shorts)
8. **Target:** First deviation beyond the swing on the opposite side; run to -2/-2.5 deviation if inside an HTF FVG

---

## Trusting the Buy/Sell Program

When SMT confirms, the buy or sell program has been activated — this means **all subsequent entry models in that session become higher probability**. The program switch is the market saying: "This direction is now in effect."

**Trust the buy program when:**
- A sell-side liquidity pool was taken (15M swing low or larger) before the reversal
- After the sweep, bullish PDAs hold and FVGs stay open (LRLR begins)
- SMT at the sweep = strongest possible confirmation

> "Once that happens, whatever model you use — even a breakout model — is going to work." — Vol 4 Class 2

**Do NOT trust SMT when:**
- No opposing liquidity was taken before the signal (HRLR conditions without a sweep = false SMT)
- Futures contracts are near rollover (stale contract creates false divergence)
- Manual intervention is occurring (both indices may crack simultaneously)

---

## Strongest/Weakest Index by Day Type

In trending conditions, the indices contribute differently:

| Day Type | Weakest Index | Trading Implication |
|---|---|---|
| Strongly bullish | NQ ("sixth sister") | Use ES for cleaner long entries; NQ will lag |
| Strongly bearish | ES (holds up longer) | NQ leads the decline; YM provides clearest confirmation |

If YM and ES made the day's high/low while NQ is still lagging → the bullish/bearish program is still intact. NQ will eventually follow.

---

## Contract Rollover — Critical Caution

Near futures contract rollover (quarterly), the expiring contract starts "cracking" as volume drains. This looks like SMT but is just stale data.

**Protocol:**
1. Check CME futures data for NQ and ES volume
2. When next contract volume exceeds front month → switch immediately to the fresher contract
3. If you see unexpected cracking near rollover → check contract dates before calling it an SMT signal

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Trading SMT without pre-existing bias | Divergence without bias is random noise |
| Acting on SMT without a PDA entry signal | The SMT identifies the zone; the PDA (inversion FVG, rejection block) is the actual trigger |
| Trading SMT outside kill zones | SMT during lunch or off-hours has much lower follow-through |
| Not switching contracts at rollover | Stale contract = false SMT; buying/selling against a phantom signal |
| Using SMT as a trend-following signal | SMT is a reversal confluence tool, not a continuation signal |

---

# --- MACHINE_READABLE_STRATEGY ---

```yaml
strategy_id: smt-confirmation-entry
strategy_name: SMT Confirmation Entry (Intermarket Divergence)
version: 1
direction: long_or_short  # Signal is symmetric; direction from HTF bias
role: confirmation_confluence  # Highest-confidence confluence layer; not standalone

instruments:
  triad: [NQ, ES, YM]
  primary_watch: ES  # Most stable; clearest divergence
  confirming: YM    # Often the index that "cracks" first

smt_signal:
  bullish:
    condition: NQ (or YM) makes lower low; ES makes higher low at the same level
    meaning: Smart money accumulating; manipulation leg complete
  bearish:
    condition: ES makes higher high; NQ makes lower high at same level
    meaning: Smart money distributing; manipulation leg complete
  pdr_variant:
    condition: Two indices tap a shared PDA; one does not react
    entry: Inversion FVG or next LTF signal at the failing index's reaction zone

setup_conditions:
  - HTF FVG bias confirmed on 4H
  - Opening price position correct (below midnight for longs; above for shorts)
  - Price at major liquidity level (minimum 15M swing magnitude)
  - SMT divergence confirmed at that level during active kill zone
  - Contract rollover not in effect (fresher contract in use)
  - No manual intervention signals

entry:
  timeframe: 1M to 5M
  signals_in_priority_order:
    - Inversion FVG at the reversal zone
    - Rejection block (opening price of the sweep candle)
    - CSD (breach of down-close candle opening prices)
    - OTE block (if price retraced deep enough)

stop_logic: Below the liquidity sweep low (bullish) or above the sweep high (bearish)

target_logic:
  first_target: First deviation beyond opposite swing (-1 deviation)
  runner_target: -2 to -2.5 deviation; extend to -4/-7 if inside major HTF FVG (HPDL)

checklist:
  - [ ] 4H FVG bias confirmed
  - [ ] Opening price position correct (below midnight open for longs)
  - [ ] Price at major liquidity level (15M+ swing)
  - [ ] Kill zone active (London or NY AM = highest probability)
  - [ ] Three-chart setup ready: ES | NQ | YM (current front-month contracts)
  - [ ] Contract rollover check: using fresher contract
  - [ ] SMT signal confirmed: one index new extreme; other fails
  - [ ] LTF entry signal identified at reversal zone (inversion FVG / rejection block / CSD)
  - [ ] Stop placed below sweep low (or above sweep high for shorts)
  - [ ] Deviation targets pre-marked (-1 partial, -2/-2.5 runner)

timeframes:
  bias: [1H, 4H, Daily]
  smt_identification: [15M, 1H]
  entry: [1M, 5M]

avoid_conditions:
  - No opposing liquidity taken before SMT signal (HRLR without sweep = false signal)
  - Contract rollover (stale contracts produce false divergence)
  - Manual intervention in progress
  - SMT signal outside kill zones (lunch, overnight without London KZ)
  - No pre-existing HTF bias

trust_program_when:
  - Sell-side liquidity pool taken before bullish SMT (minimum 15M swing low)
  - After sweep: bullish PDAs hold and FVGs stay open (LRLR begins)

related_models:
  - daily-bias-model       # Prerequisite — HTF bias must be established first
  - reversal-raid-on-stops # SMT often appears at the same sweep as raid-on-stops
  - consolidation-model    # SMT at Asia/London consolidation boundary
  - london-model           # Classic London SMT at Asia SSL sweep
```
