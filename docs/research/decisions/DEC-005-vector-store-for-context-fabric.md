# Decision: DEC-005 — Vector Store for Context Fabric

## Context
The context fabric needs vector search for semantic retrieval over documents, chunks, and memory items. The store must support tenant-scoped metadata filtering.

## Options
1. **pgvector (Postgres extension)** — Co-located with metadata DB. Simpler ops, single query path. Limited ANN performance at very large scale.
2. **Qdrant** — Dedicated vector DB with rich payload filtering and namespace support. Separate service to operate.
3. **Pinecone** — Managed service with namespace-based isolation and metadata filters. Cloud-only; vendor lock-in.
4. **No vector search initially** — Use only lexical/deterministic retrieval. Limits semantic discovery.

## Recommendation
Option 1 (pgvector) for MVP if volume is small. Move to Option 2 (Qdrant) if retrieval latency or scale exceeds Postgres capabilities. Both support the metadata-first filtering pattern required for tenant isolation.

## Research Source
Topic 08 — Hybrid Context Fabric (Sections 7, 1.3)

## Affects
- `engine/context.py` — vector store provider interface
- Ingestion pipeline — embedding and indexing
- Retrieval pipeline — filtered ANN queries
- Infrastructure — Postgres extension or separate service

## Status
Proposed

## Decided by
(pending)
