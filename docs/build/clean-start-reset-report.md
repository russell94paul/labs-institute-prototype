# Clean Start / Reset Report

**Date**: 2026-05-18
**Phase**: 00 — Clean Start / Reset Branch
**Status**: Complete

## Branch

`conductor-platform-rebuild`

## Backup

Checkpoint commit `8d36a02` ("checkpoint before conductor platform rebuild") serves as the safety point. No backup branch created (working tree was clean at start).

## Files/Folders Deleted (28 files)

All LABS Institute legacy artifacts:

| Category | Files removed | Count |
|----------|-------------|-------|
| Product specs | `docs/product/*.md` | 3 |
| Workflows | `docs/workflows/*.md` | 2 |
| Research | `docs/research/labs-institute/*` | 3 |
| Prompts | `prompts/labs/*` | 2 |
| Projects | `projects/labs-institute/*` | 1 |
| Dashboard | `dashboard/labs/**/*` | 13 |
| Build docs | `docs/build/{backlog,acceptance-criteria,orchestrator-guardrails}.md` | 3 |
| Index | `docs/README.md` (old) | 1 |

## Files/Folders Quarantined (1 file)

| File | Reason |
|------|--------|
| `conductor_platform_build_pack_v5.zip` → `.cleanup-quarantine/` | Redundant with extracted folder |

## Files/Folders Kept

- `engine/` — Conductor core (server, sessions, stage_scripts)
- `agents/` — Orchestration agents (5 definitions)
- `dashboard/index.html`, `dashboard/pages/`, `dashboard/styles/` — Active Conductor UI
- `shared/prompts/` — Reusable prompt fragments
- `templates/` — Pipeline + stack templates
- `docs/inputs/` — Product inputs (from Research Intake phase)
- `docs/research/` — Research system (minus labs-institute)
- `docs/architecture/` — Architecture docs
- `docs/decisions/` — ADRs
- `docs/prompts/` — Claude execution prompts
- `docs/build/` — Build tracking
- `docs/reference-repos/` — Cross-repo analysis
- `config/` — Research topics registry
- `conductor_platform_build_pack_v5/` — Build pack (extracted)
- `CLAUDE.md`, `PROGRESS.md`, `sessions.json`, `.gitignore`

## Checks Run

| Check | Result |
|-------|--------|
| `git status` | Clean (only staged cleanup changes + new files) |
| Server health (`http://127.0.0.1:8888`) | 200 OK |

## Remaining Risks

- None identified. All deletions are clearly LABS Institute artifacts with no imports or dependencies from Conductor core.

## Recommended Next Prompt

```
conductor_platform_build_pack_v5/conductor_platform_build_pack_v5/docs/prompts/00-repo-restructure-and-roadmap-ingestion.md
```
