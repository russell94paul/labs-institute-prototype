---
tags: [decision]
status: accepted
created: 2026-05-23
updated: 2026-05-23
---

# DEC-001: Subdirectory-per-app, not branch-per-app

## Context

Multiple apps will be built on Conductor (Labs Institute, GrooveNet, Neurospect). Initial approach was a separate git branch per app. Concern: framework improvements made while building one app wouldn't flow to others without rebasing.

## Decision

All apps live as subdirectories under `projects/` on the main branch. Each app gets its own project config, phase specs, wiki, and dashboard pages, but they share the Conductor engine, design system, and API layer.

## Consequences

- Framework improvements compound immediately — no merge/rebase overhead
- Apps can't diverge from each other's framework version
- Slightly more discipline needed to keep project-specific code isolated
- Easy to extract an app into its own repo later if needed
