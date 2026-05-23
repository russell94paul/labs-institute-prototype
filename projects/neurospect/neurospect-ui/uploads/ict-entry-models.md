---
tags: [concept, business-logic, ict, entry-models, fvg, order-blocks, ote, model-2022, csd, neurospect]
aliases: [ICT Entry Models, FVG, Fair Value Gap, Order Block, OB, OTE, Optimal Trade Entry, Model 2022, Propulsion Block, Rejection Block, Breaker Block, BPR, IOFED, BAG, OPE Order Block]
sources:
  - sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md
  - sources/neurospect/2026-04-18-vol1-class1-notes.md
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md
  - sources/neurospect/2026-04-18-vol1-class3-notes.md
  - sources/neurospect/2026-04-18-vol3-class5-model-2022-ote-csd.md
  - sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md
created: 2026-04-18
updated: 2026-04-22
---

# ICT Entry Models

Entry models are the specific PDA (Premium/Discount Array) patterns and zones that trigger trade entries **after** narrative, structure, and liquidity context are established. They are confirmation signals — validity depends entirely on alignment with higher-timeframe bias and the current draw on liquidity.

---

## Three-Step Execution Framework (Axel / AXL)

This is the universal entry process used by AXL for every trade:

1. **Step 1 — High Timeframe (15M or above):** Find the important confluence (main PDA — FVG, OB, rejection block, liquidity level)
2. **Step 2 — Lower Timeframe (15M or below):** Find plus confluences that support the analysis (additional FVG or OB that reinforces the HTF idea)
3. **Step 3 — Entry Timeframe (1M or below):** Look for change of structure, confirmations, and entry

Without all three steps, the trade is considered high-risk. Step 3 is where entries are taken (15s, 5s, or 1M timeframes).

---

## Fair Value Gap (FVG)

Three-candle imbalance where candle 1's high does not touch candle 3's low (bullish) or candle 1's low does not touch candle 3's high (bearish). Candle 2 is the gap.

See [[ict-liquidity]] for full FVG explanation (BISI, SIBI, mitigation rules).

**Entry precision:**
- Best entries: **at or below the CE** (consequent encroachment = 50% of the gap) for longs
- Most precise: just **one tick below candle 3's low** (bullish FVG)
- Enter above 50%: don't try to enter at the 50% — you'll miss trades where price only kisses the top and runs
- If two FVGs exist on the same expansion: enter on the first (upper) and allow stop for the second

**Inversion FVG:** A bearish FVG that price closes above becomes a bullish support zone. When price returns to it and respects the 50%, it's now trading as a bullish FVG.

**IOFED:** First FVG of the expansion. If price returns but does NOT close below the CE → highest-probability entry. See [[ict-liquidity]].

**BAG (Breakaway Gap):** FVG that price never returns to. Occurs during LRLR (low-resistance liquidity run) conditions. Do not expect these to fill before continuation.

---

## Order Blocks (OB)

An order block is the **last opposing candle** before a significant move. It represents institutional order accumulation.

**Bullish OB:** Single down-close candle immediately before an upward expansion  
**Bearish OB:** Single up-close candle immediately before a downward expansion

