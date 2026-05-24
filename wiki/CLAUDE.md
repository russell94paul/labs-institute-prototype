# Conductor Wiki

Project knowledge base for the Conductor product orchestrator. Documents architecture decisions, session learnings, and cross-cutting patterns.

## Structure

```
wiki/
├── index.md                    # Master page index
├── concepts/architecture/      # System architecture docs
├── decisions/                  # Decision records (DEC-NNN-title.md)
├── processes/                  # Operational runbooks
└── sessions/                   # Session work logs (significant sessions only)
```

## Conventions

- YAML frontmatter: `tags`, `created`, `updated`
- `[[wikilinks]]` for cross-references
- One page per concept — update existing rather than duplicate
- Session logs only for significant work (new features, architecture changes)
