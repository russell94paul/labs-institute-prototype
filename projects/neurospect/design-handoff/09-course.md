# NeuroSpect Interactive ICT Course — Design Spec

## Overview

A free-tier interactive ICT trading course accessible on the marketing site after waitlist signup. Users complete a trading profile questionnaire, receive a personalized learning path, and work through 5 modules of structured ICT curriculum with 4 types of interactive assessments including live candlestick chart exercises.

This is a **content marketing and lead qualification engine** — it demonstrates the depth of NeuroSpect's ICT knowledge, captures rich profile data for personalization, and converts passive visitors into engaged learners who are pre-qualified for paid tiers.

## Why This Matters

- Proves NeuroSpect's ICT knowledge is real and deep — not a ChatGPT wrapper
- Creates a sticky engagement loop before the product launches (visitors return to continue the course)
- Captures trading profile data (experience, struggles, goals) for future personalization and tier matching
- The interactive chart exercises are unlike anything in trading education today
- Each assessment naturally surfaces the paid features that would help the learner improve
- Completion rate and failure patterns validate which product features to prioritize

---

## Pages

### Course Landing (`/course`)

**Purpose:** Curriculum overview. Convert visitors to enrolled learners.

```
+----------------------------------------------------------+
|  Nav (fixed)                                             |
+----------------------------------------------------------+
|                                                          |
|  HERO                                                    |
|  "Master ICT Concepts. Prove It on the Chart."           |
|  Sub: Free 5-module curriculum with interactive           |
|  assessments, candlestick chart exercises,               |
|  and personalized learning paths.                        |
|                                                          |
|  [Start Course] [View Curriculum]                        |
|  Disclaimer badge: "Educational only — not trading       |
|  advice"                                                 |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  CURRICULUM OVERVIEW                                     |
|  5 module cards in a vertical timeline/stepper:          |
|                                                          |
|  [1] Foundations          [locked/unlocked]     3 lessons |
|      Liquidity, FVGs, Practice                           |
|                                                          |
|  [2] Price Delivery       [locked]              4 lessons |
|      APD stages, Consolidation, Expansion, Reversals     |
|                                                          |
|  [3] Session & Bias       [locked]              4 lessons |
|      Power of Three, Kill Zones, Deviations, Bias        |
|                                                          |
|  [4] Market Structure     [locked]              4 lessons |
|      Swings, Fractality, Structure Deviations, OTE       |
|                                                          |
|  [5] Order Flow & SMT     [locked]              2 lessons |
|      HTF/LTF Order Flow, SMT Divergence                  |
|                                                          |
|  [*] Entry Models Library  [locked until 5 complete]     |
|      7 strategies with machine-readable checklists       |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  WHAT YOU'LL LEARN (3-column grid)                       |
|  - Identify FVGs, order blocks, liquidity sweeps         |
|  - Build a daily bias from HTF to LTF                    |
|  - Validate setups with a structured checklist           |
|  - Recognize all 4 stages of price delivery              |
|  - Use kill zones and session context                    |
|  - Detect SMT divergence for confluence                  |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  ASSESSMENT PREVIEW                                      |
|  4 cards showing assessment types:                       |
|                                                          |
|  [Concept Quiz]    [Chart ID]    [Scenarios]  [Engage]   |
|   Multiple choice   Click on      "What would  Matching, |
|   and true/false    the chart     you do?"     sequencing |
|                                                          |
|  Each card shows a mini preview/mockup of the            |
|  interaction                                             |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  CTA: "Join the Waitlist to Start Learning"              |
|  → Links to /course/profile                              |
|                                                          |
+----------------------------------------------------------+
|  WaitlistForm                                            |
+----------------------------------------------------------+
```

### Profile Questionnaire (`/course/profile`)

**Purpose:** Collect trading experience, goals, and struggles. Generate personalized path.

