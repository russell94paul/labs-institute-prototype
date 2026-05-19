# Rollback: Clean Start / Reset Branch

## What This Phase Changed

- Deleted 28 LABS Institute legacy files across 6 directories
- Quarantined `conductor_platform_build_pack_v5.zip` to `.cleanup-quarantine/`
- Created new `docs/README.md`, cleanup inventory, cleanup report
- Created `docs/checklists/.gitkeep`, `docs/templates/.gitkeep`

## How to Rollback

### Option 1: Git revert (recommended)
```
git revert <commit-hash>
```

### Option 2: Restore from checkpoint
```
git checkout 8d36a02 -- docs/product/ docs/workflows/ docs/research/labs-institute/ prompts/labs/ projects/labs-institute/ dashboard/labs/ docs/build/backlog.md docs/build/acceptance-criteria.md docs/build/orchestrator-guardrails.md
```

## What Is NOT Affected by Rollback

- `engine/` — untouched
- `dashboard/index.html`, `dashboard/pages/conductor.html`, `dashboard/pages/sessions.html` — untouched
- `docs/inputs/`, `docs/research/prompts/`, `config/` — untouched
