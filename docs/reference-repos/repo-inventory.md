# A. Repository Inventory

> Inspected 2026-05-18. All repos under `C:\Users\PaulRussell\repos\`.

## Tier 1 — Direct Relevance to Conductor

| Repo | Purpose | Tech Stack | Status |
|------|---------|------------|--------|
| **conductor** | Multi-agent product orchestrator (this repo) | Python, vanilla HTML/CSS/JS | Phase 0 complete; Phases 1-3 planned |
| **ccx** | Agent sidecar — MCP server, team messaging, auto-learning, presence | Python 3.12, FastAPI, Docker, MCP JSON-RPC | Production; 391 tests |
| **zeus-memory** | Persistent semantic memory — hybrid search, RBAC, multi-tenant, 3.6M+ memories | Python 3.11, FastAPI, asyncpg, pgvector, Voyage AI | Production; 50+ test modules |
| **claude_code_enhanced** | Enhanced Claude Code — 356 skills, 27 tools, lifecycle hooks, project templates | Bash/Python, Claude Code hooks | Production; predecessor to CCX |
| **wiki** | LLM knowledge base — 399 pages, cross-linked, daily ingest pipeline | Markdown (Obsidian-compatible) | Active; 50+ ingest operations |

## Tier 2 — Partial Relevance (Patterns / Reference)

| Repo | Purpose | Tech Stack | Relevance |
|------|---------|------------|-----------|
| **eclipse_exp** | Enterprise analytics platform — AI chat, task boards, roadmaps, connectors | Next.js 16, FastAPI, PostgreSQL RLS | UI patterns, chat engine, task board |
| **observability** | Monitoring stack — synthetic probes, Prometheus, Grafana, Slack alerts | Docker, Python, Uptime Kuma, Grafana | Post-deploy monitoring patterns |
| **core_api** | Core business API — Cosmos DB, RBAC, JWT | FastAPI, Cosmos DB | RBAC patterns, API conventions |
| **workflows** | Azure Functions event processor — timer triggers, data sync | Python, Azure Functions, Cosmos DB | Automation/cron patterns |

## Tier 3 — Low / No Relevance

| Repo | Purpose | Why Low |
|------|---------|---------|
| **atlas** | Internal admin Next.js app | Generic CRUD; no orchestration patterns |
| **zeus-chat-exp** | Experimental chat app | Early-stage; no stable patterns yet |
| **dispatcher** | Azure queue processor | Minimal code; Azure-specific |
| **portal** | Legacy Django admin dashboard | Template-based; superseded by eclipse_exp |
| **flight-check** | Client media management app | Domain-specific (Fusion92); no reusable patterns |
| **clients** | Per-client Eclipse configs + Snowflake SQL | Data warehouse config; not relevant |
| **connector** | Eclipse connector runtime | Docker-based ETL; not relevant |
| **concept-***, **prospect-site-template**, etc. | Client demos, prototypes | No reusable orchestration patterns |

## B. Capability Summary per Repo

### conductor (this repo)
- Session lifecycle management (create, run, cancel, delete)
- Claude Code subprocess dispatch with worktree isolation
- Atomic JSON state persistence
- Template-driven prompt system (6 templates)
- Agent definitions with YAML frontmatter (architect, implementer, reviewer, tester, deployer)
- Pipeline templates (YAML DAG definitions)
- Quality gates per session (compiles, tests_pass, requirements_met, no_security_issues)
- SPA dashboard with client-side routing
- **Not yet implemented:** pipeline DAG engine, phase parser, project API, agent registry

### ccx
- MCP server (15 tools) for Claude Code on-demand feature pull
- Event-driven queue architecture (fast/slow handler separation)
- Team messaging (inbox, send, presence heartbeats)
- Auto-learning via Sonnet 4.6 server-side (zero user context cost)
- Hot-reload skills via Docker volume + inotify
- Per-session multi-tenant isolation (ADR-005)
- Dead-letter queue for failed writes
- 10 lifecycle hooks (fire-and-forget HTTP)
- Secret scrubbing on all outbound data

### zeus-memory
- Hybrid search: BM25 (25%) + pgvector semantic (60%) + entity/graph (15%) with RRF
- Cross-encoder reranking (Voyage Rerank-2.5)
- 9 ingestion pipelines (email, Slack, QBO, HubSpot, Graph Teams, Nextcloud, web, Avoma, API specs)
- Multi-tenant RLS with hierarchy-aware access grants
- RBAC (20 permissions, role authority matrix)
- OAuth 2.0 (authz code + PKCE + client credentials)
- Task management with DAG dependencies (Kahn's topological sort)
- Content classification: origin × sensitivity × intent (3D)
- Entity extraction (NERD) + LLM profile synthesis
- 16 ADRs documenting architecture decisions

### claude_code_enhanced
- 356 reusable skill files across 55+ categories
- 30+ command skills (learn, msg, journal, deploy-watch, discover-skills)
- 21 lifecycle hooks (session start/stop, auto-learn, presence)
- 27 Python tools (multi-agent orchestrator, parallel executor, agent TUI, QA suite)
- Project template pattern (YYYY-MM-DD naming, PROGRESS.md, status.json)
- Auto-learn virtuous cycle (session → tool log → Sonnet synthesis → Zeus Memory → next session)
- Model routing (Opus/Sonnet/Haiku per task type)

### wiki
- 399 Markdown pages with YAML frontmatter + bidirectional wikilinks
- 7 directory categories (entities, concepts, processes, tickets, daily, workplan, standup)
- Automated daily notes ingest (type-tagged notes → wiki page updates)
- Action item extraction (explicit + heuristic)
- Lint operation (orphan pages, stale info, missing cross-refs)
- Append-only log.md audit trail
- 14 clients, 12 repos, 20+ tools, 40+ tickets documented

### eclipse_exp
- AI chat with Claude + SSE streaming + intent classification + tool orchestration
- Task board (Kanban + WebSocket real-time updates)
- Roadmap / feature catalog / strategic map views
- 50+ data connectors with self-service onboarding
- Profitability engine (QBO + Power BI labour cost)
- 70+ RLS-protected database migrations
- Mantine UI component library
- structlog JSON logging + OpenTelemetry tracing
