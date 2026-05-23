# Repo Work Guard, Session Lock, and Execution Queue

## Overview

Conductor orchestrates Claude Code sessions, pipeline stages, research ingestion, and phase transitions. As execution becomes more autonomous and parallel, the risk of concurrent modifications to the same repo, branch, or file set increases. The Work Guard is a safety layer that prevents destructive overlaps, enforces commit checkpoints, and queues work that cannot safely run concurrently.

## Why Process Detection Alone Is Insufficient

Checking whether a Claude Code process is running (via PID or process table) is necessary but not sufficient:

- **Zombie PIDs**: A crashed session leaves a PID that no longer corresponds to a running process, but the working tree may be in a dirty state with uncommitted partial changes.
- **Multiple repos**: A single Claude Code process may operate across repos, so a PID check on one repo says nothing about what the session is actually touching.
- **Session intent opacity**: A running PID does not reveal which files the session plans to modify, which branch it targets, or which phase it belongs to. Two sessions could both be running validly but targeting overlapping files.
- **External editors**: The user may have uncommitted changes from manual editing, IDE refactors, or other tools — no Claude PID to detect, but the repo is not in a safe state for autonomous execution.
- **Worktree isolation gaps**: Even with git worktrees, shared config files (phase-status.json, pipeline state) can be modified by multiple sessions unless explicitly coordinated.

The Work Guard combines PID awareness with repo-level state inspection: lock files, git dirty-tree checks, branch tracking, touched-path declarations, and heartbeat liveness.

## Repo-Level Session Lock

### Lock File

A single lock file at `.conductor/runtime/session-lock.json` represents the active claim on the repo's working tree. This file:

- Is created when a session, pipeline stage, or autonomous task begins execution.
- Is updated with heartbeat timestamps during execution.
- Is released (deleted) on clean completion or explicit cancellation.
- Is **gitignored** — it is runtime state, not project state.

### Lock Fields

```json
{
  "lockId": "uuid-v4",
  "repoPath": "C:\\Users\\PaulRussell\\repos\\conductor",
  "branch": "conductor-platform-rebuild",
  "worktreePath": null,
  "phaseId": "P0-pipeline-dag",
  "sessionType": "phase-execution",
  "owner": "claude-code",
  "pid": 12345,
  "startedAt": "2026-05-19T14:30:00Z",
  "lastHeartbeatAt": "2026-05-19T14:35:00Z",
  "status": "active",
  "touchedPaths": ["engine/pipelines.py", "engine/phases.py", "config/phase-status.json"],
  "expectedCommitRequired": true,
  "latestCommitAtStart": "abc1234",
  "handoffPath": "docs/build/session-handoffs/p0-pipeline-dag-engine-handoff.md",
  "allowParallel": false,
  "riskLevel": "high",
  "queuedJobs": []
}
```

### Session Types

| Type | Description | Lock behavior |
|------|-------------|---------------|
| `phase-execution` | Running a build phase | Exclusive lock on main worktree |
| `research-ingestion` | Ingesting research outputs | Shared lock if docs-only, exclusive if touching config |
| `pipeline-stage` | Running a pipeline stage | Lock scoped to worktree (shared or isolated) |
| `autonomous-task` | Background autonomous work | Exclusive or worktree-isolated depending on policy |
| `manual-edit` | User is editing manually | Advisory — detected via dirty tree, not lock file |

## Git Dirty-Tree Gate

Before any autonomous execution begins, the Work Guard checks `git status`:

- **Clean tree**: Safe to proceed — acquire lock and begin.
- **Dirty tree (unstaged changes)**: Block execution. The user or a previous session has uncommitted work. The Work Guard reports the dirty paths and recommends: commit, stash, or discard before proceeding.
- **Dirty tree (staged but uncommitted)**: Block execution. Same as above — staged changes indicate in-progress work.
- **Untracked files in watched paths**: Warning, not a hard block. Untracked files in `engine/`, `dashboard/`, or `config/` are flagged; untracked files in `docs/` or `local-inputs/` are ignored.

The dirty-tree gate is the first check and short-circuits all other checks if the tree is not clean.

## Commit-Before-Next-Phase Rule

Each phase execution must end with a commit (or an explicit skip-commit override with approval). This ensures:

