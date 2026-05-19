# P3 — Phase Template OS + Execution Queue

**Phase:** P3-phase-template-os
**Priority:** P3
**Dependencies:** P2-onboarding (completed)
**Decisions required:** DEC-003 (worktree isolation — approve), DEC-004 (event store — approve)
**Research required:** Topic 02 synthesis (completed)
**Risk:** Medium
**Complexity:** XL

---

## Goal

Make phases machine-executable. Currently, phases are markdown files with YAML frontmatter (parsed by `engine/phases.py`) and a JSON registry (`config/phase-status.json`). This phase adds a formal template schema, variable injection, an execution queue with priority and concurrency controls, and a phase runner UI integrated into the dashboard.

## Context

The pipeline DAG engine (`engine/pipelines.py`) can execute stage sequences, but phase definitions are passive metadata — they describe what to build, not how to execute it. The work guard (`engine/work_guard.py`) provides safety gates. The event system (`engine/events.py`) provides real-time streaming. P3 connects these into a self-driving execution loop.

## Scope

### Engine: `engine/templates.py`

Phase template engine:
- Template schema definition (YAML) with typed variables, defaults, validation rules
- Variable injection: resolve `${project.name}`, `${phase.id}`, `${config.*}` references
- Template inheritance: base templates with override layers
- Template validation: schema check before execution
- Template registry: discover + load templates from `templates/` directory

### Engine: `engine/queue.py`

Execution queue:
- Priority queue with configurable concurrency limit (default: 1, max from work-guard policy)
- Queue items: phase ID, priority, requested-by, requested-at, estimated duration
- Queue lifecycle: pending → queued → executing → completed/failed/cancelled
- Gate integration: work guard safe-to-run check before dequeue
- Event emission: `queue.item.enqueued`, `queue.item.started`, `queue.item.completed`

### Config: `config/template-schema.json`

JSON Schema for phase templates:
- Required fields: id, name, goal, stages, acceptance_criteria
- Optional fields: variables, constraints, deliverables, rollback_plan
- Stage fields: id, name, command_or_prompt, depends_on, timeout, retry_policy

### Dashboard: Phase Runner UI

Add phase execution controls to Build Studio or as standalone page:
- Queue view: pending, active, completed items
- Phase launch: select template, fill variables, preview dry run, submit to queue
- Execution monitor: real-time SSE feed of running phase, stage progress
- History: past executions with outcomes, duration, files changed

### Templates: Initial set

Create at least 3 example templates in `templates/`:
1. `research-ingestion.yaml` — ingest a Deep Research topic (stages: validate input, synthesize, extract decisions, update status)
2. `feature-build.yaml` — standard feature build (stages: plan, implement, test, review, report)
3. `docs-update.yaml` — documentation update (stages: identify scope, write, validate links)

## API Routes

- `GET /api/templates` — list available templates
- `GET /api/templates/{id}` — get template details with schema
- `POST /api/templates/validate` — validate a template definition
- `GET /api/queue` — get queue state (pending, active, completed)
- `POST /api/queue` — enqueue a phase execution
- `DELETE /api/queue/{id}` — cancel a queued/running item
- `POST /api/queue/{id}/priority` — update priority of queued item

## Integration Points

- `engine/pipelines.py` — queue items create pipeline runs
- `engine/work_guard.py` — safe-to-run gate before execution
- `engine/events.py` — emit queue and template events
- `engine/bootstrap.py` — phase status updates on completion
- `engine/phases.py` — template-driven phase definition loading

## Acceptance Criteria

- [ ] Template schema validates correctly (positive and negative cases)
- [ ] Variable injection resolves all reference types
- [ ] Queue respects concurrency limits from work-guard policy
- [ ] Queue blocks execution when work guard reports unsafe
- [ ] Events stream for all queue state transitions
- [ ] Phase runner UI shows queue, allows launch, shows execution progress
- [ ] At least 3 working template definitions in `templates/`
- [ ] Existing pipeline/session/event APIs unchanged
- [ ] All existing dashboard pages still functional

## Boundaries

- No autonomous execution — queue requires manual trigger or approval
- No agent dispatch — that's P4
- No memory/context integration — that's P5
- No multi-tenancy — that's P7
- No secrets/credentials handling
- No external service dependencies

## Deliverables

- `engine/templates.py`
- `engine/queue.py`
- `config/template-schema.json`
- `templates/research-ingestion.yaml`
- `templates/feature-build.yaml`
- `templates/docs-update.yaml`
- Dashboard phase runner (page or Build Studio tab)
- `docs/build/p3-phase-template-os-build-report.md`
- `docs/build/rollback/p3-phase-template-os-rollback.md`
- `docs/build/session-handoffs/p3-phase-template-os-handoff.md`
