# Synthesis: 08 — Hybrid Context Fabric: Wiki, Memory, Knowledge Graph & Project Context Packs

**Source report:** `local-inputs/research-inbox/08-hybrid-context-fabric-wiki-memory-knowledge-graph.report.md`
**Synthesized:** 2026-05-19
**Research date:** 2026-05-18

---

## Key Findings

1. **Context is a governed data product, not a manual wiki or a single vector DB.** The recommended design is a five-layer hybrid context fabric: source-of-truth layer, canonical knowledge layer, retrieval layer, context-pack layer, and governance/evaluation layer.

2. **Source-of-truth separation is the most important architectural choice.** Raw source snapshots (Jira, Confluence, Git, research reports) must remain distinct from generated memory. Generated memory cites the source, carries its own confidence/freshness/evaluation status, and never overwrites the source.

3. **Metadata-first retrieval is mandatory.** Every retrieval call must apply tenant/client/project/phase/visibility filters before semantic search. This is necessary for multi-tenant safety, cost, relevance, and debuggability.

4. **The wiki repo becomes an output surface, not the primary knowledge store.** Conductor generates Markdown knowledge workspace files for transparency and agent ingestion, but authoritative state lives in structured stores with versioned provenance.

5. **Context packs are build artifacts.** Every Claude Code session receives a reproducible, reviewable, traceable context pack with item IDs, retrieval traces, token budgets, and role-specific sections. Packs are assembled by policy, not ad hoc prompt stuffing.

6. **Memory requires lifecycle governance.** Agent observations start as `candidate` memory. They pass through evaluation gates to become `trusted_project`, then optionally `trusted_client`, `trusted_tenant`, or `trusted_global`. Quarantine and rollback are first-class operations.

7. **Contradiction is a first-class state.** Facts are stored with validity intervals and supersession links. Unresolved conflicts are surfaced, not hidden by "latest chunk wins."

8. **Knowledge graph complements vector search.** Graph traversal handles impact analysis, dependency queries, conflict detection, and supersession — questions where embeddings are weak. MVP can use Postgres tables; graph DB later.

9. **Optional memory providers.** Zeus-memory, Mem0, Zep, or LangChain/LlamaIndex can be providers behind Conductor's own interfaces. Conductor owns governance, provenance, and promotion policy.

10. **Six knowledge classes must be distinguished:** raw source snapshots, normalized documents, chunks, extracted entities/relationships/facts, generated syntheses, and agent memory. Each has different trust, editability, and lifecycle properties.

---

## Architecture Implications

- **New `engine/context.py` interfaces needed:**
  - `ContextFabric` — ingest, search, build_pack, inspect, feedback
  - `ContextPackBuilder` — plan, retrieve, assemble, save manifest
  - `MemoryGovernance` — create candidate, evaluate, promote, quarantine, rollback
- **Source adapter framework:** Protocol-based adapters for wiki/Markdown, Jira/Linear, Git repo, Confluence/GDocs, research reports, deployment context, memory providers.
- **Storage layout:**
  - Postgres for metadata, RLS, lifecycle, evaluations
  - pgvector or Qdrant for embeddings
  - Postgres tables or Kuzu for graph (MVP); Neo4j later
  - Git/S3 for raw snapshots
  - Postgres full-text for lexical search
- **Retrieval pipeline:** Query router selecting between deterministic/lexical/vector/graph retrieval, with metadata prefiltering, score normalization, reranking, and retrieval trace logging.
- **Chunking strategy:** Source-aware (heading-aware for Markdown, field-separated for tickets, symbol-aware for code), targeting 300-900 tokens per chunk.
- **Context pack policies:** YAML-defined assembly policies with per-section token budgets, source preferences, trust tiers, and freshness/conflict controls.

---

## Roadmap Implications

The report proposes a 6-phase MVP sequence for the context fabric:

| Phase | Focus | Key Deliverables |
|---|---|---|
| Phase 0 | Foundations | KnowledgeScope, metadata schema, provider interfaces |
| Phase 1 | Source adapters + snapshots | Wiki, research, Git, ticket adapters; chunking; source index |
| Phase 2 | Vector retrieval + filters | Vector index, mandatory scope filters, retrieval traces |
| Phase 3 | Context pack builder | Project/phase/task packs, pack policies, manifests |
| Phase 4 | Memory lifecycle | MemoryItem table, candidate extraction, review queue, project-trusted retrieval |
| Phase 5 | Lightweight graph | Entity/relationship tables, deterministic extraction, graph-expanded packs, conflicts |
| Phase 6 | Evaluation loop | Golden tasks, pack quality checks, outcome ingestion, promotion batches, rollback |

