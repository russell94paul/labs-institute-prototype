# NeuroSpect Marketing Site — Sitemap & Page Specs

## Navigation

Fixed top nav (64px height, `bg-black/70` with `backdrop-blur-2xl`):
- Logo (left): Mark + "NeuroSpect" wordmark → links to `/`
- Links (right): Compare | Performance | Course | Research | Workflows | Architecture | Pricing | [Join Waitlist] (CTA button)

## Pages

### 1. Landing Page (`/`)

**Purpose:** First impression. Communicate the product, build excitement, capture emails.

| Section | Component | Content Summary |
|---|---|---|
| Hero | `Hero.astro` | Headline + tagline + 2 CTAs + early access badge |
| Stats Bar | (in Hero) | 4 KPIs: 36K+ lines, 7 entry models, 5 course modules, 100+ journal fields |
| Pain Points | `Problems.astro` | 6 cards: trader problem → NeuroSpect solution |
| AI Coach Demo | `CoachDemo.astro` | Interactive chat mockup + 4 value prop cards |
| Features | `Features.astro` | 8 feature cards with tier badges |
| Waitlist CTA | `WaitlistForm.astro` | Email capture form |

---

### 2. Compare Page (`/compare`)

**Purpose:** Competitive differentiation. Show why NeuroSpect replaces fragmented tools.

| Section | Component | Content Summary |
|---|---|---|
| Hero | `CompareHero.astro` | "Stop Duct-Taping Your Trading Workflow" + 2 anchor CTAs |
| Capability Matrix | `CapabilityMatrix.astro` | 14-capability x 7-tool comparison table |
| Subscription Stack | `SubscriptionStack.astro` | Before ($125-710/mo) vs After ($29-349/mo) cost comparison |
| Workflow Friction | `WorkflowFriction.astro` | Before (7 tools) vs After (1 platform) workflow + 5 KPI cards |
| Questions Grid | `QuestionsGrid.astro` | 8 questions traders can't answer with existing tools |
| Outperform Visual | `OutperformVisual.astro` | 6 cards on where NeuroSpect outperforms |
| CTA | `CompareCTA.astro` | "Numbers Don't Lie" + links to Performance Lab and Waitlist |
| Waitlist | `WaitlistForm.astro` | Email capture |

---

### 3. Performance Lab (`/performance`)

**Purpose:** Eye-catching data visualization. Show traders what structured improvement looks like.

| Section | Component | Content Summary |
|---|---|---|
| Hero | `PerformanceHero.astro` | "Performance Lab" intro + disclaimer |
| Trader Maturity | `TraderMaturity.astro` | 4 trader tier cards showing progression |
| Equity Curve | `EquityCurveChart.astro` | **INTERACTIVE CHART** — Chart.js line chart, 4 equity curves over 20 trading days, clickable trade markers |
| KPI Summary | `KpiSummaryCards.astro` | Key metrics per tier (win rate, PnL, profit factor, etc.) |
| Trade Detail | `TradeDetailPanel.astro` | **INTERACTIVE SLIDE PANEL** — Opens on chart marker click, shows per-tier outcome comparison |
| Analytics Tabs | `AnalyticsTabs.astro` | **INTERACTIVE TABS + CHART** — Day-of-week bar chart, session table, setup table, mistakes grid, risk metrics |
| Tier Analytics | `TierAnalyticsPanel.astro` | **INTERACTIVE ACCORDION** — Expandable per-tier detailed metrics (core, risk, quality, highlights) |
| Improvement Table | `TraderImprovementTable.astro` | Before/after improvement table per tier |
| Bottom CTA | `PerformanceBottom.astro` | Summary + CTA |
| Waitlist | `WaitlistForm.astro` | Email capture |

---

### 4. Interactive ICT Course (`/course`)

**Purpose:** Free-tier interactive course. Content marketing + lead qualification.

| Section | Component | Content Summary |
|---|---|---|
| Hero | `CourseHero.astro` | "Master ICT Concepts. Prove It on the Chart." + curriculum preview |
| Curriculum | `ModuleOverview.astro` x5 | 5 module cards in vertical timeline/stepper with lock state |
| What You'll Learn | (inline) | 6-card grid of learning outcomes |
| Assessment Preview | (inline) | 4 cards previewing quiz, chart ID, scenarios, engagement |
| CTA | `CourseCTA.astro` | "Join the Waitlist to Start Learning" → `/course/profile` |
| Waitlist | `WaitlistForm.astro` | Email capture |

**Sub-pages:**

| Page | Purpose |
|---|---|
| `/course/profile` | Trading profile questionnaire (4 steps: experience, style, struggles, goals) → personalized path |
| `/course/module-1` through `/course/module-5` | Lesson content + 4 assessments per module |
| `/course/entry-models` | Capstone: 7 entry model deep-dives (unlocked after 5 modules) |

