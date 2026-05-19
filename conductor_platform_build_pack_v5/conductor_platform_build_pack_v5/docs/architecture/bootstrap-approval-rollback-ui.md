# Bootstrap Console: Approvals, Rollback, and Modified Files UI

The Bootstrap Orchestration Console should expose file-based approval and rollback state before the full Build Studio exists.

## Required views

### Approval Queue

Shows open, approved, rejected, deferred, and resolved approval requests from:

- `docs/build/approval-requests.md`
- phase-specific build reports
- phase-status config, when available

Each approval should show:

- title
- phase
- risk level
- recommended action
- alternatives
- pros/cons
- files affected
- rollback plan
- status
- created/resolved dates

### Modified Files

Shows created, modified, moved, deleted, and quarantined files from:

- `docs/build/change-manifest.md`
- `docs/build/rollback/*.md`

Each row should show:

- path
- action
- reason
- phase
- risk level
- rollback method

### Rollback Center

Shows available checkpoints and rollback files:

- git checkpoint command/tag/commit
- phase rollback document
- file-level restore instructions
- branch/worktree guidance

The UI should never auto-rollback without user approval.

### Quarantine Review

Shows quarantined files and lets the user decide whether to restore, keep archived, or delete later.

### Parallelization Status

Reads:

- `config/phase-status.json`
- `docs/build/parallelization-status.md`

Shows:

- eligible work
- blocked work
- safe parallel candidates
- must-serialize phases
- recommended branch/worktree
- max concurrency recommendation

## Initial behavior

Before APIs exist, this UI can be read-only or generate copyable commands. Do not overbuild. The goal is enough visibility to coordinate Conductor's own buildout.