This is a parallel workstream to the orchestration engine and multi-tenant foundation.

---

## New Risks

| Risk | Severity | Notes |
|---|---|---|
| Tenant data leak through retrieval | Critical | Hard tenant boundary in every store (RLS, vector namespace, graph partition); pack leak scans |
| Generated memory becomes false authority | High | Source separation, provenance, confidence, lifecycle gates; never overwrite source truth |
| Context packs too large/stale | Medium | Token budgets, reranking, freshness penalties, manifest appendix |
| Vector search retrieves plausible but wrong items | Medium | Metadata prefilters, source priority, reranking, graph/deterministic checks |
| Knowledge graph extraction noise | Medium | Constrained ontology, confidence scores, review gates, evaluations |
| Manual review bottleneck for memory promotion | Medium | Risk-based gating; auto-promote low-risk episodic memory; human review for high-impact |
| Provider lock-in (vector/graph/memory) | Low | Provider interfaces, mirrored metadata, export/import jobs |
| Cost/latency growth from hybrid retrieval | Medium | Query router, metadata prefilter, caching, async indexing, top-K limits |

---

## Decisions Required

1. **DEC-013: Vector store for MVP** — pgvector (Postgres-native, simpler) vs. Qdrant/Pinecone (dedicated, more features). Report recommends pgvector for small scale, Qdrant if separate service is acceptable.
2. **DEC-014: Graph store for MVP** — Postgres tables vs. embedded graph (Kuzu) vs. Neo4j. Report recommends Postgres tables for MVP.
3. **DEC-015: Wiki repo role** — Generated output surface vs. authoritative store. Report recommends generated output.
4. **DEC-016: Memory provider integration** — zeus-memory as optional provider vs. hard dependency. Report recommends optional provider behind Conductor interfaces.
5. **DEC-017: Embedding model** — Single general-purpose model for MVP vs. code-specialized. Report recommends single model, evaluate code-specific later.
6. **DEC-018: Context pack format** — Markdown sections vs. structured JSON. Report recommends Markdown with YAML manifest.
7. **DEC-019: Memory promotion gates** — Automated evaluation-only vs. human-in-the-loop. Report recommends both: auto for low-risk, human for high-impact.

---

## Implementation Recommendations

1. **Start with Phase 0 foundations** — define `KnowledgeScope`, metadata envelope, and provider interfaces before building any retrieval.
2. **Build wiki and research adapters first** — these sources already exist in the repo.
3. **Enforce metadata-first retrieval from the start** — no vector query without tenant/project scope.
4. **Generate Markdown workspace files** from structured state, keeping the wiki useful for humans and agents.
5. **Add provenance to every generated item** — evidence refs, extraction method, confidence, evaluation status.
6. **Build context packs as the primary agent input** — replace ad hoc prompt construction with policy-driven pack assembly.
7. **Use atomic memory items** — one claim per MemoryItem, not multi-topic bundles.
8. **Track retrieval traces** for every pack — enables debugging, evaluation, and cost analysis.

---

## Phase Changes

- Context fabric is a **parallel workstream** alongside multi-tenant foundation and orchestration engine enhancement.
- Phase 0-1 (foundations + adapters) can begin immediately since they primarily create interfaces and ingest existing Markdown/research content.
- Phase 2-3 (vector retrieval + packs) depend on the metadata schema and should wait for the Postgres migration decision from Topic 01.
- Phase 4-6 (memory lifecycle, graph, evaluation) are medium-term and build on the foundation layers.

---

## Open Questions

1. When will Conductor migrate from JSON to PostgreSQL? The context fabric's metadata schema and RLS-based isolation depend on this.
2. Should zeus-memory integration be built in Phase 1 as a provider, or deferred until the core system proves itself?
3. What is the expected volume of sources to ingest initially? (Determines vector store sizing.)
4. Should the context pack builder be a standalone module or integrated into the agent dispatch path in `engine/agents.py`?
5. How should the generated Markdown workspace relate to the existing wiki repo at `C:\Users\PaulRussell\repos\wiki`?
6. What embedding model and dimension should be the starting choice?
7. Should graph extraction run during ingestion or as a background batch job?
