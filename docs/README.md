# Conductor Platform Documentation

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `inputs/` | Non-secret product inputs (vision, personas, use cases, demo, inventory) |
| `research/` | Deep Research prompts, syntheses, decisions, status tracking |
| `architecture/` | Architecture documents and policies |
| `decisions/` | Architecture Decision Records (ADRs) |
| `prompts/` | Claude Code execution prompts (ingestion, synthesis, design) |
| `build/` | Build tracking (change manifest, blockers, approvals, rollback, reports) |
| `reference-repos/` | Cross-repo analysis and integration opportunities |
| `checklists/` | Pre-build and compliance checklists |
| `templates/` | Reusable document templates |

## Build Pack

The source-of-truth build pack is at:

```
conductor_platform_build_pack_v5/conductor_platform_build_pack_v5/
```

It contains the master build sequence, architecture docs, prompt files, ADRs, checklists, and templates for the Conductor platform rebuild.
