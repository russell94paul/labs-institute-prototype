# Autonomy, Approval, and Rollback Policy

This policy lets Conductor-building agents move quickly without asking for permission on every routine file while still protecting the repo, credentials, client data, production systems, and ownership boundaries.

## Operating model

Agents may perform broad reversible work inside a dedicated branch or worktree for the requested phase. They should pause only for high-risk or irreversible decisions.

### Allowed without asking

Agents may autonomously:

- inspect files and folders
- classify files as keep, delete, or quarantine
- create docs, prompts, configs, templates, tests, and UI scaffolding
- edit files clearly within the requested phase scope
- move uncertain files into quarantine
- delete files clearly identified as abandoned old product-delivery/app artifacts, if a backup branch or checkpoint exists
- update build reports, change manifests, blockers, approval requests, and rollback plans

### Must ask before doing

Agents must pause for approval before:

- deleting files that may contain reusable Conductor core logic
- changing secrets, credentials, `.env` files, production configs, or deployment configs
- destructive database or schema migrations
- auth, authorization, RLS, tenant isolation, or security-boundary changes
- force-pushing, rebasing shared branches, deleting branches, or merging to main
- adding paid services, cloud resources, external managed services, or major dependencies
- modifying legal, license, ownership, compliance, or IP-related files
- sending repo/client data to external services
- deploying anything
- continuing into the next phase after the requested phase is complete

## Decision rule

```
Low risk + reversible → proceed and document.
Medium risk + uncertain → quarantine and report.
High risk or irreversible → request approval.
```

## Approval request format

When approval is needed, the agent must provide:

- decision needed
- recommendation
- at least two alternatives
- pros and cons
- risk impact
- timeline impact
- cost/complexity impact
- files affected
- rollback option
- what will be done if approved

## Mandatory phase artifacts

Every phase should maintain or update:

- `docs/build/change-manifest.md`
- `docs/build/blockers.md`
- `docs/build/approval-requests.md`
- `docs/build/rollback/<phase-id>-rollback.md`

For every created, modified, moved, deleted, or quarantined file, record:

- original path
- new path, if moved
- reason
- risk level
- rollback method

## Secrets rule

Raw secrets must never be written to prompts, docs, reports, logs, vector DB, context packs, or agent memory. Agents should use secret references only.

## Production rule

No production deployment, production data mutation, destructive migration, paid cloud provisioning, or credential rotation should happen without explicit approval and a rollback plan.
