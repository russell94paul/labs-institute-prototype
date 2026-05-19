# Rollback Plan: P0 Pipeline DAG Engine

**Date**: 2026-05-18
**Phase**: P0-pipeline-dag
**Risk level**: Low — all changes are additive

## Rollback scope

This phase added new files and extended `engine/server.py`. No existing files were replaced or removed. No database migrations. No external service changes.

## Steps to rollback

### 1. Remove new engine modules

```powershell
Remove-Item engine/pipelines.py
Remove-Item engine/phases.py
```

### 2. Remove dashboard page

```powershell
Remove-Item dashboard/pages/pipelines.html
```

### 3. Revert server.py changes

Restore `engine/server.py` to the pre-P0 version:

```powershell
git checkout HEAD~1 -- engine/server.py
```

Or manually:
- Remove `from engine import pipelines` import
- Remove all pipeline handler methods (`_match_pipeline_route`, `_handle_*_pipeline*`, etc.)
- Remove `_pipeline_session_launcher` function
- Remove `pipelines.configure()` and `pipelines.load_state()` from `main()`
- Remove `pipelines.shutdown()` from `_shutdown()`
- Remove pipeline route entries from `do_GET`, `do_POST`

### 4. Revert config/docs

```powershell
git checkout HEAD~1 -- config/phase-status.json
git checkout HEAD~1 -- docs/build/change-manifest.md
git checkout HEAD~1 -- docs/build/approval-requests.md
```

### 5. Clean up data files

```powershell
Remove-Item dashboard/data/pipelines.json -ErrorAction SilentlyContinue
```

### 6. Remove build docs

```powershell
Remove-Item docs/build/p0-pipeline-dag-engine-build-report.md
Remove-Item docs/build/rollback/p0-pipeline-dag-engine-rollback.md
Remove-Item docs/build/session-handoffs/p0-pipeline-dag-engine-handoff.md
```

## Verification after rollback

1. `python engine/server.py` starts without errors
2. `GET /api/sessions` responds
3. `GET /api/bootstrap/phases` responds
4. Dashboard loads at http://127.0.0.1:8888/
5. Bootstrap console works at http://127.0.0.1:8888/#bootstrap
