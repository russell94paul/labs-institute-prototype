---
tags: [index, conductor]
created: 2026-05-23
updated: 2026-05-23
---

# Conductor Wiki — Index

## Architecture
- [[session-lifecycle]] — Session subprocess model, worktree isolation, callback system
- [[validation-engine]] — Auto-validation on session completion, evidence tracking, quality gates
- [[rollback-mechanisms]] — Pipeline snapshots, worktree rollback, merge approval gates
- [[session-continuation]] — Resuming completed sessions with user direction
- [[phase-orchestration]] — NeuroSpect phase management via Conductor dashboard

## Decisions
- [[DEC-001-per-session-callbacks]] — Fix singleton callback, enable per-session completion hooks

## Sessions
- [[2026-05-23-phase2-and-orchestration]] — Phase 2 backend + Conductor phase dashboard + validation/rollback/interactive
