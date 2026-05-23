---
tags: [course, module-5, smt, intermarket, cracking-correlation, divergence, neurospect]
aliases: [SMT Divergence Lesson, Cracking Correlation, Module 5 Lesson 2]
sources:
  - sources/neurospect/2026-04-18-vol4-class2-smt-divergence.md
  - sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md
  - sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md
created: 2026-04-22
updated: 2026-04-22
module: 5
lesson: 2
---

# Module 5, Lesson 2: SMT Divergence

**Prerequisites:** [[concepts/course/module-3-session-and-bias/01-power-of-three|Module 3, Lesson 1 — Power of Three]], [[concepts/course/module-5-order-flow-and-smt/01-htf-ltf-order-flow|Lesson 1 — Order Flow]]  
**Entry Model:** [[concepts/entry-models/smt-confirmation-entry|SMT Confirmation Entry Model]] — full checklist and YAML  
**Reference:** [[concepts/business-logic/ict-smt|ICT SMT Divergence KB]]

---

## Concept

SMT (Smart Money Technique / Smart Money Tool / Smart Money Timing) is an intermarket analysis tool that uses **divergence between NQ, ES, and YM** to confirm when the manipulation leg of Power of Three has completed. It is the highest-confidence reversal signal in this system — but it requires a pre-existing bias to be valid.

> "The algorithm sends a message to the source code: we hit the level. ES doesn't need to come all the way back because the source code thinks the level was already hit." — Vol 4 Class 2

The core logic is simple: NQ, ES, and YM are all connected to the same main algorithm (the "source code"). They normally move in lockstep toward the same liquidity levels. When one index diverges — fails to take the same level the others are taking — the source code registers the level as "hit" anyway. That diverging index then **does not need to return to that level**. This asymmetry signals accumulation or distribution.

---

## The Triad

| Index | Ticker | Character |
|---|---|---|
| Nasdaq 100 | NQ | Most volatile; widest moves; "the crazy one" |
| S&P 500 | ES | Most stable; preferred for standard setups |
| Dow Jones 30 | YM | Special divergence pattern; "the one that confirms" |

**Important:** All three are connected to the same source code, but each has an **independent sub-algorithm**. The sub-algorithms run differently. This is why you get SMT divergence — the sub-algorithm for ES decides it has "hit" the level even though ES price didn't reach it.

---

## What Cracking Correlation Means

"Cracking correlation" = one index breaks away from the synchronized movement of the other two at an important price level.

**Bullish cracking correlation (accumulation):**
- NQ makes a lower low (takes the sell-side liquidity level)
- YM also makes a lower low (or sometimes: YM fails while NQ takes it)
- **ES makes a higher low** (fails to take the sell-side)
- ES "recorded" the level as hit → no need to return
- Signal: smart money is **accumulating longs** at this level; reversal coming

**Bearish cracking correlation (distribution):**
- ES makes a higher high (takes the buy-side liquidity level)
- **NQ makes a lower high** (fails to take the same level)
- NQ "recorded" the level as hit (because ES and YM did)
- Signal: smart money is **distributing at this level**; reversal lower coming

> "NQ is making lower highs while ES is making higher highs, higher highs, higher highs. You actually don't need level 2 data or an extra software. Distribution. The market makers are showing you the distribution right here in both indices and then they deliver toward lower prices." — Vol 4 Class 2

---

## Price SMT vs. PDR SMT

| Type | When It Occurs | Signal |
|---|---|---|
| **Price SMT** | At a major liquidity pool (swing high/low, daily high/low, weekly high/low) — one index takes it while another fails | Strongest signal; at the exact reversal level |
| **PDR SMT** | All three indices reach the same PDA (breaker block, FVG), but only two react to it — the third fails to tap it at the same time | Subtler signal; based on PDA reaction timing, not price extreme |

**PDR SMT example (Vol 4 Class 2):**
- NQ and YM both return to a shared bullish breaker block and bounce
- ES does NOT tap the same breaker block at the same time (it arrives later or not at all)
- That "crack in the PDR reaction" = PDR SMT
- Entry: inversion FVG or next LTF entry signal in the bullish direction

---

## How to Set Up Charts for SMT

Three methods, in order of preference:

**Method 1 — Separate panes:**
1. On your main chart (NQ), click Compare/Add Symbol
2. Type ESU25 (or current front-month ES contract)
3. Select "New Pane" → ES appears below NQ on the same chart
4. Repeat for YM in a third pane
- Best for: clear visual comparison of price levels; easy to see divergence

**Method 2 — Same percentage scale (overlaid):**
1. Compare/Add Symbol → ESU25
2. Select "Same Percentage Scale"
3. Change ES to a line chart (thinner)
4. Adjust color (e.g., white or orange) so NQ and ES are visually distinct
- Best for: quick glance during live trading; both on one chart

**Method 3 — Three separate templates:**
- Maintain three chart windows: ES | YM | NQ side by side
- Best for: pre-market analysis sessions, not live trading

**Contract note:** Always use the **current front-month contract** for each index. Near quarterly rollover, the expiring contract starts "cracking" due to volume drain — this looks like SMT but is just stale data. Check CME volume to confirm which contract is dominant.

---

## Where SMT Appears

