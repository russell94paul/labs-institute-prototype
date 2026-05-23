# P0.5 — Repo Work Guard, Session Lock, and Execution Queue

## Implementation Prompt

You are implementing P0.5 of the Conductor platform: a minimal Work Guard that adds repo-level safety checks before session execution.

### Prerequisites

- P0 Pipeline DAG Engine is complete.
- Architecture doc exists at `docs/architecture/repo-work-guard-session-lock.md`.
- ADR exists at `docs/decisions/ADR-0009-repo-work-guard-session-lock.md`.
- Policy config exists at `config/work-guard-policy.json`.
- Example lock file exists at `docs/templates/session-lock.json`.
- Status template exists at `docs/templates/work-guard-status.md`.

### Scope — Build Only These

1. **`engine/work_guard.py`** — A standalone module that provides:

   - `check_git_status(repo_path) -> dict` — Returns `{"clean": bool, "dirty_files": list, "branch": str, "latest_commit": str}`.
   - `read_lock(repo_path) -> dict | None` — Reads `.conductor/runtime/session-lock.json` if it exists, returns parsed JSON or `None`.
   - `acquire_lock(repo_path, lock_data) -> bool` — Creates the lock file. Fails if a lock already exists and is not stale. Uses atomic write (write to `.tmp`, rename).
   - `release_lock(repo_path, lock_id) -> bool` — Deletes the lock file if `lockId` matches. Returns `False` if the lock belongs to another session.
   - `update_heartbeat(repo_path, lock_id) -> bool` — Updates `lastHeartbeatAt` in the lock file.
   - `is_stale(lock_data, timeout_minutes) -> bool` — Returns `True` if `lastHeartbeatAt` is older than `timeout_minutes`.
   - `check_pid_alive(pid) -> bool` — Cross-platform PID liveness check.
   - `safe_to_run(repo_path) -> dict` — The main entry point. Returns `{"safe": bool, "checks": {...}, "recommended_action": str}`. Checks: no active non-stale lock, clean working tree, previous phase committed, no path overlap.
   - `get_status(repo_path) -> dict` — Returns full Work Guard status for dashboard display.

2. **API routes in `engine/server.py`**:

   - `GET /api/work-guard/status` — Returns `get_status()` result.
   - `GET /api/work-guard/safe-to-run` — Returns `safe_to_run()` result.
   - `POST /api/work-guard/lock` — Acquires a lock (body: lock data).
   - `DELETE /api/work-guard/lock` — Releases the active lock.
   - `POST /api/work-guard/heartbeat` — Updates heartbeat for active lock.

3. **Bootstrap Console integration** — Add a Work Guard status indicator to `dashboard/pages/bootstrap.html`:
   - A status badge showing lock state (unlocked / locked / stale).
   - A "Safe to Run?" check that calls the API and displays the result.
   - Do not modify existing Bootstrap Console features — only add the status indicator.

### Scope — Do NOT Build

- Do not modify the pipeline engine's execution logic.
- Do not modify session creation/launch in `engine/sessions.py` (future phase will integrate lock acquisition into session lifecycle).
- Do not implement the full job queue (future phase).
- Do not implement worktree orchestration (future phase).
- Do not implement automatic heartbeat injection (future phase).
- Do not read, write, or modify `.env`, secrets, credentials, or deployment configs.
- Do not install new dependencies — use only Python stdlib and modules already in the project.

### Policy Config

Read `config/work-guard-policy.json` for configurable behavior:
- `lockFilePath` — where to write the lock file.
- `heartbeatTimeoutMinutes` — threshold for stale lock detection.
- `blockOnDirtyWorkingTree` — whether to block on dirty tree.
- `requireCommitBeforeNextPhase` — whether to enforce commit checkpoints.
- `staleLockBehavior` — `"auto-recover"` or `"require-approval"`.

### File Conventions

- Keep `engine/work_guard.py` under 400 lines.
- Use atomic writes for the lock file (write to `.tmp`, then rename).
- No comments unless the WHY is non-obvious.
- No docstrings longer than one line.
- Ensure `.conductor/runtime/` directory is created on first lock acquisition if it does not exist.

### Testing

- Verify `safe_to_run` returns `{"safe": true}` on a clean repo with no lock.
- Verify `safe_to_run` returns `{"safe": false}` when a lock file exists.
- Verify `safe_to_run` returns `{"safe": false}` when the working tree is dirty.
- Verify stale lock detection works with a heartbeat older than the timeout.
- Verify lock acquire/release round-trip.
- Verify the API routes respond correctly.
- Verify the Bootstrap Console badge renders.

### Deliverables

After implementation, create:
- `docs/build/p0-5-repo-work-guard-session-lock-build-report.md`
- `docs/build/rollback/p0-5-repo-work-guard-session-lock-rollback.md`
- `docs/build/session-handoffs/p0-5-repo-work-guard-session-lock-handoff.md`
- Update `config/phase-status.json` — set `p0-5-repo-work-guard-session-lock` status to `"completed"`.
- Update `docs/build/change-manifest.md` with all created/modified files.
