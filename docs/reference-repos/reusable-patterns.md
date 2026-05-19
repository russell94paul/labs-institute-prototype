# D. Reusable Architecture Patterns + E. Reusable UI/Workflow Patterns

## Architecture Patterns

### 1. Sidecar MCP Architecture (from ccx)
**Pattern:** Docker sidecar exposes features via MCP JSON-RPC. Thin hooks POST events; sidecar processes async; Claude pulls on-demand via MCP tools.
**Why it matters:** 97% context reduction vs wrapper approach. Conductor could expose pipeline state, agent status, and memory as MCP tools that agents pull when needed rather than injecting into every prompt.
**Applicability:** High — Conductor's agents are Claude Code sessions. MCP is native.

### 2. Event Queue with Fast/Slow Handler Split (from ccx)
**Pattern:** Input queue receives all events. Fast handlers run inline (<50ms). Slow handlers spawn background tasks. Output queue batches writes to external services.
**Why it matters:** Conductor manages parallel sessions. Events (session started, stage complete, gate passed, review needed) need fast dispatch without blocking.
**Applicability:** High — replace Conductor's polling model with event-driven updates.

### 3. Hybrid Search with RRF (from zeus-memory)
**Pattern:** Three signals — BM25 keyword (25%), pgvector semantic (60%), entity/graph (15%) — fused via Reciprocal Rank Fusion, optionally reranked by cross-encoder.
**Why it matters:** Conductor's context retrieval (lessons learned, prior builds, similar projects) needs quality search over heterogeneous content.
**Applicability:** Medium — adopt when Conductor has enough stored context to justify search infra.

### 4. Content Classification 3D (from zeus-memory)
**Pattern:** Every piece of content classified on three independent dimensions: origin (authoritative/ai_generated/user_contributed/system), sensitivity (public/internal/confidential/restricted), intent (reference/operational/personal_note/system_internal).
**Why it matters:** Conductor stores build outputs, agent decisions, user requirements, and system logs. Classification determines what to surface, what to protect, and what to expire.
**Applicability:** Medium — implement when Conductor manages cross-project knowledge.

### 5. Task DAG with Kahn's Algorithm (from zeus-memory)
**Pattern:** Tasks stored with dependency edges. Topological sort via Kahn's algorithm determines execution order. Unblocked tasks are parallelizable.
**Why it matters:** Conductor's pipeline stages are a DAG. This is exactly what `pipelines.py` needs.
**Applicability:** High — direct implementation target for Phase 2.

### 6. Atomic State + Dead Letter Queue (from ccx, conductor)
**Pattern:** State written to .tmp then renamed (atomic). Failed writes go to dead_letters.jsonl with retry metadata. Operator recovers later.
**Why it matters:** Conductor already uses atomic writes. Adding dead-letter for failed session outputs, pipeline state transitions prevents silent data loss.
**Applicability:** High — extend existing pattern.

### 7. Per-Session Isolation via Key Binding (from ccx)
**Pattern:** Each MCP session binds user_id + tenant_id + api_key at creation. All downstream calls use per-session credentials, never global fallback.
**Why it matters:** Conductor sessions run in worktrees. Extending isolation to API keys prevents cross-project credential leakage as Conductor scales.
**Applicability:** Medium — needed when Conductor serves multiple users/projects.

### 8. Auto-Learn Virtuous Cycle (from ccx, cce)
**Pattern:** Session ends → tool log parsed → Sonnet synthesizes learnings (failures, successes, decisions) → stored in Zeus Memory → next session retrieves relevant learnings.
**Why it matters:** Conductor builds get better over time. Each pipeline run should capture what worked, what failed, and what was learned. Next run retrieves relevant history.
**Applicability:** High — core differentiator for autonomous delivery.

### 9. Agent Definitions as Markdown + YAML Frontmatter (from conductor, cce)
**Pattern:** Agent = markdown file with YAML frontmatter (name, model, budget, max_turns) + body (system prompt). Loaded at runtime, no code changes needed.
**Why it matters:** Already in Conductor. Validate this is the right long-term format by comparing with CCE's 356-skill library.
**Applicability:** Already implemented — refine and extend.