**Interactive elements:**
- `ConceptQuiz.astro` — Multiple choice with explanations
- `ChartIdentification.astro` — Click on candlestick chart to identify ICT patterns (lightweight-charts)
- `ScenarioEngine.astro` — Branching "what would you do?" with A+/B/C/F grading
- `EngagementTest.astro` — Drag-to-match, sequencing, time-pressure chart ID
- `GradingPanel.astro` — Pass/fail with study assignments on failure
- `ProgressTracker.astro` — Module + assessment completion tracking (localStorage)

**Design spec:** See `09-course.md` for full wireframes, assessment designs, chart specs, and data requirements.

---

### 5. EdgeLab Research Studio (`/research`)

**Purpose:** Interactive demo of EdgeLab's three research engines. Flagship technical credibility page.

| Section | Component | Content Summary |
|---|---|---|
| Hero | `ResearchHero.astro` | "Your Trading Edge, Engineered" + launch terminal CTA |
| Engine Overview | `EngineCards.astro` | 3 neon cards: Feature Discovery, Regime Optimization, NSLM Studio |
| Feature Discovery | `FeatureDiscovery.astro` | Before/after model comparison + 10-row feature table |
| Regime Optimization | `RegimeOptimization.astro` | 6 regime cards + parameter adjustment table + dynamic condition modifiers |
| NSLM Feature Studio | `FeatureStudio.astro` | **INTERACTIVE TERMINAL** — Add features, run simulations, compare results, parameter sweeps |
| Feature Library | `FeatureLibrary.astro` | Searchable/filterable feature catalog (20+ features) |
| CTA | `ResearchCTA.astro` | "Stop guessing. Start engineering." + waitlist |
| Waitlist | `WaitlistForm.astro` | Email capture |

**Interactive elements:**
- Feature injection (add/remove features with sliders and toggles)
- Simulation runner (pre-computed results, animated display)
- Parameter sweep (table + chart showing optimal zones)
- Run comparison (side-by-side metrics table)
- Dynamic condition selectors (regime, day, news, SMT, liquidity, price cycle)
- NSLM reasoning sample with feature suggestion

**Design spec:** See `10-edgelab-studio.md` for full wireframes, terminal layout, and data requirements.

---

### 6. Workflows Page (`/workflows`)

**Purpose:** Show how NeuroSpect serves 4 trader profiles, from beginner to automated.

| Section | Component | Content Summary |
|---|---|---|
| Hero | (inline) | "Four Ways to Trade with NeuroSpect" + progression indicator |
| Tier 1 | `WorkflowTier.astro` | Discretionary ICT Trader — workflow steps + components |
| Tier 2 | `WorkflowTier.astro` | Quant Trader |
| Tier 3 | `WorkflowTier.astro` | Hybrid Trader |
| Tier 4 | `WorkflowTier.astro` | S-Tier Trader (with safety callout) |
| Waitlist | `WaitlistForm.astro` | Email capture |

---

### 7. Architecture Page (`/architecture`)

**Purpose:** Technical credibility. Show the 6-component system and how data flows.

| Section | Component | Content Summary |
|---|---|---|
| Hero | (inline) | "Six Components. One Platform." |
| Diagram | (inline SVG) | **ANIMATED SVG** — 6 component nodes with neon glow, animated connection lines with flowing particles, layer labels |
| Component Cards | (inline) | 6 neon-card detail cards (one per component) |
| Data Flow | (inline) | 4-step numbered explanation (Ingest → Retrieve → Research → Execute) |
| Waitlist | `WaitlistForm.astro` | Email capture |

---

### 8. Pricing Page (`/pricing`)

**Purpose:** Clear tier comparison. Drive waitlist signups.

| Section | Component | Content Summary |
|---|---|---|
| Hero | (inline) | "Grow Into Your Edge" |
| Tier Cards | (inline) | 6 pricing cards: Free ($0) → Team ($499/mo). "Most Popular" on Trader ($99). |
| Educator CTA | (inline) | "For ICT Educators & Mentors" — $199/mo + 15-25% revenue share |
| Note | (inline) | Launch pricing + early access lock-in |
| Waitlist | `WaitlistForm.astro` | Email capture |

---

## Shared Components

| Component | Used On | Purpose |
|---|---|---|
| `Base.astro` (layout) | All pages | Nav + footer + ScrollAnimator + meta tags |
| `WaitlistForm.astro` | All pages | Email capture form with success state |
| `ScrollAnimator.astro` | All pages | IntersectionObserver for scroll-triggered animations |

## Footer

All pages: Logo + legal disclaimer ("NeuroSpect is an educational tool. Not financial advice. Past performance does not guarantee future results. Trading involves risk of loss.")
