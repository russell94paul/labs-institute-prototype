# Prompt: Design Hybrid Context Fabric from Repos

This is a **future execution prompt**. Do NOT run it now. Run it when you are ready to design the context/memory architecture by inspecting the actual repos.

## Prerequisites

- Topics 01, 02, and 05 Deep Research outputs should be synthesized
- Topic 08 Deep Research output should ideally be available
- You should have access to `repos/wiki`, `repos/zeus-memory`, and `repos/conductor`

## Prompt

Copy and paste the following into Claude Code:

---

Inspect the following repos to design a Hybrid Context Fabric for Conductor:

1. **repos/wiki** — Currently stores ingested company context, Confluence docs, repo information, client information, ticket information, deployment context, and other operational entities. The user does NOT want a manually maintained wiki. The goal is a generated hybrid memory/context system.

2. **repos/zeus-memory** — May provide semantic memory/vector retrieval and reusable memory patterns. Treat as an optional semantic memory provider/reference pattern, NOT a hard dependency.

3. **repos/conductor** — The orchestration platform. Should become the context router, governance layer, project memory manager, and context pack builder.

For each repo, inspect:
- Directory structure
- Key files and their purpose
- Data models and schemas
- Existing memory/context patterns
- Integration points

Then create or update the following:

### docs/architecture/hybrid-context-fabric.md

Design the overall architecture covering:

- **Source Registry** — catalog of all knowledge sources (wiki, zeus-memory, code repos, ticket systems, Confluence, research outputs, session logs)
- **Source Adapters** — how to read from each source type (file reader, API client, git log parser, MCP connector)
- **Structured Knowledge Layer** — normalized metadata store for entities, relationships, and facts
- **Knowledge Graph Layer** — entity graph with typed relationships (project → client → tickets → deployments)
- **Vector Memory Layer** — embeddings for semantic search, with metadata-first filtering before vector retrieval
- **Context Router** — given a task/query, assemble the right context pack from the right sources with the right scope
- **Context Pack Builder** — produce scoped context bundles for AI agents (project packs, phase packs, review packs)
- **Metadata-first filtering** — filter by tenant, project, client, source type, freshness, confidence before semantic search
- **Tenant/project/client isolation** — RLS-aware retrieval, scoped memory, no cross-tenant leakage
- **Source citations** — every memory item traces back to its source document, commit, ticket, or session
- **Stale/conflicting knowledge detection** — detect when facts contradict, when sources are outdated, when context has drifted
- **Memory promotion/quarantine/rollback** — evaluation gates before memory is promoted to trusted/global status
- **Evaluation-gated self-improvement** — feedback loops that measure whether memory improves or degrades agent performance
- **Knowledge Workspace UI concepts** — search, graph browsing, approvals, source inspection, context pack review

### docs/architecture/hybrid-wiki-memory-context-engine.md

Detail the integration between:
- wiki (structured entity store, current source of truth for company/client/ticket context)
- zeus-memory (optional vector/semantic memory layer)
- conductor (context router, governance, project memory manager)

Include a component diagram in text form.

### docs/decisions/ADR-0007-hybrid-context-fabric.md

Create an ADR documenting:
- Decision: adopt a hybrid context fabric instead of a single-source memory system
- Rationale: wiki has structured entity knowledge, zeus-memory has semantic retrieval patterns, conductor needs both plus governance
- Consequences: need source adapters, metadata schema, evaluation gates, and a context router

### docs/research/prompts/05-context-memory-vector-db-self-improvement.md

Review and update if the existing prompt needs refinement based on what you learned from the repo inspection.

### config/research-topics.json

Verify Topic 08 entry is present and accurate.

### docs/build/change-manifest.md

Update with all files created or modified.

## Important Constraints

- **Do NOT copy raw sensitive wiki/client content into Conductor docs.** Reference by structure only.
- **Do NOT ingest secrets.**
- **Do NOT implement production code.** This prompt produces architecture docs and config only.
- **zeus-memory is optional** — design for it as a pluggable provider, not a required dependency.
- The system should support **project-level and product-level memories** like NeuroGraph for NeuroSpect (scoped knowledge workspaces per project/product).

## Stop After

Architecture docs and config updates. Do not proceed into implementation.

---
