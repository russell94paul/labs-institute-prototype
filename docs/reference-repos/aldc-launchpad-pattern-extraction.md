# ALDC Launchpad — Pattern Extraction

**Source repo:** `C:\Users\PaulRussell\repos\aldc-launchpad`
**Date:** 2026-05-19
**Status:** Reference analysis only — no code copied

---

## Reusable Patterns to Extract

### 1. Pipeline DAG with Mixed Stage Types

**Pattern:** A single pipeline engine that dispatches three distinct stage types — AI sessions (`claude-p`), Python callables (`script`), and human/automated gates (`gate`) — all sharing the same dependency graph.

**Why it's reusable:** Most orchestration tools handle only one stage type. Launchpad's mixed-type DAG is Conductor's core value proposition: pipelines where AI, code, and humans collaborate through the same dependency graph.

**Adoption phase:** P3 Phase Template OS (template schema must support all three stage types)

### 2. Shared Worktree Per Pipeline

**Pattern:** All stages in a pipeline share one git worktree. Stage 1's commits are visible to Stage 2. The branch naming convention `pipeline/{ticket}-{id}` makes it traceable.

**Why it's reusable:** This is more practical than per-stage worktrees for sequential workflows. Each stage builds on the previous one's work. Conductor's P4 should support both per-task and per-pipeline worktree modes.

**Adoption phase:** P4 Agent Runtime (worktree isolation model)

**Caveat:** Shared worktrees break down with parallel stages that write to the same files. Conductor needs the merge queue from DEC-003 for parallel cases.

### 3. ScriptContext / ScriptResult Contract

**Pattern:** Stage scripts receive a `ScriptContext` dataclass (pipeline_id, stage_name, ticket_id, client_code, environment, params, prior_results, worktree_path) and return a `ScriptResult` (success, data, error, summary). Prior stage results are passed forward as a dict.

**Why it's reusable:** Clean, testable contract. Scripts don't need to know about the orchestrator. The `prior_results` dict enables data flow between stages without coupling.

**Adoption phase:** P3 Phase Template OS (formalize the stage execution contract)

### 4. Context Enrichment from Multiple Sources

**Pattern:** Before launching any AI session, the orchestrator assembles context from 6 sources: tracker ticket, wiki page, related wiki pages (via wikilink following), client registry, credential status, and prior session learnings. Each source has a character limit.

**Why it's reusable:** The multi-source assembly pattern is exactly what Conductor's context packs should do. The character budgeting prevents context blowup.

**Adoption phase:** P5 Context + Memory Core MVP (context pack assembly)

### 5. Agent Quick-Launch UX

**Pattern:** The orchestrator dashboard has 5 agent buttons in a side panel. Each shows a focused form (pipeline/session selector, optional notes), launches a short claude -p session (max 5 turns), and displays results inline.

**Why it's reusable:** Quick-launch agents are a killer UX pattern — one-click access to specialized AI capabilities without leaving the current workflow.

**Adoption phase:** P4 Agent Runtime (agent dispatch + UI)

### 6. Condition Gate Polling

**Pattern:** Condition gates poll a check function (e.g., `check_docker_image` via GitHub Actions API, `check_branch_merged` via `gh` CLI) every N seconds until success or timeout. The gate advances the pipeline automatically on success.

**Why it's reusable:** Many workflows need to wait for external systems. The poll-with-timeout pattern is universal.

**Adoption phase:** P3 Phase Template OS (gate types in template schema)

### 7. Atomic JSON Persistence

**Pattern:** All state files are written to `.tmp` first, then atomically renamed. This prevents corruption from process crashes during writes.

**Why it's reusable:** Already adopted by Conductor (same pattern in `engine/pipelines.py`). Validates the approach.

**Adoption phase:** Already adopted (P0)

### 8. SPA Data Preload

**Pattern:** On load, the SPA shell fires parallel `fetch()` calls for all JSON data files, populates `window.LaunchpadData`, and all pages read from this global. Pages also have a standalone `fetch()` fallback for direct-access.

**Why it's reusable:** Already adopted by Conductor as `window.ConductorData`. Validates the approach.

**Adoption phase:** Already adopted (00-bootstrap)

### 9. Pipeline-Aware Session Completion

**Pattern:** When a session completes, `_pipeline_advance_after_session()` calls `pipeline_engine.on_session_complete()` which finds and dispatches the next ready stages. This is the glue between the session lifecycle and the DAG engine.

