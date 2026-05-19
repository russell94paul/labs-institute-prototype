# conductor-start

Start a Conductor session safely. Read-only status check — never modifies files.

## When to use

At the beginning of any Conductor work session. Gives you current branch, phase status, blockers, and a safe-to-run determination before you touch anything.

## Steps

1. Read `AGENTS.md` if it exists in the repo root (skip silently if missing).
2. Read `docs/AGENT_ENTRYPOINT.md` if it exists (skip silently if missing).
3. Run `git status` and `git branch --show-current`.
4. Read `config/phase-status.json` — identify the current phase (latest completed) and next phase (first eligible `not_started`).
5. Read `config/work-guard-policy.json`.
6. Check `.conductor/runtime/session-lock.json` — if present, report lock holder and whether the lock is stale (heartbeat older than `heartbeatTimeoutMinutes` from policy).
7. Find the most recent file in `docs/build/session-handoffs/` (by filename sort or git log) and read it.
8. Read `docs/build/blockers.md` — extract open blockers.
9. Read `docs/build/approval-requests.md` — extract pending approvals.

## Report format

Print a structured report:

```
## Conductor Session Start

**Branch:** <branch name>
**Working tree:** clean | dirty (<N> modified, <M> untracked)
**Current phase:** <phaseId> — <name> (status)
**Next phase:** <phaseId> — <name> | none eligible
**Blockers:** <count open> | none
**Approvals needed:** <count pending> | none
**Session lock:** none | active (holder, age) | stale (holder, age)
**Safe to run:** true | false — <reason if false>
**Recommended next action:** <from handoff or phase-status nextRecommendedAction>
```

## Constraints

- **Read-only.** Do not modify any files.
- Do not start, advance, or execute any phase.
- Do not acquire or release session locks.
- Do not run engine code or start the server.
- Do not commit, push, or create branches.
- If `config/phase-status.json` is missing, report that the phase system is not initialized and stop.
