# L. Prioritized Improvement Backlog + M. Recommended Next Implementation Prompt

## L. Prioritized Improvement Backlog

### P0 — Foundation (implement next, blocks everything else)

| # | Item | Source | Effort | Description |
|---|------|--------|--------|-------------|
| 1 | **Pipeline DAG Engine** (`engine/pipelines.py`) | zeus-memory task_dag_service, conductor templates | Medium | Parse YAML templates into DAG. Kahn's topological sort. Dispatch ready stages to session manager. Track stage completion. Handle dependencies. |
| 2 | **Phase Parser** (`engine/phases.py`) | conductor agents/architect.md output format | Low-Med | Parse structured markdown phase definitions (frontmatter + body). Validate required fields. Extract deliverables, constraints, acceptance criteria. |
| 3 | **Event System** | ccx queue architecture | Medium | In-process event queue. Events: session_started, session_output, session_complete, stage_complete, gate_passed, gate_failed, pipeline_complete. SSE endpoint for dashboard. |
| 4 | **Pipeline Dashboard Page** | eclipse_exp TaskBoard, conductor existing SPA | Medium | Kanban-style view: stages as columns, sessions as cards. Real-time via SSE. Card shows status, cost, runtime. Click → slide-in detail. |

### P1 — Context & Intelligence (makes Conductor smart)

| # | Item | Source | Effort | Description |
|---|------|--------|--------|-------------|
| 5 | **Context Manager** (`engine/context.py`) | ccx, zeus-memory, wiki patterns | Medium | Pluggable context assembly. Local sources (project files, prior outputs, git). Optional Zeus Memory and Wiki enrichment. Token-budgeted. |
| 6 | **Auto-Learn Pipeline** | ccx auto_learner, cce auto-learn hook | Medium | Post-pipeline hook: parse JSONL → Sonnet synthesis → store learnings (Zeus + local). Next run retrieves relevant learnings. |
| 7 | **Agent Dashboard** | cce agent-tui, eclipse_exp WebSocket | Low-Med | Grid view of active sessions. Name, model, status, tokens, cost, runtime. Live updates via SSE. |
| 8 | **Hot-Reload Agent/Template Definitions** | ccx skills hot-reload | Low | File watcher on agents/ and templates/. Re-index on change. No server restart needed. |
| 9 | **Agent Registry** (`engine/agents.py`) | conductor existing agent .md files | Low-Med | Load agent definitions from agents/. Index by name. Dispatch by role. Validate frontmatter (model, budget, max_turns). |

### P2 — Polish & Power (makes Conductor good)

| # | Item | Source | Effort | Description |
|---|------|--------|--------|-------------|
| 10 | **Quality Gate Evidence** | zeus-memory content classification, eclipse_exp tool audit | Low | Enrich gates with evidence (test output, review verdict, scan results). Store timestamp + reporting agent. |
| 11 | **Pipeline Resume** | original design | Medium | Resume failed pipeline from last successful stage. Re-use existing worktree. Skip completed stages. |
| 12 | **Wiki Context Source** | wiki | Low | Query wiki by project tags. Return relevant pages with frontmatter. Token-budgeted extraction. |
| 13 | **DAG Visualization** | zeus-memory task DAG, general | Medium | Render pipeline as directed graph. Color-coded nodes. Dependency edges. Critical path. |
| 14 | **Cost Circuit Breaker** | ccx budget patterns | Low | Pipeline-level budget tracking. Pause if cumulative cost exceeds threshold. Alert operator. |
| 15 | **Kanban Pipeline View** | eclipse_exp TaskBoard | Medium | Richer pipeline view with drag-drop stage ordering, manual gate override buttons, status filters. |
| 16 | **ADR Documentation** | ccx, zeus-memory ADR patterns | Low | Create docs/decisions/. ADR-001: DAG engine choice. ADR-002: State persistence model. ADR-003: Agent definition format. |

### P3 — Scale & Ecosystem (makes Conductor complete)

| # | Item | Source | Effort | Description |
|---|------|--------|--------|-------------|
| 17 | **MCP Server** | ccx MCP protocol | High | Expose pipeline state as MCP tools. Agents query on-demand. Full JSON-RPC implementation. |
| 18 | **Zeus Memory Deep Integration** | zeus-memory hybrid search | Medium | Beyond simple store/retrieve: use hybrid search with RRF for context retrieval. Content classification for build artifacts. |
| 19 | **Context Inspector** | original design | Medium | Debug panel showing assembled context per session: sources queried, results, truncations, token usage. |
| 20 | **Build Timeline** | original design | Medium | Horizontal timeline visualization. Pipeline stages as segments. Sessions as blocks. Color = outcome. |
| 21 | **Multi-Project Support** | conductor projects/ pattern, cce project templates | Medium | Project registry API. Per-project pipelines. Cross-project learnings via Zeus Memory. |
| 22 | **Deployment Verification** | observability health checks | Low | Post-deploy stage queries health endpoints. Reports status. Integrates with observability stack. |
| 23 | **Scaffolder** (`engine/scaffolder.py`) | conductor existing design | Medium | Project bootstrapping: create directory structure, git init, initial files, register in Conductor. |

