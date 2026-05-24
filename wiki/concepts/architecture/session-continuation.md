---
tags: [architecture, sessions, interactive, continuation]
created: 2026-05-23
updated: 2026-05-23
---

# Session Continuation

Allows users to resume completed/failed sessions with additional direction.

## Why Not True Interactivity?

`claude -p` closes stdin after the initial prompt — it's a batch model. The CLI doesn't support follow-up input mid-session. Three alternatives were evaluated:

| Option | Verdict |
|---|---|
| Keep stdin open | Not viable — `-p` mode doesn't read stdin after initial prompt |
| MCP server for input requests | Viable but overengineered for current scale |
| **Session resume (chosen)** | Works within constraints, moderate complexity |
| Accept as batch | Default mode — continuation is the escape hatch |

## How It Works

1. Session completes (succeeded/failed/timeout)
2. User reviews output in dashboard
3. User types direction in "Continue Session" textarea
4. `POST /api/sessions/{sid}/continue` with `{"input": "..."}`
5. New session created in the **same worktree** with a continuation prompt
6. Continuation prompt includes: previous session output summary + user direction
7. New session linked: `continued_from: original_sid`

The key insight: **the worktree IS the context**. Code changes from the previous session are on disk. The prompt just needs to orient Claude.

## API

- `POST /api/sessions/{sid}/continue` — body: `{"input": "...", "budget_usd": 5.0}`

## Limitations

- Previous session's in-memory state (reasoning, tool results) is lost
- Context reconstructed from JSONL output (truncated to 8KB)
- Each continuation costs more (Claude re-reads the codebase)
- No auto-detection of "needs input" — user decides when to continue

## Related

- [[validation-engine]] — validation failure is a natural trigger for continuation
- [[rollback-mechanisms]] — rollback before continuing if work went off-track
