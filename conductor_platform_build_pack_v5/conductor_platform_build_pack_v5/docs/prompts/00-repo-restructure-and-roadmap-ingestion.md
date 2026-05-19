# Prompt: Repo Restructure and Roadmap Ingestion

You are an autonomous engineering/product agent working in the Conductor repo. Preserve existing functionality. Do not perform destructive git operations. Do not expose secrets. Do not ingest raw client data. Prefer local-first, testable changes. Write build reports under docs/build/. Stop at the requested phase.


## Mission
Prepare the repo for the updated Conductor platform vision.

## Tasks
1. Inspect current repo structure.
2. Identify existing app/server/UI/docs/configs/prompts/agents/sessions/pipeline files.
3. Create missing docs/config/template directories without breaking runtime code.
4. Add architecture docs, roadmap docs, ADRs, and phase template config locations.
5. Do not move runtime code unless imports and tests are updated.
6. Create docs/build/repo-restructure-and-roadmap-ingestion-report.md.

## Acceptance Criteria
- Roadmap docs exist.
- Prompt/config locations are clear.
- Existing app still runs.
- Existing tests/checks are passing or unchanged.


## Autonomy and rollback addendum

Proceed autonomously for routine reversible restructuring work inside the current branch. Do not ask for permission for every file.

Create or update:

```text
docs/build/change-manifest.md
docs/build/blockers.md
docs/build/approval-requests.md
docs/build/rollback/repo-restructure-roadmap-ingestion-rollback.md
```

Pause only for high-risk actions: deleting uncertain reusable core code, secrets/env files, production/deployment configs, destructive schema changes, auth/RLS/security boundaries, legal/license/IP files, force-push/rebase/merge-to-main/delete-branch, cloud/paid resources, deployment, or continuing into the next phase.

If uncertain, quarantine and report.
