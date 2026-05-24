---
tags: [decision, architecture, conductor]
status: accepted
created: 2026-05-23
updated: 2026-05-23
sources: [roadmap/status.md, CLAUDE.md, project.json]
---

# DEC-001: Neurospect → Conductor Integration

## Decision

Integrate Neurospect fully into the Conductor framework by fixing broken metadata, archiving stale artifacts, and connecting to Conductor's phase engine and memory store — without touching any working product code.

## Audit Findings (2026-05-23)

### What's Production-Ready (Untouched)
- **Backend** (api/): FastAPI + SQLAlchemy 2.x async + Postgres 16. 9 routers, 9 models, 11 enums, 6 services, 5 Alembic migrations, 9 test files.
- **Frontend** (app/): React 19 + TS + Vite + shadcn/ui. 15 pages, 35+ components, 9 hooks. Full trade journal, analytics, AI coach, Prop Shield, billing.
- **Wiki** (wiki/): 135+ pages. ICT business logic, course (5 modules, 17 pages), 7 entry models with YAML, 8 architecture docs, 60+ source transcripts.
- **Phase commands** (.claude/commands/ns-phase*.md): 15 files with detailed deliverables/constraints/acceptance criteria.

### What Was Broken (Fixed)
1. **project.json**: Was "parked" with empty phases. → Now "active" with all 13 phases, correct statuses, stack definition.
2. **Phase READMEs**: 6 had wrong frontmatter (said not_started when complete/in_progress). All were empty stubs. → All 13 now have correct status/dates, inline goals/deliverables/constraints/acceptance criteria from command files.
3. **30 phase directories**: 17 stale v1/v2 artifacts. → Moved to roadmap/archive/v1-v2-phases/.
4. **No memory store**: → Initialized with 8 seed memories (decisions, milestones, patterns).
5. **NeuroLLM.md**: Stale v0 spec in project root. → Moved to initial-plan/NeuroLLM-v0.md.

### Phase Status (from status.md)
| Phase | Status | Notes |
|---|---|---|
| 0 (Marketing) | in_progress | 0A substantially complete, 0B not started |
| 1 (Data Foundation) | **complete** | 2026-05-10 → 2026-05-13 |
| 2 (Trader Workspace) | in_progress | Analytics done, journal/behavior WIP |
| 3 (Prop Shield) | **complete** | 2026-05-10 → 2026-05-13, FIRST REVENUE |
| 4-5 (Events, EdgeLab) | not_started | Blocked on research |
| 6 (AI Trade Review) | in_progress | Basic Claude calls, no RAG |
| 7-9 | not_started | |
| 10 (Allocation) | in_progress | Code in worktree |
| 11 (ML) | not_started | Deep research needed |
| 3-NG (NeuroGraph) | in_progress | Research only |

## Conductor Mapping Decisions

| Neurospect | Conductor | Decision |
|---|---|---|
| NeuroCore (3-signal retrieval) | memory.py (keyword-only) | **Separate concerns.** memory.py for project decisions/learnings. NeuroCore stays in api/ as domain-specific RAG. |
| wiki/ (135+ pages) | project wiki | **Already in place.** Mature, keep as-is. |
| Mentor (AI coaching) | No equivalent | **Domain-specific.** Keep in api/app. |
| NeuroGraph | No equivalent | **Domain-specific.** Keep in api/app. |
| roadmap/ phases | project.json phases[] | **Populated.** project.json has all 13 phases. roadmap/ keeps detailed specs. |
| neurospect-ui/ | Separate from dashboard | **Old marketing UI.** Not the ops dashboard. Keep separate. |
| .claude/commands/ | Session boot prompts | **Keep as slash commands.** Session-level, not pipeline-level. |

## Gap Analysis

### Research Done
- ICT knowledge base: 135+ wiki pages, 5 course modules, 7 entry models with YAML
- Tech stack decisions: all documented in wiki/concepts/architecture/
- Trade schema: fully designed and implemented
- AI Coach architecture: designed and implemented
- Prop Shield: designed and implemented
- Marketing design: comprehensive 12-page design handoff

### Research Needed (Future Sessions)
| Topic | Phase | What to Investigate |
|---|---|---|
| ICT event detection algorithms | P4 | FVG/sweep/OB detection primitives, market data APIs |
| Backtesting framework | P5 | vectorbt vs custom, Monte Carlo, walk-forward |
| Hybrid retrieval (NeuroCore) | P6 | BM25 + pgvector + entity, Reciprocal Rank Fusion |
| Graph schema design | P3-NG | Node/edge types, temporal awareness, Neo4j vs Postgres CTEs |
| NSLM model family | P11 | ICT-aware model design, evaluation methodology |

### Can Start Immediately
- Continue Phase 2 (Trader Workspace — behavior metrics, journal enhancements)
- Continue Phase 0B (CI/CD, Sentry, data model audit)
- Phase 4 research (ICT event detection design)

## What Changed

Files modified:
- `project.json` — rewritten with correct metadata
- `roadmap/phases/phase-*/README.md` — all 13 reconciled with status.md + populated with deliverables
- `roadmap/archive/` — created with 17 stale directories
- `memory/` — initialized with 8 seed memories
- `initial-plan/NeuroLLM-v0.md` — moved from project root

Files NOT modified:
- api/ (all backend code)
- app/ (all frontend code)
- wiki/ (all knowledge base pages)
- .claude/commands/ (all phase boot prompts)
- roadmap/status.md (authoritative status dashboard)
