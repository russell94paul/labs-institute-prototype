# conductor-handoff

Create a session handoff document summarizing completed work for the next session.

## When to use

At the end of a work session, before compacting context or starting a new session. Captures what was done, what changed, and what comes next.

## Steps

1. Run `git branch --show-current`.
2. Run `git log -1 --oneline` to get the latest commit.
3. Run `git diff --stat HEAD~1` (or appropriate range) to identify files changed in this session. If the session spans multiple commits, adjust the range.
4. Summarize the work completed in this session — what was built, fixed, or configured.
5. List commands, tests, or checks that were run and their results.
6. Read `docs/build/blockers.md` — note any open blockers.
7. Read `docs/build/approval-requests.md` — note any pending approvals.
8. Read `config/phase-status.json` — identify the current phase and next recommended phase.
9. Determine rollback notes — what would need to be reverted if this session's work is rejected.
10. Recommend whether to: continue in this session, compact context, or start a new session.

## Output

Save the handoff file to `docs/build/session-handoffs/<phase-or-task>-handoff.md` using this format:

```markdown
# Session Handoff — <Title>

**Phase:** <phaseId or task name>
**Date:** <YYYY-MM-DD>
**Branch:** <branch>
**Latest commit:** <hash> <message>
**Status:** <completed | partial | blocked>

## What Was Done

<Summary of work completed>

## Files Changed

| File | Change |
|------|--------|
| <path> | <created/modified/deleted — brief description> |

## Commands/Checks Run

- <command> — <result>

## Blockers

<Open blockers or "None">

## Approvals Needed

<Pending approvals or "None">

## Rollback Notes

<What to revert and how, or "Clean addition — delete created files">

## Recommended Next Steps

| Priority | Action | Description |
|----------|--------|-------------|
| A | <action> | <description> |

## Session Recommendation

<Continue | Compact context | New session> — <reason>
```

11. If the work is significant enough to warrant a change manifest entry, append to `docs/build/change-manifest.md` with the same section format used by previous entries.

## Constraints

- Do not proceed into the next phase.
- Do not start new implementation work.
- Do not modify engine, dashboard, or config files (except `docs/build/change-manifest.md`).
- Do not commit or push — the handoff document itself should be part of the user's next commit.
- Allowed to create: the handoff file and a change-manifest entry. Nothing else.
