# Phase 0: Research & Validation — Planning Boot Prompt

_Generated 2026-05-10 by `/sync`. Do not edit manually._

## Phase Context

**Phase:** 0 — Research & Validation
**Track:** A (Coaching)
**Status:** in_progress
**Engineer:** Paul Russell
**Estimated effort:** 2 engineers x 3 weeks = 6 engineer-weeks

## Goals

Validate first customer, prototype RAG, select tech stack, confirm editorial curation timeline.

## Deliverables

| # | Deliverable | Priority | Status |
|---|---|---|---|
| 1 | Instructor content access agreement | Gate | Unresolved |
| 2 | RAG prototype with wiki content | P0 | Not started |
| 3 | Vector DB selected (pgvector recommended) | P0 | Not started |
| 4 | Embedding model selected | P0 | Not started |
| 5 | 50 Q&A evaluation pairs | P0 | Not started |
| 6 | Competitive teardown | P1 | Not started |
| 7 | Linear workspace set up | P1 | Done (23 tickets) |
| 8 | CI/CD pipeline (GitHub Actions) | P1 | Not started |
| 9 | Sentry error monitoring | P1 | Not started |
| 10 | Marketing site (6 pages) | P1 | Done |
| 11 | Live Trading Simulator | P1 | In Progress (NEU-27) |

## Exit Criteria

RAG prototype returns relevant passages for **80%+ of test questions**.

## Upstream Deviations

No upstream deviations — Phase 0 is the first phase.

## Current Phase Deviations

1. **Marketing site added** (2026-05-10) — Originally not in Phase 0 scope. Built 6 pages. Phase 3 "landing page" clarified as product app.
2. **Live Trading Simulator added** (2026-05-10) — `/simulator` page. Design spec at `design-handoff/08-live-simulator.md`.
3. **Track C phases added** (2026-05-10) — Phases 11-16 (Business & Operations). Phase 11 gates Phase 1.

## ⚠ Track C Gate Warning

**Phase 11 (Content Licensing)** is `not_started` but gates **Phase 1 (RAG MVP)**. Content licensing work should begin before Phase 0 completes.

## What Already Exists

| Asset | Location |
|---|---|
| ICT knowledge base (5 concepts + 7 entry models + 5 course modules) | `wiki/concepts/business-logic/`, `wiki/concepts/entry-models/`, `wiki/concepts/course/` |
| Transcript pipeline architecture | `wiki/concepts/architecture/transcript-pipeline.md` |
| Source transcripts (20+ files) | `wiki/sources/neurospect/` |
| AI coach system prompt template | `wiki/concepts/ai-coach/system-prompt-template.md` |
| Linear workspace (23 tickets, Phase 0-4) | NeuroSpect-Platform (NEU) |
| Marketing site (6 pages) | `site/` |
| Design handoff package | `design-handoff/` |

## Open Questions & Decisions to Make

### Critical (gates)

1. **Instructor content access commitment** — Single gate for the entire project.
2. **IP / content license agreement** — Needed before ingesting content. Now tracked as Phase 11 deliverable.

### Technical (Phase 0 scope)

3. **pgvector vs external vector DB** — Plan recommends pgvector. Validate for corpus size.
4. **Embedding model** — OpenAI text-embedding-3-small vs BGE-M3. Trade-off: cost vs vendor lock-in vs latency.
5. **Chunking strategy for ICT content** — ICT concepts are interconnected. Naive chunking loses context.

### Product (inform future phases)

6. **Auth provider** — Discord-only or add email/password?
7. **Billing model** — Per-instructor or platform-wide?
8. **Compliance posture** — Legal counsel before beta? (Now tracked as Phase 12)

## Relevant Wiki Content

- `wiki/concepts/architecture/transcript-pipeline.md` — Transcript processing
- `wiki/concepts/ai-coach/system-prompt-template.md` — Draft coaching prompt
- `roadmap/plan.md` §20 — Phase 0 tickets
- `roadmap/plan.md` §27 — NeuroCore architecture (3-signal hybrid search)

## Cross-Wiki Notes

- **Vlad's wiki:** Phase 0 page scaffolded but empty.
- **Paul's wiki:** Phase 0 in_progress. Prompt-versioning module spec at `paul-wiki/components/prompt-versioning-module.md`.

---

_Load this prompt when starting a planning/design session for Phase 0._
