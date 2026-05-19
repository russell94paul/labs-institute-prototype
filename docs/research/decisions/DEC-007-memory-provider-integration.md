# Decision: DEC-007 — Memory Provider Integration Strategy

## Context
Zeus-memory (and potentially Mem0, Zep, or other services) may provide semantic memory, vector retrieval, and reusable memory patterns. Conductor must decide whether to hard-depend on an external provider or treat it as optional.

## Options
1. **Hard dependency on zeus-memory** — All memory goes through zeus-memory APIs. Tight coupling; blocked if provider is unavailable.
2. **Optional provider behind Conductor interfaces (recommended)** — Conductor owns governance, provenance, and promotion policy. Zeus-memory (or Mem0, Zep, etc.) is one pluggable provider among several. Conductor mirrors lifecycle state.
3. **No external provider** — Build all memory capabilities in-house. More work; reinvents capabilities that providers already offer.

## Recommendation
Option 2. Define `MemoryProvider` and `VectorStoreProvider` interfaces in `engine/context.py`. Zeus-memory can be the first provider, but Conductor controls tenant isolation, evaluation, promotion, quarantine, and rollback. Provider IDs and lifecycle state are mirrored in Conductor's metadata DB.

## Research Source
Topic 08 — Hybrid Context Fabric (Sections 1.1, 15.3, 19.1)

## Affects
- `engine/context.py` — provider interfaces
- Memory lifecycle — Conductor controls promotion/quarantine regardless of provider
- Retrieval pipeline — provider results go through Conductor's reranking and pack assembly
- Multi-tenant isolation — Conductor enforces scope even if provider doesn't

## Status
Proposed

## Decided by
(pending)