```
+----------------------------------------------------------+
|  Nav (fixed)                                             |
+----------------------------------------------------------+
|                                                          |
|  HERO (compact)                                          |
|  "Tell Us About Your Trading"                            |
|  Sub: "Takes 60 seconds. We'll build a learning path     |
|  customized to your experience and goals."               |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  PROFILE FORM (multi-step, 4 steps)                      |
|                                                          |
|  Step indicator: [1]--[2]--[3]--[4]                      |
|                                                          |
|  STEP 1: Experience                                      |
|  ┌──────────────────────────────────────────────┐       |
|  │ How long have you been trading ICT?           │       |
|  │ ○ Less than 6 months                          │       |
|  │ ○ 6-12 months                                 │       |
|  │ ○ 1-2 years                                   │       |
|  │ ○ 2+ years                                    │       |
|  │                                                │       |
|  │ What's your trading experience level?          │       |
|  │ ○ Beginner — Still learning concepts           │       |
|  │ ○ Intermediate — Know concepts, inconsistent   │       |
|  │ ○ Advanced — Consistently profitable           │       |
|  │ ○ Prop firm — Trading funded accounts          │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  STEP 2: Style & Instruments                             |
|  ┌──────────────────────────────────────────────┐       |
|  │ What do you trade?                             │       |
|  │ □ NQ (Nasdaq futures)                          │       |
|  │ □ ES (S&P futures)                             │       |
|  │ □ Forex (EUR/USD, GBP/USD, etc.)              │       |
|  │ □ Crypto                                       │       |
|  │ □ Other                                        │       |
|  │                                                │       |
|  │ How do you trade?                              │       |
|  │ ○ Discretionary — pure chart reading           │       |
|  │ ○ Quant-curious — interested in data/stats     │       |
|  │ ○ Hybrid — discretionary + some rules          │       |
|  │ ○ Systematic — mostly rule-based               │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  STEP 3: Struggles (select up to 3)                      |
|  ┌──────────────────────────────────────────────┐       |
|  │ What's holding you back? (pick up to 3)        │       |
|  │                                                │       |
|  │ [pill] Can't identify setups in real-time      │       |
|  │ [pill] Know concepts but can't execute          │       |
|  │ [pill] Overtrade / take bad setups              │       |
|  │ [pill] Can't build a daily bias                 │       |
|  │ [pill] Don't understand market structure        │       |
|  │ [pill] Struggle with risk management            │       |
|  │ [pill] Can't backtest my ideas                  │       |
|  │ [pill] Don't know which setups work for me      │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  STEP 4: Goals (select up to 2)                          |
|  ┌──────────────────────────────────────────────┐       |
|  │ What are you working toward?                   │       |
|  │                                                │       |
|  │ [pill] Pass a prop firm challenge               │       |
|  │ [pill] Become consistently profitable           │       |
|  │ [pill] Automate my strategy                     │       |
|  │ [pill] Understand ICT concepts deeply           │       |
|  │ [pill] Build a systematic trading process       │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  [Build My Learning Path →]                              |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  PERSONALIZED PATH (appears after submission)            |
|                                                          |
|  "Your Custom ICT Learning Path"                         |
|                                                          |
|  Based on: Intermediate, NQ, Discretionary               |
|  Focus areas: Daily bias, setup identification           |
|                                                          |
|  Recommended order:                                      |
|  [1] Foundations ← "Quick review"                        |
|  [3] Session & Bias ← "PRIORITY — matches your          |
|       struggle with daily bias"                          |
|  [2] Price Delivery                                      |
|  [4] Market Structure ← "Key for real-time ID"          |
|  [5] Order Flow & SMT                                    |
|                                                          |
|  [Start Module 1 →]                                      |
|                                                          |
+----------------------------------------------------------+
```

### Module Page (`/course/module-{N}`)

**Purpose:** Lesson content + assessments for one module. This is the core learning experience.

