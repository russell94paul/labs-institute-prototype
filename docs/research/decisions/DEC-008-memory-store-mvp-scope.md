# Decision: DEC-008 — Memory Store MVP Scope

## Context
Topic 05 recommends a 10+ table PostgreSQL memory ledger with evidence linking, evaluation, retrieval logging, quarantine, entity extraction, and relationship tracking. Building all of this for P1 risks overengineering before the core memory loop is validated. We need to decide which tables and capabilities ship in MVP.

## Options
1. **Minimal ledger (3 tables)** — `memories`, `memory_evidence`, `memory_retrieval_events`. Supports candidate → validated_project → quarantined lifecycle, evidence linking, and retrieval logging. Defer evaluation, entity extraction, relationships, revisions, and feedback tables.
2. **Core ledger (6 tables)** — Add `memory_evaluations`, `memory_feedback`, `memory_quarantine_events` to Option 1. Supports automated evaluation gates and human feedback collection from the start.
3. **Full schema (10 tables)** — Build everything from the report's design. Includes entity extraction, relationships, revisions, and all evaluation dimensions.
4. **No DB yet** — Keep memory as structured JSON files (like current state layer). Defer PostgreSQL migration entirely.

## Recommendation
Option 1 (minimal ledger). Validates the core memory loop — extract, link evidence, retrieve, log, quarantine — without the overhead of evaluation infrastructure. Add evaluation tables (Option 2) once the memory extraction pipeline produces enough candidates to evaluate meaningfully.

## Research Source
Topic 05 — Context, Memory, Vector DB & Self-Improvement (Sections 3, 5.3, 14)

## Affects
- Database migration planning
- `engine/context.py` — memory retrieval interface
- P1 Build Studio scope
- Infrastructure requirements (PostgreSQL + pgvector)

## Status
Proposed

## Decided by
(pending)
