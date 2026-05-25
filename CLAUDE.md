# Conductor — Product Orchestrator

General-purpose app/product orchestrator that manages the full lifecycle: requirements → phases → pipelines → code → review → deploy. Extracted from patterns proven in aldc-launchpad and neurospect orchestrators.

## Architecture

```
conductor/
├── engine/                 # Python backend
│   ├── server.py           # HTTP server + API routing
│   ├── sessions.py         # Claude Code session lifecycle
│   ├── pipelines.py        # DAG pipeline engine (YAML-driven)
│   ├── phases.py           # Phase manager (markdown-driven)
│   ├── memory.py           # Per-project memory store (zeus-memory patterns)
│   ├── agents.py           # Agent registry + dispatch
│   ├── context.py          # Pluggable context enrichment
│   ├── events.py           # Event system + SSE pub/sub
│   ├── scaffolder.py       # Project bootstrapping
│   ├── onboarding.py       # AI chat onboarding (Claude API or CLI)
│   └── stage_scripts/      # Pipeline automation scripts
├── dashboard/              # Vanilla HTML/CSS/JS SPA
│   ├── index.html          # SPA shell
│   ├── styles/base.css     # Design system
│   └── pages/              # Per-page HTML files
├── templates/              # Pipeline + stack templates
├── agents/                 # Agent definitions (.md files)
├── projects/               # Per-project configs, wikis, memory stores
│   ├── <slug>/project.json # Project registry + phase definitions
│   ├── <slug>/wiki/        # Per-project wiki (decisions, learnings, patterns)
│   ├── <slug>/memory/      # Per-project memory ledger (zeus-memory lite)
│   └── wiki-template/      # Wiki conventions template
└── shared/prompts/         # Reusable prompt fragments
```

## Running

```bash
python engine/server.py
# Serves on http://127.0.0.1:8888
```

## API

### Sessions
- `GET    /api/sessions` — list all sessions
- `POST   /api/sessions` — create + launch a session
- `GET    /api/sessions/{id}` — get session details
- `GET    /api/sessions/{id}/output` — get session output (JSONL)
- `PATCH  /api/sessions/{id}` — update quality gates / learnings
- `POST   /api/sessions/{id}/cancel` — cancel a running session
- `DELETE /api/sessions/{id}` — delete session + cleanup

### Projects (Phase 1)
- `GET    /api/projects` — list projects
- `POST   /api/projects` — create project
- `GET    /api/projects/{slug}` — get project details

### Pipelines (Phase 2)
- `GET    /api/pipelines` — list pipelines
- `POST   /api/pipelines` — create + start pipeline
- `GET    /api/pipelines/{id}` — get pipeline details
- `POST   /api/pipelines/{id}/advance` — advance past a gate

### Events
- `GET    /api/events` — event history (query: `limit`, `type`, `since`)
- `GET    /api/events/stream` — SSE stream (real-time events)
- `GET    /api/events/stats` — event system statistics

### Agents (Phase 3)
- `GET    /api/agents` — list available agents
- `POST   /api/agents/run` — run an agent

### Memory (per-project, zeus-memory lite)
- `GET    /api/projects/{slug}/memory` — list memories (query: `type`, `status`, `limit`, `offset`)
- `POST   /api/projects/{slug}/memory` — store a memory
- `POST   /api/projects/{slug}/memory/store` — store a memory (alias)
- `POST   /api/projects/{slug}/memory/search` — keyword search memories
- `GET    /api/projects/{slug}/memory/{id}` — recall a memory + evidence
- `PATCH  /api/projects/{slug}/memory/{id}` — update a memory
- `POST   /api/projects/{slug}/memory/{id}/evidence` — link evidence to a memory
- `GET    /api/projects/{slug}/memory/stats` — memory store statistics

### Onboarding (AI chat)
- `POST   /api/onboarding/chat` — send message, get Claude response (creates session if no session_id)
- `GET    /api/onboarding/{session_id}` — get conversation state + blueprint
- `POST   /api/onboarding/{session_id}/create` — create project from finalized blueprint

### GrooveNet (project-specific)
- `GET    /api/groovenet/events` — list events
- `POST   /api/groovenet/events` — create event
- `GET    /api/groovenet/sets` — list DJ sets
- `POST   /api/groovenet/sets` — log a DJ set
- `GET    /api/groovenet/profile` — get DJ profile
- `PUT    /api/groovenet/profile` — update DJ profile

## Data Layer

All state persisted as JSON:
- `dashboard/data/sessions.json` — session state + config
- `dashboard/data/pipelines.json` — pipeline state
- `dashboard/data/projects.json` — project registry
- `dashboard/data/sessions/` — per-session JSONL output files
- `projects/<slug>/memory/memories.json` — per-project memory ledger
- `projects/<slug>/memory/evidence.json` — memory evidence links
- `projects/<slug>/memory/retrieval_log.json` — retrieval audit trail
- `dashboard/data/onboarding-sessions.json` — AI onboarding chat sessions

## Key Patterns

- **Atomic writes**: state files written to `.tmp` then renamed
- **Binary pipe reading**: `bufsize=0` for Windows subprocess compatibility
- **Shared pipeline worktrees**: all stages in a pipeline share one git worktree
- **Quality gates**: `{compiles, tests_pass, requirements_met, no_security_issues}` per session
- **Phase definitions**: structured markdown with frontmatter (goal, deliverables, constraints, acceptance criteria)
- **Pipeline templates**: YAML files defining stage sequences with dependencies

## Conventions

- No comments unless the WHY is non-obvious
- No docstrings longer than one line
- Engine modules are kept under 400 lines each
- Dashboard pages are self-contained HTML files that read from `window.ConductorData`
- Agent definitions are markdown files with YAML frontmatter
