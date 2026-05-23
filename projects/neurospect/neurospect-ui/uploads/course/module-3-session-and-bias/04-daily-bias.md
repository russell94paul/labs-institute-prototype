---
tags: [course, module-3, daily-bias, htf-fvg, opening-price, neurospect]
aliases: [Daily Bias Lesson, HTF Bias Framework, Module 3 Lesson 4]
sources:
  - sources/neurospect/2026-04-18-vol2-class4-daily-bias-practice.md
  - sources/neurospect/2026-04-18-vol2-class4-notes.md
created: 2026-04-22
updated: 2026-04-22
module: 3
lesson: 4
---

# Module 3, Lesson 4: Daily Bias

**Prerequisites:** [[concepts/course/module-1-foundations/01-what-moves-the-market|Module 1, Lesson 1 — What Moves the Market]], [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]]  
**Reference:** [[concepts/business-logic/ict-narratives|ICT Narratives KB]]

---

## Concept

Daily bias is the assessment of whether the next trading day will be **bullish or bearish** with approximately 80% assurance — before the session begins. Getting bias wrong is the biggest obstacle to profitability: you can have the perfect entry model and still lose if you're trading against the algorithm's intent for the day.

> "What I use every single day. This is what really has helped me to develop over an 80% of win rate when we talk about daily bias... After understanding this approach, trading became easier, at least for me. And that was like the first little big approach toward constant profitability." — MrWitness, Vol 2 Class 4

The core principle:

> **Bias = Liquidity → Inefficiency → Liquidity**

The market is always moving toward one of these — never both simultaneously. If price is inside an inefficiency (FVG), it is targeting nearby liquidity. If price has just taken liquidity, it is targeting the nearest inefficiency in the delivery direction.

---

## Step 1: Find the HTF Inefficiency

Look for the **cleanest, most decisive FVG** on these timeframes (check in ascending order):

- 1H → 2H → 3H → 4H → Daily

**Rule:** Start at 1H. If multiple FVGs appear on 1H, step up to 2H and look for one clean gap. Step up again if still multiple. The 4H timeframe is usually where one dominant FVG becomes clear.

**Why 4H?** Institutions trade the daily, weekly, 4H, and 1H — not the 5-minute or 15-minute. The 4H FVG captures institutional intent and cuts through intraday noise.

**How to use the FVG for bias:**
- Price **inside a bullish 4H FVG** → look for longs every day until the FVG is violated
- Price **inside a bearish 4H FVG** → look for shorts every day until the FVG is violated
- Price **closed above** the FVG → bias has shifted; look for higher liquidity targets
- Price **closed below** a bullish FVG → bias has shifted bearish; re-evaluate

> "As long as price remains inside of this inefficiency on this time frame, you're going to keep looking for liquidity outside of this range." — Vol 2 Class 4

**If no clean FVG exists:** Look for the nearest external liquidity level (swing high or swing low on 1H or Daily) and target that directly.

**The alternating cycle:** Liquidity → FVG → Liquidity → FVG → Liquidity. The market alternates. After taking a major swing high (liquidity), price seeks an inefficiency. After filling the FVG, price seeks the next swing high/low (liquidity).

---

## Step 2: Check Opening Price Position

Once the HTF bias is established, align it with the intraday opening price context from Power of Three:

| HTF Bias | Opening Price Position | Signal |
|---|---|---|
| Bullish (inside bullish 4H FVG) | Price below midnight open | **Best longs** — full confluence |
| Bullish | Price below 8:30 AND 9:30 open | **High probability** longs |
| Bullish | Price above all opens | Lower probability; smart money distributing; wait |
| Bearish (inside bearish 4H FVG) | Price above midnight open | **Best shorts** — full confluence |
| Bearish | Price above 8:30 AND 9:30 open | **High probability** shorts |

**The best long setups:** price below midnight open + 8:30 open + 9:30 open simultaneously, while inside a bullish 4H FVG.

**Edge case — 8:30 is already below midnight open:**
- If 8:30 opens lower than midnight open, 8:30 already did the "manipulation job"
- 9:30 may continue higher, using 8:30 as the low anchor
- You are still below one opening price → still valid for longs

---

## Step 3 (Optional): Use Opening Price as Entry Context