**Rules (AXL's approach):**
- Use the **body only** (not wicks) for measuring the OB range
- The OB's **opening price** is the defining level — not the high or low
- A reaction at the OB's opening price = algorithmic signature
- Entry: at or above the 0.5% (50%) of the OB body for longs; at or below for shorts

**Propulsion Block:**  
An order block that forms **after** price has already respected a prior order block of the same type. The sequence: price taps OB #1 → bounces → creates OB #2 during that bounce. OB #2 is the propulsion block — it signals that speed and velocity is activating. Prefer the propulsion block over a standalone OB.

> "The order block formed after respecting the first one becomes your propulsion block." — YouTube: First Week of March (2026-03-07)

**OPE Order Block (sniper entry):**  
An order block that has a **fair value gap in its upper portion** (for bullish). This is the highest-probability entry combination. When the market retraces into the OB and the FVG in the upper quadrant is tapped:
- The FVG is the sniper entry — most precise; only requires a few ticks of drawdown
- Stop loss below the three candles that create the FVG (not the full OB)
- The FVG in the upper quadrant of the OB will typically stay open and become a breakaway gap once the trade works

> "Whenever I see a fair value gap in the upper portion of the order block, that's going to be your sniper entry." — YouTube: First Week of March (2026-03-07)

---

## Rejection Block

The **candle that takes liquidity** and then has a sharp reaction. Specifically:
- The opening price of the candle that sweeps the liquidity level is the rejection block
- Not just the wick — the opening price of the sweeping candle
- After a MSS forms, expect price to return to the rejection block level and respect it
- Confirmation: immediate reaction (fast bounce) off the rejection block level

---

## Breaker Block

An order block that price has **closed through** (invalidated) and then revisits from the other side. The violated OB now acts as resistance (for a bullish → bearish flip) or support (for a bearish → bullish flip).

---

## Volume Imbalance

Similar concept to FVG — an area where price moved so fast that volume was one-sided. Treated like an FVG for entries. AXL notes: big wicks act like FVGs / volume imbalances — "the market always comes back for the 50% of the wick."

---

## Balanced Price Range (BPR)

A range where price has delivered **both buy-side and sell-side** within it — it is now "balanced." Two characteristics:
- No single wick; both sides have been delivered
- Price that re-enters a BPR is not expected to deliver a clean 2022 model or OTE
- When price approaches a BPR, expect choppy back-and-forth (HRLR conditions)
- A BPR can be used as a consolidation range — look for the EQ and a PDA near it

---

## Optimal Trade Entry (OTE)

The OTE is a deep Fibonacci retracement into the **golden zone** — the 62%–79% area. The midpoint (0.705) is the most precise level.

**When to use OTE instead of the 50% expansion entry:**
- High-resistance liquidity run conditions
- Market structure shift where price **does not retrace to 50% discount** after the MSS
- This signals Model 2022 conditions → expect deep OTE retracement

**OTE Block:** An order block that is **in concert with** (at the same level as) the 62–79% Fibonacci zone. This is the highest-probability entry combination.

---

## Model 2022 + OTE

The complete model for "deep retracement" entries:

**Setup conditions:**
1. A market structure shift (MSS) occurs — ITL is taken out
2. Price expands higher but **fails to return to 50% discount** → Model 2022 conditions
3. Expect a deep retracement to the OTE zone (62–79%)

**Entry:**
1. Identify the intermediate-term low (ITL) price leg — from ITL to the expansion swing high
2. Measure 62–79% Fibonacci on this leg
3. Find the bullish OB (highest down-close candle, body only) in the OTE zone
4. Enter at/above the 50% of the OTE block
5. Stop below the OTE block low (a true OB's closing price should not be touched)

**Change in State of Delivery (CSD)** is the key confirmation before or instead of waiting for a full MSS:
- Group of down-close candles in discount whose **opening price is breached** = CSD
- CSD often precedes the MSS — take the CSD entry and let the MSS be a post-entry confirmation
- "I want to see price trade above this opening price" = looking for CSD

---

## Kill Zone Context

All entry models must be taken **inside an active kill zone**:
- Asia: 8 PM – midnight
- London: 2 AM – 5 AM
- NY AM: 8:30 AM – 11:30 AM
- NY PM: 1:30 PM – 4:00 PM

Outside these windows, avoid entries (especially on high-impact news days).

---

## Entry Checklist

1. **HTF narrative correct?** (inside bullish/bearish FVG on 4H)
2. **Opening price position correct?** (below open for longs, above for shorts)
3. **DOL identified?** (1H/15M swing high or low)
4. **External AND internal liquidity swept?** (highest-probability condition)
5. **PDA in discount/premium zone?** (FVG or OB at or below 50% for longs)
6. **Change of structure in entry timeframe?** (1M or below — high closes above internal high)
7. **Stop logic clear?** (below the FVG or below the OTE block)

---

## See Also

- [[ict-market-structure]] — MSS and CSD prerequisites for Model 2022
- [[ict-liquidity]] — FVG mechanics, BISI/SIBI, IOFED, BAG
- [[ict-narratives]] — consolidation, expansion, retracement models
- [[ict-smt]] — SMT as confluence for entry timing
- [[ict-deviations]] — OTE deviation levels for precise exits
