# Decision: DEC-003 — Worktree Isolation Model

## Context
The current pipeline engine shares one git worktree across all stages. This blocks safe parallelism and makes it impossible to attribute diffs to individual tasks or roll back cleanly.

## Options
1. **Keep shared worktree** — Simple, works for sequential pipelines. Blocks all parallelism; tasks can contaminate each other.
2. **Per-task worktrees (recommended)** — Each independent task gets its own git worktree and branch. A merge queue handles integration. Enables safe parallel execution.
3. **Per-lane worktrees** — Group related tasks into lanes sharing a worktree. More complex than per-task; less isolation.

## Recommendation
Option 2 for independent tasks. Use the branch naming convention `conductor/{project}/{run_id}/task-{task_id}` with an integration branch `conductor/{project}/integration/{run_id}`. Dependent tasks start from the merged output of their prerequisite. Small sequential pipelines can still use a single worktree as an optimization.

## Research Source
Topic 02 — Agent Orchestration, DAGs & Parallelization (Section 7)

## Affects
- `engine/pipelines.py` — stage/task dispatch
- New `engine/git_worktrees.py` module
- `engine/sessions.py` — session working directory
- Dashboard — merge queue and conflict views

## Status
Proposed

## Decided by
(pending)
