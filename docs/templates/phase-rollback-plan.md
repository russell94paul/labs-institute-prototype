# Phase Rollback Plan: <phase-id>

## Checkpoint

- **Branch:** `<branch-name>`
- **Commit/tag before phase:** `<checkpoint>`
- **Rollback command:**

```bash
git reset --hard <checkpoint>
```

## File-level rollback

| File/path | Action to reverse | Command/instruction |
|---|---|---|

## Quarantine restore

| Quarantined path | Original path | Restore command/instruction |
|---|---|---|

## Risks

## Validation after rollback

```bash
# commands to confirm repo health
```