```
+----------------------------------------------------------+
|  Nav (fixed)                                             |
+----------------------------------------------------------+
|                                                          |
|  MODULE HEADER                                           |
|  ┌──────────────────────────────────────────────┐       |
|  │ Module 1 of 5                                  │       |
|  │ FOUNDATIONS                                     │       |
|  │ Liquidity, Fair Value Gaps, and Practice        │       |
|  │ ███████░░░ 70% complete     3 lessons           │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  LESSON NAVIGATION (horizontal tabs or sidebar)          |
|  [1.1 Liquidity ✓] [1.2 FVGs ●] [1.3 Practice ○]      |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  LESSON CONTENT                                          |
|                                                          |
|  Section heading in white, body in slate-300.            |
|  Content sourced from wiki/concepts/course/ pages.       |
|                                                          |
|  Includes:                                               |
|  - Concept explanation (2-4 paragraphs)                  |
|  - Key rules (bulleted, highlighted card)                |
|  - Worked example with annotated chart                   |
|  - Common mistakes (amber/warning card)                  |
|  - "Study this before the assessment" callout            |
|                                                          |
|  INLINE CHART EXAMPLE                                    |
|  ┌──────────────────────────────────────────────┐       |
|  │                                                │       |
|  │  ┌────────────────────────────────────────┐   │       |
|  │  │      CANDLESTICK CHART                  │   │       |
|  │  │      (lightweight-charts)               │   │       |
|  │  │                                          │   │       |
|  │  │  Annotations:                            │   │       |
|  │  │  → FVG zones highlighted in cyan         │   │       |
|  │  │  → Liquidity levels as dashed lines      │   │       |
|  │  │  → Displacement candles marked            │   │       |
|  │  │                                          │   │       |
|  │  └────────────────────────────────────────┘   │       |
|  │  Caption: "NQ 5-min — bullish FVG forms..."   │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  [Mark Lesson Complete ✓] [Next Lesson →]               |
|                                                          |
+----------------------------------------------------------+
|                                                          |
|  ASSESSMENTS (appear after all lessons marked complete)   |
|                                                          |
|  "Test Your Knowledge"                                   |
|  "Complete all 4 assessments to unlock Module 2"         |
|                                                          |
|  Assessment cards (2x2 grid):                            |
|  ┌────────────────┐ ┌────────────────┐                  |
|  │ CONCEPT QUIZ   │ │ CHART ID       │                  |
|  │ 10 questions    │ │ 5 exercises     │                  |
|  │ 80% to pass     │ │ 70% to pass     │                  |
|  │ ○ Not started   │ │ ○ Not started   │                  |
|  │ [Start →]       │ │ [Start →]       │                  |
|  └────────────────┘ └────────────────┘                  |
|  ┌────────────────┐ ┌────────────────┐                  |
|  │ SCENARIOS      │ │ ENGAGEMENT     │                  |
|  │ 5 scenarios     │ │ 3 exercises     │                  |
|  │ 75% to pass     │ │ 80% to pass     │                  |
|  │ ○ Not started   │ │ ○ Not started   │                  |
|  │ [Start →]       │ │ [Start →]       │                  |
|  └────────────────┘ └────────────────┘                  |
|                                                          |
+----------------------------------------------------------+
```

---

## Assessment Type Designs

### Type 1: Concept Quiz

```
+----------------------------------------------------------+
|                                                          |
|  CONCEPT QUIZ — Module 1: Foundations                    |
|  Question 3 of 10                                        |
|  ████████░░░░░░░░░░░                                     |
|                                                          |
|  "What creates a Fair Value Gap?"                        |
|                                                          |
|  ┌──────────────────────────────────────────────┐       |
|  │ ○  A moving average crossover                  │ ←gray |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  A 3-candle displacement leaving a price    │ ←gray |
|  │    gap between candle 1's body and candle 3    │       |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  A volume spike above the 20-period average │ ←gray |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  A gap between Friday close and Monday open │ ←gray |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  After answering:                                        |
|  ┌──────────────────────────────────────────────┐       |
|  │ ✓ CORRECT                                      │ ←green|
|  │                                                │       |
|  │ A Fair Value Gap (FVG) is a 3-candle pattern   │       |
|  │ where a displacement candle leaves a gap        │       |
|  │ between the bodies of candles 1 and 3.          │       |
|  │ This creates an area of price inefficiency.     │       |
|  │                                                │       |
|  │ See: Module 1, Lesson 2 — Fair Value Gaps       │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  [Next Question →]                                       |
|                                                          |
+----------------------------------------------------------+
```

Design notes:
- Selected answer: neon border glow (emerald for correct, red for incorrect)
- Unselected answers: standard neon-card styling
- Explanation card: appears below with slide-down animation
- Progress bar: brand-400 fill on slate-800 track
- Question transitions: fade/slide animation

### Type 2: Chart Identification (Interactive Candlestick)

