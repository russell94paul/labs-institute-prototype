# P0.5 — Work Guard Build Report

**Phase:** p0-5-repo-work-guard-session-lock
**Date:** 2026-05-19
**Status:** Completed
**Branch:** conductor-platform-rebuild

## Summary

Implemented the minimal Work Guard safety layer: a standalone `engine/work_guard.py` module providing repo-level safety checks (git dirty-tree, session lock, stale lock detection, PID liveness), five API endpoints on `engine/server.py`, and a Work Guard status panel on the Bootstrap Console.

## Deliverables

| Artifact | Path | Status |
|----------|------|--------|
| Work Guard module | `engine/work_guard.py` | Created |
| API routes (5 endpoints) | `engine/server.py` | Modified |
| Bootstrap Console Work Guard UI | `dashboard/pages/bootstrap.html` | Modified |
| Phase status update | `config/phase-status.json` | Modified |
| Build report | `docs/build/work-guard-build-report.md` | Created |
| Rollback plan | `docs/build/rollback/work-guard-rollback.md` | Created |
| Session handoff | `docs/build/session-handoffs/p0-5-work-guard-handoff.md` | Created |

## API Endpoints Added

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/work-guard/status` | Full Work Guard status |
| GET | `/api/work-guard/safe-to-run` | Safety check result |
| POST | `/api/work-guard/lock` | Acquire session lock |
| DELETE | `/api/work-guard/lock` | Release session lock |
| POST | `/api/work-guard/heartbeat` | Update lock heartbeat |

## Work Guard Module Functions

- `check_git_status(repo_path)` — branch, commit, dirty/clean state
- `read_lock(repo_path)` — read lock file or None
- `acquire_lock(repo_path, lock_data)` — create lock (atomic write)
- `release_lock(repo_path, lock_id)` — delete lock if ID matches
- `update_heartbeat(repo_path, lock_id)` — update heartbeat timestamp
- `is_stale(lock_data, timeout_minutes)` — stale lock detection
- `check_pid_alive(pid)` — cross-platform PID check
- `safe_to_run(repo_path)` — main safety gate
- `get_status(repo_path)` — full status for dashboard

## Bootstrap Console Integration

- Work Guard banner added below header showing lock status, safe-to-run badge, and branch/commit info
- New "Work Guard" tab with detailed Git State, Session Lock, Safety Checks, and Recommended Action panels
- Refresh button triggers on-demand Work Guard status check
- Status auto-loads on page refresh

## Validation

- `engine/work_guard.py` under 400 lines (232 lines)
- Module imports cleanly
- Lock acquire/release roundtrip works
- `safe_to_run` returns correct results for clean/dirty tree states
- Server imports cleanly with new routes
- `.conductor/runtime/` already gitignored
- No secrets or env files read or modified
- No external dependencies added

## Not Implemented (Deferred)

- Session lifecycle lock integration (`engine/sessions.py` unchanged)
- Pipeline engine lock integration (`engine/pipelines.py` unchanged)
- Full job queue management
- Worktree orchestration
- Automatic heartbeat injection
- Force-release UI controls (future Build Studio feature)
