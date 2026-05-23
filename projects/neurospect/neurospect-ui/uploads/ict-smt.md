---
tags: [concept, business-logic, ict, smt, intermarket, order-flow, neurospect]
aliases: [SMT, Smart Money Technique, Smart Money Tool, SMT Divergence, Cracking Correlation, The Triad, NQ ES YM]
sources:
  - sources/neurospect/2026-04-18-vol4-class2-smt-divergence.md
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-20-stream-0830-nfp-fri-tape-reading.md
  - sources/neurospect/2026-04-20-stream-tue-10-fed-chair-testifies.md
  - sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md
created: 2026-04-18
updated: 2026-04-22
---

# SMT Divergence

SMT (Smart Money Technique / Smart Money Tool) is an intermarket analysis tool that uses divergence between correlated equity indices to confirm or signal a reversal. It is a **confluence tool**, not a standalone entry signal — you need a pre-existing bias before using it.

## The Triad

SMT is applied using the three major US equity futures indices:

| Name | Futures Ticker | Character |
|---|---|---|
| Nasdaq 100 | NQ | Most volatile, widest moves, fastest execution required |
| S&P 500 | ES | Most stable, mid-range volatility, preferred by MrWitness |
| Dow Jones 30 | YM | Special — diverges differently; often the confirming index |

These three indices run on the same algorithmic source code but with independent sub-algorithms. They normally **move in tandem**, so when one breaks correlation, it signals institutional intent.

---

## Cracking Correlation

A cracking (broken) correlation occurs when **one index fails to do the same thing as the other two** at an important price level. This is the core SMT signal.

When the correlation cracks:
- The algorithm has "recorded" the level as hit (because 2 of 3 hit it)
- The non-confirming index will not need to reach that level
- This creates **accumulation** (bullish) or **distribution** (bearish) at those levels

> "The algorithm sends a message to the source code: we hit the level. ES doesn't need to come all the way back because the source code thinks the level was already hit." — Vol 4 Class 2

---

## Bullish SMT (Accumulation Signal)

**Condition:** NQ and/or YM make a lower low at a major liquidity level, while **ES makes a higher low** (or fails to take that same low).

- Signals: smart money is accumulating long positions
- The ES "cracking" away from the lower low is the tell
- Expect a reversal higher from that zone

---

## Bearish SMT (Distribution Signal)

**Condition:** ES makes higher highs while **NQ makes lower highs** at a major liquidity level.

- Signals: smart money is distributing (selling) as retail buys the breakout
- NQ's inability to make new highs is the tell
- Expect a reversal lower from that zone

---

## Price SMT vs. PDR SMT

| Type | Description |
|---|---|
| **Price SMT** | One index makes lower low / higher low at a price level (big pool of liquidity) that another index takes or fails to take |
| **PDR SMT** | One index fails to tap the same PDA (order block, FVG) at the same time as the others — a fractured reaction at a shared PDA level |

PDR SMT example: NQ and YM both return to and bounce from a bullish breaker block; ES does not tap it at the same time. That crack in PDR reaction is the SMT. Enter on an inversion FVG or the next entry signal in the direction of the reversal.

---

## How to Set Up Charts

**Option 1 — Separate panes:**  
In TradingView: Add Symbol → ES (or NQ/YM) → New Pane. Shows both price charts stacked — easy to compare highs/lows visually.

**Option 2 — Overlay (same scale):**  
Add Symbol → Same Percentage Scale → Change to line chart → adjust color/thickness. Both instruments on one chart, easier for quick glances during live trading.

**Option 3 — Three-panel template:**  
Separate templates/charts for each: ES | YM | NQ side by side. Best for full analysis sessions.

---

## Context Requirements

1. **Have a bias first.** SMT is most powerful when you already know the market is bullish or bearish (via HTF FVG + opening price position from [[ict-narratives]]).
2. **SMT at the manipulation leg.** The manipulation leg of Power of Three is where SMT most frequently appears — price sweeps below midnight open, one index makes a lower low, another doesn't → accumulation, reversal imminent.
3. **Combine with a PDA entry.** After identifying SMT, wait for the entry signal: inversion FVG, rejection block, or OTE block at the reversal zone.

## Trusting the Buy/Sell Program

SMT divergence is one of the signals that a **program switch** has occurred. Once confirmed, all entry models become higher probability.

**Trust the buy program when:**
- The market has taken a sell-side liquidity pool (at minimum a 15-minute swing low) before the reversal
- After this sweep, bullish PDAs start holding and FVGs stay open (LRLR conditions begin)
- SMT at the sweep = strongest possible confirmation

**Trust the sell program when:**
- The market has taken a buy-side liquidity pool before the reversal
- Bearish PDAs start holding and FVGs stay open to the downside

> "How do you know to trust a buy program? The market has taken a big sell-side pool. Or at least a minor one. Once that happens, whatever model you use — even a breakout model — is going to work." — YouTube: +1000 Points NQ (2026-03-04)

Conversely, if the market is delivering toward your bias WITHOUT taking any opposing liquidity first, expect high-resistance conditions and deep retracements even after SMT signals.

## NQ vs. ES vs. YM: Strongest/Weakest in Trending Markets

In strongly trending conditions, the three indices do not contribute equally:

- **Weakest asset on a bullish day:** NQ ("the sixth sister" — lags behind, doesn't take highs as cleanly)
  → Use ES for cleaner long entries on bullish trending days
- **Weakest asset on a bearish day:** ES often holds up longer than NQ or YM
  → NQ can lead the decline; YM provides the clearest confirmation

Live trading note (streams): "YM and ES made higher highs for the day; NQ is the sixth sister, still dancing." → MrWitness uses this to confirm the bullish bias is still intact even when NQ lags.

This is distinct from the "Six Sisters" concept (a separate intramarket pattern, Vol 4 future class). Here "sixth sister" is informal stream language for the lagging index.

Source: `sources/neurospect/2026-04-20-stream-0830-nfp-fri-tape-reading.md`, `sources/neurospect/2026-04-20-stream-tue-10-fed-chair-testifies.md`

---

## SMT in the London Model / Consolidation Model

In the 2022 model (Vol 1 Class 2), MrWitness demonstrates SMT at the London session low:
- Asia consolidates; London takes the SSL (Asia low)
- At that exact SSL, ES fails to make a new lower low while NQ does → classic bullish SMT
- Entry: expansion retracement model or consolidation model above the EQ

---

## SMT vs. Six Sisters

A related but **different** concept called "Six Sisters" is referenced in Vol 4 as a future topic (not yet in the captured curriculum). Do not confuse the two:
- **SMT**: intermarket divergence between NQ/ES/YM
- **Six Sisters**: a different intramarket pattern (details pending curriculum capture)

---

## See Also

- [[ict-market-structure]] — SMT confirms market structure at the ITL/ITH
- [[ict-liquidity]] — SMT often signals that a liquidity sweep is completing
- [[ict-narratives]] — SMT is most powerful at the manipulation leg of Power of Three
- [[ict-entry-models]] — entry patterns to use after SMT signals accumulation/distribution
- [[ict-order-flow]] — SMT as an order flow distribution/accumulation signal
- [[ict-live-commentary]] — live "cracking correlation" calls and trust-the-program framework in practice
