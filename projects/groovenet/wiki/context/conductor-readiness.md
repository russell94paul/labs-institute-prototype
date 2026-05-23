---
tags: [context, architecture]
created: 2026-05-23
updated: 2026-05-23
sources: [docs/build/p3-plus-roadmap-planning-report.md, docs/roadmap/master-build-sequence.md]
---

# Conductor Framework Readiness for App Building

## What's Done (P0-P2 + Session 2026-05-23)

### Core Engine
- Pipeline DAG engine with dependency resolution
- Phase manager (markdown with YAML frontmatter)
- Event system + SSE pub/sub
- Session orchestrator (Claude Code lifecycle)
- Work Guard (repo lock + safety checks)

### App Framework (added 2026-05-23)
- Project registry (`projects/<slug>/project.json`)
- Per-project wiki (decisions, learnings, patterns, context)
- Per-project memory store (zeus-memory lite — store/search/recall/evidence)
- GrooveNet P0 prototype (event discovery, set tracker, matching)
- API CRUD patterns for project-specific data
- Dashboard SPA with routing + design system

### What's NOT Needed Before Building Apps
The full P3-P15 roadmap (Phase Template OS, Agent Runtime, Multi-Tenant RLS, Client Portal, etc.) is for Conductor-as-a-SaaS-product. For building individual apps, the current framework is sufficient.

### What Might Be Needed During App Building
- **Phase Template OS (P3)** — if we want structured phase execution with automated pipelines. Can be built incrementally as needed.
- **Context + Memory Core (P5)** — lightweight version already exists. Upgrade to postgres/zeus-memory when app data outgrows JSON files.
- **Agent Runtime (P4)** — only needed when we want autonomous parallel work streams.

## Build Order

1. Conductor framework (done enough to start)
2. Labs Institute — DJ artist management portal
3. GrooveNet — DJ collective cross-collaboration
4. Neurospect — TBD

## Decision

Start building Labs Institute now. Add Conductor framework features as the app build exposes real needs, not speculatively from the roadmap. See [[DEC-001-subdirectory-not-branch]] for project isolation approach.