SMT is most powerful at these locations:

1. **The manipulation leg of Power of Three** — the final sweep below (bullish day) or above (bearish day) the midnight open, where smart money needs to trap retail before the real direction begins. SMT at this exact sweep is the clearest signal.

2. **At the Asian range boundaries** — London takes the Asia low; the Asia SSL sweep is where SMT often prints at the London KZ.

3. **Session highs/lows** — previous day high/low, previous week high/low; these are the "big pools of liquidity."

4. **After an MSS** — if a market structure shift fired but you missed the OTE entry, SMT at the next consolidation low (during the retracement) gives you another entry signal.

---

## Bullish SMT Entry Process (Step by Step)

1. Confirm HTF bias: inside bullish 4H FVG + price below midnight open
2. Price sweeps below an important sell-side liquidity level (AMD manipulation leg)
3. Watch all three indices: NQ and/or YM takes the SSL; **ES makes a higher low**
4. Cracking correlation confirmed → accumulation signal
5. Switch to entry TF (1M–5M)
6. Look for LTF entry signal at the reversal zone:
   - Inversion FVG (bearish FVG that price closed above)
   - Rejection block (opening price of the sweep candle)
   - CSD (down-close candles whose opening price is breached)
7. Enter with stop below the SSL sweep low
8. Target: first deviation beyond the ITH → runner to -2/-2.5

---

## Trusting the Program After SMT

Once SMT fires at a liquidity sweep, it does more than signal a single trade — it confirms the **program switch**. The buy program (or sell program) is now active for the session.

> "How do you know to trust a buy program? The market has taken a big sell-side pool. Or at least a minor one. Once that happens, whatever model you use — even a breakout model — is going to work." — YouTube: +1000 Points NQ (2026-03-04)

After a confirmed bullish SMT at the manipulation low:
- Every subsequent pullback within the session is a potential long entry
- Standard models (E&R, OTE, consolidation) all have higher probability
- LRLR conditions are likely to prevail → entries at OBs and FVGs

When NO opposing liquidity has been taken before price moves in your direction → **do not trust the program**. Expect HRLR and deep retracements regardless of SMT-like signals.

---

## Worked Example: Vol 4 Class 2 Live Session

**Distribution scenario (live NQ vs. ES overlay):**

1. ES is making higher highs, higher highs, higher highs on the 1H chart
2. NQ is making lower highs at the same points (NQ cannot take the same levels ES is taking)
3. At the most recent high: ES takes out the hourly swing high; NQ makes a lower high
4. This is bearish cracking correlation → distribution in progress
5. Price drops from the distribution zone toward the sell-side target

**Accumulation scenario (same session, later):**

1. At the day's sell-side liquidity zone: NQ makes a new lower low; ES makes a higher low
2. YM also fails to take the NQ's low
3. Cracking correlation at the SSL → accumulation signal → bullish reversal
4. Entry: wait for LTF inversion FVG or rejection block at the sweep level
5. Price reverses and delivers to the buy-side targets

---

## SMT vs. Six Sisters (Coming in Vol 4)

**Do not confuse these:**

- **SMT (this lesson):** Intermarket divergence between NQ, ES, YM at a liquidity level → accumulation or distribution signal
- **Six Sisters (future topic):** A different intramarket pattern — not yet captured in the curriculum

If you see reference to "six sisters" in streams, that is the informal term MrWitness uses for NQ when it is lagging behind ES and YM in a trend (not the same as SMT). The actual "Six Sisters" concept as a formal entry model is a separate Vol 4 class not yet available.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Using SMT without a pre-existing bias | Divergence without bias = random interpretation; need to know which direction to favor first |
| Acting on SMT without a PDA entry signal | SMT identifies the zone; still need inversion FVG, rejection block, or OTE block as the actual trigger |
| Trading SMT at rollover without checking contracts | Stale contract creates false cracking correlation |
| Trading SMT outside kill zones | Lower probability; manipulation legs happen inside kill zones |
| Confusing PDR SMT with Price SMT | PDR SMT is a subtler, lower-probability signal; requires extra caution |

---

## Homework

1. Set up a three-panel or two-pane SMT chart layout (NQ + ES, or NQ + ES + YM).
2. For five consecutive trading days: identify the manipulation leg of Power of Three (the sweep below/above midnight open).
3. At each manipulation leg: check the three indices. Was there cracking correlation (one made the extreme, others didn't)?
4. Record: how often did SMT appear at the manipulation leg? What was the outcome (reversal vs. continuation)?
5. Track your chart setup: which method (new pane vs. overlay) lets you spot the divergence fastest?

---

## See Also

- [[concepts/entry-models/smt-confirmation-entry|SMT Confirmation Entry Model]] — full checklist and YAML strategy block
- [[concepts/course/module-3-session-and-bias/01-power-of-three|Module 3, Lesson 1 — Power of Three]] — the manipulation leg where SMT most frequently appears
- [[concepts/course/module-5-order-flow-and-smt/01-htf-ltf-order-flow|Lesson 1 — Order Flow]] — LRLR conditions that follow a confirmed SMT program switch
- [[concepts/business-logic/ict-smt|ICT SMT Divergence KB]] — full reference including NQ/ES/YM trending behavior and trust-the-program framework
