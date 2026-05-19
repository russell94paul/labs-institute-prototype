# conductor-work-guard

Check whether it is safe to start another task or session. Read-only safety gate.

## When to use

Before starting any new work, phase execution, or autonomous operation. Also useful mid-session to verify the working tree hasn't drifted into an unsafe state.

## Steps

1. Run `git status` — report clean/dirty, list modified and untracked files.
2. Run `git branch --show-current`.
3. Run `git log -1 --oneline` — report latest commit hash and message.
4. Check `.conductor/runtime/session-lock.json`:
   - If missing: lock status is `none`.
   - If present: read it, report holder, session ID, phase, acquired time.
   - Compute lock age. Read `config/work-guard-policy.json` for `heartbeatTimeoutMinutes` (default 10). If lock age exceeds timeout, mark as `stale`.
5. Read `docs/build/blockers.md` — extract open blockers.
6. Read `docs/build/approval-requests.md` — extract pending approvals that block work.
7. Determine `safeToRun`:
   - `false` if working tree is dirty and `blockOnDirtyWorkingTree` is true in policy.
   - `false` if an active (non-stale) session lock exists.
   - `false` if a stale lock exists and `staleLockBehavior` is `require-approval`.
   - `true` otherwise.

## Report format

```
## Work Guard Status

**Lock status:** none | active (holder: <name>, session: <id>, age: <duration>) | stale (holder: <name>, age: <duration>)
**Working tree:** clean | dirty (<details>)
**Branch:** <branch name>
**Latest commit:** <hash> <message>
**Open blockers:** <count> | none
**Pending approvals:** <count> | none
**Safe to run:** true | false — <reason>
**Recommended action:** <action>
```

Recommended actions:
- If safe: "Proceed with next phase or task."
- If dirty tree: "Commit or stash changes before proceeding."
- If active lock: "Another session is running. Wait or check if it completed."
- If stale lock: "Lock is stale. Request approval to force-release, or investigate."
- If blockers exist: "Review open blockers before starting new work."

## Constraints

- **Read-only.** Do not modify any files.
- Do not clear or release locks.
- Do not commit, stash, or reset the working tree.
- Do not run engine code or start the server.
- Do not start, advance, or execute any phase.
- Do not run ingestion or research operations.
