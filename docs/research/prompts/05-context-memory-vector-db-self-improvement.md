# Deep Research Prompt: Context, Memory, Vector DB & Self-Improvement

## Purpose

Research best practices for building a multi-level AI context and memory system, informing Conductor's memory architecture, vector DB design, and self-improvement loops.

## When to Run

Run after Topics 1 and 2 (Priority 3). The memory system is critical for Conductor's self-improvement capability.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research best practices for building a multi-level AI context and memory system for a product-building platform. The system should support project-level memory, tenant-level memory, global reusable memory, vector search, metadata filtering, RLS-aware retrieval, evaluation gates, memory quarantine, rollback, stale context detection, and self-improvement loops. Focus on preventing bad memories from degrading performance.**

Context: I'm building a product orchestration platform (called "Conductor") that uses AI agents (Claude Code) to build software products. Each build generates knowledge: what worked, what failed, what patterns emerged, what decisions were made and why. I want Conductor to remember and reuse this knowledge to improve over time.

The challenge is that not all memories are good. Bad recommendations, failed approaches, and outdated patterns can degrade future performance if blindly reused. The memory system needs built-in quality control.

The platform is multi-tenant — memory must respect tenant boundaries (some memory is tenant-specific, some is global).

Current stack: Python backend, vanilla HTML/CSS/JS frontend, JSON file storage (evolving to database + vector DB).

I need to understand:

1. **Memory architecture** — how to design a multi-level memory hierarchy: session memory (current build), project memory (this product), tenant memory (this client), global memory (all builds). How memories promote from session → project → tenant → global. What gates each promotion.

2. **Vector DB design** — which vector database to use (Pinecone, Weaviate, Qdrant, ChromaDB, pgvector). Embedding model selection. Chunk size and overlap strategies. How to handle structured vs. unstructured memories. Index design for fast retrieval.

3. **Metadata schema** — what metadata to attach to each memory. At minimum: tenant_id, project_id, memory_type, confidence_score, source, created_at, last_accessed, access_count, evaluation_status. How metadata enables filtering and RLS.

4. **Evaluation loop** — how to evaluate whether a memory is helping or hurting performance. Metrics for memory quality. How to detect when a memory is causing bad recommendations. Human-in-the-loop evaluation vs. automated evaluation.

5. **Promotion/quarantine process** — how memories move from "candidate" to "trusted" to "global". What triggers promotion. What triggers quarantine. How to quarantine a memory without losing it (it might be useful in a different context). How to rehabilitate quarantined memories.

6. **Regression testing strategy** — how to test that the memory system isn't degrading overall performance. A/B testing with/without specific memories. Performance baselines. How to attribute performance changes to specific memories.

7. **Multi-tenant/RLS design** — how to ensure the vector DB respects tenant boundaries. How to share global memories without leaking tenant-specific data. How to handle memories that reference tenant-specific artifacts.

8. **Stale context detection** — how to detect when a memory is outdated (the codebase changed, the client's requirements changed, a technology became obsolete). TTL strategies. Active vs. passive staleness detection.

9. **Self-improvement loops** — how the platform uses memory to improve over time. Feedback loops from build outcomes to memory quality. How to measure improvement. How to prevent memory bloat.

Provide your output as a structured report with:
- Memory architecture (levels, promotion rules, data flow)
- Vector DB design (technology choice, schema, indexing)
- Metadata schema (fields, types, constraints)
- Evaluation loop (metrics, process, automation)
- Promotion/quarantine process
- Regression testing strategy
- Multi-tenant/RLS design
- Implementation roadmap (MVP → full system)

Reference existing systems: LangChain memory, LlamaIndex, Mem0, Zep, MemGPT. Compare approaches.

---

## Expected Output Filename

`05-context-memory-vector-db-self-improvement.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Context manager architecture (`engine/context.py`)
- Vector DB selection and schema
- Memory promotion/quarantine workflow
- Agent context injection
- Multi-tenant data isolation in memory
- Self-improvement metrics and feedback loops
