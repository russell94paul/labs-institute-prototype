---
tags: [course, module-4, deviations, market-structure, itl, stl, two-set, targets, neurospect]
aliases: [Structure Deviations Lesson, Two-Set Deviations, Module 4 Lesson 3]
sources:
  - sources/neurospect/2026-04-18-vol3-class4-market-structure-deviations.md
  - sources/neurospect/2026-04-18-vol2-class3-measuring-manipulation-deviations.md
created: 2026-04-22
updated: 2026-04-22
module: 4
lesson: 3
---

# Module 4, Lesson 3: Market Structure Deviations (Two-Set Anchoring)

**Prerequisites:** [[concepts/course/module-4-market-structure/01-swing-classification|Lesson 1 — Swing Classification]], [[concepts/course/module-3-session-and-bias/03-deviations|Module 3, Lesson 3 — Deviations (Power of Three)]]  
**Reference:** [[concepts/business-logic/ict-deviations|ICT Deviations KB]]

---

## Concept

Module 3's deviation lesson taught you to anchor Fibonacci from the manipulation leg of Power of Three — one set of deviations. This lesson upgrades that to **two sets** anchored from market structure swings. The two-set method is more precise because it gives you a convergence zone — where both deviation sets overlap — which is the highest-confidence HOD/LOD target.

> "You want to be measuring two deviations for this exercise. Not just one, like in the Power of Three class, but this is going to be looking for more precision." — MrWitness, Vol 3 Class 4

The -2/-2.5 HOD/LOD rule from Module 3 still applies. The two-set method is how you find the exact price level within that zone.

---

## The Two Swings to Measure From

After a market structure shift (ITL formed, MSS fires, price expanding higher), anchor from two swings:

### Set 1 — Intermediate-Term Low Price Leg

**What:** The price leg from the ITL to the swing high that **initiated** the ITL price leg lower.

**Why:** This is the "real manipulation move" — the one that trapped sellers into thinking a new downtrend was underway. It is the full dealing range for the reversal.

**How to anchor:**
- Find the ITL (the low that created or filled a FVG on its way down)
- Find the swing high immediately preceding the ITL price leg (the high from which price broke lower to create the ITL)
- Measure from ITL → that initiating swing high
- Project deviations upward from the swing high

**First target:** The first swing high above the initiating high (the buy-side liquidity target) → take the first partial at the first deviation BEYOND that level.

### Set 2 — Short-Term Low Price Leg (The Measuring Swing)

**What:** The price leg from the STL immediately to the right of the ITL (the first retracement after the MSS) to the swing high of that same move.

**Why:** This "measuring swing" acts as a calibration — it shows how much energy the move has after the MSS fires. It provides secondary deviation levels that converge with Set 1.

**How to anchor:**
- Find the STL to the right of the ITL (the first pullback after the MSS)
- Find the high of the move that the STL retraced from
- Measure from that STL → that swing high
- Project deviations upward

---

## How to Use Convergence

When Set 1 and Set 2 produce deviation levels at or near the same price area:

| Convergence | Signal |
|---|---|
| Set 1 and Set 2 at same level | HOD/LOD zone confirmed; highest confidence |
| Convergence at -2/-2.5 | Ideal exit; matches Power of Three HOD/LOD rule |
| Convergence overlapping HTF FVG | HPDL — maximum confidence exit |
| -4 and -5 from both sets converge | Extended target; valid on high-momentum sessions |

> "When these are converging, that is where you want to be paying attention to. And you can see that these are pretty much close to each other and the minus seven to the minus two, that is pretty much close to the high of the day." — Vol 3 Class 4

**The midpoint between two converging levels** is the most precise HOD/LOD: if Set 1 prints -2 at 21,100 and Set 2 prints -2 at 21,120, the HOD/LOD is approximately 21,110.

---

## Step-by-Step Application

1. **Identify the ITL** — confirm it fills or creates a gap (not just a STL)
2. **Identify the initiating high** — the swing high immediately before the ITL price leg
3. **Anchor Set 1:** Fibonacci from ITL → initiating high; project deviations upward
4. **Mark Set 1 levels:** -0.5, -1, -1.5, -2, -2.5, -3, -4, -5
5. **Identify the STL to the right** of the ITL (first retracement after MSS)
6. **Identify the high** that the STL retraced from
7. **Anchor Set 2:** Fibonacci from STL → that high; project deviations upward
8. **Mark Set 2 levels**
9. **Look for convergence:** where do Set 1 and Set 2 levels cluster?
10. **Mark the convergence zone** as the HOD/LOD target
11. **Execute partials** at first deviation of Set 1; run toward convergence zone

---

## Worked Example 1: London Session (Vol 3 Class 4 Live)

**Setup (Bullish day):**
- London session creates the manipulation low (ITL)
- The London session low sits below the midnight open
- Initiating high = London session high (the high before the London sweep lower)

**Set 1 anchoring:**
- From London session low → London session high
- -1 deviation above the first swing high target = +16–17 handles beyond the target
- The first deviation adds ~$330 per contract at 20 NQ contract size

**Set 2 (measuring swing):**
- From the STL to the right of the ITL (NY pre-market retracement) → the high
- Second deviation set converges with Set 1 near -2/-2.5

**HOD:**
- Price eventually prints at the -2 to -2.5 convergence zone
- From there: market structure shift lower (bodies starting to close below the 50% of the dealing range → confirmed reversal)

---

## Worked Example 2: Holiday Liquidity (Vol 3 Class 4 Live)

**Setup (Multi-day):**
- Thursday holiday session created thin liquidity levels
- Friday: price targets Thursday's holiday levels during London
- Two sets of deviations anchored from the ITL and STL

**Result:**
- Convergence zone at minus five to minus five-point-five
- HOD of the holiday session = midpoint between those two levels to the tick
- "For the high of the holiday, right between the minus five-point-five and minus five-point-five. The 50% of those two levels. That's what you get for the high of the holiday." — Vol 3 Class 4

---

## Timing Note

The two-set method is most precise for:
- **London session** HOD/LOD (highest clarity — London creates the cleanest manipulation legs)
- **NY AM reversal** (after 8:30–9:30 manipulation)
- **PM session** for final high/low of day

Use 15M–1H swings for the ITL and STL anchoring. Smaller timeframe swings produce noisy deviation levels.

---

## Common Mistakes

| Mistake | Why It Fails |
|---|---|
| Using only one set of deviations | One set shows a zone; two sets show the precise level inside the zone |
| Using a STL as the Set 1 anchor instead of the ITL | The Set 1 must start from the ITL (gap-qualified), not a suspect STL |
| Applying the -2/-2.5 rule without looking for convergence | The -2/-2.5 is a range; convergence tells you exactly where within that range |
| Over-extending in absence of HTF liquidity | -5 to -7 targets require an HTF FVG or liquidity pool in that zone |

---

## See Also

- [[concepts/course/module-3-session-and-bias/03-deviations|Module 3, Lesson 3 — Deviations (Power of Three)]] — single-set anchoring from AMD manipulation leg
- [[concepts/course/module-4-market-structure/01-swing-classification|Lesson 1 — Swing Classification]] — ITL/STL identification required for this method
- [[concepts/business-logic/ict-deviations|ICT Deviations KB]] — full reference including HPDL and practical targets table
- [[concepts/course/module-4-market-structure/04-model-2022-ote-csd|Lesson 4 — Model 2022 + OTE]] — deviation exits combined with OTE entries
