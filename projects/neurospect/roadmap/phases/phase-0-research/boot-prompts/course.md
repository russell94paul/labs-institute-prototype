# NeuroSpect Interactive ICT Course — Boot Prompt

_Generated 2026-05-11 by `/sync`. Marketing site course section for Phase 0._

## What to Build

An interactive, free-tier ICT trading course accessible on the marketing site (`site/`). Users join the waitlist, fill out a trading profile, and unlock a structured 5-module ICT curriculum with interactive assessments, grading, and rich candlestick chart visualizations.

This is a **content marketing play and product validation tool** — it demonstrates the depth of NeuroSpect's ICT knowledge, validates that traders engage with structured learning, and captures qualified leads with rich profile data for future personalization.

---

## User Flow

### 1. Waitlist Signup → Profile Creation

Enhance the existing `WaitlistForm.astro` (or create a dedicated `/course` signup flow):

1. **Email capture** (existing)
2. **Trading profile questionnaire** (new):
   - Trading experience: `beginner` | `intermediate` | `advanced` | `prop_firm`
   - Time trading ICT: `< 6 months` | `6-12 months` | `1-2 years` | `2+ years`
   - Primary instrument: `NQ` | `ES` | `Forex` | `Crypto` | `Other`
   - Current trading style: `discretionary` | `quant-curious` | `hybrid` | `automated`
   - Biggest struggle (select up to 3):
     - "I can't identify setups in real-time"
     - "I know the concepts but can't execute"
     - "I overtrade and take bad setups"
     - "I can't build a daily bias"
     - "I don't understand market structure"
     - "I struggle with risk management"
     - "I can't backtest my ideas"
     - "I don't know which setups work for me"
   - Goals (select up to 2):
     - "Pass a prop firm challenge"
     - "Become consistently profitable"
     - "Automate my strategy"
     - "Understand ICT concepts deeply"
     - "Build a systematic trading process"
3. **Profile stored in localStorage** (no backend for marketing site)
4. **Personalization output**: custom course path recommendation + priority modules

### 2. Personalized Course Path

Based on the profile, generate a recommended learning path:

- **Beginners** → Full sequential path (Modules 1 → 5 → Entry Models)
- **Intermediate** → Skip/skim Module 1, start deep at Module 2, emphasis on their struggle areas
- **Advanced** → Module 4-5 deep dive + Entry Models, with remedial links for gaps
- **Prop firm traders** → Risk-focused path with session/kill zone emphasis (Module 3) + execution discipline

All users have access to all content — the personalization is a recommended order and priority flagging, not gating.

### 3. Course Structure

Each tier of the product should have:
- **Course section** — the interactive ICT curriculum (free tier = full course)
- **Guide to using it** — how to use NeuroSpect tools for that tier's workflow
- **Practice assignments** — tier-appropriate exercises

---

## Course Curriculum

Source of truth: `wiki/concepts/course/README.md` (5 modules, 18 lessons)

### Module 1 — Foundations
| Lesson | Concept | From |
|--------|---------|------|
| 1.1 | What Moves the Market (Liquidity & Inefficiency) | Vol 1, Class 1 |
| 1.2 | Fair Value Gaps (FVG / BISI / SIBI) | Vol 1, Class 1 |
| 1.3 | Homework & Practice | Vol 1, Class 1 |

### Module 2 — Price Delivery
| Lesson | Concept | From |
|--------|---------|------|
| 2.1 | Four Stages of Algorithmic Price Delivery | Vol 1, Class 2 |
| 2.2 | Consolidation Model | Vol 1, Class 3 |
| 2.3 | Expansion & Retracement Model | Vol 1, Class 3 |
| 2.4 | Reversals (Three Types) | Vol 1, Class 4 |

