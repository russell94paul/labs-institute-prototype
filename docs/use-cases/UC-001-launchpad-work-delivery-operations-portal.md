# UC-001 — Launchpad: Work Delivery & Operations Portal

**Type:** Pilot use-case / internal rebuild candidate
**Source repo:** `C:\Users\PaulRussell\repos\aldc-launchpad`
**Registered:** 2026-05-19
**Status:** Reference only — no code copied, no connections made

---

## Purpose

Register ALDC Launchpad as Conductor's first real pilot use-case. Launchpad is a partially built work/task delivery application that manages Claude Code sessions for Jira ticket work across ALDC's analytics operations. It serves as both a reference implementation (patterns Conductor should learn from) and the first internal rebuild/migration candidate (a real product Conductor will eventually manage).

## Why This Is the First Conductor Pilot

1. **Shared DNA** — Launchpad was built by the same developer (Paul) using the same patterns that Conductor generalizes: DAG pipelines, Claude Code session management, context enrichment, worktree isolation, specialized agents, stage scripts, and a vanilla HTML/JS SPA dashboard. Conductor's P0 Pipeline DAG Engine was directly informed by Launchpad's `scripts/pipelines.py`.

2. **Real operational load** — Launchpad manages real Jira tickets, real Prefect connector deployments, real Snowflake data landing, and real client credentials. It's not a toy — it's the daily operations tool for ALDC's analytics delivery.

3. **Known pain points** — Launchpad has scaling and maintenance issues that Conductor's architecture is designed to solve (see Pain Points below).

4. **Proof case** — If Conductor can absorb Launchpad's workflows and make them better, it validates the platform thesis for external clients.

5. **Minimal external risk** — This is an internal tool. Migration mistakes don't affect paying clients directly (as long as ticket delivery continues).

## Current Launchpad Capabilities

### Session Orchestrator (`scripts/orchestrator.py`)
- HTTP server on port 8765 serving the SPA + API
- Claude Code session management: launch, monitor, cancel
- `claude -p --output-format stream-json` subprocess management
- Up to 8 parallel sessions via ThreadPoolExecutor
- Budget and timeout enforcement per session
- Session output persistence as JSONL files
- Quality gates per session (compiles, tests_pass, requirements_met, no_security_issues)

### Pipeline DAG Engine (`scripts/pipelines.py`)
- 4 pipeline types: connector-migration (13 stages), prefect-infra (6), credential-provision (7), data-parity-test (5)
- 3 stage types: `claude-p` (AI session), `script` (Python callable), `gate` (manual or condition-polled)
- Dependency-driven dispatch: finds ready stages whose dependencies are all completed
- Shared worktree per pipeline: all stages stack commits in one branch
- Atomic JSON persistence

### Context Enrichment
- 6 data sources per session: tracker ticket, wiki page, related wiki pages, client registry, credential status, prior session learnings
- Ticket-to-client mapping (prefix dict: GP→GEP, FU92→F92, DV→DV)
- Wiki page following with `[[wikilink]]` resolution
- Character-limited context assembly (8000 chars ticket wiki, 3000 chars per related page)

### Worktree Isolation
- Per-pipeline worktrees in `.sessions/pipe_{ticket}_{id}/`
- Branch naming: `pipeline/{ticket}-{id}`
- Shared across all stages in a pipeline
- `--dangerously-skip-permissions` for write access

### Specialized Agents
- 5 agents: zeus-review, code-review, user-testing, deploy, refactor
- Short sessions (max 5 turns) with focused system prompts
- Context injection: pipeline state, session output, recent diffs

### Stage Scripts (`scripts/stage_scripts/`)
- Jira transitions and comments
- Prefect connector deployment and flow triggering
- Snowflake data verification and parity checks
- Condition gate polling (Docker image ready, branch merged)
- `ScriptContext`/`ScriptResult` dataclass contract

### Dashboard (`platform/master/`)
- Vanilla HTML/CSS/JS SPA, no build step
- 15+ pages: Hub, Orchestrator, Connectors, Credentials, Tracker, Client Boards, Onboarding Wizard, Platform Dashboard, Engineering, Prospects, Architecture, Roadmap, Vision
- Data preload: 7 parallel JSON fetches into `window.LaunchpadData`
- Orchestrator page: 3-panel layout (Ticket Inbox | Pipeline Detail | Zeus Chat + Agents)
- 3-second polling for session/pipeline status updates

### Additional Infrastructure
- Azure Functions for credential exchange, connector activation, portal auth
- CLI tools for multi-tenant provisioning (Snowflake, Zeus, Portal)
- Client registry (`shared/client-registry.json`) as the spine connecting all systems
- Connector submodule with 40+ Prefect v3 connectors
- Cube.js semantic layer, Apache Superset dashboards

## Target Future State

Launchpad's workflows should eventually run as Conductor-managed pipelines with:
- Conductor's Phase Template OS defining the pipeline templates
- Conductor's Agent Runtime dispatching the specialized agents
- Conductor's Context + Memory replacing the manual context assembly
- Conductor's Work Guard managing session safety instead of ad-hoc worktree creation
- Conductor's Event System providing real-time streaming instead of 3-second polling
- Conductor's Security Foundation handling credential references instead of direct Key Vault access

