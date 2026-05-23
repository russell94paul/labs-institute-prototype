# Rollback Plan — P0-events (Event System + SSE + Live Dashboard)

**Phase:** P0-events
**Date:** 2026-05-19
**Risk:** Low — additive changes only, no existing behavior modified

## Rollback Strategy

P0-events is fully additive. Rolling back means removing the new module and reverting the hook additions. No existing functionality depends on events.

## Steps

### 1. Delete new file

```bash
rm engine/events.py
```

### 2. Revert module hooks

In each file, remove the `from engine import events` import and all `events.emit(...)` calls:

- `engine/server.py` — remove events import, SSE handler, event endpoints, event routes, events.configure/shutdown calls
- `engine/bootstrap.py` — remove events import, remove `old_status` capture and `events.emit()` in `update_phase_status()`
- `engine/pipelines.py` — remove events import, remove all `events.emit()` calls
- `engine/sessions.py` — remove events import, remove all `events.emit()` calls
- `engine/work_guard.py` — remove events import, remove all `events.emit()` calls

### 3. Revert dashboard

Remove from `dashboard/pages/bootstrap.html`:
- SSE connection indicator HTML and CSS
- Events tab and panel
- All JS related to EventSource, event rendering, and auto-refresh
- Event-related CSS classes

### 4. Revert config

In `config/phase-status.json`, set P0-events status back to `not_started`.

### 5. Revert CLAUDE.md

Remove `events.py` from architecture tree and Events API section.

## Safe Checkpoint

The commit immediately before P0-events is the safe rollback target. Use:

```bash
git log --oneline -5
git revert <p0-events-commit-hash>
```

## Risk Assessment

- **No data loss** — events are in-memory only
- **No API breaking changes** — new endpoints only; existing endpoints unchanged
- **No state file changes** — no new persistent state files
- **Dashboard safe** — Events tab removal doesn't affect other tabs