### Module 3 — Session Context & Bias
| Lesson | Concept | From |
|--------|---------|------|
| 3.1 | Power of Three (AMD) | Vol 2, Class 1 |
| 3.2 | Session Kill Zones & Opening Prices | Vol 2, Class 2 |
| 3.3 | Deviations (Fibonacci Targeting) | Vol 2, Class 3 |
| 3.4 | Daily Bias | Vol 2, Class 4 |

### Module 4 — Market Structure
| Lesson | Concept | From |
|--------|---------|------|
| 4.1 | Swing Classification (STH/ITH/LTH) | Vol 3, Class 2 |
| 4.2 | Market Structure Fractality | Vol 3, Class 4 |
| 4.3 | Structure Deviations (Two-Set Targeting) | Vol 3, Class 5 |
| 4.4 | Model 2022, OTE, CSD | Vol 3, Class 4 |

### Module 5 — Order Flow & SMT
| Lesson | Concept | From |
|--------|---------|------|
| 5.1 | HTF/LTF Order Flow | Vol 4, Class 1 |
| 5.2 | SMT Divergence | Vol 4, Class 2 |

### Capstone — Entry Models Library
After completing all 5 modules, unlock entry model deep-dives:
- Consolidation Model
- Daily Bias Model
- Expansion & Retracement Model
- London Model
- Model 2022 OTE
- Reversal / Raid on Stops
- SMT Confirmation Entry

Source: `wiki/concepts/entry-models/`

---

## Assessment System

Each module has **4 types of assessments**, progressively harder:

### Type 1: Concept Quiz
Multiple-choice and true/false questions testing conceptual understanding.

Example (Module 1):
- "What creates a Fair Value Gap?" → [3 candle displacement / Moving average cross / Volume spike / News event]
- "True or false: Liquidity rests above swing highs" → True
- "Which of these is a BISI?" → [Show 4 chart snippets, select the bullish imbalance]

**Implementation:** Static question bank in TypeScript data files. Randomize question order. Show explanation after each answer. Score: correct / total.

### Type 2: Chart Identification (Interactive)
Users interact with a real candlestick chart and must identify specific concepts by clicking/drawing on the chart.

Examples:
- "Click on the Fair Value Gap in this chart" → user clicks on the 3-candle gap
- "Draw the displacement candle" → user selects a candle
- "Identify the liquidity sweep" → user clicks the wick that took out the swing high
- "Mark the order block" → user selects the candle range
- "Where is the market structure shift?" → user clicks the break of structure point

**Implementation:** Synthetic deterministic OHLC data rendered with lightweight-charts (TradingView). Overlay click zones or marker regions that map to correct answers. Tolerance-based hit detection (within N candles / pixels of the correct location).

### Type 3: Scenario Engine
Present a market scenario and ask what the trader would do.

Examples:
- "NQ is in the NY AM kill zone. Price swept the previous day's low and displaced upward through a 1H FVG. What do you look for next?" → [Wait for pullback to FVG / Enter immediately / Wait for SMT confirmation / Skip — no HTF bias]
- "You're long and price reaches your first target. The 15M shows a CISD forming. What do you do?" → [Take partial / Move stop to breakeven / Close full / Hold for full target]
- "Your daily bias is bullish but price opens above the PDH. What adjustment do you make?" → [Flip bias to bearish / Wait for reclaim of PDH / Look for short-term buys only / Skip the session]

**Implementation:** Branching scenario trees with explanation for each choice. Some scenarios have multiple "acceptable" answers with different quality ratings (A+ = best practice, B = acceptable, C = suboptimal, F = mistake).

### Type 4: Knowledge Engagement Tests
Additional interactive formats to reinforce learning:

- **Concept Matching** — drag/drop to match ICT terms to their definitions
- **Sequencing** — arrange the 4 stages of algorithmic price delivery in correct order
- **Fill-in-the-Checklist** — given a setup, fill in the missing checklist items for an entry model
- **Time-Pressure Identification** — chart scrolls through candles in real-time (simulated), user must identify the concept within N seconds
- **Compare & Contrast** — given two similar chart patterns, identify which is a valid setup and which is a trap

