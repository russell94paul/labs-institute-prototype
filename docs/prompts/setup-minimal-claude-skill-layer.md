# Setup: Minimal Claude Skill Layer for Conductor

Reusable prompt for creating the minimal Claude Code skill layer. Run this after P0 and P0.5 are complete and the working tree is clean.

## Prerequisites

- P0 Pipeline DAG Engine committed
- P0.5 Work Guard committed
- Working tree clean on `conductor-platform-rebuild`
- `config/phase-status.json` exists with completed phases
- `config/work-guard-policy.json` exists

## Prompt

```
You are working in the Conductor repo.

Create a minimal Claude Code skill layer using the modern format:
.claude/skills/<skill-name>/SKILL.md

Read first:
- AGENTS.md (if exists)
- docs/AGENT_ENTRYPOINT.md (if exists)
- config/phase-status.json
- config/work-guard-policy.json
- Latest handoff from docs/build/session-handoffs/
- docs/build/change-manifest.md
- docs/build/blockers.md
- docs/build/approval-requests.md

Create three skills:

1. conductor-start — Read-only session start. Reports branch, phase status,
   blockers, approvals, lock state, safe-to-run, recommended next action.

2. conductor-work-guard — Read-only safety gate. Reports lock status,
   dirty/clean tree, safe-to-run, recommended action.

3. conductor-handoff — Creates session handoff doc under
   docs/build/session-handoffs/. Summarizes work, files changed, blockers,
   rollback notes, next steps. May append to change-manifest.md.

Also create:
- docs/architecture/claude-minimal-skill-layer.md (rationale + reference)
- docs/prompts/setup-minimal-claude-skill-layer.md (this prompt, for reuse)
- Update docs/build/change-manifest.md

Do NOT create: /phase-advance, /run-phase, /run-autonomous, /deploy,
/merge, /create-pr. Those wait until after P1 Build Studio.

Constraints:
- No engine code changes
- No dashboard code changes
- No config file changes (except change-manifest.md)
- No secrets or env files touched
- Skills are thin wrappers around existing repo state
```

## Verification checklist

- [ ] `.claude/skills/conductor-start/SKILL.md` exists
- [ ] `.claude/skills/conductor-work-guard/SKILL.md` exists
- [ ] `.claude/skills/conductor-handoff/SKILL.md` exists
- [ ] `docs/architecture/claude-minimal-skill-layer.md` exists
- [ ] No files in `engine/` were modified
- [ ] No files in `dashboard/` were modified
- [ ] No config files were modified (except docs)
- [ ] `docs/build/change-manifest.md` updated
- [ ] All skills are read-only except handoff (which only creates docs)
