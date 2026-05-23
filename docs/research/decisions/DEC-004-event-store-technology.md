# Decision: DEC-004 — Event Store Technology

## Context
The orchestration engine needs an immutable event log as source of truth for execution history, dashboard state, audit, and state reconstruction.

## Options
1. **Append-only JSONL files (recommended for MVP)** — One `events.jsonl` per pipeline run. Simplest to implement; works with current file-based state. Limited query capabilities.
2. **PostgreSQL events table** — Structured, queryable, supports RLS. Requires DB migration to be completed first.
3. **Dedicated event store (EventStoreDB, Kafka)** — Full-featured event sourcing. Operational overhead; premature for current scale.

## Recommendation
Option 1 for MVP. Design the event envelope and schema now so migration to Option 2 (PostgreSQL) is straightforward once the DB migration from Topic 01 is complete.

## Research Source
Topic 02 — Agent Orchestration, DAGs & Parallelization (Section 10)

## Affects
- `engine/pipelines.py` — state transitions
- Dashboard — SSE streaming and state reconstruction
- Audit logging — event visibility and retention

## Status
Approved — 2026-05-19

## Decided by
Paul Russell

## Current State
P0-events implemented an in-memory ring buffer (500 events, deque-based) with SSE streaming. This serves as the pre-MVP implementation. The approved path is: in-memory ring buffer → JSONL persistence → PostgreSQL.

## Approval Notes
Approved for P3 Phase Template OS. JSONL-per-run event persistence confirmed as next step. Implementation deferred to P3; this approval unblocks execution audit trail design.
