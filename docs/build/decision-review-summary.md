# Decision Review Summary — DEC-001 through DEC-007

**Date:** 2026-05-19
**Branch:** conductor-platform-rebuild
**Purpose:** Pre-P1 decision review — determine which decisions gate Build Studio and which can defer.
**Sources:** Syntheses 01, 02, 08; DEC-001 through DEC-007; P1 Build Studio prompt.

---

## Executive Summary

None of DEC-001 through DEC-007 strictly block P1 Build Studio. P1 is a dashboard/UI replacement (project registry, phase launcher, pipeline monitor, build reports, approval placeholder) that integrates with the existing pipeline engine. It does not introduce multi-tenancy, secrets handling, context fabric, or vector search.

Two decisions (DEC-003, DEC-004) softly inform P1 UI design but do not block starting P1. Five decisions (DEC-001, DEC-002, DEC-005, DEC-006, DEC-007) relate to workstreams that come after P1.

**Recommendation:** Approve all 7 decisions in principle. Defer implementation of all except DEC-003 and DEC-004, which should be confirmed before P1 so the UI can account for worktree views and persistent event history.

---

## Decision Reviews

### DEC-001 — Default Tenancy Model

| Field | Value |
|-------|-------|
| **Recommended option** | Hybrid: shared schema + RLS now, `tenants.isolation_mode` for future upgrade |
| **Alternatives** | Shared schema only; schema-per-tenant; database-per-tenant |
| **Pros** | Simple MVP, lowest ops overhead, upgrade path to enterprise isolation tiers |
| **Cons** | RLS blast radius if misconfigured; requires full DB migration from current JSON files |
| **Risk** | Medium — RLS misconfiguration = cross-tenant data leak (critical severity, medium likelihood with proper testing) |
| **Gates P1?** | No — P1 is a dashboard replacement; no DB migration or multi-tenancy |
| **Can defer?** | Yes — until the DB migration phase |
| **Source** | Synthesis 01, Sections 3-4 |
| **Suggested status** | **Approve in principle, defer implementation** |

**Notes:** The current system uses JSON files for all state. This decision only matters when Conductor migrates to PostgreSQL, which is a separate phase. Approving the principle now avoids re-debating later.

---

### DEC-002 — Secrets Management Backend

| Field | Value |
|-------|-------|
| **Recommended option** | Broker abstraction + local dev storage; swap in Vault/AWS later |
| **Alternatives** | HashiCorp Vault now; AWS Secrets Manager now |
| **Pros** | Fast MVP, clean interface, no vendor lock-in, no ops overhead |
| **Cons** | No production-grade rotation until swap; local storage is dev-only |
| **Risk** | Low for MVP — no external clients or real credentials yet |
| **Gates P1?** | No — P1 doesn't handle tenant secrets or credentials |
| **Can defer?** | Yes — until agent runtime needs real credential access |
| **Source** | Synthesis 01, Section 11 |
| **Suggested status** | **Approve in principle, defer implementation** |

**Notes:** The broker abstraction pattern is standard. The only real decision is whether to build it when the agent runtime needs it or earlier. No urgency.

---

### DEC-003 — Worktree Isolation Model

| Field | Value |
|-------|-------|
| **Recommended option** | Per-task worktrees with merge queue; sequential pipelines can skip |
| **Alternatives** | Keep shared worktree; per-lane worktrees |
| **Pros** | Enables safe parallelism, clean rollback, per-task diff attribution |
| **Cons** | Git complexity, merge queue overhead, disk usage for worktrees |
| **Risk** | Medium — merge conflicts in parallel execution; mitigated by write-set conflict detection |
| **Gates P1?** | Soft yes — P1 UI should plan for merge queue/worktree views if this model is confirmed |
| **Can defer?** | Decision should be confirmed now; implementation can defer |
| **Source** | Synthesis 02, Section 7 |
| **Suggested status** | **Approve** |

**Notes:** The work-guard policy already has `allowParallelWorktrees: true` and `maxConcurrentWorktrees: 2`, which assumes this model. The branch naming convention `conductor/{project}/{run_id}/task-{task_id}` is sound. P1 Build Studio should include placeholder views for worktree state even if the full implementation comes later.

**Consistency check:** Aligns with `config/work-guard-policy.json`. No conflict.

---

### DEC-004 — Event Store Technology

| Field | Value |
|-------|-------|
| **Recommended option** | Append-only JSONL per pipeline run for MVP |
| **Alternatives** | PostgreSQL events table; EventStoreDB/Kafka |
| **Pros** | Simple, file-based, no DB dependency, natural migration path |
| **Cons** | Limited cross-run querying, no analytics, no full-text search over events |
| **Risk** | Low — straightforward migration to Postgres when ready |
| **Gates P1?** | Soft yes — P1 consumes events via SSE; should know if persistent history will be available |
| **Can defer?** | Current in-memory ring buffer (P0-events) works for P1; JSONL persistence can be added during or after P1 |
| **Source** | Synthesis 02, Section 10 |
| **Suggested status** | **Approve with clarification** |

**Notes:** P0-events built an in-memory ring buffer (500 events, deque-based) with SSE streaming. This is neither JSONL nor Postgres — it's a pre-MVP implementation that works but loses history on server restart. The decision should acknowledge the current state: in-memory ring buffer → JSONL persistence → Postgres.

**Recommended update to DEC-004:** Add a "Current State" section noting the in-memory implementation from P0-events and position JSONL as the next step.

---

### DEC-005 — Vector Store for Context Fabric