- The git log records what each phase actually changed.
- Rollback to pre-phase state is a single `git revert` or `git reset`.
- The next phase starts from a known-clean state.
- Session handoff documents reference a specific commit hash.

The Work Guard enforces this by comparing `latestCommitAtStart` (recorded in the lock) with `HEAD` at completion. If `HEAD` has not advanced and files were modified, the phase cannot be marked as complete.

## Heartbeat

Active sessions update `lastHeartbeatAt` in the lock file periodically (recommended: every 60 seconds). The heartbeat serves two purposes:

1. **Liveness detection**: If `lastHeartbeatAt` is older than the configured timeout (default: 10 minutes), the lock is considered stale.
2. **Progress indication**: The dashboard can show "last active N minutes ago" for running sessions.

### Heartbeat Protocol

- On session start: create lock file with `startedAt` and `lastHeartbeatAt` set to current time.
- During execution: update `lastHeartbeatAt` every 60 seconds.
- On clean completion: delete lock file.
- On cancellation: update `status` to `"cancelled"`, leave lock file for inspection, then delete after handoff is written.

## Stale Lock Recovery

A lock is stale when `lastHeartbeatAt` is older than `heartbeatTimeoutMinutes` (default: 10). Recovery:

1. **Check PID**: If the lock has a `pid`, check if the process is still running.
   - PID alive: Lock is not stale — the heartbeat writer may have failed but the session is active. Log a warning.
   - PID dead: Lock is stale. Proceed to step 2.
   - No PID: Treat as stale. Proceed to step 2.
2. **Check git status**: Is the working tree dirty?
   - Dirty: The stale session left uncommitted changes. **Do not auto-recover.** Flag for user intervention. Recommend: inspect changes, commit or discard, then remove lock.
   - Clean: The session likely completed but failed to clean up the lock. Auto-remove the lock file and log the recovery.
3. **Policy override**: If `staleLockBehavior` is set to `"auto-recover"`, clean stale locks are removed automatically. If set to `"require-approval"`, all stale locks require user confirmation.

## Session Ownership

Each lock records an `owner` field:
- `"claude-code"` — a Claude Code session via Conductor
- `"pipeline-stage"` — a pipeline-managed stage execution
- `"user"` — manual user work (advisory lock)
- `"research-ingestion"` — research ingestion task

Ownership determines who can release the lock:
- The session that created the lock can always release it.
- A user can force-release any lock (with confirmation).
- The stale lock recovery process can release locks per policy.
- A different session cannot release another session's lock without force.

## Current Phase Tracking

The lock file's `phaseId` field links the active lock to the phase-status registry (`config/phase-status.json`). This enables:

- The dashboard to show which phase is actively executing.
- The Work Guard to prevent starting a new phase while one is running.
- Phase completion logic to verify the correct lock is active.

Phase transitions follow: **pending -> locked -> executing -> commit-required -> completed**.

## Queued Job Behavior

When a task cannot acquire the lock, it enters the queue:

```json
{
  "queuedJobs": [
    {
      "jobId": "uuid",
      "requestedAt": "2026-05-19T14:40:00Z",
      "sessionType": "research-ingestion",
      "phaseId": null,
      "requestedBy": "user",
      "priority": "normal",
      "estimatedPaths": ["docs/research/syntheses/"],
      "status": "queued",
      "reason": "Lock held by phase-execution on P0-pipeline-dag"
    }
  ]
}
```

Queue behavior:
- **FIFO by default**: Jobs run in request order when the lock is released.
- **Priority override**: `"high"` priority jobs jump the queue (with approval if policy requires).
- **Auto-start**: When the lock is released and the tree is clean, the next queued job is started automatically if `queuedJobBehavior` is `"auto-start"`. If `"notify-only"`, the user is notified but must manually start the next job.
- **Stale queue entries**: Queue entries older than 24 hours are automatically pruned.

## Overlapping File/Path Detection

Before a new session or queued job starts, the Work Guard compares its `estimatedPaths` (or `touchedPaths` from a template) against the active lock's `touchedPaths`:

- **No overlap**: Safe to run in parallel (if policy allows).
- **Overlap in docs-only paths**: Warning — may be safe if both are docs-only tasks. Policy-configurable.
- **Overlap in engine/config/dashboard paths**: Block — must serialize.
- **Overlap unknown**: If the new task cannot declare its paths, treat as potentially overlapping. Block unless running in an isolated worktree.

