---
phase: 0
name: "Research & Validation"
status: in_progress
paul_status: in_progress
vlad_status: not_started
assigned: [paul]
tickets_total: 6
tickets_done: 0
created: 2026-05-09
updated: 2026-05-13
---

# Phase 0: Research & Validation

_Canonical phase definition: `roadmap/phases/phase-0-research/README.md`_
_Boot prompts: `roadmap/phases/phase-0-research/boot-prompts/`_

## My Tickets

| Ticket | Status | Title |
|---|---|---|
| NEU-5 | Todo | Set up pgvector on existing PostgreSQL |
| NEU-6 | Todo | Evaluate embedding models |
| NEU-7 | Todo | Research chunking strategies |
| NEU-8 | Todo | Set up CI/CD pipeline |
| NEU-9 | Todo | Set up Sentry monitoring |
| NEU-27 | In Progress | Build live trading simulator page |

## Notes

### Marketing Site (2026-05-10)

Built Compare + Performance Lab pages as part of Phase 0 marketing site work.
- `/compare` — competitive intelligence (capability matrix, subscription stack, workflow friction)
- `/performance` — illustrative trader performance analytics (equity curves, KPIs, trade markers)
- Added Chart.js for interactive charts on performance page
- All data is synthetic/illustrative — clearly labeled as demo data
- See `roadmap/phases/phase-0-research/boot-prompts/marketing-site.md` for full site scope

### NEU-27: Live Simulator (2026-05-10)

Design handoff package delivered (`design-handoff/`). Next: implement `/simulator` page with interactive trading simulation.

### neurospect-ui replaces site/ (2026-05-13)

`neurospect-ui/` (React 18 CDN) is now the primary marketing site, replacing `site/` (Astro SSG).
- Phase 0 restructured into 0A (Marketing/Demo) and 0B (Technical Validation)
- Naming reconciliation done: "Sovereign Architect" → "S-Tier Trader", "Adaptive Edge Engine" → "EdgeLab Research Studio"
- "Launch App" nav link added pointing to product app
- Product guide tracked as deliverable (`docs/neurospect_product_overview_user_guide.md`)
- 7 boot prompts now available for Phase 0 (planning, execution, course, edgelab-studio, marketing-site, neurospect-ui, product-guide)

---

_Status fields synced from Linear + roadmap by `/sync`._
