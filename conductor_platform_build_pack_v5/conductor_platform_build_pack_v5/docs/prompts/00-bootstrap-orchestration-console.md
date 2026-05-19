# Prompt: Bootstrap Orchestration Console

You are working in the Conductor repo after the clean-start reset and roadmap ingestion.

## Mission

Build a lightweight **Bootstrap Orchestration Console** that helps build Conductor itself before the full Build Studio exists.

Do **not** build the full Build Studio yet.  
Do **not** implement the full memory system yet.  
Do **not** implement client portal features yet.  
Do **not** deploy.  
Do **not** perform destructive git operations without explicit approval.

The console should be temporary but useful. It should later evolve into, or be replaced by, the full Conductor Build Studio.

## Goal

Create a minimal internal UI/control layer that can:

- Read the Conductor roadmap.
- Display phases and dependencies.
- Identify eligible phases and sub-phases.
- Recommend safe parallelization.
- Track active work.
- Track blockers.
- Track reports/artifacts.
- Generate launch instructions for the correct next implementation prompt.
- Recommend branch/worktree strategy per phase.

## Required capabilities

### 1. Roadmap ingestion

Read roadmap/config files when available:

- `config/roadmap.sequence.json`
- `config/module-registry.json`
- `config/phase-template-taxonomy.json`

Fallback behavior:

- If config files are missing, scan `docs/prompts/` and build a basic phase registry from prompt filenames.
- Do not fail hard if optional roadmap fields are missing.

### 2. Phase model

Each phase should include:

- `id`
- `name`
- `description`
- `status`
- `dependencies`
- `blockedBy`
- `blocks`
- `riskLevel`
- `estimatedComplexity`
- `estimatedContextRequired`
- `expectedFiles`
- `allowedParallelism`
- `requiredAgents`
- `requiredArtifacts`
- `approvalRequired`
- `promptPath`
- `reportPath`
- `branchName`
- `activeSessionId`
- `createdAt`
- `updatedAt`

### 3. Phase statuses

Support these statuses:

- `not_started`
- `eligible`
- `blocked`
- `running`
- `needs_review`
- `failed`
- `completed`
- `skipped`
- `cancelled`

### 4. Dependency engine

Implement logic to:

- Calculate eligible phases.
- Calculate blocked phases.
- Explain missing dependencies.
- Identify critical path.
- Identify safe parallelization candidates.
- Prevent unsafe parallelization when phases touch overlapping critical files.

### 5. Sub-phase/task breakdown

Allow a phase to be decomposed into sub-phases/tasks.

Each sub-phase should include:

- `id`
- `parentPhaseId`
- `name`
- `dependencies`
- `expectedFiles`
- `riskLevel`
- `contextEstimate`
- `canRunInParallel`
- `status`

### 6. Parallelization recommendations

The console should recommend whether a phase/sub-phase can run in parallel based on:

- Dependency completion.
- File overlap.
- Risk level.
- Expected shared state changes.
- Estimated context size.
- Branch/worktree strategy.

Default rules:

- Docs-only work can usually run in parallel.
- UI-only work can run in parallel if files do not overlap.
- API-only work can run in parallel if contracts are stable.
- Core engine, auth, database, RLS, deployment, repo restructuring, session state, pipeline state, and destructive file operations must be serialized unless explicitly approved.

### 7. Branch/worktree planning

Add a branch recommendation for each phase.

Examples:

- `conductor/bootstrap-console`
- `conductor/p0-pipeline-engine`
- `conductor/p1-build-studio`
- `conductor/p2-product-onboarding`

Rules:

- Do not automatically merge branches.
- Do not delete branches.
- Do not force push.
- Generate commands/instructions rather than executing risky git operations unless the user explicitly approves.

### 8. UI requirements

Add a minimal internal UI with these sections:

- Roadmap View
- DAG View or dependency list view
- Phase Detail View
- Eligible Work Queue
- Active Sessions View
- Blockers View
- Build Reports View
- Approvals View

The UI should show:

- Phase status.
- Dependencies.
- Blockers.
- Branch name.
- Prompt path.
- Report path.
- Risk level.
- Parallelization eligibility.
- Next recommended action.

Use the existing Conductor UI stack if present. If the current UI stack is unclear, implement the smallest compatible addition rather than introducing a large new frontend framework.

### 9. Actions

Support safe actions:

- Mark phase complete.
- Mark phase blocked.
- Mark phase failed.
- Add blocker.
- Clear blocker.
- Open/view prompt.
- Copy prompt.
- Generate launch instructions.
- Generate recommended branch command.
- Generate recommended next phase list.

If existing session APIs are available, integrate lightly.  
If not, generate copyable commands/instructions and leave execution manual.

### 10. Autonomy levels

Implement or model these levels, even if only the first two are enabled initially:

- `manual`: user launches every phase.
- `assisted`: console recommends next phase.
- `semi_autonomous`: console may auto-run safe docs/test/report tasks after approval.
- `guarded_autonomous`: console may run eligible phases but pauses for risky operations.
- `full_autonomous`: disabled until evaluation, rollback, and approval systems exist.

Initial default:

- `manual` + `assisted` only.

### 11. Reports

Generate or update:

- `docs/build/bootstrap-orchestration-console-build-report.md`
- `docs/decisions/bootstrap-orchestration-console.md`

The build report should document:

- Files changed.
- How to run.
- How to use.
- Limitations.
- Next recommended phase.
- Known gaps.



### 11.5 Persistent status, approvals, and rollback files

Create and maintain these files if they do not already exist:

```text
config/phase-status.json
docs/build/parallelization-status.md
docs/build/approval-requests.md
docs/build/blockers.md
docs/build/change-manifest.md
docs/build/rollback/bootstrap-orchestration-console-rollback.md
```

`config/phase-status.json` should track:

- `phaseId`
- `status`
- `dependencies`
- `blockers`
- `expectedFiles`
- `riskLevel`
- `branchName`
- `activeSessionId`
- `canRunInParallel`
- `parallelizationReason`
- `lastUpdated`
- `nextRecommendedAction`

`docs/build/parallelization-status.md` should show:

- phases eligible to run now
- phases blocked and why
- phases safe to parallelize
- phases that must be serialized
- recommended branch/worktree for each eligible phase
- expected file-overlap risks
- recommended max concurrency
- next 3 recommended actions

Add UI surfaces for:

- Approval Queue
- Modified Files
- Rollback Center
- Quarantine Review
- Parallelization Status

The UI may initially be read-only or command-generating. Do not overbuild. Do not auto-merge, auto-rollback, or auto-delete without approval.

### 12. Acceptance criteria

The Bootstrap Orchestration Console is complete when:

- Roadmap phases can be listed.
- Dependencies can be shown.
- Eligible phases can be identified.
- Blocked phases can be explained.
- Phase detail view exists.
- Prompt paths are visible.
- Branch recommendations are visible.
- Parallelization recommendations are visible.
- Blockers can be tracked.
- Build reports can be linked.
- Next recommended phase is shown.
- The full Build Studio is not implemented yet.
- Existing Conductor behavior is not broken.
- `config/phase-status.json` exists or is generated from seed config.
- `docs/build/parallelization-status.md` exists.
- Approval Queue view exists or is represented in the UI.
- Modified Files / Change Manifest view exists or is represented in the UI.
- Rollback Center view exists or is represented in the UI.
- Quarantine Review view exists or is represented in the UI.


## Stop condition

Stop after the Bootstrap Orchestration Console.  
Do not proceed to P0 Pipeline DAG Engine in this session.