## Worktree Isolation Strategy

Git worktrees allow parallel execution by giving each session its own working directory on a separate branch:

### When to Use Worktrees

- Two tasks target different branches (e.g., a feature branch and a docs branch).
- A pipeline stage is designed for isolated execution (declared in pipeline template).
- Research ingestion needs to run while a phase is executing on the main branch.

### Worktree Lifecycle

1. **Create**: `git worktree add .conductor/worktrees/<name> -b <branch>` (or check out existing branch).
2. **Lock**: Create a separate lock file at `.conductor/worktrees/<name>/session-lock.json`.
3. **Execute**: Run the task in the worktree directory.
4. **Merge/PR**: Changes from the worktree are merged back to the main branch via PR or fast-forward.
5. **Cleanup**: Remove worktree with `git worktree remove`.

### Worktree Constraints

- Shared config files (`config/phase-status.json`, `config/work-guard-policy.json`) must not be modified from worktrees — only the main worktree can update them.
- The main worktree's lock takes precedence — if it blocks a path, no worktree can bypass that.
- Maximum concurrent worktrees: configurable (default: 2).

## When Parallel Execution Is Allowed

| Scenario | Parallel? | Condition |
|----------|-----------|-----------|
| Two docs-only tasks | Yes | Non-overlapping paths |
| Research ingestion + phase execution | Conditional | Research in worktree, no config overlap |
| Two phase executions | No | Phases are serialized by dependency chain |
| Pipeline stage in worktree + main branch work | Yes | Worktree isolation, no shared config writes |
| User manual edit + autonomous task | No | Dirty tree gate blocks autonomous start |

## When a Task Must Wait

- Active lock exists and `allowParallel` is `false`.
- Git working tree is dirty.
- Overlapping `touchedPaths` with active session.
- Previous phase has not committed its changes.
- Lock exists but is potentially stale (pending recovery check).

## When a Task Requires Approval

- `riskLevel` is `"high"` and `highRiskRequiresApproval` policy is `true`.
- Task is in `approvalRequiredFor` list in work-guard-policy.
- Stale lock recovery with dirty tree.
- Force-releasing another session's lock.
- Overriding the commit-before-next-phase rule.
- Running a queued job with `"high"` priority that jumps the queue.

## Cancellation and Resume Behavior

### Cancellation

When a session is cancelled:

1. Update lock `status` to `"cancelled"`.
2. Check git status for uncommitted changes.
3. If dirty: write a handoff document at `handoffPath` describing the partial state, changed files, and recommended next steps.
4. If clean: the cancellation was clean — delete lock, no handoff needed.
5. If the cancelled session had queued jobs, they remain queued and are re-evaluated when the lock is cleared.

### Resume

Resuming a cancelled session:

1. Read the handoff document.
2. Check if the working tree matches the expected state (same commit, same dirty files).
3. Re-acquire the lock with a new `lockId` but same `phaseId`.
4. Continue from where the cancelled session left off.

If the working tree has diverged (new commits, different dirty files), resume is not safe — the user must reconcile manually.

## Rollback Expectations

Each phase that completes under the Work Guard has:

- A known starting commit (`latestCommitAtStart`).
- A known ending commit (the commit-before-next-phase checkpoint).
- A rollback document at `docs/build/rollback/<phase-id>-rollback.md`.

Rollback procedure:
1. Reset to `latestCommitAtStart` for the phase.
2. Verify the tree is clean.
3. Update `config/phase-status.json` to revert the phase status.
4. Delete any worktrees created by the phase.

The Work Guard does not perform rollbacks — it provides the information needed for manual or semi-automated rollback.

## Future UI Requirements

The Bootstrap Console (and future Build Studio) should display:

- **Lock status indicator**: Green (no lock), yellow (lock active), red (stale lock).
- **Active session details**: Owner, phase, duration, last heartbeat.
- **Dirty tree warning**: Shown prominently if the working tree is not clean.
- **Queue view**: List of queued jobs with estimated wait, priority, and requested paths.
- **Safe-to-run check**: A button or auto-check that runs the full Work Guard evaluation and reports whether it is safe to start a new task.
- **Force-release controls**: Available to the user with confirmation dialog.
- **Phase commit timeline**: Visual showing commit checkpoints between phases.
- **Worktree status**: Active worktrees, their branches, and lock status.