### Grading System

Each assessment type has a passing threshold:
- Concept Quiz: **80%** correct
- Chart Identification: **70%** correct (tolerance for click precision)
- Scenario Engine: **75%** (weighted — A+ answers worth more)
- Knowledge Engagement: **80%** correct

**Pass → unlock next module.** Show a completion badge + breakdown of strong/weak areas.

**Fail → study assignment:**
1. Show which questions were wrong and why
2. Link back to the specific lesson section that covers the missed concept
3. Suggest re-reading specific wiki content
4. Offer a "retry" with different questions from the same question bank
5. Track attempt count (localStorage)

**Progress stored in localStorage** with structure:
```typescript
type CourseProgress = {
  profileCompleted: boolean;
  profile: TradingProfile;
  modules: Record<string, {
    lessonsCompleted: string[];
    quizScore: number | null;
    chartIdScore: number | null;
    scenarioScore: number | null;
    engagementScore: number | null;
    passed: boolean;
    attempts: number;
    weakAreas: string[];
  }>;
  entryModelsUnlocked: boolean;
  completedAt: string | null;
};
```

---

## Technical Approach

### Charting: lightweight-charts (TradingView)

**Why:** Purpose-built for OHLC/candlestick data. 40KB gzipped. The site already uses Chart.js for equity curves (line/bar/radar) — lightweight-charts handles the candlestick rendering that Chart.js cannot do well.

**Install:** `npm install lightweight-charts`

**Loading:** Same lazy-load pattern as Chart.js — dynamic `import('lightweight-charts')` inside component `<script>` tags, triggered by IntersectionObserver.

**Data:** Synthetic deterministic OHLC arrays in TypeScript data files. Each chart scenario needs 50-200 candles with specific ICT patterns embedded at known positions.

### Site Structure

```
site/src/
├── pages/
│   ├── course.astro                  # Course landing/overview page
│   └── course/
│       ├── profile.astro             # Trading profile questionnaire
│       ├── module-1.astro            # Module 1: Foundations
│       ├── module-2.astro            # Module 2: Price Delivery
│       ├── module-3.astro            # Module 3: Session Context & Bias
│       ├── module-4.astro            # Module 4: Market Structure
│       ├── module-5.astro            # Module 5: Order Flow & SMT
│       └── entry-models.astro        # Capstone: Entry Models Library
├── components/
│   └── course/
│       ├── CourseHero.astro          # Course landing hero
│       ├── ProfileForm.astro         # Trading profile questionnaire
│       ├── PersonalizedPath.astro    # Recommended learning path display
│       ├── ModuleOverview.astro      # Module card with progress indicator
│       ├── LessonViewer.astro        # Lesson content renderer
│       ├── ConceptQuiz.astro         # Multiple choice / true-false quiz
│       ├── ChartIdentification.astro # Interactive candlestick chart exercise
│       ├── ScenarioEngine.astro      # Branching scenario assessments
│       ├── EngagementTest.astro      # Matching, sequencing, fill-in exercises
│       ├── GradingPanel.astro        # Score display + pass/fail + study assignment
│       ├── ProgressTracker.astro     # Module progress sidebar/header
│       ├── CandlestickChart.astro    # Reusable lightweight-charts wrapper
│       ├── CourseNav.astro           # Module/lesson navigation
│       └── CourseCTA.astro           # Upgrade prompts for paid tiers
├── data/
│   ├── course-modules.ts            # Module/lesson structure + content
│   ├── quiz-data.ts                 # Question banks for concept quizzes
│   ├── chart-scenarios.ts           # OHLC data + correct answer regions
│   ├── scenario-trees.ts            # Branching scenario data
│   └── candlestick-data.ts          # Reusable OHLC chart datasets
```

### Nav Integration

Add "Course" to the site nav. Proposed position:
```
Compare | Performance | Course | Workflows | Architecture | Pricing
```

