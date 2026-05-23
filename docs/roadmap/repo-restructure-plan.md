# Repo Restructure Plan

## Goal

Make the repo understandable to humans and agents while avoiding destructive moves.

## Current structure (active)

```
conductor/
  engine/              # Python backend (server, sessions, pipelines, phases, agents, context, scaffolder)
  dashboard/           # Vanilla HTML/CSS/JS SPA (index.html, pages/, styles/)
  agents/              # Agent definitions (.md files)
  templates/           # Pipeline + stack templates
  shared/prompts/      # Reusable prompt fragments
  config/              # Research topics, phase configs
  docs/                # Architecture, decisions, roadmap, research, inputs, build, prompts
  local-inputs/        # Gitignored research inbox
```

## Proposed future structure (from build pack)

```
conductor/
  apps/web/            # Dashboard SPA
  apps/server/         # Python backend
  packages/            # Feature modules (core, pipelines, events, agents, build-studio, etc.)
  configs/             # Agents, pipelines, phase-templates, policies
  docs/                # Full documentation tree
  templates/           # Reports, prompts, phase outputs
  tests/               # Unit, integration, e2e, fixtures
  migrations/          # Schema migrations
  scripts/             # Utility scripts
```

## Migration rules

1. Inspect before moving.
2. Create docs/config/template directories first.
3. Do not move runtime code unless imports and tests are updated.
4. Add README files to module directories.
5. Run checks after code moves.
6. Document everything in docs/build/.

## Current status

Docs/config/template structure has been created. Runtime code (`engine/`, `dashboard/`) remains in its current location and continues to work. The monorepo restructure to `apps/packages/` will be done in a future phase when the pipeline engine and test infrastructure are in place to validate the move.
