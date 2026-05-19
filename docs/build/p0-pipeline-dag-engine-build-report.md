# Build Report: P0 Pipeline DAG Engine

**Date**: 2026-05-18
**Phase**: P0-pipeline-dag
**Branch**: conductor-platform-rebuild
**Status**: Complete

## What was built

### Core DAG Engine (`engine/pipelines.py`)

A full pipeline execution engine with:

- **Pipeline model**: id, name, template, project, stages[], worktree config, cost tracking
- **Stage model**: name, label, type (claude-p / gate), dependencies, status, session reference, cost/timing
- **Dependency resolution**: `calculate_ready_stages()` computes which stages have all dependencies met
- **Topological sort**: validates DAG is acyclic, computes execution order
- **State machine**: pending → ready → running → completed/failed/cancelled/skipped. Gates: waiting_for_approval
- **Failure propagation**: failed stages block downstream dependents
- **Retry**: reset failed/blocked stages and re-advance
- **Skip**: mark any non-terminal stage as skipped (dependencies treat skipped as met)
- **Cancel**: cancel pipeline and all non-terminal stages
- **Shared worktree**: all stages in a pipeline share one worktree path/branch
- **Session integration**: `_pipeline_session_launcher` in server.py creates sessions per stage, wires completion callback
- **Template loading**: reads YAML pipeline templates from `templates/pipelines/`
- **Dry run**: simulate a pipeline without persisting — computes ready stages, execution order, cost estimates
- **Persistence**: atomic writes to `dashboard/data/pipelines.json`
- **Server restart recovery**: running stages marked failed on restart

### Phase Definition Loader (`engine/phases.py`)

- Parse markdown files with YAML frontmatter (phase_number, phase_name, goal, deliverables, etc.)
- Convert phase specs to template variables for pipeline creation
- Directory scanner for batch phase spec loading

### API Routes (added to `engine/server.py`)

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/pipelines` | List pipelines (filter by project, status) |
| POST | `/api/pipelines` | Create pipeline from template |
| GET | `/api/pipelines/{id}` | Get pipeline detail |
| GET | `/api/pipelines/{id}/summary` | Computed summary |
| POST | `/api/pipelines/{id}/start` | Start pipeline |
| POST | `/api/pipelines/{id}/advance` | Advance past gates/completions |
| POST | `/api/pipelines/{id}/cancel` | Cancel pipeline |
| POST | `/api/pipelines/{id}/stages/{name}/retry` | Retry failed stage |
| POST | `/api/pipelines/{id}/stages/{name}/skip` | Skip a stage |
| POST | `/api/pipelines/{id}/stages/{name}/approve` | Approve gate |
| GET | `/api/templates` | List available templates |
| GET | `/api/pipelines/dry-run?template=X` | Dry run a template |

### Dashboard (`dashboard/pages/pipelines.html`)

- Pipeline list with DAG stage visualization
- KPI strip: total, running, completed, failed, cost, templates
- Three tabs: Pipelines, Templates, Dry Run
- Pipeline detail overlay with stage table + action buttons
- Auto-refresh every 5 seconds
- Actions: start, advance, cancel, retry, skip, approve gate
- Create pipeline from template via Templates tab

## Verification results

| Check | Result |
|-------|--------|
| All engine modules import | Pass |
| phase-status.json valid | Pass (9 phases) |
| Template listing | Pass (2 templates) |
| Dry run standard-phase | Pass (5 stages, correct order) |
| Pipeline create | Pass |
| Ready stage calculation | Pass (plan is ready) |
| Pipeline start + auto-advance | Pass |
| Stage completion + advancement | Pass |
| Failure propagation + blocking | Pass |
| Retry + unblock | Pass |
| Pipeline cancellation | Pass |
| API: GET /api/pipelines | Pass |
| API: POST /api/pipelines | Pass |
| API: GET /api/pipelines/{id} | Pass |
| API: GET /api/pipelines/{id}/summary | Pass |
| API: POST start/advance/cancel | Pass |
| API: GET /api/templates | Pass |
| API: GET /api/pipelines/dry-run | Pass |
| Bootstrap API still works | Pass |
| Sessions API still works | Pass |
| Server starts cleanly | Pass |

## No-regression check

- Bootstrap console: all endpoints respond correctly
- Sessions: standalone session creation unmodified
- Dashboard: existing nav links and pages unaffected
- Config: no changes to phase-status.json content (only updating status in docs step)

## Files created

- `engine/pipelines.py` — Core pipeline DAG engine (~400 lines)
- `engine/phases.py` — Phase definition loader (~120 lines)
- `dashboard/pages/pipelines.html` — Pipeline dashboard page
- `docs/build/p0-pipeline-dag-engine-build-report.md` — This report
- `docs/build/rollback/p0-pipeline-dag-engine-rollback.md` — Rollback plan
- `docs/build/session-handoffs/p0-pipeline-dag-engine-handoff.md` — Session handoff

## Files modified

- `engine/server.py` — Added pipeline API routes, session launcher, pipeline module init
- `docs/build/change-manifest.md` — Added P0 section
- `docs/build/approval-requests.md` — Marked P0 approval as fulfilled
- `config/phase-status.json` — Updated P0-pipeline-dag status to completed

## Architecture decisions

1. **Pipelines own stages, not the reverse**: Stages are embedded in the pipeline dict, not standalone entities. This keeps the DAG together and avoids cross-reference complexity.

2. **Session integration via callback**: Pipeline stages launch sessions via `sessions.create_session()`. The `_on_session_complete` callback wires back to `handle_stage_complete()`. This is a loose coupling — pipelines don't import sessions directly for state management.

3. **Shared worktree ID per pipeline**: All stages in a pipeline get the same worktree_id. The session launcher passes this through so stages chain in the same git worktree.

4. **No event system yet**: Stage transitions call an optional `_on_stage_transition` hook, but there's no SSE/event bus. That's P0-events (next phase).

5. **YAML templates**: Pipeline templates are plain YAML files with variable interpolation. No code execution in templates — just string replacement.
