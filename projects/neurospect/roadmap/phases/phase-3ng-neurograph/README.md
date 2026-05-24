---
phase: "3-NG"
name: "NeuroGraph"
status: in_progress
assigned: [paul]
started: 2026-05-13
completed: null
tickets_total: 0
tickets_done: 0
goal: "Design the persistent trading intelligence graph: data source mapping, schema design (node/edge types), seed strategy, accumulation strategy, query patterns, technology decision."
deliverables:
  - "Complete data source inventory (internal + external) with feasibility ratings"
  - "Graph schema (13 node types, 10+ edge types, properties)"
  - "Seed strategy (wiki concepts, entry models, course lessons, instruments, sessions)"
  - "Accumulation strategy (trade close, coaching, experiments, behavior metrics)"
  - "Query patterns for each component (Mentor, EdgeLab, Forensics, NeuroScore, Prop Shield)"
  - "Technology recommendation (PostgreSQL + JSONB vs Neo4j)"
  - "Implementation plan with effort estimates"
  - "External data source API research"
constraints:
  - "Plan mode first — no implementation until data source mapping approved"
  - "Must work with zero user data (seeded with wiki/concepts)"
  - "Must support deletion (GDPR/privacy)"
  - "Must not generate trading recommendations"
  - "Seeded data is read-only; user data is personal (multi-tenant)"
acceptance_criteria:
  - "Complete data source inventory"
  - "Graph schema document (all node/edge types)"
  - "Seed strategy document"
  - "Accumulation strategy document"
  - "Query patterns document"
  - "Technology recommendation with tradeoffs"
  - "Implementation plan with effort estimates"
  - "External API research (availability, cost, rate limits)"
compliance_gate: "GDPR/privacy — memory deletion support required"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 3-NG: NeuroGraph

Persistent trading intelligence graph. The compounding moat — switching to a competitor means losing all accumulated intelligence.

Plan-mode-first phase. Research artifacts exist (free-data strategy, data source evaluation) but no code implementation yet.

See `/ns-phase3-neurograph` for full implementation guide.

## Deviations

_None yet._
