# Neurospect Wiki — Schema

You are maintaining Paul Russell's Neurospect sub-wiki. Neurospect is a personal trading-journal and AI-coaching project (ICT / Smart Money Concepts). This wiki is the persistent knowledge base for the project: source data (mentor video transcripts), course/strategy concepts, app architecture, decisions, and operational notes.

## Isolation Rule (read first)

This wiki is **fully decoupled** from Paul's ALDC / Analytic Labs work wiki at `C:\Users\PaulRussell\repos\wiki`.

- **No outbound references to ALDC business logic, architecture, client information, or concepts.** Do not link to ALDC client pages, tools, deployment runbooks, or business rules from anywhere in this wiki.
- **The single allowed inbound reference is ALDC research → Neurospect.** AI / app design research from the ALDC wiki may be reused here. Currently this manifests as: the distributed-workflow pattern docs at `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\` are referenced by absolute path (never by `[[wikilink]]`) from this wiki's tracker(s).
- **Do not write into the ALDC wiki from any Neurospect session.** Lane is the `wiki/` directory of the `neurospect` monorepo. Cross-lane edits to `../api/` or `../app/` are allowed in cross-cutting PRs (e.g., the Architecture Doc Integrity rule below), but other workstreams' code-only changes are out-of-lane.

If you find Neurospect content sitting inside the ALDC wiki (legacy: `C:\Users\PaulRussell\repos\wiki\entities\projects\neurospect.md`), it should be migrated here and removed from the ALDC wiki — that's the kickoff workstream's first task.

## Purpose

This wiki exists so any Claude Code session pointed at this directory can immediately understand:

- What Neurospect is and what stage it's at
- The ICT / Smart Money Concepts strategy (concepts, narratives, day-of-week / liquidity / news framing)
- The mentor video corpus (sources, transcripts, structured course KB)
- The application architecture (journal, analytics, AI coach, future live commentary)
- Decisions made and why
- Operational state (what's deployed, what's in flight, what's blocked)

## Directory Structure

This wiki lives at `wiki/` inside the `neurospect` monorepo. Sibling dirs `../api/` (FastAPI backend) and `../app/` (React frontend) hold the code; the wiki holds the docs, decisions, transcripts, and trackers.

```
wiki/
├── CLAUDE.md              # THIS FILE — read first, always
├── index.md               # Master catalog
├── log.md                 # Append-only operation log
├── sources/               # RAW SOURCES — immutable
│   └── neurospect/        # Video transcripts, mentor materials
├── vault/                 # CREDENTIALS — gitignored, never expose
├── entities/              # One page per distinct thing
│   ├── projects/          # neurospect.md (top-level project entity)
│   ├── tools/             # Future: brokers, data feeds, libraries
│   └── people/            # Mentor(s), contacts
├── concepts/              # Ideas, strategy, architecture
│   ├── architecture/      # App design, data model, AI coach architecture
│   ├── business-logic/    # ICT concepts, narratives, strategy rules
│   └── patterns/          # Recurring trading or app patterns
├── processes/             # Step-by-step runbooks
│   ├── distributed-workflow/  # Active workstream trackers (mirrors ALDC pattern)
│   └── operations/        # Future: data pipelines, model retraining, etc.
├── tickets/               # One page per ticket if/when ticketing is adopted
├── daily/                 # Daily notes, POAs
└── assets/                # Images, charts
```

## Page Format

```markdown
---
tags: [entity, neurospect]
aliases: [Alternative Name]
sources: [sources/neurospect/path/to/transcript.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Page Title

Brief one-paragraph summary.

## Section

Content with [[wikilinks]] to related pages within this wiki only. Cross-wiki references (to the ALDC research/pattern docs) use absolute paths, never wikilinks.

## See Also

- [[Related Page 1]]
- [[Related Page 2]]
```

### Conventions

- `[[wikilinks]]` for internal cross-references **within this wiki only**.
- Cross-wiki references use full absolute paths.
- Tags in YAML frontmatter, not inline.
- Cite sources for factual claims (transcript file, mentor video, paper, etc.).
- One page per entity/concept/process — update existing rather than duplicate.
- Split pages over ~200 lines into focused sub-pages.

## Core Operations

### 1. Ingest

Mirror of the ALDC wiki's ingest operation, scoped to Neurospect-only sources:

1. Read source file(s) thoroughly.
2. Extract entities (mentors, brokers, instruments), concepts (ICT narratives, liquidity rules, day-of-week framing), and processes (journaling workflow, trade-review checklist).
3. Check this wiki's `index.md` for existing pages; update or create per [[CLAUDE|Page Format]].
4. Cross-reference with `[[wikilinks]]` (in this wiki only).
5. Update `index.md`. Append a row to `log.md`.

### 1b. Ingest Daily Notes

When Paul says "ingest today's neurospect notes" or similar:

1. Read `daily/YYYY-MM-DD.md`.
2. Parse `## Note` blocks (same format as the ALDC wiki's daily template).
3. Route to the right page; same explicit + heuristic action-item extraction.
4. Update target pages, cross-reference, append to `log.md`.

A future `action-items.md` may be added once daily-note ingest is in regular use here. Don't add it preemptively.

### 2. Query

Search and synthesize from this wiki only. If a question requires ALDC context, surface that explicitly — do not silently pull ALDC content into Neurospect answers.

### 3. Lint

Periodic health check. Same categories as the ALDC wiki: orphans, stale info, missing cross-refs, index gaps, contradictions, empty sections. **Additional Neurospect-specific check:** any wikilink, citation, or content reference pointing back into the ALDC wiki — flag and remove (the only allowed cross-wiki reference is ALDC research → Neurospect, by absolute path, in trackers).

## Distributed Workflow

This wiki uses the same parallel-sessions pattern documented in the ALDC wiki. The pattern docs live there and are referenced by absolute path:

- Pattern: `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
- Lifecycle: `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md`
- Template: `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\tracker-template.md`

Trackers for this wiki live at `processes/distributed-workflow/active/`.

## Architecture Doc Integrity

### Source-of-truth hierarchy

Once code exists in `../api/` or `../app/`, the **code is the ground truth**. Architecture docs in this wiki describe the design **as implemented** — not as originally planned.

If an implementation session makes a better decision than what the wiki says, the session MUST update the relevant wiki doc(s) before marking the workstream phase as complete. Tracker session logs are not a substitute for updating the architecture doc itself.

### Canonical doc per topic

Each architectural topic has ONE canonical doc. Other docs may link to it but must not restate its content (restating creates drift). When two docs disagree, the canonical doc wins and the stale doc must be updated or retired.

| Topic | Canonical doc | Notes |
|---|---|---|
| Trade data model (DDL, ENUMs, indexes, API surface) | `concepts/architecture/trade-schema.md` | |
| Backend project layout, deps, auth flow | `concepts/architecture/phase2-project-structure.md` | Supersedes `tech-stack.md` §2-4 |
| AI Coach pipeline (webhook, Claude, polling) | `concepts/architecture/tradingview-connector.md` | Supersedes `tech-stack.md` §5 |
| Env vars | `../api/.env.example` | Wiki docs should reference, not duplicate |
| R2 storage key pattern | `concepts/architecture/phase2-project-structure.md` | Supersedes `tech-stack.md` §6 |

When the canonical doc is a code file (e.g. `.env.example`), wiki docs should reference it rather than duplicating its content.

### Post-implementation reconciliation (mandatory)

Any session that writes code in `../api/` or `../app/` must, before signing off:

1. Re-read every wiki page listed in the active tracker's "See Also" section.
2. Diff claims in those pages against the actual code.
3. Update any page where the code diverges from the wiki.
4. If a page cannot be fixed in this session, add `stale_warning:` to its frontmatter (see below).

This is not optional. Stale architecture docs are worse than no docs — they cause future sessions to build the wrong thing.

### Staleness markers

If a wiki doc is known to be out of date but cannot be fixed in the current session:

1. Add to frontmatter: `stale_warning: "<what's stale and why — one line>"`
2. Add a visible warning at the top of the page body (below the frontmatter):
   `> **STALE:** <what's stale>. See <canonical doc> for current state.`
3. Remove both markers once the doc is reconciled.

Sessions MUST check for `stale_warning` in frontmatter when reading any architecture doc. If present, read the canonical doc instead and do not trust the stale content.

## Context Management

When context usage exceeds **50%**, proactively tell Paul:

> Context is over 50%. Recommend starting a new session to avoid degraded performance. Here's a summary of what's done and what's remaining: [summary].

Do not wait to be asked. Include enough handoff context (what was completed, what's next, any open decisions) so the new session can pick up cleanly.

## Rules

1. **Never modify files in `sources/`.** They are immutable raw material.
2. **Never expose credentials outside `vault/`.** Pages may reference credentials by name, never by value.
3. **Always update `index.md`** when creating or significantly updating a page.
4. **Always append to `log.md`** for ingest and lint operations.
5. **Prefer updating over creating.** Check `index.md` before making a new page.
6. **Flag contradictions explicitly.** Never silently overwrite.
7. **Cite sources.** Every factual claim should trace to a source file or transcript.
8. **Respect the Isolation Rule.** No ALDC content in this wiki except ALDC research consumed via absolute paths in trackers.
9. **Reconcile after implementation.** Any session that modifies `neurospect-api` must run the post-implementation reconciliation checklist (see §Architecture Doc Integrity) before signing off.
10. **Never trust a stale doc.** If a page has `stale_warning:` in its frontmatter, read the canonical doc instead.

## Paul's Preferences

- Handles git commits himself — never run `git commit`.
- Prefers detailed step-by-step guidance for UI operations.
- Prefers concise output for code and git operations.
