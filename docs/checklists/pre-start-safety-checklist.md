# Pre-Start Safety Checklist

Use this checklist before running the clean-start reset or any repo-changing phase.

## Git safety

- [ ] Current branch state committed or intentionally stashed.
- [ ] Backup branch created or tagged.
- [ ] New working branch created for Conductor clean-start work.
- [ ] `git status --short` reviewed.
- [ ] No important untracked files ignored by accident.

## Scope safety

- [ ] Old app/product-delivery artifacts are expected to be removed or quarantined.
- [ ] Reusable Conductor core code must be preserved.
- [ ] The phase prompt says to stop after the requested phase.
- [ ] No implementation should begin during cleanup unless explicitly requested.

## Secrets and client data

- [ ] No raw secrets should be copied into prompts or reports.
- [ ] `.env` files should not be printed.
- [ ] Client data/artifacts should not be ingested unless explicitly approved.
- [ ] Credentials should be represented as secret references only.

## Autonomy and approval

- [ ] Routine reversible edits are allowed.
- [ ] Uncertain files should be quarantined, not silently deleted.
- [ ] High-risk actions require approval.
- [ ] Approval requests must include options, trade-offs, risk, timeline, cost/complexity, affected files, and rollback.

## Rollback

- [ ] A checkpoint commit/tag exists or will be created before changes.
- [ ] Every phase will create/update a change manifest.
- [ ] Every phase will create/update a rollback plan.
- [ ] Deletions and quarantine actions will be documented.