---

## M. Recommended Next Implementation Prompt

The following prompt is designed to be given to a Conductor session (or Claude Code directly) to implement the P0 items. It assumes the current Phase 0 is complete and builds on the existing codebase.

---

### Prompt: Conductor Phase 1 — Pipeline DAG Engine + Event System + Dashboard

```
You are implementing Phase 1 of Conductor, the multi-agent product orchestrator.

Phase 0 is complete: session lifecycle management, worktree isolation, atomic JSON persistence, 
agent definitions, pipeline templates, and a basic SPA dashboard.

Phase 1 deliverables:

1. engine/pipelines.py — Pipeline DAG Engine
   - Parse YAML pipeline templates (see templates/pipelines/*.yaml)
   - Build directed acyclic graph from stage dependencies
   - Topological sort via Kahn's algorithm to determine execution order
   - Dispatch ready stages (no unmet dependencies) to engine/sessions.py
   - Track stage status: pending → running → complete | failed
   - Handle parallel dispatch: stages with independent dependencies run simultaneously
   - Pipeline state persisted in dashboard/data/pipelines.json (atomic writes)
   - API endpoints:
     POST /api/pipelines — create pipeline from template + project context
     GET  /api/pipelines/{id} — get pipeline status with stage details
     POST /api/pipelines/{id}/advance — manually advance past a gate stage
   - Gate stages: pause pipeline, wait for operator /advance or auto-advance if all quality gates pass

2. engine/phases.py — Phase Parser
   - Parse markdown phase definitions with YAML frontmatter
   - Required frontmatter: goal, deliverables (list), constraints (list), acceptance_criteria (list)
   - Optional: dependencies, boot_files, estimated_cost
   - Validate required fields, return structured dict
   - Used by pipeline engine to enrich stage prompts with phase context

3. Event System (in engine/server.py or new engine/events.py)
   - In-process event queue (asyncio.Queue or threading.Queue)
   - Event types: pipeline_created, stage_started, stage_complete, stage_failed, 
     gate_waiting, gate_advanced, pipeline_complete, pipeline_failed
   - SSE endpoint: GET /api/events — streams events to dashboard
   - Events carry: timestamp, pipeline_id, stage_name, session_id, metadata

4. Dashboard Pipeline View (dashboard/pages/pipeline.html)
   - Kanban layout: one column per pipeline stage
   - Session cards show: status icon, agent name, runtime, cost
   - Cards move between columns as stages progress
   - Gate stages show approval button
   - Real-time updates via SSE (EventSource in JS)
   - Fits within existing SPA shell (data-route pattern, window.ConductorData)

Constraints:
- Keep engine modules under 400 lines each
- Atomic writes for all state files
- No external dependencies beyond Python stdlib (match Phase 0 approach)
- Dashboard is vanilla HTML/CSS/JS (no frameworks)
- Agent definitions are read-only reference (agents/*.md)
- Pipeline templates are read-only reference (templates/pipelines/*.yaml)

Reference the existing codebase:
- engine/server.py for API routing pattern
- engine/sessions.py for state management pattern
- dashboard/index.html for SPA shell and routing
- templates/pipelines/standard-phase.yaml for template format
- agents/*.md for agent definition format

Test by creating a pipeline from the standard-phase template for the labs-institute project
and advancing it through plan → implement stages.
```

---

### What This Prompt Achieves

After executing this prompt, Conductor will have:
- A working pipeline engine that executes multi-stage DAGs
- Real-time dashboard showing pipeline progress
- Gate stages that pause for operator approval
- Parallel stage dispatch for independent stages
- Foundation for P1 items (context manager, auto-learn, agent registry)

### Subsequent Prompts (in order)

**Phase 1b — Context Manager + Agent Registry:**
Implement `engine/context.py` (pluggable context assembly with token budgets) and `engine/agents.py` (load and dispatch agents from agents/ directory).

**Phase 1c — Auto-Learn Pipeline:**
Post-pipeline hook that parses session outputs, synthesizes learnings via Sonnet, stores locally (and optionally in Zeus Memory).

**Phase 2 — Intelligence Layer:**
Zeus Memory integration, wiki context source, quality gate evidence, pipeline resume.

**Phase 3 — Scale:**
MCP server, multi-project support, scaffolder, deployment verification.