```
+----------------------------------------------------------+
|                                                          |
|  CHART IDENTIFICATION — Module 1: Foundations            |
|  Exercise 2 of 5                                         |
|                                                          |
|  INSTRUCTION:                                            |
|  "Click on the Fair Value Gap in this NQ 5-min chart"    |
|                                                          |
|  ┌──────────────────────────────────────────────┐       |
|  │                                                │       |
|  │        INTERACTIVE CANDLESTICK CHART           │       |
|  │        (lightweight-charts)                    │       |
|  │                                                │       |
|  │    ┃                                           │       |
|  │    ┃█                                          │       |
|  │    ┃█     ┃                                    │       |
|  │    ┃█     ┃█                                   │       |
|  │     █     ┃█  ┃                                │       |
|  │     █      █  ┃█                               │       |
|  │           ██  ┃█  ┃                             │       |
|  │           ██   █  ┃█                            │       |
|  │                █  ┃█                            │       |
|  │                    █                            │       |
|  │                                                │       |
|  │  Cursor: crosshair when hovering chart          │       |
|  │  Click registers a candle/zone selection        │       |
|  │  Selected zone highlights with cyan overlay     │       |
|  │                                                │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  HINT (optional, costs 10% of exercise score):           |
|  [Show Hint]                                             |
|  "Look for a 3-candle pattern where the middle           |
|   candle displaces sharply"                              |
|                                                          |
|  [Submit Answer]                                         |
|                                                          |
|  After submission:                                       |
|  ┌──────────────────────────────────────────────┐       |
|  │ ✓ CORRECT — That's the bullish FVG              │       |
|  │                                                │       |
|  │  Chart now shows:                               │       |
|  │  → Correct zone highlighted in emerald          │       |
|  │  → Labels on candle 1, 2 (displacement), 3     │       |
|  │  → Arrow pointing to the gap                    │       |
|  │  → Text: "Gap between C1 high and C3 low"      │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
+----------------------------------------------------------+
```

Design notes:
- Chart uses lightweight-charts (TradingView) for authentic candlestick rendering
- Hover state: crosshair cursor, candle/zone highlights on mouseover
- Click: selected zone gets a semi-transparent cyan overlay
- Correct answer: zone turns emerald, annotation labels appear
- Incorrect: zone turns red, correct zone reveals with emerald + explanation
- Touch support: tap on mobile, with larger hit zones
- Chart height: 400px desktop, 280px mobile

### Type 3: Scenario Engine

```
+----------------------------------------------------------+
|                                                          |
|  SCENARIO — Module 3: Session & Bias                     |
|  Scenario 2 of 5                                         |
|                                                          |
|  MARKET CONTEXT:                                         |
|  ┌──────────────────────────────────────────────┐       |
|  │  NQ — New York AM Session                      │       |
|  │  It's 9:35 AM ET. Price swept the previous     │       |
|  │  day's low during London, then displaced        │       |
|  │  upward through a 1H Fair Value Gap.            │       |
|  │                                                │       |
|  │  [CHART: Annotated candlestick showing the      │       |
|  │   sweep + displacement + FVG]                   │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  QUESTION:                                               |
|  "What do you look for next before entering long?"       |
|                                                          |
|  ┌──────────────────────────────────────────────┐       |
|  │ ○  Enter immediately — displacement is enough  │  [C]  |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  Wait for pullback into the FVG on LTF      │  [A+] |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  Wait for SMT divergence confirmation        │  [B]  |
|  ├──────────────────────────────────────────────┤       |
|  │ ○  Skip — no HTF bias was established          │  [F]  |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  Grades hidden until answer submitted.                   |
|                                                          |
|  After submission (selected "Wait for pullback"):        |
|  ┌──────────────────────────────────────────────┐       |
|  │ ★ A+ — Best Practice                           │ ←gold |
|  │                                                │       |
|  │ Waiting for a pullback into the FVG on a        │       |
|  │ lower timeframe gives the best entry with       │       |
|  │ clear invalidation (below the FVG).             │       |
|  │                                                │       |
|  │ Other answers:                                  │       |
|  │ B — SMT confirmation adds confluence but        │       |
|  │     isn't required for this setup               │       |
|  │ C — Entering without pullback risks a poor      │       |
|  │     entry and wide stop                         │       |
|  │ F — A daily bias WAS established (sweep +       │       |
|  │     displacement = bullish bias formation)      │       |
|  │                                                │       |
|  │ Review: Module 3, Lesson 4 — Daily Bias         │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
+----------------------------------------------------------+
```