### 10. Multi-Tenant RLS (from zeus-memory, eclipse_exp)
**Pattern:** PostgreSQL Row-Level Security with SET LOCAL GUC injection per connection. Every tenant-scoped query wrapped in tenant_connection() context manager.
**Why it matters:** Relevant if Conductor ever serves multiple teams/orgs. Not needed for single-user local operation.
**Applicability:** Low (now) — revisit if Conductor becomes multi-tenant.

### 11. ADR Documentation (from ccx, zeus-memory)
**Pattern:** Numbered Architecture Decision Records in `docs/decisions/`. Each ADR: context, decision, consequences, status (accepted/superseded).
**Why it matters:** Conductor is making foundational architecture choices now. Documenting them prevents re-litigation and helps future contributors understand why.
**Applicability:** High — start ADR-001 now.

---

## UI/Workflow Patterns

### 1. Kanban Task Board with WebSocket Updates (from eclipse_exp)
**Pattern:** Multi-column Kanban board. REST API for mutations, WebSocket broadcasts for real-time multi-user updates. Task cards show priority badge, assignee, due date, dependency graph.
**Why it matters:** Conductor's pipeline view needs exactly this — stages as columns, sessions as cards, real-time status updates.
**Applicability:** High — reference architecture for Conductor's pipeline/board view.

### 2. AI Chat with Tool Result Classification (from eclipse_exp)
**Pattern:** SSE-streamed chat. Each tool result classified by tool name → routed to specialized renderer (table, metrics, task list, sources). Pluggable view components.
**Why it matters:** Conductor needs a chat/command interface for interacting with agents. The classifier pattern prevents monolithic rendering.
**Applicability:** Medium — useful if Conductor adds an interactive agent chat panel.

### 3. Agent TUI Dashboard (from claude_code_enhanced)
**Pattern:** Terminal UI rendering agent cards with token counts, duration, status. Live-updating during multi-agent parallel sessions.
**Why it matters:** Conductor dispatches parallel sessions. A dashboard view (web or terminal) showing all active agents is essential.
**Applicability:** High — translate TUI concept to web dashboard.

### 4. Intent Classification Before LLM (from eclipse_exp)
**Pattern:** Deterministic keyword routing classifies user intent before calling Claude. Reduces LLM calls and cost by routing known patterns to specific tools.
**Why it matters:** Conductor's agent dispatch could use intent classification to route tasks to the right agent without LLM overhead.
**Applicability:** Medium — useful for the agent registry (Phase 3).

### 5. Project Template with Mandatory Structure (from claude_code_enhanced)
**Pattern:** Every project follows: README.md + PROGRESS.md + status.json. Enforced at creation, updated each session. Archive workflow moves to storage.
**Why it matters:** Conductor's `projects/` directory already has a project.json pattern. Standardizing with PROGRESS.md and status tracking improves observability.
**Applicability:** High — extend existing project pattern.

### 6. Slide-In Detail Panel (from conductor)
**Pattern:** Click a card → slide-in overlay panel shows detail view. No full page navigation. Breadcrumb auto-generated.
**Why it matters:** Already in Conductor. Good pattern for session detail, pipeline stage detail, review findings.
**Applicability:** Already implemented — extend to new views.

### 7. Daily Notes Ingest Pipeline (from wiki)
**Pattern:** Handwritten notes in daily/ with type tags → automated distribution to wiki pages → action item extraction → index update.
**Why it matters:** Conductor could use a similar pattern for build logs: each pipeline run produces notes → automated extraction of learnings, failures, decisions → stored as build memory.
**Applicability:** Medium — adapt for build log processing.

### 8. Hot-Reload Skills via File Watch (from ccx)
**Pattern:** Skills directory mounted as Docker volume. inotify watches for file changes, triggers re-index. No container restart needed.
**Why it matters:** Conductor's agent definitions and pipeline templates should be hot-reloadable. Adding/modifying an agent shouldn't require server restart.
**Applicability:** High — implement for agents/ and templates/ directories.
