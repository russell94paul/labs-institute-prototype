# Cleanup Inventory

**Date**: 2026-05-18
**Phase**: 00 — Clean Start / Reset Branch

## Classification

### DELETE_OLD_PROCESS

| Path | Reason | Risk |
|------|--------|------|
| `docs/product/labs-institute-growth-gig-intelligence-platform.md` | Old LABS Institute product spec (DJ/artist platform) | None — replaced by Conductor platform vision |
| `docs/product/LABS_Institute_Growth_Gig_Intelligence_Platform_Spec.md` | Duplicate LABS Institute spec | None |
| `docs/product/mvp-scope.md` | LABS Institute MVP scope | None |
| `docs/workflows/master-simulator.md` | LABS Institute financial/marketing simulator workflow | None |
| `docs/workflows/roadmap-builder.md` | LABS Institute roadmap builder workflow | None |
| `docs/research/labs-institute/` | Entire directory — LABS Institute research (assumptions, deep-research, README) | None |
| `prompts/labs/` | LABS Institute UI build prompts | None |
| `projects/labs-institute/` | LABS Institute project config (project.json) | None |
| `dashboard/labs/` | LABS Institute dashboard UI (separate SPA) | None |
| `docs/build/backlog.md` | LABS Institute task backlog (LABS-001 through LABS-032) | None |
| `docs/build/acceptance-criteria.md` | LABS Institute acceptance criteria (artist profiles, gig workflows) | None |
| `docs/build/orchestrator-guardrails.md` | LABS Institute guardrails (simulator, social posts, contracts) | None |
| `docs/README.md` | Reading order for LABS Institute docs — now outdated | None — will be replaced |

### KEEP_CONDUCTOR_CORE

| Path | Reason |
|------|--------|
| `engine/` | Core Conductor server, sessions, pipeline automation |
| `agents/` | Orchestration agents (architect, deployer, implementer, reviewer, tester) |
| `dashboard/index.html` | Conductor SPA shell |
| `dashboard/pages/conductor.html` | Conductor console (87KB, 6 views) |
| `dashboard/pages/sessions.html` | Session management page |
| `dashboard/styles/` | Conductor CSS |
| `dashboard/data/` | Data directory (gitignored contents) |
| `shared/prompts/` | Reusable prompt fragments |
| `templates/` | Pipeline + stack templates |
| `CLAUDE.md` | Codebase documentation |
| `sessions.json` | Root session config |
| `.gitignore` | Git ignore rules |
| `.claude/` | Claude Code settings |
| `.conductor-sessions/` | Session workspace (gitignored) |

### KEEP_ROADMAP

| Path | Reason |
|------|--------|
| `docs/inputs/` | Product inputs (vision, personas, use cases, demo, inventory) |
| `docs/research/prompts/` | Deep Research prompts (7 topics) |
| `docs/research/syntheses/` | Synthesis outputs |
| `docs/research/decisions/` | Decision candidates |
| `docs/research/README.md` | Research workflow |
| `docs/research/research-index.md` | Topic index |
| `docs/research/research-status.md` | Status board |
| `docs/research/synthesis-log.md` | Synthesis log |
| `docs/prompts/` | Claude ingestion/synthesis prompts |
| `docs/architecture/` | Architecture docs |
| `docs/decisions/` | ADRs |
| `docs/reference-repos/` | Repo analysis from prior session |
| `docs/build/change-manifest.md` | Change tracking |
| `docs/build/blockers.md` | Blockers |
| `docs/build/approval-requests.md` | Approvals |
| `docs/build/parallelization-status.md` | Parallel work tracking |
| `docs/build/rollback/` | Rollback plans |
| `docs/build/preflight-safety-report.md` | Preflight results |
| `docs/build/conductor-console-build-report.md` | Console build report |
| `docs/build/research-inputs-intake-system-report.md` | Research system report |
| `config/research-topics.json` | Research registry |
| `local-inputs/` | Local research inbox |
| `PROGRESS.md` | Session progress log |
| `conductor_platform_build_pack_v5/` | Build pack (source of truth for prompts) |

### REVIEW_REQUIRED

| Path | Question | Decision |
|------|----------|----------|
| `conductor_platform_build_pack_v5.zip` | Redundant with extracted folder? | Quarantine — harmless but unnecessary |