Design notes:
- Scenario context card: neon-card with chart embedded
- Answer grades (A+, B, C, F): hidden until submitted, then color-coded
- A+ = emerald glow, B = brand/cyan, C = amber, F = red
- All answer explanations shown after submission (learn from every option)
- Scenarios can branch: some have follow-up questions based on your answer

### Type 4: Engagement Tests

**Concept Matching** (drag & drop):
```
+----------------------------------------------------------+
|                                                          |
|  Match each ICT term to its definition:                  |
|                                                          |
|  TERMS              DEFINITIONS                          |
|  ┌──────────┐      ┌────────────────────────────┐       |
|  │ FVG      │ ───→ │ 3-candle price inefficiency │       |
|  └──────────┘      └────────────────────────────┘       |
|  ┌──────────┐      ┌────────────────────────────┐       |
|  │ OB       │      │ Swing point that traps      │       |
|  └──────────┘      │ liquidity                    │       |
|  ┌──────────┐      └────────────────────────────┘       |
|  │ MSS      │      ┌────────────────────────────┐       |
|  └──────────┘      │ Break of market structure    │       |
|  ┌──────────┐      └────────────────────────────┘       |
|  │ CISD     │      ┌────────────────────────────┐       |
|  └──────────┘      │ Last candle before           │       |
|                     │ displacement                 │       |
|                     └────────────────────────────┘       |
|                                                          |
|  Drag terms to match. Lines connect on correct match.    |
|  Mobile: tap term, tap definition (2-tap match).         |
|                                                          |
+----------------------------------------------------------+
```

**Sequencing** (drag to reorder):
```
+----------------------------------------------------------+
|                                                          |
|  Put the 4 stages of Algorithmic Price Delivery          |
|  in the correct order:                                   |
|                                                          |
|  Drag to reorder:                                        |
|  ┌──────────────────────────────────────────────┐       |
|  │  ≡  Expansion                                  │       |
|  ├──────────────────────────────────────────────┤       |
|  │  ≡  Consolidation                              │       |
|  ├──────────────────────────────────────────────┤       |
|  │  ≡  Reversal                                   │       |
|  ├──────────────────────────────────────────────┤       |
|  │  ≡  Retracement                                │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  Correct order reveals with numbered badges              |
|  and a brief explanation of each stage.                  |
|                                                          |
+----------------------------------------------------------+
```

**Time-Pressure Chart ID**:
```
+----------------------------------------------------------+
|                                                          |
|  SPEED ROUND — Identify the concept!                     |
|  ⏱ 8 seconds remaining                                  |
|                                                          |
|  ┌──────────────────────────────────────────────┐       |
|  │          CANDLESTICK CHART                     │       |
|  │   (candles animate in one-by-one, left→right)  │       |
|  │                                                │       |
|  │   A specific pattern is forming...             │       |
|  │                                                │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  What is this?                                           |
|  [FVG] [Order Block] [MSS] [Liquidity Sweep] [CISD]    |
|                                                          |
|  Timer bar: brand-400 shrinking to red as time runs out  |
|  Correct: candle animation pauses, answer glows emerald  |
|  Timeout: answer reveals with explanation                |
|                                                          |
+----------------------------------------------------------+
```

---

## Grading Panel Design

Appears after completing all questions in an assessment:

