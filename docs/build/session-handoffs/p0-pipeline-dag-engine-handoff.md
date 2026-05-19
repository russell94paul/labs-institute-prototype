# Session Handoff: P0 Pipeline DAG Engine

**Date**: 2026-05-18
**From session**: P0 Pipeline DAG Engine
**To session**: P0 Event System + SSE + Live Dashboard (when ready)

## What was completed

### P0 Pipeline DAG Engine

Built the core pipeline execution model for Conductor. Pipelines are DAGs of stages that execute in dependency order, with automatic advancement, failure propagation, retry/skip/cancel, gate approval, and session integration.

**Engine** (`engine/pipelines.py`):
- Pipeline and stage state machines with full lifecycle
- DAG dependency resolution (`calculate_ready_stages`)
- Cycle detection and DAG validation
- Topological sort for execution ordering
- Failure propagation to downstream stages
- Retry with automatic unblocking of dependents
- Skip, cancel, gate approval
- Shared worktree strategy per pipeline
- Session launcher integration (creates `claude -p` sessions per stage)
- YAML template loading from `templates/pipelines/`
- Dry run simulation (no persistence)
- Atomic state persistence to `dashboard/data/pipelines.json`
- Server restart recovery (running stages → failed)

**Phase loader** (`engine/phases.py`):
- Markdown + YAML frontmatter parser for phase definitions
- Variable extraction for pipeline template interpolation
- Directory scanner for batch loading

**API routes** (added to `engine/server.py`):
- Full CRUD + lifecycle for pipelines (12 endpoints)
- Template listing and dry run
- Session launcher wires stage completion back to pipeline advancement

**Dashboard** (`dashboard/pages/pipelines.html`):
- Pipeline list with stage DAG visualization
- Template browser with create-from-template
- Dry run viewer with execution order and cost estimates
- Pipeline detail overlay with per-stage actions
- Auto-refreshing KPI strip

## What the next session must do

### P0 Event System + SSE + Live Dashboard

This phase depends on the pipeline DAG engine being complete. It should:

1. **Build `engine/events.py`**: Event bus for pipeline/session state transitions
2. **Add SSE endpoint**: `GET /api/events` with server-sent events
3. **Build `dashboard/pages/pipeline-live.html`**: Real-time pipeline execution view
4. **Wire events**: Pipeline stage transitions → event bus → SSE → dashboard
5. **Replace polling**: Dashboard currently polls every 5 seconds; SSE should replace this

### Key files to reference

| File | Purpose |
|------|---------|
| `engine/pipelines.py` | DAG engine — `_on_stage_transition` hook is the integration point for events |
| `engine/sessions.py` | Session manager — `_on_session_complete` callback is already used by pipelines |
| `engine/server.py` | HTTP server — add SSE endpoint here |
| `dashboard/pages/pipelines.html` | Pipeline dashboard — update to use SSE instead of polling |
| `config/phase-status.json` | Update P0-events status when starting |
| `templates/pipelines/standard-phase.yaml` | Reference template for testing |

### Integration points

- `pipelines.set_on_stage_transition()` — already exists, currently unused. Wire this to the event bus.
- `sessions.set_on_complete()` — currently used by pipeline session launcher. The event system should observe this too (may need a multi-listener pattern).
- SSE should stream: pipeline created/started/completed/failed, stage transitions, session output lines.

### Constraints

- Do NOT implement full Build Studio, client portal, memory/vector DB
- Do NOT deploy, touch secrets, auth/RLS, or cloud resources
- Keep SSE simple — no WebSocket, no complex pub/sub

## Verification

- Server runs: `python engine/server.py` → http://127.0.0.1:8888
- Pipeline API: http://127.0.0.1:8888/api/pipelines
- Templates: http://127.0.0.1:8888/api/templates
- Dry run: http://127.0.0.1:8888/api/pipelines/dry-run?template=standard-phase
- Pipeline dashboard: http://127.0.0.1:8888/#pipelines
- Bootstrap console: http://127.0.0.1:8888/#bootstrap (unchanged)
- P0-pipeline-dag shows as "completed" in phase status
