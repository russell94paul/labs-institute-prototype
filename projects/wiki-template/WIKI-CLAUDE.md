# Project Wiki — Conventions

Per-project wiki that lives at `projects/<slug>/wiki/`. Same format as the global wiki at `repos/wiki` but scoped to a single Conductor-managed project.

## Page Format

```markdown
---
tags: [decision, architecture, learning, incident, pattern]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [session-id, url, or reference]
---

# Page Title

Content here. Use [[wikilinks]] for cross-references within the project wiki.
```

## Directory Structure

```
projects/<slug>/wiki/
├── index.md              # Master catalog of all pages
├── log.md                # Append-only operation log
├── decisions/            # ADRs and design choices
├── learnings/            # What worked, what failed, why
├── patterns/             # Reusable patterns discovered during build
├── incidents/            # Bugs, outages, debugging sessions
└── context/              # Domain knowledge, business rules, constraints
```

## Decision Records

Decisions use a lightweight ADR format:

```markdown
---
tags: [decision]
status: proposed | accepted | superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# DEC-NNN: Title

## Context
What prompted this decision.

## Decision
What we decided and why.

## Consequences
What changes as a result. Trade-offs accepted.
```

## Learning Entries

Learnings capture what worked and what didn't:

```markdown
---
tags: [learning]
type: success | failure | discovery
created: YYYY-MM-DD
session: session-id-if-applicable
---

# Title

## What happened
Brief description.

## Why it matters
Impact on future work.

## Action
What to do differently / what to keep doing.
```

## Vector DB Alignment

Learning and decision entries are structured to feed into zeus-memory when the vector integration lands:
- Each entry becomes a retrievable memory chunk
- Tags and metadata enable filtered retrieval by type, date, and topic
- Wikilinks create a knowledge graph that maps to entity relationships
- The `sources` field provides provenance tracing back to sessions and artifacts

## When to Update

- **After every phase completion** — what was built, decisions made, patterns discovered
- **After incidents** — root cause, fix, prevention
- **After design decisions** — even small ones, if they'd confuse a future session
- **After failed approaches** — what was tried and why it didn't work

## Operations

- **Add**: Create page → update index.md → append to log.md
- **Update**: Edit page → update `updated:` date → append to log.md
- **Query**: Check index.md → read relevant pages → follow wikilinks
