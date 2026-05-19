# Prompt: Current Branch Cleanup + Legacy App Removal

You are an autonomous engineering/product agent working in the Conductor repo.

## Situation
The current branch may contain work from an older app/product-delivery process that is no longer desired. The updated direction is to build Conductor as a reusable, multi-tenant, domain-agnostic product-building platform with Build Studio, Product Onboarding Studio, Client Product Portal, Trust-Aware Access, Data Platform Modernization, Market/Growth, Context/Memory, Infrastructure/Ops, and Self-Improvement.

The goal is to remove folders/files tied to the old process while preserving legitimate Conductor core/runtime functionality.

## Non-Negotiable Safety Rules
- Do not expose secrets.
- Do not ingest raw client data.
- Do not delete credentials, environment files, private keys, local databases, or client data. Instead, flag them in the report.
- Do not run destructive git commands such as `git reset --hard`, `git clean -fdx`, force push, or branch deletion.
- Do not remove working Conductor runtime code unless it is clearly old-product-specific and not imported by the current app.
- Do not make production infrastructure changes.
- Preserve the ability to run the current Conductor server/UI if they exist.
- Before deleting files, create a written cleanup plan under `docs/build/current-branch-cleanup-plan.md`.

## Mission
Clean the current branch so it no longer contains folders/files related to the old app process, then prepare it for the updated Conductor platform roadmap.

## Step 1 — Inspect Current Git/Repo State
Run safe read-only checks:
- current branch name
- `git status --short`
- recent commits on this branch
- top-level directory tree
- package/runtime entrypoints
- existing tests/check commands
- existing docs/prompts/config files

Write findings to:

```text
docs/build/current-branch-cleanup-plan.md
```

## Step 2 — Classify Files and Folders
Classify files/folders into these buckets:

### KEEP_CORE
Conductor runtime code, server code, session/orchestration code, agent definitions, git/worktree helpers, existing pipeline infrastructure, package configs, tests, UI shell, and anything required for the current app to run.

### KEEP_ROADMAP
Updated Conductor platform docs, roadmap docs, prompts, phase templates, architecture docs, ADRs, config JSON, build reports, and other files from this build pack.

### REMOVE_LEGACY
Files/folders clearly tied to the old abandoned app/product process. Examples:
- app-specific product screens/routes/components unrelated to Conductor
- old product-specific docs/prompts/specs
- hard-coded app/client names from the previous process
- demo-specific data or generated artifacts not needed for Conductor
- obsolete product workflow files that conflict with the new Build Studio roadmap
- abandoned implementation stubs for the old app

### REVIEW_REQUIRED
Anything ambiguous, potentially imported, potentially containing data/secrets, or possibly useful as a reusable pattern.

## Step 3 — Dependency Check Before Removal
Before removing anything classified as REMOVE_LEGACY:
- search imports/references
- check routes/navigation references
- check tests/build configs
- check package scripts
- identify whether removal breaks app boot

If a legacy file is referenced by the app, either:
1. remove the reference safely, or
2. move the file to REVIEW_REQUIRED and explain why.

## Step 4 — Clean the Branch
After the cleanup plan is written, remove only files/folders classified as REMOVE_LEGACY.

Do not remove REVIEW_REQUIRED items unless they are proven obsolete and non-sensitive.

When removing old UI routes/pages, replace broken navigation with updated Conductor platform placeholders only if needed:
- Build Studio
- Product Onboarding Studio
- Client Product Portal
- Data Platform Modernization Studio
- Market/Growth Engine
- Context/Memory
- Infrastructure/Ops
- Self-Improvement

## Step 5 — Ingest/Align Roadmap Pack
Ensure these folders exist:

```text
docs/build/
docs/architecture/
docs/prompts/
docs/checklists/
docs/templates/
docs/decisions/
config/
```

Preserve the build pack under a stable location such as:

```text
docs/conductor-platform/
```

Do not scatter duplicate copies across the repo.

## Step 6 — Validation
Run the safest available checks, such as:
- install check if dependencies already exist
- lint/typecheck if available
- unit tests if available
- app boot/server smoke test if available

If checks fail, fix only cleanup-related breakages. Do not start new feature implementation in this phase.

## Step 7 — Final Report
Create:

```text
docs/build/current-branch-cleanup-report.md
```

Include:
- branch name
- summary of old process artifacts removed
- files/folders kept
- ambiguous items requiring human review
- runtime files preserved
- tests/checks run
- failures or warnings
- next recommended prompt to run

## Acceptance Criteria
- Old product/process-specific folders and files are removed or listed for review.
- Conductor core/runtime files are preserved.
- Roadmap pack is available in a stable docs location.
- No raw secrets/client data are copied into docs, prompts, vector DB, logs, or build reports.
- The current app/server still runs, or any pre-existing failure is clearly documented.
- A cleanup report exists under `docs/build/current-branch-cleanup-report.md`.
- The next recommended phase is `00-repo-restructure-and-roadmap-ingestion.md`.