```
+----------------------------------------------------------+
|                                                          |
|  ┌──────────────────────────────────────────────┐       |
|  │                                                │       |
|  │           ✓ PASSED — Module 1 Quiz              │       |
|  │           Score: 9/10 (90%)                     │       |
|  │           Threshold: 80%                        │       |
|  │                                                │       |
|  │  Strong areas:                                  │       |
|  │  ● FVG identification           10/10           │       |
|  │  ● Liquidity concepts           9/10            │       |
|  │                                                │       |
|  │  Needs review:                                  │       |
|  │  ● Displacement vs normal candle  0/1           │       |
|  │    → Review: Lesson 1.2, "Displacement Rules"  │       |
|  │                                                │       |
|  │  [Continue to Chart Identification →]           │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
|  FAILED state:                                           |
|  ┌──────────────────────────────────────────────┐       |
|  │                                                │       |
|  │           ✗ NOT YET — Module 2 Quiz             │       |
|  │           Score: 6/10 (60%)                     │       |
|  │           Need: 80%    Attempt: 2 of ∞          │       |
|  │                                                │       |
|  │  Study these before retrying:                   │       |
|  │                                                │       |
|  │  ┌────────────────────────────────────────┐   │       |
|  │  │ 1. Consolidation vs Expansion           │   │       |
|  │  │    → Re-read Lesson 2.2                 │   │       |
|  │  │    → Focus on: timeframe alignment      │   │       |
|  │  ├────────────────────────────────────────┤   │       |
|  │  │ 2. Retracement invalidation             │   │       |
|  │  │    → Re-read Lesson 2.3                 │   │       |
|  │  │    → Focus on: when FVG fill = invalid  │   │       |
|  │  ├────────────────────────────────────────┤   │       |
|  │  │ 3. Reversal recognition                 │   │       |
|  │  │    → Re-read Lesson 2.4                 │   │       |
|  │  │    → Focus on: 3 reversal types          │   │       |
|  │  └────────────────────────────────────────┘   │       |
|  │                                                │       |
|  │  [Review Lessons] [Retry Quiz →]               │       |
|  └──────────────────────────────────────────────┘       |
|                                                          |
+----------------------------------------------------------+
```

Design notes:
- Pass: emerald border glow, checkmark icon, confetti-style subtle particle animation
- Fail: amber border glow (not red — encouraging, not punishing), study assignment cards
- Study assignments: each links directly to the relevant lesson section
- Retry: different questions from the question bank (not the same quiz)
- Attempt count shown but unlimited retries allowed

---

## Progress Tracking

### Module Progress Header (persistent on module pages)

```
┌──────────────────────────────────────────────────────────┐
│  Module 1: Foundations                                     │
│                                                            │
│  Lessons:  [✓] 1.1  [✓] 1.2  [○] 1.3                    │
│  Assess:   [✓] Quiz [●] Chart [○] Scenario [○] Engage    │
│  Status:   In Progress — 2 of 4 assessments passed         │
│  ██████████████░░░░░░░░░░ 50%                              │
└──────────────────────────────────────────────────────────┘
```

### Course Progress Sidebar (on `/course` landing)

```
YOUR PROGRESS
┌────────────────────┐
│ Module 1  ✓ 100%   │ ← emerald
│ Module 2  ● 60%    │ ← brand
│ Module 3  ○ 0%     │ ← slate (locked)
│ Module 4  ○ 0%     │ ← slate (locked)
│ Module 5  ○ 0%     │ ← slate (locked)
│ Entry Models 🔒     │
├────────────────────┤
│ Overall: 32%        │
│ ████░░░░░░░░        │
└────────────────────┘
```

---

## Tier Upsell Integration

At natural break points (after passing a module, on failure, on capstone), show contextual upsells:

```
┌──────────────────────────────────────────────────────────┐
│  WITH NEUROSPECT MENTOR ($29/mo):                         │
│                                                            │
│  "You missed 2 questions about daily bias formation.       │
│   With Mentor, the AI coach would have caught this pattern │
│   in your journal and assigned targeted review before       │
│   your next trading session."                              │
│                                                            │
│  [Learn About Mentor →]  [Continue Free Course]            │
└──────────────────────────────────────────────────────────┘
```

Upsell cards:
- After Module 1-2: Mentor ($29) — AI coaching for concept reinforcement
- After Module 3-4: Trader ($99) — EdgeLab backtesting to validate learned setups
- After Module 5: Research ($199) — NSLM experiments on ICT strategies
- After Entry Models: Quant ($349) — Hybrid model building

---

## Candlestick Chart Specifications

### Technology: lightweight-charts (TradingView)

Library: `npm install lightweight-charts`
Bundle: ~40KB gzipped, lazy-loaded

### Chart Styling (dark theme)

```
Background:     transparent (uses section background)
Grid lines:     rgba(255, 255, 255, 0.04)
Text/labels:    #64748b (slate-500)
Crosshair:      #94a3b8 (slate-400), dashed
Up candle:      #34d399 (emerald-400) — body fill + wick
Down candle:    #f87171 (red-400) — body fill + wick
Volume bars:    rgba(100, 116, 139, 0.2) (slate, subtle)
```

### Annotation Overlays

