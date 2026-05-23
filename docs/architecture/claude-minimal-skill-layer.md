# Claude Minimal Skill Layer

## Why minimal skills now

The Conductor platform is mid-build. P0 (Pipeline DAG Engine) and P0.5 (Work Guard) are complete, but the phase execution APIs, event system (P0-events), and Build Studio (P1) are not yet built. Skills that wrap phase execution or autonomous operations would be premature — the underlying APIs will change as those phases ship.

The three skills created now wrap **read-only status checks** and **documentation workflows** that are already stable:
- Git state inspection
- Phase status reading (`config/phase-status.json`)
- Work Guard status checking (lock file + policy)
- Session handoff creation (markdown docs)

These are safe to ship because they don't depend on APIs that will change.

## Why the full skill library is deferred

The following skills are intentionally **not** created until after P1 Build Studio:

| Deferred skill | Reason |
|----------------|--------|
| `/phase-advance` | Phase execution API not yet stable |
| `/run-phase` | Requires event system (P0-events) for monitoring |
| `/run-autonomous` | Requires Work Guard integration with sessions + pipeline engine |
| `/deploy` | No deployment pipeline exists yet |
| `/merge` | Branch strategy not finalized for multi-phase work |
| `/create-pr` | PR workflow depends on Build Studio review gates |

These skills should be created after:
1. P0-events (Event System + SSE) is complete
2. P1-build-studio MVP ships
3. The phase execution and session lifecycle APIs stabilize
4. Work Guard is integrated with session auto-acquire/release

## Available skills

### /conductor-start

**Purpose:** Start a Conductor session safely with full status context.

**Reads:**
- `AGENTS.md`, `docs/AGENT_ENTRYPOINT.md` (if they exist)
- Git status and branch
- `config/phase-status.json`
- `config/work-guard-policy.json`
- `.conductor/runtime/session-lock.json` (if present)
- Latest session handoff from `docs/build/session-handoffs/`
- `docs/build/blockers.md`
- `docs/build/approval-requests.md`

**Modifies:** Nothing. Read-only.

**Use when:** Beginning any Conductor work session.

### /conductor-work-guard

**Purpose:** Check whether it is safe to start another task or session.

**Reads:**
- Git status, branch, latest commit
- `.conductor/runtime/session-lock.json`
- `config/work-guard-policy.json`
- `docs/build/blockers.md`
- `docs/build/approval-requests.md`

**Modifies:** Nothing. Read-only.

**Use when:** Before starting new work, mid-session safety checks, or when unsure if another session is active.

### /conductor-handoff

**Purpose:** Create a session handoff document.

**Reads:**
- Git status, branch, recent commits, diff stats
- `config/phase-status.json`
- `docs/build/blockers.md`
- `docs/build/approval-requests.md`

**Modifies:**
- Creates `docs/build/session-handoffs/<name>-handoff.md`
- May append to `docs/build/change-manifest.md`

**Use when:** End of a work session, before compacting or switching sessions.

## What skills must never touch

All three skills are prohibited from modifying:
- `engine/` — no engine code changes
- `dashboard/` — no dashboard changes
- `config/phase-status.json` — no phase state changes
- `config/work-guard-policy.json` — no policy changes
- `.conductor/runtime/` — no lock file changes
- Any secrets, `.env` files, or credentials
- Git state (no commits, pushes, resets, branch creation)

The only write-capable skill is `/conductor-handoff`, limited to creating handoff documents and appending to the change manifest.
