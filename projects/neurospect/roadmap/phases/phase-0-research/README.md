---
phase: 0
name: "Research & Validation"
status: in_progress
track: "A (Coaching)"
assigned: [paul]
started: 2026-05-10
completed: null
tickets_total: 6
tickets_done: 0
created: 2026-05-09
updated: 2026-05-13
---

# Phase 0: Research & Validation

Validate first customer, prototype RAG, select tech stack, confirm editorial curation timeline.

## Goals

_See `roadmap/plan.md` Phase 0 for detailed goals._

## Exit Criteria

_See `roadmap/plan.md` Phase 0 for exit criteria._

## Deliverables

### Phase 0A: Marketing, Demo & Product Positioning

#### Marketing Site (`neurospect-ui/`)

Interactive marketing/demo site deployed separately from the product app. Replaces the deprecated `site/` (Astro SSG) codebase.

Pages:
- `/` — Landing (hero, pain points, features, waitlist)
- `/compare` — Competitive Intelligence (capability matrix, subscription stack, workflow friction)
- `/performance` — Performance Lab (illustrative equity curves, KPI analytics, trade marker analysis)
- `/course` — Interactive ICT Course (5 modules, 18 lessons, 4 assessment types, candlestick charts)
- `/course/profile` — Trading profile questionnaire (experience, goals, struggles)
- `/course/module-1` through `/course/module-5` — Module pages with lessons + assessments
- `/course/entry-models` — Capstone: Entry Models Library (unlocked after 5 modules)
- `/research` — EdgeLab Research Studio (interactive feature injection, regime optimization, NSLM feature studio)
- `/workflows` — Trader tier profiles
- `/architecture` — System diagram
- `/pricing` — Pricing tiers

Tech: React 18 CDN + Custom CSS + SVG visualizations (candlestick simulator, equity curves, typing-animation AI coach demo). Hash-based routing, no build step.
Deploy: Cloudflare Pages (TBD)

> **Note:** `site/` (Astro 5.8 + Tailwind 3.4 + Chart.js) is deprecated. All marketing site work now happens in `neurospect-ui/`.

#### Live Trading Simulator (NEU-27)

Multi-tier live trading simulator with real-time candlestick chart, tier reasoning animations, trade logging, and loss analysis.

#### Interactive ICT Course (`/course`)

Free-tier course accessible after waitlist signup. Content sourced from `wiki/concepts/course/` (5 modules, 18 lessons) and `wiki/concepts/entry-models/` (7 strategies).

Key features:
- Trading profile questionnaire → personalized learning path
- 4 assessment types per module: concept quiz, interactive chart identification, scenario engine, engagement tests
- Interactive candlestick charts for chart identification exercises
- Grading: pass (advance) / fail (study assignment based on mistakes)
- Progress tracked in localStorage
- Tier-specific course sections showing what each pricing tier unlocks

Boot prompt: `boot-prompts/course.md`

#### EdgeLab Research Studio (`/research`)

Interactive demo of EdgeLab's three research engines — the technical credibility page for quant-curious traders.

Three engines:
1. **Feature Discovery Engine** — analyzes trade outcomes, discovers features that separate wins from losses, auto-engineers new features
2. **Regime-Adaptive Optimization** — classifies 6 market regimes, auto-tunes parameters per regime, applies dynamic condition modifiers
3. **NSLM Feature Studio** — injects features into NSLM prompts, runs simulations, sweeps parameters, generates bespoke feature suggestions

Key features:
- Interactive research terminal: add features → run simulation → compare results
- Parameter sweep with optimal zone visualization
- Dynamic condition selectors (regime, day, news, SMT, liquidity swept, price cycle)
- Feature Library with 20+ features, searchable/filterable
- NSLM reasoning samples with feature-by-feature gate checks

Boot prompt: `boot-prompts/edgelab-studio.md`

#### Product Guide (`docs/`)

Product overview and user guide at `docs/neurospect_product_overview_user_guide.md`. Covers all 6 components, tier workflows, EdgeLab engines, course curriculum, competitive matrix, pricing, analytics surfaces, and glossary.

Boot prompt: `boot-prompts/product-guide.md`

#### Design Handoff Package

Design specs in `design-handoff/` for all marketing site pages.

#### App Navigation Link

Navigation link from product app (`app/`) to marketing site (`neurospect-ui/`).

#### Naming Reconciliation

Ensure all product names match canonical names defined in `CLAUDE.md` product hierarchy across all marketing pages, docs, and boot prompts.

**Phase 0A exit criteria:** All marketing pages functional in `neurospect-ui/`, naming consistent with canonical product hierarchy, deployed to hosting, app nav link works.

### Phase 0B: Technical Validation

- Instructor content access agreement (gate)
- RAG prototype with wiki content
- Vector DB: pgvector (NEU-5)
- Embedding model: text-embedding-3-small (NEU-6)
- Chunking research (NEU-7)
- 50 Q&A evaluation pairs
- CI/CD pipeline (NEU-8)
- Sentry error tracking (NEU-9)

**Phase 0B exit criteria:** RAG prototype returns relevant passages for 80%+ of test questions.

## Boot Prompts

- `boot-prompts/planning.md`
- `boot-prompts/execution.md`
- `boot-prompts/course.md`
- `boot-prompts/edgelab-studio.md`
- `boot-prompts/neurospect-ui.md`
- `boot-prompts/product-guide.md`

## Deviations

Captured in `deviations.md` as implementation progresses.
