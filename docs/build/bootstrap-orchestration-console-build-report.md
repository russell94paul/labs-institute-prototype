# Bootstrap Orchestration Console — Build Report

**Phase**: 00-bootstrap
**Date**: 2026-05-18
**Status**: Completed

## Summary

Built a lightweight internal control surface for managing the Conductor platform build before the full Build Studio exists. Provides phase tracking, dependency visualization, eligible work queue, blocker tracking, parallelization recommendations, and rollback center.

## Files Created

| File | Purpose |
|------|---------|
| `engine/bootstrap.py` | Phase dependency engine — computes eligible, blocked, parallelizable phases, critical path |
| `dashboard/pages/bootstrap.html` | Self-contained SPA page with 10 tabbed views |
| `docs/build/bootstrap-orchestration-console-build-report.md` | This report |
| `docs/build/rollback/bootstrap-orchestration-console-rollback.md` | Rollback instructions |
| `docs/build/session-handoffs/bootstrap-orchestration-console-handoff.md` | Session handoff |
| `docs/decisions/bootstrap-orchestration-console.md` | ADR for bootstrap console |

## Files Modified

| File | Changes |
|------|---------|
| `engine/server.py` | Added bootstrap API routes (`/api/bootstrap/phases`, `/api/bootstrap/summary`, PATCH/POST per-phase) |
| `dashboard/index.html` | Added "Bootstrap" nav link + route entry |
| `config/phase-status.json` | Marked 00-bootstrap as completed |
| `docs/build/change-manifest.md` | Added Phase 5 section |
| `docs/build/blockers.md` | Updated with current state |
| `docs/build/approval-requests.md` | Updated with current state |
| `docs/build/parallelization-status.md` | Updated for post-bootstrap state |

## How to Run

```bash
python engine/server.py
# Open http://127.0.0.1:8888/#bootstrap
```

## How to Use

1. Click "Bootstrap" in the top nav bar
2. **Roadmap tab**: See all 9 phases with status, risk, complexity, and parallelization eligibility
3. **Dependencies tab**: Layered DAG view + critical path visualization
4. **Work Queue tab**: Eligible phases with "Copy Prompt" and "Launch" buttons, plus next recommendation
5. **Blockers tab**: Phases blocked and why, with missing dependency detail
6. **Approvals tab**: Approval-gated phases with required agents
7. **Reports tab**: Build report paths per phase
8. **Parallelization tab**: Which phases can run in parallel vs. must serialize
9. **Changes tab**: Files modified in this phase
10. **Rollback tab**: Rollback commands and all rollback plan links
11. **Quarantine tab**: Quarantined files and review status

Click any phase row to open Phase Detail View with full metadata, branch command, prompt path, and action buttons (Mark Complete, Mark Blocked, Launch Instructions).

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/bootstrap/phases` | List all phases |
| GET | `/api/bootstrap/summary` | Computed summary (eligible, blocked, critical path, next) |
| GET | `/api/bootstrap/phases/{id}` | Get single phase |
| PATCH | `/api/bootstrap/phases/{id}` | Update phase status |
| POST | `/api/bootstrap/phases/{id}/blocker` | Add/clear blocker |

## Autonomy Levels

Modeled but only `manual` + `assisted` enabled initially:
- `manual`: User launches every phase
- `assisted`: Console recommends next phase (current default)
- `semi_autonomous`: Future — auto-run safe docs/test tasks
- `guarded_autonomous`: Future — eligible phases with pause for risky ops
- `full_autonomous`: Disabled until evaluation, rollback, and approval systems exist

## Limitations

- UI is read-only for most operations (status changes via API or detail panel buttons)
- No WebSocket/SSE live updates — manual refresh required
- DAG view is a simple layered layout, not a full force-directed graph
- No sub-phase/task decomposition UI yet (model exists in engine)
- Quarantine review is static (shows known quarantined files)
- No file-overlap detection for parallelization (uses phase-level flags)

## Next Recommended Phase

**P0-pipeline-dag** — P0 Pipeline DAG Engine

## Known Gaps

- Sub-phase task breakdown UI (engine supports it, UI does not)
- Live SSE event updates for active sessions
- File-overlap based parallelization safety checks
- Persistent blocker/approval state beyond phase-status.json
