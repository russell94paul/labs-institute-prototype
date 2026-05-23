---
tags: [course, module-3, sessions, kill-zones, opening-prices, neurospect]
aliases: [Kill Zones Lesson, Session Windows, Module 3 Lesson 2]
sources:
  - sources/neurospect/2026-04-18-vol2-class2-notes.md
  - sources/neurospect/2026-04-18-vol2-class1-power-of-three.md
  - sources/neurospect/2026-04-18-vol2-class1-notes.md
created: 2026-04-22
updated: 2026-04-22
module: 3
lesson: 2
---

# Module 3, Lesson 2: Session Kill Zones

**Prerequisites:** [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]]  
**Reference:** [[concepts/business-logic/ict-narratives|ICT Narratives KB]]

---

## Concept

Kill zones (KZs) are specific time windows during which the highest-probability setups form. The market engineers liquidity before each KZ and then delivers inside it. **One of the four KZs will set the high or low of the day** — your job is to be positioned before that extreme prints.

> "That's the essence: marry time (the KZs) with place (the right opening price), and let Power of Three do the rest." — Vol 2 Class 2 Notes

---

## The Five Kill Zones

| Session | Time (Eastern) | Opening Price Anchor | Notes |
|---|---|---|---|
| **Asia** | ~7:00 PM – midnight | 7:00 PM / 6:00 PM session open | Often consolidation; can be quirky; worth separate study |
| **London** | 2:00 AM – 5:00 AM | Midnight (00:00) open | Takes one side of Asia, delivers to the other; classic 2022 model |
| **NY AM** | 8:30 AM – 11:30 AM | 8:30 open + 9:30 open | Most active; 8:30 creates one side; 9:30 may continue or manipulate |
| **Lunch** | ~11:30 AM – 1:30 PM | — | Lower energy; transition; generally avoid new entries |
| **NY PM** | 1:30 PM – 4:00 PM | 1:30 PM open | Often sets the final high/low of the session |

The **London kill zone** most frequently sets the HOD or LOD of the day, followed by NY AM.

---

## How Kill Zones Work: The Rule

Apply the AMD framework from Lesson 1 to each session's opening price:

- **Bullish day:** During the KZ, if price is below the relevant opening price → look for longs back through and away from it
- **Bearish day:** During the KZ, if price is above the relevant opening price → look for shorts back through and away from it

This is the entire edge. Each KZ has an anchor opening price; each opening price is an AMD cycle.

---

## NY AM — The Two-Part Session

NY AM requires extra attention because it has **two distinct opening prices**:

**8:30 Open (CME futures open):**
- Often creates one side of the session (the HOD or LOD)
- A manipulation below 8:30 on a bullish day = accumulation for the 9:30 continuation

**9:30 Open (RTH open):**
- May **continue** the 8:30 move (if the manipulation completed at 8:30)
- May **manipulate** the 8:30 high/low (AMD cycle restarts with 9:30 as anchor)
- Use both 8:30 and 9:30 as "magnets" and decision lines

**Example (bullish day):**
- 8:30 opens, price drops below 8:30 open (manipulation)
- Price begins to rally (accumulation complete)
- 9:30 opens, price drops again below 9:30 open (second manipulation leg)
- Price then rallies through both opens and delivers to the target

This is why the highest probability condition is: price below midnight + 8:30 + 9:30 opens simultaneously.

---

## Highest-Probability Setup

The confluence of multiple opening prices below (or above) price is the maximum confidence signal.

**For longs (bullish day):**
- Price below midnight open ✓
- Price below 8:30 open ✓
- Price below 9:30 open ✓
- All three = highest probability long; look for longs toward the buy-side target

**For shorts (bearish day):**
- Price above midnight open ✓
- Price above 8:30 open ✓
- Price above 9:30 open ✓
- All three = highest probability short; look for shorts toward the sell-side target

---

## Opening Range Gap (ORG)

The ORG is the gap between the previous RTH close (~4:00 PM) and today's 9:30 RTH open.

- **Large ORG (>50 handles on NQ):** Trending conditions; lower-resistance delivery expected; LRLR likely
- **Small ORG (<50 handles on NQ):** Choppy, overlapping delivery expected; HRLR likely; use OTE model

See [[concepts/business-logic/ict-order-flow|ICT Order Flow]] for LRLR/HRLR framework.

---

## Targets at Each Kill Zone

Favor these levels as targets in each session:

- **Asia KZ targets:** prior-session highs/lows; Asia session EQ; FVGs from the previous NY PM
- **London KZ targets:** Asia session high/low (London sweeps one side and delivers to the other)
- **NY AM targets:** Previous day high/low; overnight displacement levels; 4H/Daily FVG boundaries
- **NY PM targets:** Session extremes; prior PM high/low; weekly targets

Use standard entry tools (FVG, OB, rejection block, CE) around the opening-price lines inside each KZ.

---

## Kill Zone Quick Reference

Mark these five levels on every chart before the session:

1. 6:00 PM / 7:00 PM (Asia session open)
2. 00:00 (midnight open — London anchor + daily anchor)
3. 8:30 (CME futures open)
4. 9:30 (RTH open)
5. 1:30 PM (PM session open)

Then answer three questions:
1. What is my bias today? (See [[concepts/course/module-3-session-and-bias/04-daily-bias|Lesson 4]])
2. Am I below (bullish) or above (bearish) the relevant opening price for the active KZ?
3. What is the nearest liquidity/PDA target in the direction of the bias?

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Trading outside kill zones | Low probability; price engineering, not delivery |
| Using the wrong opening price anchor | Asia uses 7 PM open, not midnight; London uses midnight open |
| Expecting 9:30 to always continue 8:30 | Sometimes 9:30 reverses 8:30; read which opening price is below and which is above |
| Entering during lunch (11:30–1:30) | Transitional chop; next session needs to reset |
| Ignoring the ORG size | Small ORG days need OTE entries, not standard 50% discount entries |

---

## Homework

1. **Each day before the open:** mark all five opening prices on a clean chart. Color-code them distinctly.
2. **Observe for one week:** which kill zone sets the HOD? Which sets the LOD? Track in your journal.
3. **On NY AM days:** note whether 9:30 continues 8:30's move or manipulates it. Record which outcome.
4. **On a bullish day:** check if price was below all three AM opens (midnight, 8:30, 9:30) at any point. Was that the LOD?

---

## See Also

- [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]] — AMD framework applied inside each KZ
- [[concepts/course/module-3-session-and-bias/04-daily-bias|Lesson 4 — Daily Bias]] — knowing before the session which direction to favor
- [[concepts/business-logic/ict-narratives|ICT Narratives KB]] — session timing tables and economic calendar framing
- [[concepts/entry-models/london-model|London Entry Model]] — the London KZ entry model specifically
