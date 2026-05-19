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
│   ├── agents.py           # Agent registry + dispatch
│   ├── context.py          # Pluggable context enrichment
│   ├── events.py           # Event system + SSE pub/sub
│   ├── scaffolder.py       # Project bootstrapping
│   └── stage_scripts/      # Pipeline automation scripts
├── dashboard/              # Vanilla HTML/CSS/JS SPA
│   ├── index.html          # SPA shell
│   ├── styles/base.css     # Design system
│   └── pages/              # Per-page HTML files
├── templates/              # Pipeline + stack templates
├── agents/                 # Agent definitions (.md files)
├── projects/               # Active project configs
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

## Data Layer

All state persisted as JSON in `dashboard/data/`:
- `sessions.json` — session state + config
- `pipelines.json` — pipeline state
- `projects.json` — project registry
- `data/sessions/` — per-session JSONL output files

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
