# Synthesis Log

Record of all research synthesis operations.

| Date | Topic | Synthesis file | Key findings | Decisions created | Notes |
|------|-------|---------------|-------------|-------------------|-------|
| 2026-05-19 | 01 — Multi-Tenant SaaS, RLS & Client Portals | [synthesis](syntheses/01-multi-tenant-saas-rls-client-portals.synthesis.md) | Pooled schema + RLS, control/app plane separation, secrets-as-references, agent principals, approval workflows, SOC 2 audit | DEC-001, DEC-002 | 10 key findings, 7 risks, 5 open questions |
| 2026-05-19 | 02 — Agent Orchestration, DAGs & Parallelization | [synthesis](syntheses/02-agent-orchestration-dag-parallelization.synthesis.md) | Native DAG engine, 4-concern separation, two-level DAGs, append-only events, per-task worktrees, write-set conflicts, approval gates, compensation rollback | DEC-003, DEC-004 | 10 key findings, 7 risks, 8-phase MVP plan |
| 2026-05-19 | 08 — Hybrid Context Fabric | [synthesis](syntheses/08-hybrid-context-fabric-wiki-memory-knowledge-graph.synthesis.md) | 5-layer hybrid fabric, source-truth separation, metadata-first retrieval, context packs as artifacts, memory lifecycle governance, contradiction as first-class state, graph complements vector | DEC-005, DEC-006, DEC-007 | 10 key findings, 8 risks, 6-phase MVP plan |
| 2026-05-19 | 05 — Context, Memory, Vector DB & Self-Improvement | [synthesis](syntheses/05-context-memory-vector-db-self-improvement.synthesis.md) | Memory as governed evidence system, PostgreSQL+pgvector MVP, 5-level memory hierarchy, 4 memory categories, promotion by evidence not frequency, quarantine not deletion, hard retrieval filters before vector search, hybrid retrieval, context packs with block priorities, attribution and regression testing | DEC-008, DEC-009, DEC-010 | 10 key findings, 7 risks, 6 open questions |
