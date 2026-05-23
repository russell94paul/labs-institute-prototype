# Research Index

## Topics

| # | Topic | Priority | Status | Prompt | Output | Synthesis |
|---|-------|----------|--------|--------|--------|-----------|
| 01 | Multi-Tenant SaaS, RLS & Client Portals | 1 | Synthesized | [prompt](prompts/01-multi-tenant-saas-rls-client-portals.md) | [report](../../local-inputs/research-inbox/01-multi-tenant-saas-rls-client-portals.report.md) | [synthesis](syntheses/01-multi-tenant-saas-rls-client-portals.synthesis.md) |
| 02 | Agent Orchestration, DAGs & Parallelization | 1 | Synthesized | [prompt](prompts/02-agent-orchestration-dag-parallelization.md) | [report](../../local-inputs/research-inbox/02-agent-orchestration-dag-parallelization.report.md) | [synthesis](syntheses/02-agent-orchestration-dag-parallelization.synthesis.md) |
| 03 | AI-Guided Onboarding & Decision Simulation | 5 | Pending | [prompt](prompts/03-ai-product-onboarding-decision-simulation.md) | — | — |
| 04 | Data Platform Modernization Factory | 4 | Pending | [prompt](prompts/04-data-platform-modernization-factory.md) | — | — |
| 05 | Context, Memory, Vector DB & Self-Improvement | 3 | Synthesized | [prompt](prompts/05-context-memory-vector-db-self-improvement.md) | [report](../../local-inputs/research-inbox/05-context-memory-vector-db-self-improvement.report.md) | [synthesis](syntheses/05-context-memory-vector-db-self-improvement.synthesis.md) |
| 06 | Secure Credential & Artifact Workflows | 6 | Pending | [prompt](prompts/06-secure-credential-artifact-workflows.md) | — | — |
| 07 | Market Intelligence & Growth Engine | 7 | Pending | [prompt](prompts/07-market-intelligence-growth-engine.md) | — | — |
| 08 | Hybrid Context Fabric: Wiki, Memory, Knowledge Graph & Project Context Packs | 1 | Synthesized | [prompt](prompts/08-hybrid-context-fabric-wiki-memory-knowledge-graph.md) | [report](../../local-inputs/research-inbox/08-hybrid-context-fabric-wiki-memory-knowledge-graph.report.md) | [synthesis](syntheses/08-hybrid-context-fabric-wiki-memory-knowledge-graph.synthesis.md) |

## Decisions Extracted

| ID | Title | Source Topics | Status |
|---|-------|---------------|--------|
| DEC-001 | Default tenancy model | 01 | Proposed |
| DEC-002 | Secrets management backend | 01 | Proposed |
| DEC-003 | Worktree isolation model | 02 | Proposed |
| DEC-004 | Event store technology | 02 | Proposed |
| DEC-005 | Vector store for context fabric | 08 | Proposed |
| DEC-006 | Wiki repo role | 08 | Proposed |
| DEC-007 | Memory provider integration | 08 | Proposed |
| DEC-008 | Memory store MVP scope | 05 | Proposed |
| DEC-009 | Memory extraction trigger | 05 | Proposed |
| DEC-010 | Evaluation harness MVP scope | 05 | Proposed |

## Recommended Run Order

1. ~~Topic 01 — Multi-Tenant SaaS (foundational architecture)~~ **Synthesized**
2. ~~Topic 02 — Agent Orchestration (core engine)~~ **Synthesized**
3. ~~Topic 08 — Hybrid Context Fabric (wiki + memory + knowledge graph)~~ **Synthesized**
4. ~~Topic 05 — Context & Memory (self-improvement capability)~~ **Synthesized**
5. Topic 04 — Data Platform Modernization (proof case)
6. Topic 03 — AI Onboarding & Decisions (user-facing)
7. Topic 06 — Secure Credentials (security layer)
8. Topic 07 — Market Intelligence (growth layer)

## Recommended Next Research Topic

**Topic 04 — Data Platform Modernization Factory** (Priority 4). Dependencies on Topics 01 and 02 are satisfied. Directly relevant to the ALDC proof case and blocked only on the service inventory input (Blocker #2).
