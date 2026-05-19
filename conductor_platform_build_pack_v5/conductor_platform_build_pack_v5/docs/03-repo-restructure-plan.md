# Repo Restructure Plan

## Goal

Make the repo understandable to humans and agents while avoiding destructive moves.

## Proposed structure

```text
conductor/
  apps/
    web/
    server/
  packages/
    core/
    pipelines/
    events/
    agents/
    build-studio/
    onboarding/
    client-portal/
    access-manager/
    data-modernization/
    market-growth/
    context-memory/
    infra-ops/
    self-improvement/
    shared/
  configs/
    agents/
    pipelines/
    phase-templates/
    policies/
  docs/
    architecture/
    decisions/
    roadmap/
    prompts/
    build/
    reference-repos/
    client-portal/
    context-manager/
    data-modernization/
    growth/
    security/
  templates/
    reports/
    prompts/
    phase-outputs/
  tests/
    unit/
    integration/
    e2e/
    fixtures/
  migrations/
  scripts/
  local_state/
```

## Migration rules

1. Inspect before moving.
2. Create docs/config/template directories first.
3. Do not move runtime code unless imports and tests are updated.
4. Add README files to module directories.
5. Run checks after code moves.
6. Document everything in docs/build/.
