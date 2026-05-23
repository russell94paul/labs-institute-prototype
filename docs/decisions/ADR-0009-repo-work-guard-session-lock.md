# ADR-0009: Repo Work Guard, Session Lock, and Execution Queue

**Status:** Proposed
**Date:** 2026-05-19
**Deciders:** Paul Russell
**Category:** Safety / Execution Control

## Context

Conductor is evolving toward semi-autonomous and parallel execution of build phases, pipeline stages, research ingestion, and agent tasks. The P0 Pipeline DAG Engine is complete, providing dependency resolution and stage lifecycle management. However, nothing currently prevents:

- Two Claude Code sessions from modifying the same repo simultaneously.
- A research ingestion task from running while a phase execution is in progress, causing file conflicts.
- A cancelled session from leaving partial, uncommitted changes that block subsequent work.
- A new phase from starting before the previous phase has committed its changes, making rollback impossible.
- The user from unknowingly starting autonomous work while they have uncommitted manual edits.

Without a safety layer, increasing autonomy increases the risk of lost work, merge conflicts, and unrecoverable state. This risk is especially acute on Windows, where file locking behavior and process management differ from Unix assumptions.

The existing autonomy-approval-rollback policy (ADR-0004) defines when approval is needed and how rollback works, but does not address runtime concurrency control or session-level locking.

## Decision

Conductor will implement a **Repo Work Guard** — a runtime safety layer that checks repo state, manages session locks, and queues or blocks work that cannot safely execute concurrently.

The Work Guard will:

1. **Maintain a session lock file** at `.conductor/runtime/session-lock.json` (gitignored) that records the active session's identity, branch, phase, touched paths, and heartbeat.
2. **Gate on git dirty-tree status** — autonomous execution is blocked if the working tree has uncommitted changes.
3. **Enforce commit-before-next-phase** — each phase must produce a commit before the next phase can start, ensuring clean rollback boundaries.
4. **Use heartbeat-based liveness** — active sessions update a heartbeat timestamp; stale locks (no heartbeat for N minutes) trigger recovery checks.
5. **Detect path overlaps** — new tasks declare their expected touched paths; if they overlap with the active session's paths, the task is blocked or queued.
6. **Support worktree isolation** — tasks that can run in isolated git worktrees may execute in parallel with the main branch session.
7. **Queue blocked jobs** — tasks that cannot run immediately are queued with priority ordering and auto-start or notify-only behavior.

Policy is externalized to `config/work-guard-policy.json`, making behavior configurable without code changes.

## Options Considered

### Option A: PID-Based Process Detection Only

Check whether a Claude Code process is running before starting a new session.

- **Pros**: Simple, no new files or state management.
- **Cons**: Misses dirty-tree state, cannot detect path overlaps, no queue, no heartbeat, no commit enforcement. Zombie PIDs and multi-repo sessions make this unreliable.
- **Verdict**: Insufficient as a standalone solution. PID checks are included as one signal within the Work Guard, not as the primary mechanism.

### Option B: Git Branch Locking (One Branch Per Session)

Require each session to operate on a unique branch, preventing overlap.

- **Pros**: Strong isolation via git.
- **Cons**: Forces branch-per-task even for serialized phases on the same branch. Merge complexity increases. Shared config files still conflict. Does not address dirty-tree or commit checkpoints.
- **Verdict**: Useful as an isolation mechanism (via worktrees) but not as the primary concurrency control.

### Option C: File-Based Lock + Dirty-Tree Gate + Heartbeat + Queue (Recommended)

Combine a runtime lock file, git status checks, heartbeat liveness, path overlap detection, commit enforcement, and a job queue.

- **Pros**: Comprehensive coverage of the failure modes. Policy-driven behavior. Works with existing git workflows. Supports both serialized and parallel execution patterns. Lock file is simple JSON — no external dependencies.
- **Cons**: More complex to implement than PID-only. Heartbeat requires periodic writes. Lock file can become stale if the process crashes without cleanup.
- **Verdict**: Recommended. The complexity is justified by the safety guarantees, and stale lock recovery handles the crash case.

### Option D: External Lock Service (Redis, File Lock Daemon)

Use an external service to manage distributed locks.

- **Pros**: Battle-tested distributed locking semantics.
- **Cons**: Adds a dependency. Overkill for single-machine, single-repo operation. Conductor is not yet distributed.
- **Verdict**: Not needed at current scale. Could be revisited if Conductor supports multi-machine execution.

## Recommended Approach

**Option C** — File-based lock with dirty-tree gate, heartbeat, path overlap detection, commit enforcement, and job queue.

Implementation should be phased:
1. **P0.5 (this phase)**: Architecture docs, policy config, templates, and implementation prompt. No runtime code changes.
2. **P0.5 implementation**: Minimal Work Guard that can check git status, detect/create/release locks, detect stale locks, and report `safeToRun`. Expose status to Bootstrap Console.
3. **Future**: Full queue management, worktree orchestration, automatic heartbeat injection into session lifecycle, Build Studio integration.

## Consequences

### Positive

- **Safety**: Prevents concurrent modification of the same files by multiple sessions.
- **Auditability**: Lock file and commit checkpoints create a clear execution history.
- **Rollback confidence**: Commit-before-next-phase ensures each phase can be individually reverted.
- **Visibility**: Dashboard integration shows users whether it is safe to start new work.
- **Composability**: Policy-driven behavior allows different projects to configure different safety levels.

### Negative

- **Execution friction**: The Work Guard may block tasks that could theoretically run safely, requiring manual override or queue management.
- **Stale lock risk**: If a session crashes without cleanup and the stale lock recovery policy is conservative, subsequent tasks are blocked until a user intervenes.
- **Implementation cost**: The full Work Guard (heartbeat, queue, worktree orchestration) is a non-trivial subsystem.

### Neutral

- **No external dependencies**: The lock file approach works without additional infrastructure.
- **Git-native**: Uses git status and worktrees — no custom VCS integration.
- **Policy is data**: Changing behavior requires editing a JSON file, not code.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Lock file corruption (partial write) | Low | Medium | Atomic writes (write to .tmp, rename) — already a Conductor convention |
| Heartbeat writer fails silently | Medium | Low | Stale lock recovery handles this; PID check as secondary signal |
| User ignores Work Guard warnings | Medium | Medium | Make warnings prominent in dashboard; require explicit override for high-risk actions |
| Worktree merge conflicts | Medium | Medium | Path overlap detection prevents concurrent modification of the same files |
| Clock skew affects heartbeat timeout | Low | Low | Use monotonic time where possible; generous timeout default (10 minutes) |

## Future Implementation Notes

- The Work Guard should be a standalone module (`engine/work_guard.py`) that can be imported by the session launcher, pipeline engine, and API server.
- The Bootstrap Console should call the Work Guard's `safeToRun` check before displaying "Start Phase" buttons.
- Pipeline stages should acquire and release locks as part of their lifecycle, integrating with the existing stage state machine in `engine/pipelines.py`.
- The session launcher in `engine/sessions.py` should create and manage locks, including heartbeat updates.
- Research ingestion tasks should declare their expected paths upfront and acquire shared or isolated locks accordingly.
- The Work Guard should not modify core pipeline behavior — it is an advisory and gating layer, not an execution engine.
