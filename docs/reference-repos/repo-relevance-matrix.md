# C. Relevance Matrix

Scores: 1 (irrelevant) to 10 (essential). Scored against Conductor's mission: autonomous multi-agent delivery console.

| Repo | Context/Memory | Product Building | UI/UX | Engineering | Overall | Action |
|------|---------------|-----------------|-------|-------------|---------|--------|
| **ccx** | 9 | 8 | 3 | 9 | **9** | Integrate |
| **zeus-memory** | 10 | 6 | 2 | 8 | **8** | Integrate |
| **wiki** | 8 | 4 | 1 | 3 | **6** | Context source |
| **claude_code_enhanced** | 7 | 7 | 5 | 6 | **7** | Extract patterns |
| **eclipse_exp** | 3 | 5 | 9 | 7 | **6** | Extract patterns |
| **observability** | 2 | 3 | 2 | 7 | **4** | Reference only |
| **core_api** | 1 | 2 | 1 | 5 | **3** | Reference only |
| **workflows** | 1 | 3 | 1 | 4 | **2** | Reference only |
| **atlas** | 1 | 1 | 2 | 2 | **1** | Ignore |
| **zeus-chat-exp** | 2 | 1 | 2 | 1 | **1** | Ignore |
| **dispatcher** | 1 | 1 | 1 | 2 | **1** | Ignore |
| **portal** | 1 | 1 | 1 | 1 | **1** | Ignore |
| **flight-check** | 1 | 1 | 2 | 3 | **1** | Ignore |

## Dimension Breakdown

### Context/Memory (weight: high)
| Repo | Score | Rationale |
|------|-------|-----------|
| zeus-memory | 10 | Production semantic search, hybrid retrieval, content classification, entity extraction |
| ccx | 9 | MCP memory tools, auto-learning, session context, team memory |
| wiki | 8 | 399 cross-linked knowledge pages, daily ingest pipeline, structured query |
| claude_code_enhanced | 7 | Skills library, project templates, tool-use logging for learning |
| eclipse_exp | 3 | Chat history, semantic catalog — but domain-specific |

### Product Building Intelligence (weight: high)
| Repo | Score | Rationale |
|------|-------|-----------|
| ccx | 8 | Task management, project lifecycle, skill system, multi-agent coordination |
| claude_code_enhanced | 7 | Multi-agent orchestrator, model routing, QA suite, project templates |
| zeus-memory | 6 | Task DAG (Kahn's algorithm), work classifier, agent cost tracking |
| eclipse_exp | 5 | Chat intent routing, tool orchestration, onboarding wizard |
| wiki | 4 | Ticket tracking, process runbooks — but static/manual |

### UI/UX (weight: medium)
| Repo | Score | Rationale |
|------|-------|-----------|
| eclipse_exp | 9 | Kanban, roadmap, feature catalog, AI chat, pipeline views, Mantine patterns |
| claude_code_enhanced | 5 | Agent TUI (terminal dashboard for multi-agent sessions) |
| ccx | 3 | Status line, but no visual UI |
| others | 1-2 | No transferable UI patterns |

### Engineering Practices (weight: medium)
| Repo | Score | Rationale |
|------|-------|-----------|
| ccx | 9 | 391 tests, 6 ADRs, mutation testing, Semgrep, secret scanning, fail-open design |
| zeus-memory | 8 | 16 ADRs, RLS, content security (injection detection), CI/CD with staging PR DBs |
| eclipse_exp | 7 | 3,800+ backend tests, OpenTelemetry, rate limiting, structlog |
| observability | 7 | Full monitoring stack, but narrow scope |
| claude_code_enhanced | 6 | Hook-based automation, QA tools, but less formal testing |
| core_api | 5 | JWT/RBAC patterns, but Cosmos DB specific |

## Recommended Actions Summary

| Action | Repos |
|--------|-------|
| **Integrate** | ccx, zeus-memory |
| **Extract patterns** | claude_code_enhanced, eclipse_exp |
| **Context source** | wiki |
| **Reference only** | observability, core_api, workflows |
| **Ignore** | atlas, zeus-chat-exp, dispatcher, portal, flight-check, clients, connector, concept-*, etc. |
