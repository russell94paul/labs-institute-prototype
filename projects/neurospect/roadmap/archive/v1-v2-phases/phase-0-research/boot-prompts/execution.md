# Phase 0: Research & Validation — Execution Boot Prompt

_Generated 2026-05-12 by `/phase 0`. Do not edit manually._

## Phase Context

**Phase:** 0 — Research & Validation
**Track:** A (Coaching)
**Status:** in_progress
**Engineer:** Paul Russell — working on NEU-27 (live simulator) + Phase 0 research
**Assigned:** Paul
**Exit Criteria:** RAG prototype returns relevant passages for **80%+ of test questions**.

## What to Build

Validate first customer, prototype RAG, select tech stack, confirm editorial curation timeline.

### Deliverables (by priority)

| # | Deliverable | Priority | Status |
|---|---|---|---|
| 1 | Instructor content access agreement | Gate | Unresolved |
| 2 | RAG prototype with wiki content (retrieval quality benchmarked) | P0 | Not started |
| 3 | Vector DB selected (pgvector recommended) | P0 | Not started |
| 4 | Embedding model selected (text-embedding-3-small recommended) | P0 | Not started |
| 5 | 50 Q&A evaluation pairs | P0 | Not started |
| 6 | Competitive teardown (Price Action Lover, ICT GPTs) | P1 | Not started |
| 7 | Linear workspace set up | P1 | Done (23 tickets created) |
| 8 | CI/CD pipeline (GitHub Actions) | P1 | Not started |
| 9 | Sentry error monitoring | P1 | Not started |
| 10 | Marketing site (Astro + Tailwind + Chart.js) | P1 | Done (6 pages built) |
| 11 | Live Trading Simulator (`/simulator`) | P1 | In Progress (NEU-27) — design spec in `design-handoff/08-live-simulator.md` |
| 12 | Interactive ICT Course (`/course`) — 5 modules, 4 assessment types | P1 | Scoped, not built — `design-handoff/09-course.md`, `boot-prompts/course.md` |
| 13 | EdgeLab Research Studio (`/research`) — 3 engines, interactive terminal | P1 | Scoped, not built — `design-handoff/10-edgelab-studio.md`, `boot-prompts/edgelab-studio.md` |

## Active Linear Tickets

Phase 0 tickets — 5 Todo + 1 In Progress, all assigned to **Paul**:

| Ticket | State | Priority | Title |
|---|---|---|---|
| **NEU-27** | **In Progress** | High | Build live trading simulator page (/simulator) |
| NEU-5 | Todo | Urgent | Set up pgvector on existing PostgreSQL |
| NEU-6 | Todo | Urgent | Evaluate embedding models (OpenAI 3-small vs BGE-M3) |
| NEU-7 | Todo | High | Research chunking strategies for ICT content |
| NEU-8 | Todo | High | Set up CI/CD pipeline (GitHub Actions) |
| NEU-9 | Todo | High | Set up Sentry error monitoring |

**Suggested execution order:** NEU-27 (in progress) → NEU-5 → NEU-6 → NEU-7 → (NEU-5+6+7 feed the RAG prototype) → NEU-8 → NEU-9

## Key Files to Create or Modify

| File / Directory | Purpose | Exists? |
|---|---|---|
| `api/app/models/wiki_chunk.py` | SQLAlchemy model for wiki chunks + pgvector column | No |
| `api/app/coach/rag/` | RAG retrieval pipeline module | No |
| `api/app/coach/rag/ingest.py` | Wiki content → chunks → embeddings pipeline | No |
| `api/app/coach/rag/retrieve.py` | Hybrid retrieval (BM25 + semantic + entity) | No |
| `api/app/routers/chat.py` | Coaching chat API endpoint | No |
| `api/alembic/versions/` | Migration: pgvector extension + wiki_chunks table | Exists (dir) |
| `evals/phase0/` | 50 Q&A evaluation pairs + eval harness | No |
| `wiki/concepts/architecture/rag-pipeline.md` | Architecture doc for RAG decisions | No |

## Technical Decisions Made

### From planning sessions

