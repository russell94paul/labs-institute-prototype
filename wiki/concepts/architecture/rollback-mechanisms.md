---
tags: [architecture, rollback, pipelines, git]
created: 2026-05-23
updated: 2026-05-23
---

# Rollback Mechanisms

Pipeline-level rollback via git snapshots and worktree branch resets.

## Snapshot

When `start_pipeline()` is called, `git rev-parse main` captures the current HEAD. Stored as `pipeline["snapshot"] = {branch, commit, timestamp}`.

## Rollback Flow

1. Pipeline fails or produces bad output
2. Worktree is preserved (not auto-cleaned on failure)
3. User clicks "Rollback to Snapshot" in pipeline detail
4. `git reset --hard {snapshot_commit}` on the worktree branch
5. Pipeline status → `rolled_back`
6. Rollback recorded in `pipeline["rollback_history"]`

Safe because worktree branches are isolated — never pushed, never shared.

## Merge Approval

Pipeline completion no longer means auto-merge. New flow:
1. Pipeline completes → status = `completed`
2. User reviews validation results
3. User clicks "Approve Merge" → `merge_approved = True`
4. Actual git merge remains manual (PR or manual merge)

## API

- `POST /api/pipelines/{pid}/rollback` — rollback to snapshot
- `POST /api/pipelines/{pid}/merge` — approve merge
- `GET /api/pipelines/{pid}/snapshot` — view snapshot + rollback history

## Related

- [[validation-engine]] — validation failure triggers rollback option
- [[session-continuation]] — user can continue after reviewing failed work
