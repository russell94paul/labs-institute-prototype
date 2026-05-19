# 00 — Clean Start / Reset Branch Prompt

Use this prompt before any roadmap/restructure/build work if the current branch contains old product-delivery files, folders, or app artifacts that no longer match the new Conductor platform direction.

## Mission

Clean the current branch so the repository is aligned to the new Conductor platform roadmap and contains no folders, files, docs, prompts, generated app code, or artifacts from the abandoned/old product-delivery process.

This is a repository hygiene and reset phase only.

Do **not** implement the new Conductor platform yet.
Do **not** start the pipeline DAG engine yet.
Do **not** migrate old app code into the new architecture unless it is confirmed to be reusable Conductor core code.

## Safety rules

1. Before deleting anything, inspect the repo and create a backup branch or safety commit.
2. Never delete `.git`, package lockfiles, environment examples, core server/session code, or current Conductor engine code unless there is clear evidence they belong only to the abandoned app.
3. Do not delete secrets or env files by printing them. If secrets are found, document their paths only and recommend secure handling.
4. Prefer moving uncertain items into a temporary quarantine folder or documenting them for review instead of deleting blindly.
5. Preserve anything that is clearly part of Conductor core, including server/session/orchestration code, agent definitions, pipeline templates, UI shell, config, tests, and repo docs that still apply.
6. Remove old app/product artifacts that conflict with the new Conductor platform direction.
7. Keep the final repo state buildable.



## Autonomy, approval, and rollback policy

Do not ask for permission for every file. Proceed autonomously for routine reversible cleanup work inside the current feature branch.

You may autonomously:

- inspect, classify, create, edit, move, and delete files that are clearly within this cleanup phase
- delete files clearly classified as old abandoned app/product-delivery artifacts after a safety point exists
- quarantine uncertain files instead of deleting them
- create reports, templates, placeholders, and docs/build artifacts

You must pause for approval before:

- deleting uncertain reusable Conductor core logic
- modifying secrets, credentials, `.env` files, production configs, or deployment configs
- destructive database/schema changes
- auth, RLS, tenant isolation, or security-boundary changes
- force-pushing, rebasing shared branches, merging to main, or deleting branches
- adding paid services, cloud resources, or major external dependencies
- modifying legal, license, compliance, ownership, or IP files
- deploying anything
- continuing into the next phase

If uncertain, quarantine and report.

Maintain or create:

```text
docs/build/approval-requests.md
docs/build/blockers.md
docs/build/change-manifest.md
docs/build/rollback/clean-start-reset-rollback.md
```

Every approval request must include recommendation, alternatives, pros/cons, timeline impact, cost/complexity impact, risk, files affected, and rollback plan.

## Step 1 — Inspect current branch

Run and record:

```bash
git status --short
git branch --show-current
git log --oneline -5
find . -maxdepth 3 -type d | sort
find . -maxdepth 4 -type f | sort
```

Also inspect key files:

```bash
ls -la
find . -maxdepth 3 -iname '*lab*' -o -iname '*ortho*' -o -iname '*neuro*' -o -iname '*demo*' -o -iname '*client*' -o -iname '*old*'
```

Do not assume those names are all deletable. Use them only as clues.

## Step 2 — Create safety point

If the working tree has changes, create a backup branch before cleanup:

```bash
git switch -c backup/pre-conductor-platform-reset-$(date +%Y%m%d-%H%M%S)
git add -A
git commit -m "backup: preserve pre-reset branch state" || true
```

Then return to the working branch or create the new clean branch:

```bash
git switch -
git switch -c chore/conductor-platform-clean-start
```

If a backup branch already exists, do not create duplicates unnecessarily. Document what you did.

## Step 3 — Classify repo contents

Create:

```text
docs/build/cleanup-inventory.md
```

Classify each top-level folder and important file as one of:

- `KEEP_CONDUCTOR_CORE`
- `KEEP_SHARED_TOOLING`
- `KEEP_DOCS_ROADMAP`
- `MIGRATE_LATER`
- `QUARANTINE_UNCERTAIN`
- `DELETE_OLD_PROCESS`

For every `DELETE_OLD_PROCESS` item, include:

```text
path
reason
why it is not part of the new Conductor platform
risk of deletion
```

For every `QUARANTINE_UNCERTAIN` item, explain what must be reviewed before deletion.

## Step 4 — Apply cleanup

After classification, remove only items that are clearly old app/product/process artifacts.

Examples of likely deletion candidates:

```text
old product-specific app folders
old generated UI prototypes unrelated to Conductor
old LABS/Ortho/NeuroSpect-specific build artifacts in the Conductor repo
abandoned prompt outputs
obsolete docs that contradict the new roadmap
old pipeline plans for the previous app direction
old client-specific data samples or artifacts that should not live in this repo
```

Examples of things to preserve unless proven obsolete:

```text
server.py
sessions.py
git_ops.py
agent definitions
pipeline template YAML files
Conductor UI shell
package.json / pyproject.toml / requirements files
README files that describe current Conductor behavior
docs/reference-repos
docs/conductor-platform
existing tests
```

Use commands like:

```bash
git rm -r <clearly-old-path>
```

For uncertain files, use quarantine:

```bash
mkdir -p .cleanup-quarantine
mkdir -p .cleanup-quarantine/<original-parent-path>
git mv <uncertain-path> .cleanup-quarantine/<original-parent-path>/
```

Add `.cleanup-quarantine/README.md` explaining why each item was moved.

## Step 5 — Add new repo structure placeholders

Create the new roadmap-aligned structure if it does not already exist:

```text
docs/conductor-platform/
docs/architecture/
docs/decisions/
docs/build/
docs/prompts/
docs/checklists/
docs/templates/
config/conductor/
```

Do not duplicate files if the build pack already provides them.

## Step 6 — Verify repo health

Run available checks:

```bash
git status --short
```

Then run whichever are available:

```bash
npm install --ignore-scripts || true
npm run lint || true
npm run test || true
npm run build || true
pytest || true
python -m pytest || true
```

Do not invent success. Record what exists, what passed, what failed, and what was unavailable.

## Step 7 — Produce cleanup report

Create:

```text
docs/build/clean-start-reset-report.md
```

Include:

```text
current branch
backup branch created
files/folders kept
files/folders deleted
files/folders quarantined
reason for each deletion/quarantine
checks run
check results
remaining risks
recommended next prompt
```

The recommended next prompt should be:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-repo-restructure-and-roadmap-ingestion.md
```

If the pack is stored under a different path, use the actual path.

## Acceptance criteria

This cleanup is complete when:

- A backup branch or safety commit exists.
- Old product-delivery/app artifacts are removed or quarantined.
- The repo contains only Conductor-core, shared tooling, roadmap docs, and intentional placeholders.
- Cleanup inventory exists.
- Cleanup report exists.
- Current repo health checks are documented.
- The repo is ready for roadmap ingestion and restructuring.

Stop after cleanup. Do not start implementation.