- **Vector DB:** pgvector (plan recommendation) — avoid separate service for small corpus
- **Embedding model:** Evaluate OpenAI text-embedding-3-small vs BGE-M3 (NEU-6)
- **Transcript pipeline:** Manual + Whisper (decided during kickoff)
- **Monorepo structure:** api/ + app/ + wiki/ merged (done)
- **Retrieval architecture:** 3-signal hybrid search via Reciprocal Rank Fusion (keyword/BM25 + semantic/pgvector + entity/tag) — see `roadmap/plan.md` §27

### Open technical questions

- **Chunking strategy** for ICT content — concepts are interconnected, naive chunking loses context (NEU-7)
- **Auth provider** — Discord-only or add email/password? (inform Phase 3)
- **Billing model** — per-instructor or platform-wide? (inform Phase 3)

## What Already Exists (head start)

| Asset | Location |
|---|---|
| ICT knowledge base (5 concepts + 7 entry models + 5 course modules) | `wiki/concepts/business-logic/`, `wiki/concepts/entry-models/`, `wiki/concepts/course/` |
| Transcript pipeline architecture | `wiki/concepts/architecture/transcript-pipeline.md` |
| Source transcripts (20+ files) | `wiki/sources/neurospect/` |
| Live commentary concepts | `wiki/concepts/business-logic/ict-live-commentary.md` |
| AI coach system prompt template | `wiki/concepts/ai-coach/system-prompt-template.md` |
| Linear workspace (23 tickets, Phase 0-4) | NeuroSpect-Platform (NEU) |
| Marketing site (6 pages) | `site/` |
| Design handoff package (8 docs) | `design-handoff/` |

## Upstream Deviations

No upstream deviations — Phase 0 is the first phase. Plan assumptions are current.

## Current Phase Deviations

### 1. Marketing site scope expansion (2026-05-10)
- **Planned:** Marketing-site boot prompt existed but was explicitly "NOT part of the Phase 0-10 roadmap"
- **Actual:** Marketing site formally added as Phase 0 deliverable. Built 6 pages including `/compare` (competitive intelligence) and `/performance` (illustrative trader performance analytics with Chart.js).
- **Impact:** Phase 0 now has two work streams: (1) technical validation and (2) marketing site. Phase 3 "landing page" clarified as product app landing page.

### 2. Live Trading Simulator added (2026-05-10)
- **Planned:** Marketing site was a static 6-page waitlist site.
- **Actual:** Live Trading Simulator (`/simulator`) added. Runs 4 trader tiers simultaneously against pre-scripted market events. Design spec at `design-handoff/08-live-simulator.md`.
- **Impact:** No impact on Phase 1+ technical work. Simulator data model may inform EdgeLab event schema (Phase 7) but they are independent.

### 3. Track C phases added (2026-05-10)
- **Planned:** Phases 0-10 only.
- **Actual:** Track C (Business & Operations) phases 11-16 added: Content Licensing, Regulatory, Go-to-Market, Retention, Competitive Intelligence, Team Scaling.
- **Impact:** Phase 11 (Content Licensing) gates Phase 1. Should start in parallel with Phase 0.

## Cross-Wiki Notes

- **Vlad's wiki:** Phase 0 page scaffolded but empty — no personal research notes yet.
- **Paul's wiki:** Phase 0 in_progress. Has a prompt-versioning module design spec (`paul-wiki/components/prompt-versioning-module.md`). `prompts/` directory scaffolded at repo root.

## ⚠ Track C Gate Warning

**Phase 11 (Content Licensing)** is `not_started` but gates **Phase 1 (RAG MVP)**. The instructor content access agreement is also the single gate for Phase 0. Content licensing work should begin before Phase 0 technical validation completes.

## Critical Gate

**Instructor content access agreement** — This is the single gate for the entire project. No evidence it has been resolved. Phase 0 technical work (pgvector, embeddings, chunking) can proceed in parallel, but the RAG prototype cannot be validated against real instructor content without this agreement.

## Reference

- `roadmap/plan.md` §20 — Phase 0 GitHub issues
- `roadmap/plan.md` §27 — NeuroCore architecture (3-signal hybrid search)
- `wiki/concepts/ai-coach/system-prompt-template.md` — Draft coaching prompt
- `wiki/concepts/architecture/transcript-pipeline.md` — Transcript processing decisions

---

_Load this prompt when starting an implementation session for Phase 0._
