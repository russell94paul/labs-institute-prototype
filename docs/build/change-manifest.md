# Change Manifest

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
