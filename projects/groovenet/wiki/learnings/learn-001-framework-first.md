---
tags: [learning]
type: discovery
created: 2026-05-23
---

# Build the framework before building apps on it

## What happened

Started building GrooveNet (P0 event discovery) directly. Realized the framework itself needs to be more solid before stacking app-specific features on it.

## Why it matters

Each app built on Conductor exposes what the framework actually needs — API patterns, data model abstractions, dashboard components. Building the framework first means each subsequent app is faster and more consistent.

## Action

Focus on getting Conductor's core patterns right (project registry, per-project data layer, wiki system, phase management) before starting Labs Institute P0. The GrooveNet prototype serves as a reference for what an app needs from the framework.