| Field | Value |
|-------|-------|
| **Recommended option** | pgvector for MVP, graduate to Qdrant at scale |
| **Alternatives** | Pinecone (managed, vendor lock-in); no vector search initially |
| **Pros** | Co-located with metadata DB, single query path, simpler ops |
| **Cons** | ANN performance ceiling at scale; requires Postgres migration first |
| **Risk** | Low — standard technology choice, well-understood trade-offs |
| **Gates P1?** | No — context fabric is a separate workstream |
| **Can defer?** | Yes — until context fabric Phase 2 (vector retrieval) |
| **Source** | Synthesis 08, Sections 7, 1.3 |
| **Suggested status** | **Defer** |

**Notes:** This decision depends on the Postgres migration (DEC-001). Both can be revisited together when the context fabric workstream starts. Topic 05 research (Context, Memory, Vector DB) would provide additional input but is not required for this decision.

---

### DEC-006 — Wiki Repo Role

| Field | Value |
|-------|-------|
| **Recommended option** | Wiki as generated output, not source of truth |
| **Alternatives** | Wiki as authoritative store; eliminate wiki entirely |
| **Pros** | Keeps diffable Markdown for humans/agents, centralizes state, reduces manual maintenance |
| **Cons** | Changes Paul's daily wiki workflow; requires building a generation pipeline |
| **Risk** | Low technically; medium operationally (workflow change) |
| **Gates P1?** | No — P1 doesn't interact with the wiki |
| **Can defer?** | Yes — until context fabric workstream |
| **Source** | Synthesis 08, Sections 1.1, 13 |
| **Suggested status** | **Approve in principle, defer implementation** |

**Notes:** This directly affects the wiki at `C:\Users\PaulRussell\repos\wiki` and Paul's daily workflow (currently manual wiki edits + Claude Code CLAUDE.md instructions). The shift to generated output is gradual — the wiki continues to work as-is until Conductor's context fabric can generate it. Approving the principle now signals the direction without requiring immediate workflow changes.

---

### DEC-007 — Memory Provider Integration

| Field | Value |
|-------|-------|
| **Recommended option** | Optional provider behind Conductor interfaces; zeus-memory as first plugin |
| **Alternatives** | Hard dependency on zeus-memory; no external provider (build in-house) |
| **Pros** | Conductor owns governance/lifecycle, provider-agnostic, clean plugin pattern |
| **Cons** | Abstraction overhead; provider capabilities may differ behind the interface |
| **Risk** | Low — standard plugin/adapter pattern |
| **Gates P1?** | No — P1 doesn't involve memory providers |
| **Can defer?** | Yes — until context fabric Phase 4 (memory lifecycle) |
| **Source** | Synthesis 08, Sections 1.1, 15.3, 19.1 |
| **Suggested status** | **Approve in principle, defer implementation** |

**Notes:** The `MemoryProvider` and `VectorStoreProvider` interfaces belong in `engine/context.py` which doesn't exist yet. This is a context fabric concern, not a P1 concern.

---

## Summary Matrix

| Decision | Suggested Status | Gates P1? | Can Defer? | Implementation Phase |
|----------|-----------------|-----------|------------|---------------------|
| DEC-001 Tenancy Model | Approve principle | No | Yes | DB migration |
| DEC-002 Secrets Backend | Approve principle | No | Yes | Agent runtime |
| DEC-003 Worktree Isolation | **Approve** | Soft yes | Decision: no; impl: yes | Pipeline enhancement |
| DEC-004 Event Store | **Approve** (with clarification) | Soft yes | Yes (in-memory works for P1) | During/after P1 |
| DEC-005 Vector Store | Defer | No | Yes | Context fabric |
| DEC-006 Wiki Role | Approve principle | No | Yes | Context fabric |
| DEC-007 Memory Provider | Approve principle | No | Yes | Context fabric |

---

## P1 Gating Analysis

**Decisions that must be resolved before P1:** None are strictly blocking.

**Decisions that should be confirmed before P1:**
- **DEC-003** — so P1 UI can include worktree/merge queue placeholder views
- **DEC-004** — so P1 UI knows whether to expect persistent event history or continue with in-memory

**Decisions that can safely wait:**
- DEC-001, DEC-002, DEC-005, DEC-006, DEC-007 — all relate to post-P1 workstreams

---

## Topic 05 Assessment

**Topic 05 — Context, Memory, Vector DB & Self-Improvement** is pending. It would provide additional depth for DEC-005, DEC-006, and DEC-007. However:

- All three decisions can be deferred past P1.
- Synthesis 08 already covers the context fabric architecture comprehensively.
- Topic 05 would add depth on self-improvement loops and memory evaluation — useful but not blocking.

**Recommendation:** Topic 05 research is **not required before P1**. Run it when the context fabric workstream is ready to start (after P1 or in parallel with late P1 work).

---

## Cross-Reference: Synthesis Decision Numbering

The synthesis documents use their own internal decision numbering that differs from the DEC files:

| Actual DEC | Synthesis Source | Synthesis Internal # |
|------------|-----------------|---------------------|
| DEC-001 | Synthesis 01 | DEC-001 (tenancy) |
| DEC-002 | Synthesis 01 | DEC-003 (secrets) |
| DEC-003 | Synthesis 02 | DEC-008 (worktree) |
| DEC-004 | Synthesis 02 | DEC-009 (event store) |
| DEC-005 | Synthesis 08 | DEC-013 (vector store) |
| DEC-006 | Synthesis 08 | DEC-015 (wiki role) |
| DEC-007 | Synthesis 08 | DEC-016 (memory provider) |

The DEC-001 through DEC-007 files represent a curated cross-cutting selection from all three syntheses. Additional decisions referenced in the syntheses (DEC-002/004-007 from synthesis 01, DEC-010-012 from synthesis 02, DEC-014/017-019 from synthesis 08) have not been extracted into standalone decision files yet. These can be created as those workstreams approach.