The Launchpad SPA itself may continue as a domain-specific frontend that reads from Conductor's APIs, or it may be replaced by Conductor's dashboard with domain-specific views.

## Current Pain Points

1. **Monolithic orchestrator** — `orchestrator.py` is server + session manager + API + context builder + pipeline bridge in one file. No separation of concerns.

2. **No persistent event stream** — Dashboard polls every 3 seconds. No SSE, no event history. (Conductor already solved this with P0-events.)

3. **Hardcoded pipeline types** — 4 pipeline types are defined inline in `pipelines.py`. No template system. (Conductor P3 addresses this.)

4. **No memory/learning loop** — Session learnings are stored as freetext in `sessions.json` but never evaluated, promoted, or quarantined. (Conductor P5 and P13 address this.)

5. **Credential handling is inline** — Stage scripts load credentials directly from Key Vault or fallback JSON. No broker abstraction. (Conductor P7/P9 addresses this via DEC-002.)

6. **No multi-tenancy** — Everything runs as Paul's local user. No tenant isolation. (Conductor P7 addresses this.)

7. **Fragile wiki integration** — Context enrichment reads wiki pages by path convention. No fallback if wiki structure changes. (Conductor P5 context packs address this.)

8. **No rollback automation** — Pipeline failures require manual cleanup. No automatic worktree cleanup on failure.

9. **Agent definitions are inline dicts** — Not externalized or parameterized. (Conductor P4 uses markdown agent definitions.)

10. **No quality gate automation** — Session quality gates exist but are never auto-populated. (Conductor P13 addresses this.)

## Rebuild vs. Refactor Framing

See `UC-001-launchpad-rebuild-vs-refactor-framework.md` for detailed analysis. The recommended approach is **strangler migration** — progressively route Launchpad workflows through Conductor's engine while keeping Launchpad operational, then retire Launchpad components as Conductor subsumes them.

## Workflows to Support

### Jira/Ticket Work
- Ticket intake from Jira (status, priority, assignee, blocked_by)
- Pipeline creation from ticket (select template, configure stages)
- Session launch with enriched prompt (ticket context, wiki, registry)
- Status transitions back to Jira on stage completion
- Structured comments on Jira tickets with pipeline results

### Prefect Connector Setup
- Connector analysis (read source code, understand schema)
- Flow file creation and local testing
- Docker image build verification (condition gate)
- Prefect deployment creation
- Flow run triggering and monitoring
- Data landing verification in Snowflake

### API/Service Setup
- Client environment provisioning (Snowflake DB, schemas, RBAC, service accounts)
- Credential link generation and submission tracking
- Key Vault provisioning and Prefect Block creation

### Client Artifact Requests
- Credential submission via secure token-based link
- Document/report generation from pipeline results
- Data health reporting and parity verification

### Approval Gates
- Manual gates for code review, merge review, promotion decisions
- Condition gates for automated checks (Docker image, branch merge)
- Quality gates per session (compiles, tests, requirements, security)

### Session/Pipeline Tracking
- Real-time session status, cost, token usage
- Pipeline DAG visualization with stage status
- Session output viewing (JSONL log)
- Historical pipeline/session browsing

### Deployment/Verification Tasks
- Connector promotion (development → UAT → production)
- Data parity testing (compare old vs. new pipeline output)
- Smoke testing and validation

## Security Boundaries

### What Conductor MUST NOT ingest from Launchpad
- Azure Key Vault credentials or secrets
- `scripts/stage_env.json` (local credential fallback)
- `shared/client-registry.json` (contains client contacts, Snowflake configs, Prefect blocks)
- `platform/master/data/credentials.json` (credential status records)
- `platform/master/data/onboardings/*.json` (client onboarding data)
- `api/credential-exchange/` service code (handles real credentials)
- `api/portal-auth/` service code (handles real auth tokens)
- Any `.env` files or Azure connection strings
- Any client data, tracker data, or prospect data

### What Conductor MAY reference as patterns
- Architecture patterns from `scripts/orchestrator.py` and `scripts/pipelines.py`
- UX patterns from `platform/master/pages/orchestrator/index.html`
- Agent definition patterns (system prompts, capability matching)
- Stage script contract (`ScriptContext`/`ScriptResult`)
- Context enrichment strategy (data sources, assembly order, character limits)
- Worktree isolation strategy (per-pipeline shared worktree, branch naming)
- Pipeline type definitions (stage sequences, dependencies, gate types)
- SPA shell patterns (data preload, routing, page development contract)

## How This Maps to Conductor Phases

See `UC-001-conductor-phase-mapping.md` for the detailed mapping. Summary:

| Conductor Phase | Launchpad Pattern |
|---|---|
| P3 Phase Template OS | Pipeline type definitions → formal templates |
| P4 Agent Runtime | Inline agent dicts → markdown agent definitions + worktree engine |
| P5 Context + Memory | 6-source context enrichment → governed context packs + memory ledger |
| P7 Security Foundation | Inline credential loading → broker abstraction + tenant isolation |
| P8 Client Portal | Client portal SPA → Conductor-managed portal with RLS |
| P10 Data Modernization | Connector migration pipeline → formal modernization workflow |
| P12 Infrastructure/Deploy | Manual deploy → automated staging/promote/rollback |
| P13 Self-Improvement | Unused learnings field → evaluation + promotion loop |
