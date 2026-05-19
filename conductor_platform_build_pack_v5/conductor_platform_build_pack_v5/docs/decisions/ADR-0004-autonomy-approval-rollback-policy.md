# ADR-0004 — Autonomy, Approval, and Rollback Policy

## Decision

Conductor-building agents may perform broad reversible work inside dedicated branches/worktrees but must pause for high-risk actions.

## Rationale

Asking for permission on every file makes development too slow. Unlimited permission is unsafe because git rollback cannot fix secret exposure, cloud costs, production mutations, legal/IP changes, or external deployments.

## Consequences

Every phase must maintain a change manifest, blockers file, approval queue, and rollback plan. Uncertain files should be quarantined instead of silently deleted. The Bootstrap Orchestration Console should expose approval, rollback, modified-file, and parallelization status in the UI.