| Annotation | Color | Style |
|---|---|---|
| FVG zone | `rgba(6, 182, 212, 0.15)` | Rectangle overlay, cyan border |
| Order block | `rgba(139, 92, 246, 0.15)` | Rectangle overlay, purple border |
| Liquidity level | `rgba(245, 158, 11, 0.4)` | Dashed horizontal line, amber |
| MSS marker | `rgba(16, 185, 129, 0.8)` | Triangle marker, emerald |
| Entry point | `rgba(6, 182, 212, 1)` | Circle marker, brand |
| Stop loss | `rgba(239, 68, 68, 0.8)` | Dashed line, red |
| Take profit | `rgba(16, 185, 129, 0.8)` | Dashed line, emerald |

### Chart Sizes

| Context | Width | Height |
|---|---|---|
| Lesson example | 100% container | 350px |
| Chart ID exercise | 100% container | 400px |
| Scenario context | 100% container | 300px |
| Speed round | 100% container | 350px |
| Mobile (all) | 100% | 250px |

---

## Synthetic OHLC Data Requirements

Each module needs chart data with specific patterns embedded:

### Module 1 Data (3 charts)
- **Chart 1A:** NQ 5-min, 120 candles. Contains: 2 bullish FVGs, 1 bearish FVG, 1 liquidity sweep (swing high)
- **Chart 1B:** NQ 15-min, 80 candles. Contains: clear displacement candle, liquidity pool at swing low
- **Chart 1C:** NQ 5-min, 100 candles. Contains: FVG that gets filled (retracement), FVG that holds

### Module 2 Data (4 charts)
- **Chart 2A:** NQ 1H, 60 candles. Contains: all 4 APD stages visible in sequence
- **Chart 2B:** NQ 15-min, 100 candles. Contains: consolidation → breakout → expansion
- **Chart 2C:** NQ 5-min, 120 candles. Contains: expansion → retracement to FVG → continuation
- **Chart 2D:** NQ 15-min, 80 candles. Contains: reversal pattern (sweep + displacement + FVG)

### Module 3 Data (4 charts)
- **Chart 3A:** NQ 5-min, 200 candles (full session). Contains: Power of Three (accumulation → manipulation → distribution) during NY AM
- **Chart 3B:** NQ 5-min, 150 candles. Contains: kill zone boundaries clearly visible, activity spike during NY AM
- **Chart 3C:** NQ 15-min, 80 candles. Contains: deviation from Fibonacci level
- **Chart 3D:** NQ 1H, 40 candles. Contains: daily bias formation (sweep + displacement + directional run)

### Module 4 Data (4 charts)
- **Chart 4A:** NQ 15-min, 100 candles. Contains: labeled STH, ITH, LTH swings
- **Chart 4B:** NQ multi-timeframe (1H + 15M overlay concept). Contains: fractal structure
- **Chart 4C:** NQ 15-min, 80 candles. Contains: structure deviation with 2-set targeting
- **Chart 4D:** NQ 5-min, 120 candles. Contains: Model 2022 OTE entry zone

### Module 5 Data (2 charts)
- **Chart 5A:** NQ 1H + 15M, 80 candles. Contains: HTF bullish order flow, LTF bearish order flow → conflict resolution
- **Chart 5B:** NQ + ES side-by-side, 60 candles each. Contains: SMT divergence (NQ makes new high, ES doesn't)

All data: deterministic, hand-crafted or seeded-random. Realistic price ranges (NQ 18000-19000 range). No actual market data.

---

## Mobile Considerations

- Profile form: full-width, one field group visible at a time (step wizard)
- Lesson content: full-width, charts scroll horizontally if needed
- Chart identification: larger tap zones, "tap to select" instead of precise clicks
- Drag-and-drop (matching, sequencing): fallback to tap-tap selection on mobile
- Progress tracker: collapsible header instead of sidebar
- Speed round: slower timer on mobile (12s instead of 8s)

---

## Relationship to Other Design Specs

| Spec | Relationship |
|---|---|
| `02-brand.md` | Course uses the same color system, card system, and typography |
| `03-sitemap.md` | Course pages to be added to sitemap (see update below) |
| `05-visualizations.md` | Candlestick charts are a new viz type; equity curves stay Chart.js |
| `08-live-simulator.md` | Simulator uses same candlestick library (lightweight-charts) — shared data patterns |

---

_All course content is educational only. Not financial advice. Trading involves significant risk of loss._