Or if the nav is getting crowded, group under a dropdown or move to a secondary nav.

---

## Tier-Specific Course Sections

Each pricing tier should have a course section showing what that tier unlocks:

| Tier | Course Content | Guide |
|------|---------------|-------|
| **Free** (waitlist) | Full 5-module ICT course + assessments + entry models | "Getting Started with ICT Concepts" |
| **Mentor** ($29) | Course + AI-coached review of assessment mistakes + personalized study plans | "Using NeuroSpect Mentor for Learning" |
| **Trader** ($99) | Course + EdgeLab backtesting of learned setups + live session analysis | "From Course to Live Trading" |
| **Research** ($199) | Course + NSLM prompt experiments on ICT setups + feature engineering | "Research-Driven Trading" |
| **Quant** ($349) | Course + hybrid model building + NeuroQuant integration | "Building Hybrid Trading Models" |
| **Team** ($499) | Course + custom curriculum for instructor's students | "Running Your Trading Education" |

---

## Content Sourcing

All course content derives from the existing wiki. **Do not invent new ICT concepts.**

| Content Need | Source |
|---|---|
| Module structure | `wiki/concepts/course/README.md` |
| Lesson content | `wiki/concepts/course/module-N-*/lesson-*.md` |
| ICT concept definitions | `wiki/concepts/business-logic/*.md` |
| Entry model checklists | `wiki/concepts/entry-models/*.md` |
| Chart patterns | Derived from concept rules (FVG = 3 candles, displacement, etc.) |
| Quiz questions | Generated from lesson content + common mistakes sections |
| Scenario trees | Generated from entry model checklists + worked examples |

---

## Synthetic Chart Data

Create deterministic OHLC datasets that embed specific ICT patterns:

### Required Patterns per Module

| Module | Patterns to Embed |
|--------|-------------------|
| 1 | FVG (bullish + bearish), liquidity sweep (swing high + low), displacement candle |
| 2 | All 4 APD stages in sequence, consolidation → expansion, retracement to FVG, reversal pattern |
| 3 | Power of Three (AMD) within NY AM session, kill zone boundaries, daily bias examples |
| 4 | STH/ITH/LTH labels, market structure shift, two-set targeting, OTE zone |
| 5 | HTF/LTF order flow alignment, SMT divergence between NQ and ES |

Each chart needs:
- 100-200 candles of 5-minute or 15-minute NQ data
- Known pattern locations for answer validation
- Realistic price action (not too clean — include noise)
- Deterministic (seeded or hand-crafted)

---

## Safety & Disclaimers

- Course content is educational only — not financial advice
- Performance examples are illustrative — not guarantees
- "This course teaches trading concepts. Trading involves significant risk of loss."
- Disclaimer visible on every course page footer (already in Base.astro)
- No claims about course completion leading to profitability

---

## Acceptance Criteria

1. `/course` landing page exists with curriculum overview
2. Profile questionnaire collects trading experience, struggles, goals
3. Personalized learning path displayed after profile completion
4. 5 module pages with lesson content
5. Each module has 4 assessment types (quiz, chart ID, scenario, engagement)
6. Interactive candlestick charts render with lightweight-charts
7. Chart identification exercises accept click input and validate answers
8. Grading system with pass/fail thresholds
9. Failed assessments show study assignments linked to specific lessons
10. Progress tracked in localStorage
11. Entry models section unlocked after 5 modules complete
12. All content sourced from wiki — no invented ICT concepts
13. All performance claims labeled illustrative
14. Responsive layout, dark theme, matches existing site design
15. `npm run build` passes with no errors

---

_The marketing site course is a Phase 0 deliverable. It validates that traders engage with structured ICT learning and captures qualified leads with rich profile data. The real personalized course system (with AI coaching, journal integration, and Mentor feedback) lives in the product app (`app/`) and is built in Phases 1-3._