**Why it's reusable:** Conductor's pipeline engine already has this pattern. Launchpad validates that the callback-on-completion approach works in practice.

**Adoption phase:** Already adopted (P0)

### 10. Ticket-to-Client Mapping

**Pattern:** A simple prefix dict maps ticket prefixes to client codes: `GP→GEP`, `FU92→F92`, `DV→DV`. This enables automatic context loading for any ticket.

**Why it's reusable:** The pattern of mapping work items to organizational context is universal. Conductor should generalize this as a configurable mapping in the context engine.

**Adoption phase:** P5 Context + Memory (context routing rules)

---

## Patterns to Avoid

### 1. Monolithic Server File

**What Launchpad does:** `orchestrator.py` is HTTP server + session manager + API routes + context builder + pipeline bridge + agent definitions in one file.

**Why to avoid:** Conductor already has proper separation (server.py, sessions.py, pipelines.py, events.py, work_guard.py). Don't collapse back into a monolith.

### 2. Inline Agent Definitions

**What Launchpad does:** Agents are Python dicts with system prompts hardcoded in `orchestrator.py`.

**Why to avoid:** Conductor should use externalized markdown agent definitions (already planned for P4). Inline dicts can't be edited without modifying engine code.

### 3. Direct Credential Loading

**What Launchpad does:** `stage_scripts/credentials.py` loads directly from Azure Key Vault on server start, populates `os.environ`, and all scripts inherit credentials.

**Why to avoid:** This is the opposite of Conductor's DEC-002 broker abstraction. Credentials should be references, not values. Conductor must never load real credentials into memory.

### 4. Polling-Based Dashboard Updates

**What Launchpad does:** The dashboard polls `GET /api/sessions` and `GET /api/pipelines` every 3 seconds.

**Why to avoid:** Conductor already has SSE via P0-events. Polling is wasteful and introduces latency.

### 5. Hardcoded Pipeline Definitions

**What Launchpad does:** 4 pipeline types are defined as Python dicts in `pipelines.py`. Adding a new type requires editing engine code.

**Why to avoid:** Conductor P3 uses YAML templates. Pipeline definitions should be data, not code.

### 6. `--dangerously-skip-permissions` for All Worktree Sessions

**What Launchpad does:** All pipeline sessions in worktrees get `--dangerously-skip-permissions`.

**Why to avoid:** This bypasses Claude Code's safety model entirely. Conductor should use `--permission-mode auto` with explicit allowlists per agent type.

### 7. `seed_phase0()` — Hardcoded Ticket Bootstrapping

**What Launchpad does:** A function creates pipelines for 4 specific Jira ticket IDs.

**Why to avoid:** Pipeline creation should be data-driven, not hardcoded. This is a one-off hack.

---

## Architecture Lessons

1. **Separation of session lifecycle from pipeline lifecycle works.** Launchpad proves that having sessions as the execution unit and pipelines as the orchestration unit is sound. Conductor's architecture mirrors this correctly.

2. **JSON file persistence is fine for single-user MVP.** Launchpad runs entirely on JSON files and it works. Conductor should resist premature Postgres migration (aligns with DEC-008 recommendation for minimal MVP).

3. **The data preload SPA pattern scales to 15+ pages.** Launchpad has 15+ dashboard pages all reading from `window.LaunchpadData`. No build step, no framework. Conductor's vanilla JS SPA approach is validated.

4. **Context enrichment quality determines session quality.** The best pipeline engineering doesn't help if the AI session gets bad context. Launchpad's 6-source enrichment is the minimum viable set.

5. **Mixed stage types in one DAG is essential.** Real workflows interleave AI work, automated scripts, and human approvals. A DAG engine that only supports one type is incomplete.

---

## UI/UX Lessons

1. **3-panel orchestrator layout is effective.** Ticket inbox (left) + pipeline detail (center) + chat/agents (right) gives operators everything they need without switching pages.

2. **Agent quick-launch buttons with minimal forms reduce friction.** One click to run a focused agent. No need to compose prompts manually.

3. **Pipeline DAG visualization needs stage-level detail.** Showing the DAG as a list of stage cards with status dots, session links, and action buttons is more useful than a pure graph visualization.

4. **Stats ticker bar (live session count, total cost) builds trust.** Operators want to see the system is working and what it costs.

5. **Session output viewer needs line-level navigation.** JSONL output can be thousands of lines. Launchpad's log viewer with scroll-to-end and search would improve Conductor's session detail.

---

## Orchestration Lessons

