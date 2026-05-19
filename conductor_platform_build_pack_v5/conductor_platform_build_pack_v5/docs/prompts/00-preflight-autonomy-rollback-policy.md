# 00 — Preflight Autonomy, Approval, and Rollback Policy Prompt

Use this prompt before the clean-start reset if the current repo/branch may contain old app work or if multiple agents may work on Conductor.

## Mission

Prepare the repository for safe autonomous work by confirming branch state, establishing rollback expectations, copying policy templates into active build docs, and preventing unnecessary permission prompts during routine work.

Do **not** clean the repo yet.  
Do **not** restructure the repo yet.  
Do **not** implement Conductor features yet.

## Autonomy policy

You have broad permission to perform reversible repo work inside the current feature branch for this requested phase.

You may autonomously:

- inspect files
- create policy docs
- create docs/build placeholders
- create rollback/report templates
- update roadmap pack references
- document branch/checkpoint instructions

Do not ask for permission for every routine file operation.

Pause only for:

- destructive changes
- secrets/credentials
- production or deployment configs
- auth/RLS/security boundaries
- legal/license/IP files
- force-push/rebase/merge-to-main/delete-branch
- cloud/paid resources
- deployment
- continuing into the next phase

If uncertain, document the issue as a blocker instead of changing it.

## Required checks

Run and record:

```bash
git status --short
git branch --show-current
git log --oneline -5
```

If the user has not already created a checkpoint, recommend these commands but do not force destructive git behavior:

```bash
git add -A
git commit -m "checkpoint: before conductor clean-start"
git tag checkpoint-before-conductor-clean-start
```

## Required files

Create or update:

```text
docs/build/approval-requests.md
docs/build/blockers.md
docs/build/change-manifest.md
docs/build/parallelization-status.md
docs/build/rollback/preflight-autonomy-rollback-policy-rollback.md
docs/build/preflight-safety-report.md
```

Use the templates from the build pack when available.

## Required report

Create:

```text
docs/build/preflight-safety-report.md
```

Include:

- current branch
- git status summary
- whether a checkpoint/tag exists
- whether docs/build exists
- what policy files were created or updated
- open blockers
- recommended next prompt

The recommended next prompt should be:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-clean-start-reset-branch.md
```

If the pack is stored under a different path, use the actual path.

## Stop condition

Stop after preflight safety setup. Do not clean, restructure, or implement features in this session.
