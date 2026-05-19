# Rollback: Preflight Autonomy + Rollback Policy

## What This Phase Created

- `docs/build/preflight-safety-report.md`
- `docs/build/rollback/preflight-autonomy-rollback-policy-rollback.md` (this file)
- `docs/architecture/autonomy-approval-rollback-policy.md`
- `docs/decisions/ADR-0004-autonomy-approval-rollback-policy.md`
- Updated: `docs/build/change-manifest.md`, `blockers.md`, `approval-requests.md`, `parallelization-status.md`

## How to Rollback

### Option 1: Git revert
```
git revert <commit-hash>
```

### Option 2: Manual removal
Delete the created files and revert the updated files to their prior state from the previous commit.

## Risk

Low — this phase only created documentation and policy files. No engine, dashboard, or infrastructure code was modified.
