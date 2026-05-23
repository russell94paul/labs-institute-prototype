# Synthesis: Topic 05 — Context, Memory, Vector DB & Self-Improvement

**Source:** `local-inputs/research-inbox/05-context-memory-vector-db-self-improvement.report.md`
**Synthesized:** 2026-05-19
**Status:** Synthesized

---

## Key Findings

1. **Memory is a governed evidence system, not a cache.** Every memory must link to source artifacts (build logs, PRs, diffs, test results, decisions). No memory without provenance.

2. **PostgreSQL + pgvector is the right MVP.** Co-locates memory storage with metadata, RLS, transactions, audit, and rollback. A vector-store adapter should exist from day one so Qdrant/Weaviate can be added later.

3. **Five-level memory hierarchy.** Session → Project → Tenant → Global → Procedural. Each level has its own trust boundary, promotion gates, and retrieval rules.

4. **Four memory categories stored separately.** Facts, decisions, patterns/playbooks, and cautionary memories (anti-patterns). Each has different evidence requirements and injection behavior.

5. **Promotion is specific → reusable, not frequent → global.** Promotion requires multiple evidence links, measured positive outcomes, contradiction checks, freshness, security scans, and regression replay tests.

6. **Quarantine is not deletion.** Suspected bad, stale, leaking, or contradicted memories go to quarantine (excluded from retrieval but preserved for audit). Rehabilitation creates new revisions linked to the original.

7. **Hard retrieval filters before vector search.** Tenant/project/access filters must execute before or inside vector search — never rely on the LLM to ignore out-of-scope memories. RLS policies enforce this in SQL.

8. **Hybrid retrieval required.** Pure vector similarity is insufficient. Combine semantic search + keyword/BM25 + metadata filters + graph/entity expansion + recency + confidence scoring + reranking.

9. **Context packs as structured artifacts.** Context assembly uses prioritized blocks (system policy → project constraints → session summary → retrieved memory → cautionary warnings) with strict token budgets.

10. **Attribution and regression testing are non-negotiable.** Every agent run logs retrieved/injected/used memory IDs and outcomes. A golden task suite runs memory vs. no-memory comparisons to gate promotions.

---

## Architecture Implications

- **`engine/context.py` evolves significantly.** Must become a full context assembler: define task query → determine allowed scopes → retrieve under RLS → rerank/budget blocks → render context pack → log injection → collect post-run attribution.
- **PostgreSQL becomes the system of record.** Memory ledger, evidence tables, evaluation tables, retrieval logs, quarantine events — all in Postgres with RLS. This accelerates the JSON→DB migration already planned.
- **Memory extraction is async, not hot-path.** Extract candidate memories after build/test outcomes are known, not during agent runs.
- **Vector-store adapter interface needed from day one.** Even if pgvector is the only backend initially, the interface allows swapping to Qdrant/Weaviate without changing retrieval logic.
- **Memory schema is large.** ~10 tables (memories, evidence, evaluations, retrieval_events, feedback, revisions, quarantine_events, entities, relationships + the main memories table). This is a substantial DB migration.

---

## Roadmap Implications

- **Aligns with Topic 08 (Context Fabric).** Topic 05 provides the memory governance layer that Topic 08's context fabric assembles from. These two research streams converge on the context.py redesign.
- **Reinforces DEC-005 (pgvector for MVP).** Topic 05 independently recommends pgvector as the MVP vector store, validating the Topic 08 recommendation.
- **Memory system spans multiple build phases.** The report outlines 6 implementation phases — from design guardrails through scale-up. This maps to P1 (schema/interfaces), P2-P3 (extraction, evaluation), P4+ (tenant/global).
- **Self-improvement loop is a later-phase capability.** The outcome-driven learning loop (build → extract → evaluate → promote → retrieve → build) depends on having the memory ledger, evaluation harness, and attribution logging in place first.
- **Project-level memory before tenant/global.** The report explicitly recommends deferring tenant and global memory until project-level memory is proven.

---

## New Risks

1. **Schema complexity and migration burden.** 10+ tables, complex state machine, multiple evaluation dimensions — risk of overbuilding before validating the core loop.
2. **Evaluation harness cost.** Running replay/regression tests for every candidate memory is expensive. Need to batch and sample judiciously.
3. **Stale memory injection.** If freshness detection lags, agents may receive outdated architectural facts or deprecated patterns.
4. **Memory bloat.** Without aggressive dedupe, clustering, and archival, the memory store grows faster than its utility.
5. **Attribution is probabilistic.** Linking build outcomes to specific memories is inexact — risk of false positives/negatives in promotion/quarantine decisions.
6. **Global memory sanitization is hard.** De-identifying tenant-specific memories for global reuse requires careful NLP and human review to avoid leakage.
7. **Prompt injection via memory.** Retrieved memory content must be treated as data, not instructions (except validated procedural memories). A malicious or badly-formed memory could influence agent behavior.

---

## New Decisions Required

| ID | Decision | Why it matters |
|----|----------|----------------|
| DEC-008 | Memory store MVP scope | How much of the 10-table schema to build in P1 vs. defer |
| DEC-009 | Memory extraction trigger | Async post-build vs. inline extraction — affects latency and data freshness |
| DEC-010 | Evaluation harness scope for MVP | Full replay suite vs. evidence+contradiction checks only |

---

## Implementation Recommendations

1. **Start with the memory record model and evidence linking.** Define `MemoryRecord`, `MemoryEvidence`, and `ContextPack` Python interfaces before building tables.
2. **Implement candidate → validated_project → quarantined first.** Skip tenant/global promotion in MVP.
3. **Build retrieval logging from the start.** Even before evaluation, log what was retrieved, injected, and the run outcome.
4. **Use context packs with block priorities.** This can be implemented in `engine/context.py` even before the full memory store exists.
5. **Defer procedural memory and autonomous learning loops.** These require the evaluation harness to be proven first.
6. **Reuse the report's SQL schema sketch** as a starting point for the PostgreSQL migration, but trim to MVP scope.

---

## Phase Changes

No changes to the existing phase structure. The memory system is additive and maps to existing P1 (Build Studio) planning as a subsystem of the context layer.

---

## Open Questions

1. When does the JSON→PostgreSQL migration happen — is it a prerequisite for memory, or do they ship together?
2. What embedding model and dimension should Conductor standardize on for the MVP?
3. How should memory interact with the existing wiki repo (Topic 08 DEC-006)? Are wiki pages a source of project memory, or a parallel system?
4. What is the minimum golden task suite size needed to make regression testing meaningful?
5. Should memory extraction run as a pipeline stage or as a background job outside the pipeline?
6. How granular should memory-type classification be at MVP? The report lists 14 types — is a subset sufficient?
