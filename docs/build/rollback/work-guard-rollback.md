# Rollback Plan — P0.5 Work Guard

**Phase:** p0-5-repo-work-guard-session-lock
**Date:** 2026-05-19
**Risk Level:** Low — additive changes only, no existing behavior modified

## What Changed

1. `engine/work_guard.py` — New file (standalone module)
2. `engine/server.py` — Added import + 5 route handlers + route wiring
3. `dashboard/pages/bootstrap.html` — Added Work Guard banner, tab, panel, and JS functions
4. `config/phase-status.json` — Updated P0.5 status to "completed"

## Rollback Steps

### Option A: Git Revert (Recommended)

```bash
git revert <commit-hash>
```

This cleanly reverses all changes in a new commit.

### Option B: Manual Rollback

1. Delete `engine/work_guard.py`
2. Revert `engine/server.py` — remove the `from engine import work_guard` import and all `_handle_*_work_guard_*` methods and route wiring
3. Revert `dashboard/pages/bootstrap.html` — remove Work Guard CSS, banner, tab, panel, and JS functions
4. Revert `config/phase-status.json` — set P0.5 status back to `"pending"`

### Option C: Reset to Pre-P0.5 Commit

```bash
git log --oneline -5
# Find the commit before P0.5 implementation
git reset --hard <pre-p0.5-commit>
```

## Impact of Rollback

- No data loss — Work Guard is read-only (status checks + advisory lock)
- Lock files in `.conductor/runtime/` are gitignored and can be safely deleted
- No other engine modules depend on work_guard.py
- Bootstrap Console functionality unaffected (Work Guard UI is additive)

## Safe Checkpoint

The commit immediately before this phase's commit is the safe rollback target.
