# Neurospect Daily Notes Template

Copy this file as `YYYY-MM-DD.md` (e.g., `2026-04-18.md`) and add notes throughout the day. When ready, ask Claude to "ingest today's neurospect notes" — it will read each entry and update the correct wiki pages.

---

## How to use

Each note is a `## Note` block with a `type:` tag. Write naturally — the type tag tells Claude where the note belongs in the wiki.

**Types:**

| Type | Where it goes | Use when... |
|------|--------------|-------------|
| `concept` | `concepts/business-logic/` | An ICT concept, narrative, or strategy rule |
| `architecture` | `concepts/architecture/` | App architecture / data model / AI coach design notes |
| `transcript` | `sources/neurospect/` (and a derived concept page) | A new mentor video transcript or excerpt |
| `decision` | Relevant page | An architectural / scope / strategy choice |
| `tool` | `entities/tools/` | Broker, data feed, library, charting tool |
| `idea` | Depends on content | Feature ideas, app ideas, study ideas |
| `general` | Claude decides | Anything that doesn't fit above |
| `action` | Future `action-items.md` | Guarantee a TODO is captured |

**Minimal format:**

```markdown
## Note
type: concept
ref: ict-day-of-week

Tuesday is typically the manipulation day relative to weekly opening price.
Avoid trading reversals on Tuesday before London close — wait for confirmation.
```

That's it. You don't need headers, formatting, or complete sentences.

---

When you tell Claude "ingest today's neurospect notes", it will:

1. Read the daily file.
2. For each `## Note` block, identify the target wiki page from `type:` + `ref:`.
3. Update that page (or create one if needed).
4. Add cross-references via `[[wikilinks]]` (within this wiki only).
5. Update `index.md` if any new pages were created.
6. Append to `log.md`.
7. The daily file itself stays in `daily/` as a permanent record.

Per the Isolation Rule in [[../CLAUDE]], never link out to ALDC wiki content from these notes or from any page they generate.
