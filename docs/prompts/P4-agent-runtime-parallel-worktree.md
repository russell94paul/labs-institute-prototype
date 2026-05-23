# P4 — Agent Runtime + Parallel Worktree Execution

**Phase:** P4-agent-runtime
**Priority:** P4
**Dependencies:** P3-phase-template-os
**Decisions required:** DEC-003 (worktree isolation — must be approved)
**Research required:** Topic 02 synthesis (completed)
**Risk:** High
**Complexity:** XL

---

## Goal

Build the agent execution layer. The pipeline engine dispatches work; agents do the work. This phase adds an agent registry, agent dispatch engine, per-task worktree isolation, a merge queue for parallel results, and an agent status UI.

## Context

The pipeline DAG engine runs stages sequentially or in parallel, but stages currently execute as subprocess sessions (`engine/sessions.py`). The work guard allows worktrees (`maxConcurrentWorktrees: 2`). DEC-003 recommends per-task worktrees with merge queue. This phase operationalizes that decision.

Agent definitions already exist as markdown files in `agents/` (currently placeholder). This phase makes them executable.

## Scope

### Engine: `engine/agents.py`

Agent registry and dispatch:
- Agent definition loader: parse markdown agent files with YAML frontmatter (capabilities, tools, constraints, model preference)
- Agent registry: discover, list, validate agent definitions
- Agent dispatch: match task requirements to agent capabilities, select appropriate agent
- Agent execution: launch agent as session with injected context, tools, and constraints
- Agent lifecycle: idle → assigned → running → completed/failed
- Capability matching: task requires ["code", "review"] → find agent with those capabilities

### Engine: `engine/worktrees.py`

Worktree isolation:
- Create per-task worktree: `git worktree add` with branch naming `conductor/{project}/{run_id}/task-{task_id}`
- Worktree lifecycle: created → in-use → merging → merged/conflict → cleaned
- Merge queue: ordered queue of completed worktree branches waiting to merge back
- Conflict detection: write-set analysis before merge attempt
- Cleanup: automatic worktree removal after successful merge or cancellation
- Disk monitoring: warn when worktree count approaches limit

### Agent Definitions: `agents/*.md`

Formalize agent definitions with executable frontmatter:
- `architect` — system design, API design, schema design
- `implementer` — code writing, file creation, configuration
- `reviewer` — code review, security scan, quality check
- `researcher` — information gathering, synthesis, decision extraction
- `tester` — test writing, validation, regression detection

### Dashboard: Agent Runtime UI

- Agent registry: list agents with capabilities, status, current assignment
- Worktree status: active worktrees, merge queue, disk usage
- Dispatch log: which agent was assigned to which task, when, outcome
- Live execution: SSE feed of agent activity

## API Routes

- `GET /api/agents` — list agents (enhance existing)
- `GET /api/agents/{id}` — agent details + capabilities
- `POST /api/agents/dispatch` — dispatch task to best-fit agent
- `GET /api/worktrees` — list active worktrees
- `POST /api/worktrees` — create worktree for task
- `DELETE /api/worktrees/{id}` — cleanup worktree
- `POST /api/worktrees/merge-queue` — add to merge queue
- `GET /api/worktrees/merge-queue` — get merge queue state

## Acceptance Criteria

- [ ] Agent definitions load from markdown with YAML frontmatter
- [ ] Dispatch matches task capabilities to agent capabilities
- [ ] Worktrees created and cleaned up correctly
- [ ] Merge queue processes in order, detects conflicts
- [ ] Concurrent worktree limit enforced (from work-guard policy)
- [ ] Agent status visible in dashboard
- [ ] Events emitted for all agent and worktree lifecycle transitions
- [ ] Existing pipeline/session APIs unchanged

## Boundaries

- No AI model integration — agents are dispatched as sessions, model selection is external
- No memory/context injection — that's P5
- No multi-tenancy — that's P7
- No autonomous triggering — queue requires approval per P3

## Deliverables

- `engine/agents.py` (enhanced)
- `engine/worktrees.py`
- `agents/architect.md`, `agents/implementer.md`, `agents/reviewer.md`, `agents/researcher.md`, `agents/tester.md`
- Dashboard agent runtime page or Build Studio tab
- `docs/build/p4-agent-runtime-build-report.md`
- `docs/build/rollback/p4-agent-runtime-rollback.md`
- `docs/build/session-handoffs/p4-agent-runtime-handoff.md`
