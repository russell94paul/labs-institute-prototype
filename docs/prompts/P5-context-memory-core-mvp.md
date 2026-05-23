# P5 — Context + Memory Core MVP

**Phase:** P5-context-memory
**Priority:** P5
**Dependencies:** P4-agent-runtime
**Decisions required:** DEC-005 (vector store), DEC-006 (wiki role), DEC-007 (memory provider), DEC-008 (memory store scope)
**Research required:** Topic 05 synthesis (completed), Topic 08 synthesis (completed)
**Risk:** High
**Complexity:** XL

---

## Goal

Build the memory ledger and context retrieval engine. Agents need context to make good decisions. This phase implements the memory candidate lifecycle, project context packs, embedding pipeline, and memory governance UI.

## Context

Synthesis 05 recommends a governed evidence system: memory as a ledger with candidate lifecycle (draft → candidate → safety_scanned → evaluated → approved → active → monitored). Synthesis 08 defines the hybrid context fabric with 5 memory planes (project, workspace, organization, optional global) and hybrid retrieval (structured + vector + graph).

DEC-008 recommends a minimal 3-table ledger for MVP: `memories`, `memory_evidence`, `memory_retrieval_events`. This avoids overengineering while validating the core memory loop.

The current system uses JSON files for all state. This phase adds the memory abstraction without requiring a full PostgreSQL migration — the initial implementation can use JSON-backed storage behind a provider interface that will swap to Postgres later.

## Scope

### Engine: `engine/memory.py`

Memory ledger:
- Memory CRUD: create, read, update, archive, quarantine
- Candidate lifecycle: draft → candidate → validated → active → quarantined
- Evidence linking: connect memories to source artifacts (files, sessions, events)
- Retrieval logging: track which memories were retrieved, when, by whom
- Memory scoping: project-level memories (MVP), workspace/org in future
- Provider interface: `MemoryProvider` abstract class, JSON file provider for MVP

### Engine: `engine/context.py`

Context retrieval:
- Context pack assembly: gather relevant memories + project config + recent events for a given task
- Retrieval strategies: recency, relevance (keyword match for MVP, vector similarity later)
- Context budget: limit context size based on task type and model constraints
- Context injection: format context pack for agent consumption

### Config: `config/memory-policy.json`

Memory governance policy:
- Max memory age before review
- Auto-quarantine rules (conflicting evidence, low confidence)
- Retrieval logging level
- Memory planes enabled (project only for MVP)

### Dashboard: Context/Memory UI

- Memory browser: list, search, filter memories by scope/status/type
- Memory detail: evidence links, retrieval history, lifecycle state
- Context pack preview: see what context an agent would receive for a given task
- Memory health: stats on active/quarantined/draft counts

## API Routes

- `GET /api/memories` — list memories (filter by scope, status, type)
- `POST /api/memories` — create memory
- `GET /api/memories/{id}` — memory detail + evidence + retrieval log
- `PATCH /api/memories/{id}` — update status (advance lifecycle, quarantine)
- `GET /api/context/pack` — assemble context pack for a task (query params: task_type, project, scope)
- `GET /api/context/stats` — memory system health stats

## Acceptance Criteria

- [ ] Memory CRUD works through API
- [ ] Candidate lifecycle transitions enforce valid state machine
- [ ] Evidence linking connects memories to source files/sessions
- [ ] Context pack assembly returns relevant memories for a task
- [ ] Retrieval events are logged
- [ ] Memory governance policy is respected
- [ ] Dashboard shows memory browser, detail, and context preview
- [ ] Provider interface allows future swap to PostgreSQL
- [ ] Existing APIs unchanged

## Boundaries

- JSON file storage for MVP (no PostgreSQL migration yet)
- Keyword-based retrieval for MVP (no vector embeddings yet — deferred to post-DEC-005 implementation)
- Project-scoped memories only (no workspace/org/global planes yet)
- No automated memory extraction from sessions (that's P13 self-improvement)
- No multi-tenancy (that's P7)

## Deliverables

- `engine/memory.py`
- `engine/context.py` (enhanced)
- `config/memory-policy.json`
- Dashboard context/memory page
- `docs/build/p5-context-memory-build-report.md`
- `docs/build/rollback/p5-context-memory-rollback.md`
- `docs/build/session-handoffs/p5-context-memory-handoff.md`
