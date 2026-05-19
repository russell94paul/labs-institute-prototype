# Rollback: Research + Inputs Intake System

## What This Phase Created

All files listed in `docs/build/change-manifest.md` under "Research + Inputs Intake System (2026-05-18)".

## How to Rollback

### Option 1: Git revert (recommended)
If the changes were committed in a single commit:
```
git revert <commit-hash>
```

### Option 2: Manual removal
Remove the following directories and their contents:
```
docs/inputs/
docs/research/prompts/
docs/research/syntheses/
docs/research/decisions/
docs/research/research-index.md
docs/research/research-status.md
docs/research/synthesis-log.md
docs/prompts/
config/research-topics.json
local-inputs/
```

Revert `.gitignore` changes (remove the `local-inputs/research-inbox/*` lines).

Revert `docs/build/` changes (remove files created by this phase).

### What is NOT affected by rollback

- `engine/` — no engine code was modified
- `dashboard/` — no dashboard code was modified
- `templates/` — no templates were modified
- Existing `docs/research/labs-institute/` — preserved as-is
- Existing `docs/build/` files — only new files were added

## Risks of Rollback

- Loss of product vision draft and research prompts (recreatable but time-consuming)
- No impact on running systems — this phase created documentation only
