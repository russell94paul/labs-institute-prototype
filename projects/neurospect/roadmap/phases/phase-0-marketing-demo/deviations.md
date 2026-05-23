---
phase: 0
name: "Research & Validation"
created: 2026-05-09
updated: 2026-05-13
---

# Phase 0 Deviations

## Deviation: Marketing site added as Phase 0 deliverable
- **Planned:** Marketing-site boot prompt existed but was explicitly scoped as "NOT part of the Phase 0-10 roadmap." Phase 0 deliverables were research-only (RAG prototype, vector DB, embeddings, eval pairs).
- **Actual:** Marketing site formally added to Phase 0. Built 6 pages: landing (`/`), compare (`/compare`), performance lab (`/performance`), workflows, architecture, pricing. Tech stack: Astro 5.8 + Tailwind 3.4 + Chart.js. Compare page is pure HTML/CSS; performance page uses Chart.js for interactive equity curves, radar charts, and analytics dashboards. All performance data is synthetic/illustrative.
- **Impact on future phases:** Phase 3 "landing page" deliverable now clarified as the product app landing page (in `app/`), distinct from the marketing site (in `site/`). Phase 0 now has two parallel work streams: (1) technical validation and (2) marketing/waitlist. No impact on Phase 1+ technical work.
- **Date:** 2026-05-10
- **Engineer:** Paul Russell

## Deviation: Live Trading Simulator added as Phase 0 deliverable
- **Planned:** Marketing site was a static 6-page waitlist site with pre-rendered charts and mock data.
- **Actual:** Live Trading Simulator (`/simulator`) added as a major new page. Runs all 4 trader tiers simultaneously against pre-scripted market events with real-time candlestick chart, tier reasoning animations, trade logging, loss analysis with mistake identification, concept review references, and improvement actions. Requires candlestick charting library (lightweight-charts or custom Canvas), event-driven playback engine, and ~3 pre-scripted trading scenarios with full tier action data. Design spec at `design-handoff/08-live-simulator.md`.
- **Impact on future phases:** No impact on Phase 1+ technical work. Simulator uses synthetic data and runs entirely client-side. The simulation data model (TierAction, SimulationEvent) may inform the actual EdgeLab event schema in Phase 7, but they are independent implementations.
- **Date:** 2026-05-10
- **Engineer:** Paul Russell

## Deviation: Interactive ICT Course added as Phase 0 deliverable
- **Planned:** Marketing site was a 6-page static site + live simulator. No educational content beyond the main product coaching flow (Phase 1+).
- **Actual:** Interactive ICT Course (`/course`) added as a major new section. Free-tier course accessible after waitlist signup. 5 modules, 18 lessons sourced from `wiki/concepts/course/` and `wiki/concepts/entry-models/`. Includes trading profile questionnaire, 4 assessment types per module (concept quiz, interactive chart identification, scenario engine, engagement tests), interactive candlestick charts via lightweight-charts, pass/fail grading with study assignments, and localStorage progress tracking. Capstone: Entry Models Library (7 strategies, unlocked after 5 modules). Design spec at `design-handoff/09-course.md`, boot prompt at `boot-prompts/course.md`.
- **Impact on future phases:** Course content validates wiki structure for RAG ingestion (Phase 1) — the course exercises test whether wiki content is structured well enough for interactive use. The assessment framework (quiz → grade → study assignment) may inform the coaching evaluation framework in Phase 4. No impact on Phase 1+ code. Adds lightweight-charts as a dependency (also used by simulator).
- **Date:** 2026-05-12
- **Engineer:** Paul Russell

## Deviation: EdgeLab Research Studio added as Phase 0 deliverable
- **Planned:** Marketing site focused on coaching product positioning. EdgeLab was a Phase 7+ concern with no public-facing presence before then.
- **Actual:** EdgeLab Research Studio (`/research`) added as an interactive demo page. Three engines: (1) Feature Discovery Engine — analyzes trade outcomes, discovers separating features, auto-engineers new ones; (2) Regime-Adaptive Optimization — classifies 6 market regimes, auto-tunes parameters, applies dynamic condition modifiers; (3) NSLM Feature Studio — injects features into NSLM prompts, runs simulations, sweeps parameters. Includes interactive research terminal, parameter sweep visualization, 20+ feature library, and NSLM reasoning samples. Design spec at `design-handoff/10-edgelab-studio.md`, boot prompt at `boot-prompts/edgelab-studio.md`.
- **Impact on future phases:** The research studio's data models and UI patterns are synthetic/illustrative but will inform EdgeLab's actual API design in Phase 7. Feature library definitions may seed the real feature registry. No code dependency — Phase 7 builds its own backend. Establishes technical credibility positioning for quant-curious traders.
- **Date:** 2026-05-12
- **Engineer:** Paul Russell

## Deviation: neurospect-ui replaces site/ as primary marketing codebase
- **Planned:** Astro SSG marketing site (`site/`) with Tailwind + Chart.js.
- **Actual:** React 18 CDN interactive demo app (`neurospect-ui/`) replaces `site/`. Uses custom CSS, SVG equity curves, candlestick simulator, typing-animation AI coach demo, hash-based routing, no build step. Richer interactivity than Astro site. `site/` is deprecated.
- **Impact on future phases:** All roadmap/boot-prompt references to `site/` need updating. Tech stack changed from SSG to CSR. No build tooling simplifies deployment but loses Astro's SSG benefits.
- **Date:** 2026-05-13
- **Engineer:** Paul Russell

## Deviation: Product overview & user guide document created
- **Planned:** No product documentation deliverable in Phase 0 scope.
- **Actual:** 1,922-line product overview at `docs/neurospect_product_overview_user_guide.md` covering all 6 components, tier workflows, EdgeLab engines, course curriculum, competitive matrix, pricing, analytics surfaces, and glossary.
- **Impact on future phases:** Content source for marketing, onboarding, and investor materials. Gaps (onboarding UX, API docs, security/privacy) become Phase 3-5 deliverables.
- **Date:** 2026-05-13
- **Engineer:** Paul Russell