The two bias steps above give ~80% directional assurance. To increase toward ~88%:
- Combine HTF FVG bias (Step 1) + opening price below/above (Step 2)
- Enter with any valid model (consolidation, E&R, reversal, OTE) at the KZ window

> "This approach is very good. Once I understood this, I started passing my first combines and started making money." — MrWitness, Vol 2 Class 4

---

## Worked Example: 4H Bullish FVG Walk-Through (Vol 2 Class 4 Live Replay)

MrWitness walks through several weeks of NQ price action showing the bias cycle:

**Phase 1 — Inside the 4H bullish FVG:**
- Price inside a bullish 4H FVG → look for longs every session toward the swing high (BSL) above
- Best entries: below midnight open, below 8:30 open
- Each day, mark the opens, confirm price is below, take any valid long model

**Phase 2 — FVG taken, liquidity target next:**
- Price rallies above the 4H FVG → no more long bias from this FVG
- Now looking for the swing high (BSL) outside the range as the next target
- Shorting opportunities appear when price is above all three opens (bearish AMD) — looking for short toward the 4H FVG below

**Phase 3 — New liquidity → new FVG:**
- Once the swing high (BSL) is taken, price creates a new FVG or volume imbalance
- New FVG = new bias anchor; cycle repeats

**Annotation from the replay:** "Right here, as long as we remain inside of this gap, I am looking for higher prices. Once I take this high — I look for the gap. Once the gap is taken — I look back for liquidity. That's it."

---

## When to Ignore the Small Structures

A common error is letting small 15M or 1M structures override the 4H bias. They don't.

While price is inside a bullish 4H FVG:
- A 15M market structure shift lower is just the manipulation leg of AMD
- A bearish FVG on the 5M is a target for the manipulation, not a reason to go short
- As long as the 4H FVG is respected (no daily close below its low), **every pullback is a long opportunity**

> "It does not matter what the minor fluctuations show you in the 50 minutes, the hourly, in terms of structure — if it's showing you a very short order block or a very fair value gap — you want to pay attention to the biggest inefficiency." — Vol 2 Class 4

---

## Daily Checklist

Apply every evening or pre-session morning:

- [ ] Identified the main FVG on 4H (or cleanest available TF if 4H has none)
- [ ] Determined whether price is inside a bullish or bearish FVG
- [ ] If no FVG: identified the nearest external liquidity target
- [ ] Checked midnight open position relative to current price
- [ ] Noted 8:30 and 9:30 opens for tomorrow
- [ ] Confirmed: bias direction + entry window (which session's KZ aligns best)
- [ ] Set expectation: "If tomorrow delivers below X open, I look for longs. If it does NOT go below the open, I wait."

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Checking bias only on 15M or 1M | Too noisy; 1H-4H-Daily is where institutional intent lives |
| Changing bias mid-session on a 5M structure | Small structures are AMD cycles inside the HTF bias; they aren't reversals |
| Looking for shorts when inside a bullish 4H FVG | The FVG is the engine; shorts here fight institutional order flow |
| Ignoring the opening price step | Step 1 gives direction; Step 2 gives the entry window — both needed |
| No plan for when the FVG is violated | Have a rule: if price closes below the bullish FVG low on a 4H candle → bias resets |

---

## Homework

Practice the bias routine for 10 consecutive trading days in your journal:

1. **Each evening:** open your chart; find the 4H FVG that is currently driving price; write one sentence: "I am inside a [bullish/bearish] 4H FVG; the target is [level]."
2. **Each morning:** note the midnight opening price and whether price is below (bullish day) or above (bearish day)
3. **After the session:** was the HOD/LOD formed during the expected bias direction? Did price stay inside the FVG?
4. Track: how often does the 4H FVG + opening price below the open = winning day direction?

> "Practice this every single day in your journals for your notes." — MrWitness, Vol 2 Class 4

---

## See Also

- [[concepts/course/module-3-session-and-bias/01-power-of-three|Lesson 1 — Power of Three]] — opening price mechanics used in Step 2
- [[concepts/course/module-3-session-and-bias/02-session-kill-zones|Lesson 2 — Session Kill Zones]] — which session to trade within the established bias
- [[concepts/business-logic/ict-narratives|ICT Narratives KB]] — full daily bias reference including weekly OP protocol
- [[concepts/entry-models/daily-bias-model|Daily Bias Entry Model]] — the machine-readable entry model for this strategy
