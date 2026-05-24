# EdgeLab Research Studio Page — Boot Prompt

_Generated 2026-05-11. Marketing site interactive research demo for Phase 0._

## What to Build

An interactive `/research` page on the marketing site that demonstrates EdgeLab's three core research engines through a live "research terminal" experience. Users inject features into an NSLM model, run simulations, sweep parameters, compare results, and watch the system adapt to market conditions.

## Three Engines (Formalized Names)

### 1. EdgeLab Feature Discovery Engine
Analyzes historical trade outcomes. Identifies patterns in wins vs losses. Automatically engineers, ranks, adds, or removes features to improve model performance. Turns every loss into a learning signal.

### 2. Regime-Adaptive Optimization Engine
Classifies the market into 6 regimes (Trending Bull/Bear, Range, HV Expansion, LV Compression, Transition). Auto-adjusts model parameters per regime. Applies dynamic condition modifiers (day of week, economic news, SMT, session liquidity, price cycle phase).

### 3. NSLM Feature Studio
Injects quantitative features as structured parameters into NSLM prompts. Runs iterative simulations to find optimal feature values. NSLM proposes new bespoke features by combining quantitative signals with ICT domain knowledge. New features validate via backtest and promote to the Feature Library.

## Technical Approach

- Route: `/research`
- Components: `site/src/components/research/` (11 components)
- Data: `site/src/data/` — features.ts, simulation-results.ts, regime-parameters.ts, sweep-results.ts
- Charts: Chart.js (equity curves, sweep charts, bar charts)
- All simulation results pre-computed (no real-time ML) — TypeScript lookup tables
- Interactive controls: vanilla JS in `<script>` tags (same pattern as performance page)

## Design Spec

Full wireframes, terminal layout, feature table, and interaction flow: `design-handoff/10-edgelab-studio.md`

## Content Sources

| Content | Source |
|---|---|
| Feature definitions | `roadmap/plan.md` §20-21 (Phase 7-8 feature store, detectors) |
| Regime classifications | `roadmap/plan.md` §21 (Phase 8 regime detector) |
| NSLM evaluation | `roadmap/plan.md` §20 Phase 7C (NSLM evaluation framework) |
| ICT concepts for features | `wiki/concepts/business-logic/*.md` |
| Entry model checklists | `wiki/concepts/entry-models/*.md` |

## Acceptance Criteria

1. `/research` page exists with hero, 3-engine overview, and all sections
2. Feature Discovery section shows before/after model comparison with 10+ features
3. Regime section shows 6 regime cards with parameter adjustment table
4. NSLM Feature Studio is interactive: add features, run simulations, see results
5. Parameter sweep shows table + chart with optimal zone
6. Comparison table supports multiple saved runs
7. Dynamic condition selectors work (regime, day, news, SMT, liquidity, price cycle)
8. Feature Library is searchable/filterable
9. All data is illustrative — clearly labeled
10. `npm run build` passes

_This is a Phase 0 marketing site deliverable. The real EdgeLab engines are built in Phases 7-8._