1. **Pipeline-session completion callback is the right coupling point.** Not polling, not events-only — a direct callback from session completion to pipeline advancement. Conductor already does this.

2. **Shared worktree per pipeline beats per-stage worktree for sequential workflows.** Each stage sees prior stages' commits. But this fails for parallel stages — Conductor needs both modes.

3. **Gate types should be first-class citizens, not afterthoughts.** Manual gates and condition gates are used in every Launchpad pipeline. They're not optional.

4. **Prior stage results should flow forward as structured data.** Launchpad's `prior_results` dict is simple and effective. Each stage can access what prior stages produced.

---

## Stage Script Lessons

1. **The ScriptContext/ScriptResult contract is clean and testable.** Adopt it in Conductor's template schema.

2. **Scripts should be idempotent where possible.** Jira transition scripts handle "already in target status" gracefully. Credential provisioning is idempotent.

3. **Non-blocking failure is sometimes correct.** Jira comment failures don't block the pipeline. Not all stage failures should be fatal.

4. **Environment-specific params belong in the pipeline, not the script.** Scripts receive environment via `ScriptContext.environment`, not from hardcoded values.

---

## Context Enrichment Lessons

1. **Character budgets prevent context blowup.** 8000 chars for the primary wiki page, 3000 for each related page, top 5 links only. Without limits, context can exceed model capacity.

2. **Wikilink following is a cheap knowledge graph.** Following `[[wikilinks]]` from a ticket page into concept/pattern pages provides surprisingly good context. Conductor's memory engine should support this.

3. **Credential status, not credential values.** Context includes "credential status: submitted, validated, provisioned" — never the actual values. This is the correct pattern for Conductor.

4. **Prior session learnings are underutilized gold.** Launchpad stores learnings but never evaluates or promotes them. Conductor P5/P13 should build the learning loop that Launchpad didn't.

---

## Agent Runtime Lessons

1. **Short sessions (max 5 turns) keep agents focused.** Long sessions drift. A 5-turn review agent produces better results than a 50-turn general-purpose agent.

2. **Agents need pipeline and session context.** The code-review agent needs to see the diff. The deploy agent needs to see the pipeline state. Context injection is per-agent, not one-size-fits-all.

3. **Agent results should feed back into the pipeline.** Currently they don't in Launchpad — agents run as side-channel tools. In Conductor, agent results should advance the DAG.

---

## Risks of Over-Coupling

1. **Launchpad is ALDC-specific.** Its pipeline types, client registry, Jira integration, and Prefect connector framework are domain-specific. Conductor should extract the patterns, not the implementations.

2. **Launchpad's data layer is not Conductor's data layer.** `shared/client-registry.json`, `data/tracker.json`, `data/credentials.json` are Launchpad-specific. Conductor should define its own data schemas.

3. **Copying code creates maintenance burden.** If Conductor copies Launchpad code, changes in one don't propagate to the other. Extract patterns and reimplement.

4. **Launchpad's security model is inappropriate for Conductor.** `--dangerously-skip-permissions`, inline credential loading, no tenant isolation. Conductor must not inherit these shortcuts.

---

## Recommended Adoption Phase for Each Pattern

| Pattern | Conductor Phase | Priority |
|---|---|---|
| Mixed-type DAG (claude-p, script, gate) | P3 Phase Template OS | High — core capability |
| ScriptContext/ScriptResult contract | P3 Phase Template OS | High — stage execution contract |
| Condition gate polling | P3 Phase Template OS | High — gate types in template schema |
| Shared worktree per pipeline | P4 Agent Runtime | High — worktree isolation model |
| Agent quick-launch UX | P4 Agent Runtime | Medium — UX pattern |
| Externalized agent definitions | P4 Agent Runtime | High — already planned |
| Multi-source context assembly | P5 Context + Memory | High — context pack design |
| Character-budgeted context | P5 Context + Memory | High — prevents blowup |
| Wikilink-following enrichment | P5 Context + Memory | Medium — cheap knowledge graph |
| Prior session learnings → memory | P5 Context + Memory / P13 Self-Improvement | Medium — learning loop |
| Ticket-to-client context mapping | P5 Context + Memory | Medium — configurable routing |
| 3-panel orchestrator layout | P4 or P6 (dashboard) | Low — UX reference |
| Stats ticker bar | P4 (dashboard) | Low — UX reference |
| Atomic JSON persistence | Already adopted (P0) | Done |
| SPA data preload | Already adopted (00-bootstrap) | Done |
| Pipeline-session completion callback | Already adopted (P0) | Done |
