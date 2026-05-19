# I. Integration Opportunities

## Direct Integrations (build into Conductor)

### 1. Zeus Memory as Build Memory Backend
**Source:** zeus-memory
**What:** Store and retrieve build context — learnings, failures, decisions, prior outputs — via Zeus Memory API.
**How:** HTTP client in `engine/context.py` calling Zeus search/store endpoints. Per-project tenant isolation via API key.
**Value:** Every pipeline run accumulates knowledge. Future runs query relevant history before planning. The hybrid search (BM25 + semantic + entity) returns high-quality context.
**Effort:** Medium (HTTP client + context enrichment logic)
**Dependencies:** Zeus API key, network access to zeus.aldc.io
**Risk:** External dependency; must work offline (graceful degradation with local fallback)

### 2. CCX MCP Protocol for Agent Communication
**Source:** ccx
**What:** Expose Conductor's pipeline state, session status, and quality gates as MCP tools. Agents query Conductor on-demand rather than having state injected.
**How:** MCP server endpoint in `engine/server.py`. Define tools: `get_pipeline_status`, `get_session_output`, `report_quality_gates`, `get_prior_learnings`.
**Value:** Agents pull only what they need. Eliminates context bloat. Aligns with CCX's proven sidecar pattern.
**Effort:** Medium-High (MCP server implementation + tool definitions)
**Dependencies:** MCP protocol library
**Risk:** Protocol complexity; must handle session lifecycle correctly

### 3. Auto-Learn Pipeline (Session → Learnings → Memory)
**Source:** ccx + cce
**What:** After each session/pipeline completes, parse tool log → synthesize learnings via Sonnet → store in Zeus Memory → retrieve for next run.
**How:** Post-session hook in `engine/sessions.py`. Parse JSONL output. Call Claude Sonnet for synthesis. Store via Zeus API.
**Value:** Conductor gets smarter with every build. Critical path failures never repeat. Known patterns accelerated.
**Effort:** Medium (output parsing + synthesis prompt + storage)
**Dependencies:** Anthropic API key (for Sonnet synthesis), Zeus Memory access

### 4. Wiki as Project Context Source
**Source:** wiki
**What:** Before planning a new project/phase, query the wiki for relevant pages (client rules, architecture decisions, deployment runbooks).
**How:** `engine/context.py` reads wiki directory, searches by wikilinks/tags, extracts relevant sections.
**Value:** Conductor agents start with institutional knowledge rather than inferring from code alone.
**Effort:** Low (file read + frontmatter parsing + tag matching)
**Dependencies:** Wiki directory accessible from Conductor's runtime
**Risk:** Wiki pages can be stale; must surface freshness metadata

### 5. Task DAG Engine (Kahn's Algorithm)
**Source:** zeus-memory (task_dag_service.py)
**What:** Implement `engine/pipelines.py` using Kahn's topological sort for stage ordering. Stages with satisfied dependencies run in parallel.
**How:** Port DAG logic. Each pipeline stage = node; dependencies = edges. Ready stages dispatched to session manager.
**Value:** Core Phase 2 deliverable. Enables multi-stage pipeline execution with proper ordering.
**Effort:** Medium (DAG logic + integration with session dispatcher)
**Dependencies:** None (pure algorithm)
**Risk:** Low — well-understood algorithm

---

## Pattern Extraction (adopt concepts, write fresh code)

### 6. Event-Driven Session Updates
**Source:** ccx (queue architecture)
**What:** Replace polling with event queue. Session state changes emit events. Dashboard subscribes via SSE or WebSocket.
**How:** In-process asyncio queue in engine. Events: session_started, session_output, session_complete, gate_passed, gate_failed. SSE endpoint for dashboard.
**Value:** Real-time dashboard updates. No polling lag. Foundation for notifications.
**Effort:** Medium (event system + SSE endpoint + dashboard JS)

### 7. Hot-Reload Agent/Template Definitions
**Source:** ccx (skills hot-reload via watchfiles)
**What:** Watch `agents/` and `templates/` directories. Re-index on file change without server restart.
**How:** watchfiles or similar file watcher in engine startup. Reload agent registry and template registry on change.
**Value:** Iterate on agent definitions without restarting server during development.
**Effort:** Low

### 8. Quality Gate Enforcement Pattern
**Source:** zeus-memory (content classification), eclipse_exp (tool audit)
**What:** Extend Conductor's quality gates with structured evidence. Each gate records: status, evidence (test output, review findings), timestamp, agent who reported it.
**How:** Enrich `quality_gates` dict with evidence fields. Gate transitions logged as events.
**Value:** Auditable gate decisions. Can replay why a gate passed/failed.
**Effort:** Low

### 9. Kanban Pipeline View
**Source:** eclipse_exp (TaskBoard)
**What:** Pipeline stages as Kanban columns. Sessions as cards within stages. Real-time movement as sessions complete.
**How:** New dashboard page `pages/pipeline.html`. Columns = stages (plan, implement, test, review, deploy). Cards = sessions with status badges.
**Value:** Visual pipeline progress. Immediate identification of blocked stages.
**Effort:** Medium (HTML/CSS/JS — no framework needed given Conductor's vanilla approach)

### 10. Agent Dashboard with Live Status
**Source:** cce (agent TUI), eclipse_exp (task board WebSocket)
**What:** Dashboard panel showing all active agents: name, model, token usage, runtime, current status, cost accumulation.
**How:** New dashboard page or panel. Polls /api/sessions for active sessions. Renders card per agent.
**Value:** Operator visibility into multi-agent execution. Essential when running 8 parallel sessions.
**Effort:** Low-Medium

---

## Context Sources (read-only integration)

### 11. Observability Stack Reference
**Source:** observability
**What:** After deploy, Conductor queries health endpoints and monitoring dashboards for deployment verification.
**How:** Post-deploy stage in pipeline template that hits health check URLs and reports status.
**Value:** Automated deployment verification closes the loop on deploy stages.
**Effort:** Low (HTTP health checks in deploy agent prompt)

### 12. ADR Pattern for Conductor Decisions
**Source:** ccx (6 ADRs), zeus-memory (16 ADRs)
**What:** Start documenting Conductor's architecture decisions in `docs/decisions/` using the ADR format.
**How:** Create ADR template. Document: DAG choice, state persistence model, agent format, MCP vs injection.
**Value:** Prevents re-litigation of decisions. Onboards future contributors faster.
**Effort:** Low (documentation only)

---

## Integration Priority Matrix

| # | Integration | Value | Effort | Priority |
|---|-------------|-------|--------|----------|
| 5 | Task DAG Engine | High | Medium | **P0 — Next** |
| 6 | Event-Driven Updates | High | Medium | **P0 — Next** |
| 7 | Hot-Reload Definitions | Medium | Low | **P1** |
| 3 | Auto-Learn Pipeline | High | Medium | **P1** |
| 1 | Zeus Memory Backend | High | Medium | **P1** |
| 10 | Agent Dashboard | High | Low-Med | **P1** |
| 9 | Kanban Pipeline View | Medium | Medium | **P2** |
| 8 | Quality Gate Evidence | Medium | Low | **P2** |
| 4 | Wiki Context Source | Medium | Low | **P2** |
| 2 | MCP Protocol | High | Med-High | **P2** |
| 12 | ADR Documentation | Low | Low | **P2** |
| 11 | Observability Checks | Low | Low | **P3** |
