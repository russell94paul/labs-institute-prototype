# Change Manifest

## DEC-003 and DEC-004 Approval for P3 (2026-05-19)

### Files Modified

**docs/research/decisions/**
- `DEC-003-worktree-isolation-model.md` — Status changed from Proposed to Approved (2026-05-19); added approval notes
- `DEC-004-event-store-technology.md` — Status changed from Proposed to Approved (2026-05-19); added current state section and approval notes

**docs/build/**
- `decision-review-summary.md` — Updated summary matrix: DEC-003 and DEC-004 marked Approved
- `approval-requests.md` — #7 updated to Partial (DEC-003/004 approved, rest pending); #10 updated (decision gate cleared); added #11 and #12 to Approved table
- `blockers.md` — Blocker #4 (DEC-003/004 not approved) moved to Resolved; 3 open blockers remain
- `change-manifest.md` — Added this section
- `session-handoffs/dec-003-004-approved-for-p3-handoff.md` — Session handoff

**config/**
- `phase-status.json` — P3 decisionGating updated to reflect approvals; nextRecommendedAction updated to "Start P3"

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No secrets/env files read or modified
- P3 remains status: not_started
- DEC-001, DEC-002, DEC-005–DEC-010 unchanged (pending/deferred/proposed)

---

## UC-001 Launchpad Pilot Registration (2026-05-19)

### Files Created

**docs/use-cases/**
- `UC-001-launchpad-work-delivery-operations-portal.md` — Pilot use-case registration: purpose, capabilities, pain points, workflows, security boundaries, phase mapping
- `UC-001-launchpad-rebuild-vs-refactor-framework.md` — 5 migration strategies compared (incremental refactor, module extraction, strangler migration, full rebuild, domain pack) with pros/cons/risk/timeline
- `UC-001-conductor-phase-mapping.md` — Launchpad patterns mapped to Conductor phases P3-P13 with specific adoption recommendations per phase

**docs/reference-repos/**
- `aldc-launchpad-pattern-extraction.md` — 10 reusable patterns, 7 anti-patterns, architecture/UX/orchestration/stage-script/context/agent lessons, adoption phase recommendations

**docs/build/**
- `session-handoffs/uc-001-launchpad-pilot-handoff.md` — Session handoff

### Files Modified

- `docs/build/change-manifest.md` — Added this section

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No Launchpad code copied into Conductor
- No secrets/env files read or modified
- No client data, credentials, or registry data added
- UC-001 registered as reference/pilot only

---

## P3+ Roadmap Planning (2026-05-19)

### Files Created

**docs/prompts/**
- `P3-phase-template-os-execution-queue.md` — P3 build prompt: phase template schema, execution queue, phase runner UI
- `P4-agent-runtime-parallel-worktree.md` — P4 build prompt: agent registry, dispatch, worktree isolation, merge queue
- `P5-context-memory-core-mvp.md` — P5 build prompt: memory ledger, context retrieval, project context packs

**docs/build/**
- `p3-plus-roadmap-planning-report.md` — Full roadmap planning report: 13 phases, decision mapping, research mapping, dependency graph, parallelization
- `session-handoffs/p3-plus-roadmap-handoff.md` — Session handoff

### Files Modified

- `config/phase-status.json` — Added 13 new phases (P3-P15), all status: not_started; existing 10 completed phases preserved unchanged
- `docs/build/blockers.md` — Added Blocker #4 (DEC-003/004 approval), updated Affects column for existing blockers
- `docs/build/approval-requests.md` — Added #10 (P3 Phase Template OS start)
- `docs/build/parallelization-status.md` — Updated for full P3+ parallelization analysis
- `docs/build/change-manifest.md` — Added this section

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No secrets/env files read or modified
- All 10 existing completed phases preserved unchanged in phase-status.json
- All 13 new phases set to not_started
- config/phase-status.json is valid JSON

---

## P2 Product Onboarding Studio (2026-05-19)

### Files Created

**dashboard/pages/**
- `onboarding-studio.html` — Product Onboarding Studio: 6 tabbed views (Start, Intake, Features, Simulator, Scenarios, Summary), 3 onboarding paths, 11-section intake form, 30-feature selection matrix, 6 dynamic sliders, 3 recommendation cards, scenario save/compare with radar chart, JSON export

**docs/build/**
- `p2-product-onboarding-studio-build-report.md` — P2 build report
- `rollback/p2-product-onboarding-studio-rollback.md` — Rollback plan
- `session-handoffs/p2-product-onboarding-studio-handoff.md` — Session handoff

### Files Modified

- `dashboard/index.html` — Added "Onboarding" nav link + route entry in SPA router
- `config/phase-status.json` — Marked P2-onboarding as completed, cleared blockedBy, updated reportPath/branchName/lastUpdated
- `docs/build/change-manifest.md` — Added this section
- `docs/build/blockers.md` — Updated (no changes to open blockers)
- `docs/build/approval-requests.md` — Added P2 approval to approved
- `docs/build/parallelization-status.md` — Updated for post-P2 state

### Constraints Verified

- No engine code modified
- No new Python dependencies
- No secrets/env files read or modified
- Build Studio still fully functional
- Bootstrap Console still fully functional
- All existing API endpoints unchanged
- No raw research reports tracked
- No real credentials collected or stored

---

## Local Dev Startup Utility + Skill (2026-05-19)

### Files Created

**scripts/**
- `start-conductor.ps1` — Start local Conductor server (checks if running, finds python, starts engine/server.py)
- `check-conductor.ps1` — Check if server is responding on port 8888 (exit 0/1)
- `stop-conductor.ps1` — Find and stop process on port 8888 with confirmation prompt

**.claude/skills/conductor-serve/**
- `SKILL.md` — Claude Code skill: start or verify the local Conductor UI server

**docs/architecture/**
- `local-dev-startup.md` — How to start/check/stop Conductor locally, troubleshooting

### Files Modified

- `docs/build/change-manifest.md` — Added this section

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No config JSON modified
- No secrets/env files read or modified

---

## P1 Build Studio MVP (2026-05-19)

### Files Created

**dashboard/pages/**
- `build-studio.html` — Build Studio MVP: 10 tabbed views (Overview, Roadmap, Dependencies, Work Queue, Approvals, Blockers, Events, Work Guard, Reports, Changes), SSE live event feed, decision queue (DEC-001–010), build progress tracking, phase detail overlay

**docs/build/**
- `p1-build-studio-build-report.md` — P1 build report
- `rollback/p1-build-studio-rollback.md` — Rollback plan
- `session-handoffs/p1-build-studio-handoff.md` — Session handoff

### Files Modified

- `dashboard/index.html` — Added "Build Studio" nav link + route entry in SPA router
- `config/phase-status.json` — Marked P1-build-studio as completed, cleared blockedBy, updated reportPath and branchName
- `docs/build/change-manifest.md` — Added this section
- `docs/build/blockers.md` — Added P1 to resolved blockers
- `docs/build/approval-requests.md` — Moved P1 Build Studio start (#8) from Pending to Approved

### Constraints Verified

- No engine code modified
- No new Python dependencies
- No secrets/env files read or modified
- Bootstrap Console still fully functional
- All existing API endpoints unchanged

---

## Deep Research Ingestion — Topic 05 (2026-05-19)

### Files Created

**docs/research/syntheses/**
- `05-context-memory-vector-db-self-improvement.synthesis.md` — Synthesis: memory as governed evidence system, PostgreSQL+pgvector MVP, 5-level hierarchy, hybrid retrieval, context packs, attribution

**docs/research/decisions/**
- `DEC-008-memory-store-mvp-scope.md` — Memory store MVP scope: minimal 3-table ledger vs. full 10-table schema
- `DEC-009-memory-extraction-trigger.md` — Memory extraction trigger: async post-build vs. inline vs. event-driven
- `DEC-010-evaluation-harness-mvp-scope.md` — Evaluation harness MVP: evidence+contradiction only vs. full replay suite

**docs/build/**
- `deep-research-ingestion-05-report.md` — Ingestion report
- `session-handoffs/deep-research-ingestion-05-handoff.md` — Session handoff

### Files Modified

- `docs/research/research-status.md` — Moved Topic 05 from Pending to Synthesized
- `docs/research/research-index.md` — Added output/synthesis links for Topic 05, added DEC-008/009/010, updated recommended next topic to 04
- `docs/research/synthesis-log.md` — Added Topic 05 synthesis entry
- `config/research-topics.json` — Set Topic 05 status to synthesized, updated synthesisPath, lastUpdated, decisionsCreated
- `docs/build/change-manifest.md` — Added this section

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No secrets/env files read or modified
- Raw reports remain in gitignored `local-inputs/research-inbox/`
- No sensitive raw content copied into committed docs

---

## Decision Review Before P1 (2026-05-19)

### Files Created

**docs/build/**
- `decision-review-summary.md` — Review of DEC-001 through DEC-007: per-decision analysis, P1 gating assessment, deferral recommendations, synthesis cross-reference
- `p1-readiness-checklist.md` — P1 Build Studio readiness: prerequisites, decision readiness, research readiness, blocker/approval status, recommended pre-P1 actions
- `session-handoffs/decision-review-before-p1-handoff.md` — Session handoff

### Files Modified

- `docs/build/blockers.md` — Added P1 non-blocking clarifications to Affects column for all 3 open blockers
- `docs/build/approval-requests.md` — Moved #4 from Pending to Approved (was already approved), added #7 (DEC batch review) and #8 (P1 Build Studio start)
- `docs/build/change-manifest.md` — Added this section

### Constraints Verified

- No engine code modified
- No dashboard code modified
- No secrets/env files read or modified
- No config JSON modified
- All 7 decisions (DEC-001 through DEC-007) represented in summary

---

## P0-events — Event System + SSE + Live Dashboard (2026-05-19)

### Files Created

**engine/**
- `events.py` — Event system: in-memory ring buffer (deque, 500 max), thread-safe pub/sub via `queue.Queue`, SSE subscriber management, event history/stats queries, graceful shutdown

**docs/build/**
- `p0-events-build-report.md` — P0-events build report
- `rollback/p0-events-rollback.md` — Rollback plan
- `session-handoffs/p0-events-handoff.md` — Session handoff

### Files Modified

- `engine/server.py` — Added `events` import, 3 new API routes (`GET /api/events`, `GET /api/events/stream`, `GET /api/events/stats`), SSE handler with keepalive, events configuration in `main()`, shutdown integration
- `engine/bootstrap.py` — Added `events` import, emit `phase.status_changed` in `update_phase_status()`
- `engine/pipelines.py` — Added `events` import, emit `pipeline.stage.status_changed` in `_transition_stage()`, emit `pipeline.created/started/completed/failed/cancelled` in lifecycle functions
- `engine/sessions.py` — Added `events` import, emit `session.created` in `create_session()`, emit `session.started` and `session.completed` in `_run_session()`
- `engine/work_guard.py` — Added `events` import, emit `work_guard.lock_acquired` in `acquire_lock()`, emit `work_guard.lock_released` in `release_lock()`
- `dashboard/pages/bootstrap.html` — Added Events tab, SSE connection indicator (Live/Connecting/Offline), live event feed panel, event type styling, auto-refresh on phase/pipeline/work_guard events, EventSource connection management
- `config/phase-status.json` — Marked P0-events as completed
- `CLAUDE.md` — Added `events.py` to architecture tree, added Events API endpoints
- `docs/build/change-manifest.md` — Added this section
- `docs/build/blockers.md` — Updated resolved blockers
- `docs/build/approval-requests.md` — Updated for P0-events

---

## Minimal Claude Skill Layer (2026-05-19)

### Files Created

**.claude/skills/conductor-start/**
- `SKILL.md` — Read-only session start skill: reports branch, phase status, blockers, approvals, lock state, safe-to-run, recommended next action

**.claude/skills/conductor-work-guard/**
- `SKILL.md` — Read-only safety gate skill: reports lock status, dirty/clean tree, safe-to-run, recommended action

**.claude/skills/conductor-handoff/**
- `SKILL.md` — Session handoff skill: creates handoff docs under `docs/build/session-handoffs/`, may append to change manifest

**docs/architecture/**
- `claude-minimal-skill-layer.md` — Architecture doc: rationale for minimal skills, deferred skills list, available skills reference, modification constraints

**docs/prompts/**
- `setup-minimal-claude-skill-layer.md` — Reusable setup prompt for recreating the skill layer

### Files Modified

- `docs/build/change-manifest.md` — Added this section

---

## P0.5 — Work Guard Implementation (2026-05-19)

### Files Created

**engine/**
- `work_guard.py` — Work Guard module: git status checks, session lock lifecycle (acquire/release/heartbeat), stale lock detection, PID liveness, safe-to-run gate, full status reporting

**docs/build/**
- `work-guard-build-report.md` — P0.5 build report
- `rollback/work-guard-rollback.md` — Rollback plan
- `session-handoffs/p0-5-work-guard-handoff.md` — Session handoff

### Files Modified

- `engine/server.py` — Added `work_guard` import + 5 API routes (`GET /api/work-guard/status`, `GET /api/work-guard/safe-to-run`, `POST /api/work-guard/lock`, `DELETE /api/work-guard/lock`, `POST /api/work-guard/heartbeat`)
- `dashboard/pages/bootstrap.html` — Added Work Guard CSS, banner (lock status + safe-to-run badge), "Work Guard" tab, detail panel (Git State, Session Lock, Safety Checks, Recommended Action), JS fetch/render functions
- `config/phase-status.json` — Updated P0.5 status from "pending" to "completed"
- `docs/build/change-manifest.md` — Added this section
- `docs/build/blockers.md` — Updated: P0 approval blocker resolved
- `docs/build/approval-requests.md` — Updated for P0.5
- `docs/build/parallelization-status.md` — Updated for post-P0.5 state

---

## P0.5 — Repo Work Guard, Session Lock, and Execution Queue — Roadmap/Docs/Config Setup (2026-05-19)

### Files Created

**docs/architecture/**
- `repo-work-guard-session-lock.md` — Architecture doc: lock model, dirty-tree gate, heartbeat, queue, worktree isolation, parallel execution rules

**docs/decisions/**
- `ADR-0009-repo-work-guard-session-lock.md` — ADR: context, decision, options considered, consequences, risks, future implementation notes

**config/**
- `work-guard-policy.json` — Work Guard policy configuration (lock path, timeouts, blocked paths, approval rules, safe task types)

**docs/templates/**
- `session-lock.json` — Example session lock file with all fields populated
- `work-guard-status.md` — Status report template (lock state, git state, phase, queue, safe-to-run)

**docs/prompts/**
- `00-p0-5-repo-work-guard-session-lock.md` — Future implementation prompt for P0.5 (scope, API routes, Bootstrap Console integration, testing, deliverables)

### Files Modified

- `.gitignore` — Added `.conductor/runtime/` to gitignore (runtime lock file location)
- `config/phase-status.json` — Added `p0-5-repo-work-guard-session-lock` phase entry (status: pending, priority: P0.5)
- `docs/build/parallelization-status.md` — Added autonomous/parallel execution hold notice until P0.5 is implemented
- `docs/build/change-manifest.md` — Added this section

---

## Deep Research Ingestion — Topics 01, 02, 08 (2026-05-19)

### Files Created

**docs/research/syntheses/**
- `01-multi-tenant-saas-rls-client-portals.synthesis.md` — Synthesis: multi-tenant architecture, RLS, client portals
- `02-agent-orchestration-dag-parallelization.synthesis.md` — Synthesis: DAG engine, parallelization, worktrees, events
- `08-hybrid-context-fabric-wiki-memory-knowledge-graph.synthesis.md` — Synthesis: context fabric, memory governance, knowledge graph

**docs/research/decisions/**
- `DEC-001-default-tenancy-model.md` — Default tenancy model decision
- `DEC-002-secrets-management-backend.md` — Secrets management backend decision
- `DEC-003-worktree-isolation-model.md` — Worktree isolation model decision
- `DEC-004-event-store-technology.md` — Event store technology decision
- `DEC-005-vector-store-for-context-fabric.md` — Vector store for context fabric decision
- `DEC-006-wiki-repo-role.md` — Wiki repo role decision
- `DEC-007-memory-provider-integration.md` — Memory provider integration decision

**docs/build/**
- `deep-research-ingestion-01-02-08-report.md` — Ingestion build report
- `session-handoffs/deep-research-ingestion-01-02-08-handoff.md` — Session handoff

### Files Modified

- `docs/research/research-status.md` — Moved topics 01, 02, 08 to Synthesized
- `docs/research/research-index.md` — Added output/synthesis links, decisions table, next recommendation
- `docs/research/synthesis-log.md` — Added three synthesis entries
- `config/research-topics.json` — Set status to synthesized, updated lastUpdated and decisionsCreated for topics 01, 02, 08
- `docs/build/change-manifest.md` — Added this section

---

## P0 Pipeline DAG Engine (2026-05-18)

### Files Created

**engine/**
- `pipelines.py` — Core pipeline DAG engine: dependency resolution, stage lifecycle, session integration, failure propagation, retry/skip/cancel, gate approval, template loading, dry run, atomic persistence
- `phases.py` — Phase definition loader: markdown+YAML frontmatter parser, variable extraction, directory scanner

**dashboard/pages/**
- `pipelines.html` — Pipeline dashboard: list, templates, dry run, detail overlay, stage actions, KPI strip

**docs/build/**
- `p0-pipeline-dag-engine-build-report.md` — P0 build report
- `rollback/p0-pipeline-dag-engine-rollback.md` — Rollback plan
- `session-handoffs/p0-pipeline-dag-engine-handoff.md` — Session handoff

### Files Modified

- `engine/server.py` — Added 12 pipeline API routes, session launcher, pipeline module initialization, shutdown integration
- `config/phase-status.json` — Marked P0-pipeline-dag as completed
- `docs/build/change-manifest.md` — Added P0 section
- `docs/build/approval-requests.md` — Marked P0 approval as fulfilled

---

## Bootstrap Orchestration Console (2026-05-18)

### Files Created

**engine/**
- `bootstrap.py` — Phase dependency engine (eligible, blocked, parallelizable, critical path, next recommendation)

**dashboard/pages/**
- `bootstrap.html` — Bootstrap Console SPA page (10 tabbed views: Roadmap, Dependencies, Work Queue, Blockers, Approvals, Reports, Parallelization, Changes, Rollback, Quarantine)

**docs/build/**
- `bootstrap-orchestration-console-build-report.md` — Phase 5 build report
- `rollback/bootstrap-orchestration-console-rollback.md` — Rollback instructions
- `session-handoffs/bootstrap-orchestration-console-handoff.md` — Session handoff for next phase

**docs/decisions/**
- `bootstrap-orchestration-console.md` — ADR for bootstrap console architecture decisions

### Files Modified

- `engine/server.py` — Added bootstrap API routes (GET/PATCH/POST for phases, summary, blockers)
- `dashboard/index.html` — Added "Bootstrap" nav link and route entry
- `config/phase-status.json` — Marked 00-bootstrap as completed
- `docs/build/change-manifest.md` — Added Phase 5 section
- `docs/build/blockers.md` — Updated with current state
- `docs/build/approval-requests.md` — Updated with current state
- `docs/build/parallelization-status.md` — Updated for post-bootstrap state

---

## Research + Inputs Intake System (2026-05-18)

### Files Created

**docs/inputs/**
- `README.md` — inputs directory guide
- `01-product-vision.md` — North Star vision document
- `02-target-users.md` — user personas
- `03-use-cases.md` — core use cases
- `04-client-onboarding-flows.md` — onboarding journey design
- `05-current-aldc-service-inventory.md` — service inventory template
- `06-current-client-migration-notes.md` — migration inventory table
- `07-security-compliance-needs.md` — security requirements
- `08-demo-script.md` — demo flow and screens
- `09-questions-for-deep-research.md` — research question index

**docs/research/**
- `README.md` — research workflow guide
- `research-index.md` — topic index with links
- `research-status.md` — kanban status board
- `synthesis-log.md` — synthesis operation log
- `syntheses/README.md` — synthesis directory guide
- `decisions/README.md` — decision file format guide
- `prompts/01-multi-tenant-saas-rls-client-portals.md`
- `prompts/02-agent-orchestration-dag-parallelization.md`
- `prompts/03-ai-product-onboarding-decision-simulation.md`
- `prompts/04-data-platform-modernization-factory.md`
- `prompts/05-context-memory-vector-db-self-improvement.md`
- `prompts/06-secure-credential-artifact-workflows.md`
- `prompts/07-market-intelligence-growth-engine.md`

**docs/prompts/**
- `ingest-new-research-output.md` — Claude ingestion prompt
- `synthesize-research-into-roadmap.md` — roadmap synthesis prompt

**config/**
- `research-topics.json` — machine-readable topic registry

**local-inputs/**
- `README.md` — local inputs guide
- `research-inbox/README.md` — inbox instructions

**docs/build/**
- `change-manifest.md` — this file
- `blockers.md` — current blockers
- `approval-requests.md` — pending approvals
- `parallelization-status.md` — parallel work tracking
- `rollback/research-inputs-intake-system-rollback.md` — rollback instructions
- `research-inputs-intake-system-report.md` — final report

### Files Modified

- `.gitignore` — added `local-inputs/research-inbox/*` ignore rule

---

## Preflight Autonomy + Rollback Policy (2026-05-18)

### Files Created

- `docs/build/preflight-safety-report.md` — preflight check results
- `docs/build/rollback/preflight-autonomy-rollback-policy-rollback.md` — rollback instructions
- `docs/architecture/autonomy-approval-rollback-policy.md` — autonomy policy (from build pack)
- `docs/decisions/ADR-0004-autonomy-approval-rollback-policy.md` — ADR (from build pack)

### Files Updated

- `docs/build/change-manifest.md` — added preflight section
- `docs/build/blockers.md` — confirmed no new blockers
- `docs/build/approval-requests.md` — no new approvals needed
- `docs/build/parallelization-status.md` — updated for setup sequence

---

## Clean Start / Reset Branch (2026-05-18)

### Files Deleted (LABS Institute legacy)

- `docs/product/labs-institute-growth-gig-intelligence-platform.md`
- `docs/product/LABS_Institute_Growth_Gig_Intelligence_Platform_Spec.md`
- `docs/product/mvp-scope.md`
- `docs/workflows/master-simulator.md`
- `docs/workflows/roadmap-builder.md`
- `docs/research/labs-institute/README.md`
- `docs/research/labs-institute/assumptions.md`
- `docs/research/labs-institute/deep-research.md`
- `prompts/labs/README.md`
- `prompts/labs/conductor-ui-build-prompt.md`
- `projects/labs-institute/project.json`
- `dashboard/labs/` (13 files — full LABS dashboard)
- `docs/build/backlog.md` (LABS task IDs)
- `docs/build/acceptance-criteria.md` (LABS acceptance)
- `docs/build/orchestrator-guardrails.md` (LABS guardrails)
- `docs/README.md` (old LABS reading order)

### Files Quarantined

- `conductor_platform_build_pack_v5.zip` → `.cleanup-quarantine/conductor_platform_build_pack_v5.zip`

### Files Created

- `docs/build/cleanup-inventory.md` — classification of all repo contents
- `docs/build/clean-start-reset-report.md` — cleanup report
- `docs/build/rollback/clean-start-reset-rollback.md` — rollback instructions
- `docs/README.md` — new Conductor platform docs index
- `docs/checklists/.gitkeep` — placeholder
- `docs/templates/.gitkeep` — placeholder
- `.cleanup-quarantine/README.md` — quarantine manifest

---

## Repo Restructure + Roadmap Ingestion (2026-05-18)

### Files Created

**docs/roadmap/** (4 files)
- `executive-summary.md` — platform executive summary
- `product-strategy.md` — product strategy and positioning
- `master-build-sequence.md` — 15-phase build sequence
- `repo-restructure-plan.md` — current vs. future structure

**docs/architecture/** (12 files from build pack)
- `platform-architecture.md`, `multi-tenant-security-rls.md`, `product-onboarding-decision-simulator.md`
- `client-product-portal.md`, `trust-aware-discovery-access.md`, `data-platform-modernization.md`
- `market-growth-engine.md`, `context-memory-self-improvement.md`, `infrastructure-deployment-operations.md`
- `evaluation-quality-gates.md`, `current-branch-reset-strategy.md`, `bootstrap-approval-rollback-ui.md`

**docs/decisions/** (3 ADRs from build pack)
- `ADR-0001-build-conductor-first.md`, `ADR-0002-progressive-access-model.md`, `ADR-0003-metadata-first-data-modernization.md`

**docs/checklists/** (6 from build pack)
- `gaps-before-build.md`, `current-client-migration-checklist.md`, `security-compliance-checklist.md`
- `no-regression-testing.md`, `branch-cleanup-classification-checklist.md`, `pre-start-safety-checklist.md`

**docs/templates/** (12 from build pack)
- `client-migration-readiness-report.md`, `artifact-gap-register.md`, `current-functionality-baseline.md`
- `product-decision-report.md`, `feature-value-cost-matrix.md`, `migration-scenario-comparison.md`
- `branch-cleanup-report.md`, `approval-requests.md`, `blockers.md`, `change-manifest.md`
- `phase-rollback-plan.md`, `parallelization-status.md`

**docs/build/**
- `repo-restructure-and-roadmap-ingestion-report.md`
- `rollback/repo-restructure-roadmap-ingestion-rollback.md`

---

## Topic 08 Hybrid Context Fabric Setup (2026-05-18)

### Files Created

- `docs/prompts/design-hybrid-context-fabric-from-repos.md` — future Claude execution prompt
- `docs/research/prompts/08-hybrid-context-fabric-wiki-memory-knowledge-graph.md` — Deep Research prompt

### Files Updated

- `config/research-topics.json` — added Topic 08
- `docs/research/research-status.md` — added Topic 08 to Pending
- `docs/research/research-index.md` — added Topic 08 row and updated run order
- `docs/research/README.md` — added Topic 08 to directory listing
- `docs/build/parallelization-status.md` — updated for current phase
- `docs/build/change-manifest.md` — added Phase 4 section
