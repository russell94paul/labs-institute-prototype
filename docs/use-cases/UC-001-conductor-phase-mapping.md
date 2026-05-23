# UC-001 — Conductor Phase Mapping

**Use case:** UC-001 ALDC Launchpad
**Date:** 2026-05-19
**Status:** Reference mapping only — no implementation

---

## Phase-by-Phase Mapping

### P3 — Phase Template OS + Execution Queue

**Launchpad patterns that inform P3:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| 4 hardcoded pipeline types in `pipelines.py` | YAML template files in `templates/` | Connector-migration, prefect-infra, credential-provision, data-parity-test become templates |
| 3 stage types (claude-p, script, gate) | Template schema stage types | P3 must support all three from day 1 — validated by Launchpad |
| `ScriptContext`/`ScriptResult` dataclasses | Formalized stage execution contract | Clean pattern — adopt directly |
| `prior_results` dict passed to each stage | Stage result forwarding in template schema | Enables data flow between stages |
| Condition gate with `poll_interval_sec` + `max_wait_min` | Gate definition in template schema | First-class gate types, not afterthoughts |
| `auto_advance=True` per stage | Auto-advance flag in template schema | Some stages should auto-dispatch downstream, some should gate |

**Launchpad pipeline types as candidate Conductor templates:**
1. `connector-migration.yaml` — 13-stage connector migration workflow
2. `prefect-infra.yaml` — 6-stage Prefect infrastructure setup
3. `credential-provision.yaml` — 7-stage credential provisioning
4. `data-parity-test.yaml` — 5-stage data parity validation

These are ALDC-domain templates. Conductor should create them as examples that validate the template schema, not as built-in features.

**Decisions that must be approved:** DEC-003 (worktree isolation), DEC-004 (event store)

---

### P4 — Agent Runtime + Parallel Worktree Execution

**Launchpad patterns that inform P4:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| 5 inline agent dicts in `orchestrator.py` | Markdown agent definitions in `agents/` | Externalize, parameterize, version control |
| Per-pipeline shared worktree in `.sessions/` | Per-pipeline worktree mode in `engine/worktrees.py` | Conductor should also support per-task worktrees (DEC-003) |
| Branch naming `pipeline/{ticket}-{id}` | Branch naming `conductor/{project}/{run_id}/task-{task_id}` | Conductor's naming is already better |
| Agent quick-launch buttons in orchestrator UI | Agent dispatch UI in dashboard | 5 focused agents with one-click launch — UX pattern to adopt |
| `--dangerously-skip-permissions` | `--permission-mode auto` with allowlists | Do NOT adopt Launchpad's permission model |
| Max 8 parallel sessions via ThreadPoolExecutor | Concurrency from work-guard policy | Conductor's approach is more configurable |
| Pipeline-aware session completion callback | Already in P0 pipeline engine | Validates the approach |

**Launchpad agents as candidate Conductor agent definitions:**
1. `agents/zeus-review.md` — operational intelligence
2. `agents/code-review.md` — structured code review
3. `agents/user-testing.md` — QA flight check
4. `agents/deploy.md` — deployment runbook
5. `agents/refactor.md` — code quality analysis

**Decisions that must be approved:** DEC-003 (worktree isolation)

---

### P5 — Context + Memory Core MVP

**Launchpad patterns that inform P5:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| 6-source context enrichment in `_build_context()` | Context pack assembly in `engine/context.py` | Generalize the multi-source pattern |
| Character budgets (8000 primary, 3000 per related) | Context budget system | Prevents blowup — adopt |
| Wikilink following for related context | Memory/context linking | Cheap knowledge graph — wikilinks as edges |
| Ticket-to-client prefix mapping | Configurable context routing rules | Generalize beyond ticket prefixes |
| Prior session learnings (stored but unused) | Memory candidate lifecycle | Learnings become memory candidates with evaluation |
| Credential status (not values) in context | Credential status references in context packs | Never values — pattern validated by Launchpad |

**Context sources Conductor should support (generalized from Launchpad):**
1. Work item context (Launchpad: tracker ticket)
2. Knowledge base context (Launchpad: wiki pages + wikilinks)
3. Organization context (Launchpad: client registry minus contacts)
4. Resource status context (Launchpad: credential status)
5. Prior session learnings (Launchpad: learnings field)
6. Pipeline state context (Launchpad: current pipeline + prior stage results)

**Decisions that must be approved:** DEC-005 (vector store), DEC-006 (wiki role), DEC-007 (memory provider), DEC-008 (memory store MVP)

---

### P6 — Research/Decision Hub

**Launchpad patterns that inform P6:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| `data/tracker.json` (ticket records) | Research topic + decision records | Launchpad tracks tickets; Conductor tracks research and decisions |
| Tracker page with filter chips | Research hub with topic/decision filters | Similar UX pattern |

P6 is lightweight and doesn't draw heavily from Launchpad. The main connection is that the research/decision corpus (DEC-001-010, Topics 01-08) already exceeds what a static markdown file can manage — Launchpad's tracker page validates the need for a dynamic hub.

---

### P7 — Multi-Tenant Security Foundation

