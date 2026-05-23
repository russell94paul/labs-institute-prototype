# Decision: DEC-006 — Wiki Repo Role in Context Fabric

## Context
A file-based wiki repo currently stores ingested company context, Confluence docs, repo info, client info, and operational entities. The user does not want to maintain it manually.

## Options
1. **Wiki as authoritative store** — Continue using the wiki repo as the primary knowledge store. Manual maintenance burden; no structured provenance or lifecycle.
2. **Wiki as generated output (recommended)** — Conductor generates Markdown workspace files from structured state. Wiki is useful for human review and agent ingestion but is not the source of truth.
3. **Eliminate wiki entirely** — All knowledge lives in DB/vector/graph. Loses transparency, diffability, and easy agent ingestion.

## Recommendation
Option 2. Continue generating Markdown files in knowledge workspace directories. These files are readable, diffable, and ingestible by Claude Code. But authoritative state (metadata, provenance, lifecycle, evaluations) lives in structured stores.

## Research Source
Topic 08 — Hybrid Context Fabric (Sections 1.1, 13)

## Affects
- Wiki repo at `C:\Users\PaulRussell\repos\wiki`
- `engine/context.py` — workspace generation
- Agent context injection — packs built from structured state, not wiki crawling
- Existing wiki workflows — shift from manual edit to generated output

## Status
Proposed

## Decided by
(pending)
