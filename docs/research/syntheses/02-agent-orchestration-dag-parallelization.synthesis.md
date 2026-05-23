# Synthesis: 02 — Agent Orchestration, DAGs & Parallelization

**Source report:** `local-inputs/research-inbox/02-agent-orchestration-dag-parallelization.report.md`
**Synthesized:** 2026-05-19
**Research date:** 2026-05-18

---

## Key Findings

1. **A Conductor-native DAG engine is the correct MVP path.** Building a custom scheduler borrows proven patterns from Temporal, Prefect, Airflow, GitHub Actions, Argo, and Tekton without adopting their operational overhead. The domain (agentic product orchestration with git worktrees, approvals, and AI sessions) is specific enough that off-the-shelf engines would need heavy adaptation.

2. **Four concerns must be separated:** planning graph (definitions), execution graph (runtime nodes), isolation graph (worktrees, leases, secrets), and event graph (immutable history). This prevents state spaghetti.

3. **DAGs operate at two levels:** phase DAG for product lifecycle dependencies, and task DAG for executable units inside each phase. The UI should preserve this hierarchy; the scheduler can flatten internally.

4. **Append-only event log is the source of truth** for execution history. State reconstruction from events + snapshots ensures reliability and auditability. Dashboard views are event-derived.

5. **Current shared worktree model blocks safe parallelism.** Tasks should get independent git worktrees with a merge queue that handles conflict detection, rebasing, and ordered integration.

6. **Write-set conflict model is essential.** Each task declares predicted write paths; the scheduler uses path-glob overlap detection to prevent parallel tasks from corrupting each other.

7. **Approval gates are pausable nodes** with explicit state machines, approver policies, timeout/escalation, and secret-scope unlocking. They are not ad hoc human checkpoints.

8. **Rollback is explicit compensation, not automatic reversal.** Unmerged code is abandoned; merged code is reverted; deployed services have compensation plans. Each side-effecting node produces a rollback plan before execution.

9. **Resource leases protect shared resources.** Durable, time-bounded leases for repos, paths, environments, secrets, and model-provider slots prevent concurrent access violations.

10. **Dynamic dependencies allow runtime graph expansion** when agents discover new work, but patches require validation (cycle check, resource check) before admission.

---

## Architecture Implications

- **P0 Pipeline DAG Engine already built** covers basic pipeline/stage lifecycle. The report recommends evolving it toward the richer model: phase/task DAG hierarchy, artifact contracts, quality gates, resource leases, worktree isolation, and event sourcing.
- **New modules recommended:**
  - `engine/git_worktrees.py` — worktree lifecycle, merge queue, conflict detection
  - `engine/resources.py` — lease manager, concurrency limiter
  - `engine/approvals.py` — approval policies, gate state machine, timeout/escalation
  - Event store (initially append-only JSONL, later DB table)
- **Phase definitions need enrichment:** `depends_on`, `produces`, `consumes`, `completion` (quality gates + approval policies), `parallelism` fields in frontmatter.
- **Task definitions are a new concept:** YAML/JSON task specs with dependencies, artifact contracts, write sets, executor config, quality gates, approval triggers, and rollback strategy.
- **Dashboard needs SSE streaming** for real-time pipeline/task state updates from the event log.

---

## Roadmap Implications

The report proposes an 8-phase MVP sequence:

| MVP Phase | Focus | Key Deliverables |
|---|---|---|
| MVP 0 | Research ingest + design alignment | This synthesis, decision candidates |
| MVP 1 | Static phase DAG | Phase frontmatter enrichment, cycle detection, topological scheduling |
| MVP 2 | Task DAG inside phases | Task definitions, ready queue, failure policies |
| MVP 3 | Event store + SSE dashboard | Append-only events, snapshots, dashboard streaming |
| MVP 4 | Resource leases + concurrency | Lease manager, path-glob conflicts, heartbeat/expiry |
| MVP 5 | Worktree isolation | WorktreeManager, branch naming, merge queue, cleanup |
| MVP 6 | Approval gates | Policy schema, state machine, dashboard cards, timeout |
| MVP 7 | Rollback + replan | Compensation plans, abandon/revert, artifact invalidation |
| MVP 8 | Dynamic dependencies | Graph patches, runtime node creation, cycle revalidation |

This builds incrementally on the existing P0 pipeline engine without requiring a rewrite.

---

## New Risks

| Risk | Severity | Notes |
|---|---|---|
| Custom engine grows into unreliable mini-Temporal | High | Keep engine small; use events/idempotency; define migration adapter boundaries to Temporal/Argo |
| Parallel agents create merge chaos | High | Worktree isolation, write-set leases, merge queue with conflict tasks |
| Dynamic dependencies make runs unpredictable | Medium | Require graph patch validation and provenance; gate risky patches |
| Approvals block forever | Medium | Timeouts, escalation, reminders, dashboard blocker panel |
| JSON state corruption at scale | Medium | Append-only events mitigate; plan DB migration |
| Secret leakage through agent sessions | High | Secret leases, approval-gated access, redacted events |
| Dashboard state drift from server | Medium | Snapshot + ordered event replay + idempotent client reducer |

---

## Decisions Required

1. **DEC-008: Worktree vs. shared checkout** — When to use per-task worktrees vs. sequential shared worktree. Report recommends per-task for independent work, shared only for tiny sequential pipelines.
2. **DEC-009: Event store technology** — JSONL files initially vs. immediate DB table. Report recommends JSONL first, DB later.
3. **DEC-010: Approval scope** — Which actions require approval by default (deploy, secret access, high-risk merge, schema migration). Report provides recommendations.
4. **DEC-011: Concurrency limits** — Default tenant/project/repo/model-provider limits. Report provides starting values.
5. **DEC-012: Rollback strategy** — Fix-forward vs. revert for merged code. Report recommends fix-forward as default for agent-written code.

---

## Implementation Recommendations

1. **Enrich existing `engine/phases.py`** with `depends_on`, `produces`, `consumes`, and `completion` fields in phase frontmatter.
2. **Add `DagValidator`** with cycle detection (DFS or Kahn's algorithm) to the pipeline engine.
3. **Create `NodeRun` state model** with the 16-state enum proposed in the report.
4. **Build event store** as append-only JSONL per run with monotonic sequence numbers.
5. **Add SSE endpoint** for real-time dashboard updates from the event stream.
6. **Create `engine/resources.py`** with lease manager and concurrency limiter.
7. **Create `engine/git_worktrees.py`** with the proposed branch naming convention and merge queue.
8. **Add approval policy schema** to phase/task definitions.
9. **Replace direct JSON mutation** with event-backed state transitions.

---

## Phase Changes

- MVP 1-2 (static phase DAG + task DAG) should follow the multi-tenant foundation, as pipeline runs need tenant context.
- MVP 3-5 (events, leases, worktrees) can proceed in parallel tracks if engineers are available.
- MVP 6-7 (approvals, rollback) depend on the multi-tenant approval model from Topic 01.

---

## Open Questions

1. Should Conductor migrate to Temporal once run complexity warrants it, or keep the native engine indefinitely?
2. What is the maximum expected parallel agent count per project in the near term?
3. Should the merge queue support auto-merge or always require human approval for integration?
4. How should dynamic task creation interact with the build phase approval model?
5. What is the priority of SSE streaming vs. polling for the dashboard MVP?
