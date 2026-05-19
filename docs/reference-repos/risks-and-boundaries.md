# J. Risks and Boundaries + K. What Not to Integrate

## Risks

### 1. Over-coupling to Zeus Memory
**Risk:** Making Zeus Memory a hard dependency kills Conductor's portability. If Zeus is down, no builds run.
**Mitigation:** Zeus Memory should be an optional context enrichment layer. Conductor must function fully with local-only state (JSON files). Memory integration via a pluggable `ContextProvider` interface — Zeus is one provider; local file search is another.

### 2. MCP Protocol Complexity
**Risk:** Implementing a full MCP server adds protocol surface area, session management, and JSON-RPC handling that may not be justified at Conductor's current scale.
**Mitigation:** Defer MCP server until Conductor has 3+ concurrent agents that need to query pipeline state. In the interim, agents get context via prompt templates (already working).

### 3. Premature Multi-Tenancy
**Risk:** Zeus-memory and CCX have sophisticated multi-tenant isolation (RLS, per-session keys, tenant hierarchies). Copying this into Conductor before it serves multiple users adds complexity for zero benefit.
**Mitigation:** Conductor is single-user/local-first. Do not add tenant isolation, RBAC, or key binding until there's a concrete multi-user requirement.

### 4. Context Bloat from Wiki Integration
**Risk:** The wiki has 399 pages. Naively injecting wiki content into agent prompts wastes tokens and may confuse agents with irrelevant context.
**Mitigation:** Wiki queries must be scoped — match by project tags, client name, or explicit wikilinks. Return summaries, not full pages. Set hard token budgets per context injection.

### 5. Auto-Learn Noise
**Risk:** The auto-learn cycle (ccx/cce pattern) can store low-quality learnings if the synthesis prompt isn't well-tuned. Noisy memory degrades future retrieval quality.
**Mitigation:** Quality gates on learnings: require structured format (failure/success/decision + evidence). Review first N sessions' learnings manually before trusting the pipeline.

### 6. Agent Definition Drift
**Risk:** Conductor's agent .md files, CCE's 356 skills, and CCX's MCP tools all define agent behavior differently. Mixing formats creates confusion about which definition is authoritative.
**Mitigation:** Conductor's agent format (YAML frontmatter + markdown body) is the canonical format. CCE skills are reference material, not runtime definitions. Do not import CCE skills into Conductor's agents/ directory.

### 7. External Service Availability
**Risk:** Zeus Memory, Anthropic API, and GitHub are external dependencies. Network issues or rate limits can stall pipeline execution.
**Mitigation:** Implement timeouts + circuit breakers on all external calls. Sessions should degrade gracefully (log warning, skip enrichment, continue with local context).

### 8. Cost Accumulation
**Risk:** Auto-learning uses Sonnet per session. Context enrichment adds API calls. Running 8 parallel sessions with Zeus queries could accumulate significant cost.
**Mitigation:** Budget tracking already exists per session. Add aggregate pipeline budget. Auto-learn should be configurable (on/off, model choice, frequency).

---

## Boundaries — What NOT to Integrate

### Do Not Import

| Source | What | Why Not |
|--------|------|---------|
| zeus-memory | RLS/multi-tenancy | Conductor is single-user. No tenant isolation needed. |
| zeus-memory | OAuth 2.0 / JWT auth | Conductor runs on localhost. No auth needed. |
| zeus-memory | 9 ingestion pipelines | Domain-specific (email, Slack, QBO). Not relevant to building software. |
| zeus-memory | Profitability engine | Business-specific. Not relevant to orchestration. |
| ccx | Docker sidecar deployment | Conductor runs as a simple Python server. Docker sidecar adds unnecessary complexity. |
| ccx | Team messaging/presence | Conductor has one operator. No team coordination needed (yet). |
| ccx | Secret scrubbing | Conductor doesn't transmit tool logs externally. Add if auto-learn is enabled. |
| cce | 356 skill files | Domain-specific to ALDC development patterns. Conductor needs its own agent definitions. |
| cce | 21 lifecycle hooks | CCE hooks are specific to Claude Code wrapper mode. Conductor has its own session lifecycle. |
| cce | Poller daemon | Replaced by CCX sidecar. Legacy pattern. |
| eclipse_exp | Next.js frontend | Conductor uses vanilla HTML/JS SPA. Adding Next.js is a full rewrite. |
| eclipse_exp | Mantine UI library | Framework dependency for a vanilla SPA. |
| eclipse_exp | PostgreSQL + asyncpg | Conductor uses JSON file persistence. DB is premature. |
| eclipse_exp | Supervisor + co-process model | Conductor is a single Python process. No need for process management. |
| observability | Uptime Kuma / Prometheus / Grafana stack | Full monitoring stack for 6 apps. Overkill for Conductor. |
| core_api | Cosmos DB patterns | Wrong database. Conductor uses files. |
| portal | Django admin | Legacy. Superseded. |
| flight-check | NextAuth + Eclipse 2 auth | Domain-specific client auth. |
| workflows | Azure Functions | Azure-specific serverless. Conductor is a long-running server. |

### Do Not Copy Code Directly

Even from high-relevance repos, do not copy-paste code:

1. **zeus-memory's hybrid_search_service.py** — 400+ lines of asyncpg queries. Conductor doesn't use PostgreSQL. Extract the algorithm (RRF weighting, signal combination), implement against Conductor's storage.

2. **ccx's queue.py** — Tightly coupled to CCX's event model. Conductor needs its own event types. Adopt the fast/slow handler split pattern, implement fresh.

3. **ccx's auto_learner.py** — References CCX-specific tool trace format, secret scrubbing patterns, and Zeus client. Build Conductor's own learning pipeline that reads its own session output format.

4. **eclipse_exp's TaskBoard components** — React/Next.js/TypeScript. Conductor is vanilla JS. Reference the UX design (columns, cards, badges), implement in plain HTML/CSS/JS.

5. **cce's multi_agent_orchestrator.py** — 13 task types and 7 agent roles specific to ALDC development. Conductor has its own agent model (architect, implementer, reviewer, tester, deployer). Don't merge taxonomies.

### Patterns to Avoid

| Pattern | Source | Why Avoid |
|---------|--------|-----------|
| Bash wrapper approach | cce | Proven inferior to sidecar (ccx). Don't replicate. |
| Global mutable state dict | zeus-memory (VALID_API_KEYS) | Caused bugs (ADR-005). Use immutable config or per-request lookup. |
| ILIKE on large datasets | zeus-memory (ADR-003) | Performance trap. Use structured search if Conductor's state grows. |
| Import-time initialization | core_api | 48-container DB bootstrap on import. Lazy initialization is safer. |
| Co-process supervisor | eclipse_exp | Unnecessary complexity for single-process server. |
| Feature flags / backwards-compat shims | any | Conductor is pre-1.0. Change code directly. |