**Launchpad patterns that inform P7 (mostly as anti-patterns):**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| Inline credential loading from Key Vault | Broker abstraction (DEC-002) | **Anti-pattern** — Conductor must not load real credentials |
| `scripts/stage_env.json` fallback | Config-based dev secrets (never in engine) | **Anti-pattern** — no credential JSON files |
| No tenant isolation | Tenant → Org → Workspace → Project hierarchy | **Gap** — Conductor must add what Launchpad lacks |
| `shared/client-registry.json` as spine | Tenant registry with RLS | Generalize the single-source pattern with proper isolation |
| Portal user auth (Azure Function) | Principal types with scoped access | Launchpad has portal auth but no RLS |

**Decisions that must be approved:** DEC-001 (tenancy model), DEC-002 (secrets management)
**Research required:** Topic 06 (Secure Credentials — pending)

---

### P8 — Client Product Portal

**Launchpad patterns that inform P8:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| `platform/portal/` client SPA | Conductor client portal page | Launchpad has a working client portal — learn from its page structure |
| Credential submission form (`connect/submit.html`) | Client artifact submission flow | Secure token-based submission — good pattern |
| Per-client analytics dashboard (via Superset) | Client-scoped dashboard views | Launchpad embeds Superset; Conductor should use native views |
| Portal-safe data filtering | RLS + `portal_safe`/`client_visible` flags | Launchpad does this informally; Conductor should enforce via RLS |
| Client boards (Navira, Fusion92) | Per-tenant workspace views | Launchpad has per-client pages with tabs |

**Research required:** Topic 03 (AI Onboarding — pending)

---

### P9 — Trust-Aware Discovery & Access Manager

No direct Launchpad equivalent. Launchpad's credential exchange (HMAC token → Key Vault → Prefect Block) is a rudimentary version of Level 3 access, but it's not progressive and doesn't have the trust framework described in Conductor's architecture.

Launchpad's `credential-exchange` Azure Function pattern is a reference for how the vault flow could work, but it should not be copied (it uses Azure-specific APIs).

---

### P10 — Data Platform Modernization Studio

**Launchpad patterns that inform P10:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| `connector-migration` pipeline (13 stages) | Modernization workflow template | The most complex Launchpad pipeline — direct proof case |
| Connector framework (40+ connectors) | Connector registry pattern | Conductor doesn't build connectors but manages their lifecycle |
| `data-parity-test` pipeline (5 stages) | Parity validation workflow template | Essential for migration confidence |
| Snowflake data verification stage scripts | Verification stage type in template schema | Launchpad validates the pattern |
| Migration catalog (`migrations/connectors/catalog.json`) | Migration tracking in modernization studio | Track migration state per connector/source |
| Branch promotion model (feature → dev → uat → main) | Environment promotion in deploy workflow | Well-tested promotion path |

**Research required:** Topic 04 (Data Platform Modernization — pending)
**Blocker:** Service inventory (Blocker #2)

---

### P12 — Infrastructure / Deploy / Ops + Sandbox Execution

**Launchpad patterns that inform P12:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| Azure Bicep IaC in `infra/` | IaC placeholder templates | Pattern of infra-as-code, not the specific implementation |
| `api/connector-activation/` provisioning | Automated environment provisioning | Snowflake DB + schemas + RBAC + service account — pattern to generalize |
| Docker image build + deploy pipeline | Container build + deploy workflow | Launchpad's condition gate for Docker image readiness is a good pattern |
| Branch promotion (dev → uat → main) | Environment promotion with approval gates | Add smoke tests and rollback |
| No rollback automation | Automated rollback on failure | **Gap** — Conductor must add what Launchpad lacks |

---

### P13 — Self-Improvement Loop

**Launchpad patterns that inform P13:**

| Launchpad Component | Conductor Equivalent | Notes |
|---|---|---|
| `learnings` field on sessions (stored, never evaluated) | Memory candidate → evaluation → promotion | Launchpad captures learnings but doesn't use them — Conductor completes the loop |
| `quality_gates` per session (never auto-populated) | Automated quality gate population | Launchpad defines the gates; Conductor automates them |
| Agent results (side-channel, no feedback loop) | Agent result → evaluation → memory | Close the loop |

**Decisions that must be approved:** DEC-009 (memory extraction trigger), DEC-010 (evaluation harness MVP)

---

## Summary: What Each Phase Gets from Launchpad

| Phase | Patterns Adopted | Anti-Patterns Avoided | Research Gap |
|---|---|---|---|
| P3 | Mixed-type DAG, ScriptContext/Result, gate polling, 4 template candidates | Hardcoded pipeline defs | None |
| P4 | Shared worktree, agent definitions, quick-launch UX, completion callback | Inline agents, skip-permissions | None |
| P5 | 6-source enrichment, char budgets, wikilink following, session learnings | None | None |
| P6 | Tracker page UX pattern | None | None |
| P7 | Client registry as spine | Inline credentials, no isolation | Topic 06 |
| P8 | Client portal structure, credential submission | None | Topic 03 |
| P10 | Connector migration pipeline, parity testing, promotion model | None | Topic 04 |
| P12 | IaC pattern, provisioning, Docker build gate | No rollback | None |
| P13 | Learnings field, quality gates | Unused learnings, no evaluation | None |
