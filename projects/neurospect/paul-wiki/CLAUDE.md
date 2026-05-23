# Paul's NeuroSpect Wiki

Personal working wiki for Paul. Obsidian vault for research-in-progress, daily notes, and working documents.

## Purpose

This is **personal working memory** — not the team source of truth. Use this for:
- Research and exploration before it's ready to share
- Architecture decision drafts
- Implementation journal (what was tried, what worked, what didn't)
- Daily/weekly working notes
- Scratch work and temporary notes

When a page matures, promote it to `wiki/` (the team wiki) by adding `promote: true` to its frontmatter.

## Structure

```
paul-wiki/
├── .obsidian/           # Obsidian vault config
├── CLAUDE.md            # This file
├── index.md             # Master index
├── research/            # Research notes (any domain: technical, product, market)
├── decisions/           # Decision records (DEC-NNN-short-title.md)
├── journal/             # Daily/weekly working notes (YYYY-MM-DD.md)
├── components/          # Per-component working docs (backtesting, neuroquant, etc.)
└── scratch/             # Temporary notes (gitignored)
```

## Conventions

- YAML frontmatter on all pages: `tags`, `created`, `updated`
- `[[wikilinks]]` for internal cross-references within this wiki
- Absolute paths for references to `wiki/`, `vlad-wiki/`, or code
- Daily journal entries: `journal/YYYY-MM-DD.md`
- Decision records: `decisions/DEC-NNN-short-title.md`
- Add `promote: true` to frontmatter when a page is ready for the team wiki

## Cross-Wiki Intelligence

NeuroCore indexes this wiki alongside Vlad's wiki and the team wiki. When working on a component, relevant content from other wikis may be surfaced automatically. Content tagged `promote: true` is prioritized for cross-wiki visibility.

## End-of-Session Rule

Before ending any session that modifies this wiki, code, or tickets, offer to run both `/sync` and `/lint`:

1. **`/sync`** — Updates tickets, boot prompts, phase status, and flags cross-wiki content from this session's work.
2. **`/lint`** — Checks that all roadmap artifacts are consistent. As you add ideas, rename components, and reorganize phases, changes touch multiple files but not always all of them at once. `/lint` catches that drift before the next session inherits stale or conflicting context.

## What Does NOT Belong Here

- Canonical ICT concepts or architecture docs (those go in `wiki/`)
- Secrets, credentials, or API keys
- Large binary files (charts, screenshots → use `wiki/assets/` or R2)
