# Branch Cleanup Classification Checklist

Use this checklist before removing old branch files.

## Keep Core
- Server/API entrypoints
- Session orchestration code
- Git/worktree helpers
- Agent definitions
- Existing pipeline/session templates
- Package manifests and lockfiles
- Tests relevant to Conductor runtime
- UI shell needed to run the app
- Environment examples with no real secrets

## Keep Roadmap
- Current Conductor platform roadmap docs
- Build Studio specs
- Product Onboarding Studio specs
- Multi-tenant/RLS/security docs
- Client Product Portal docs
- Trust-aware discovery/access docs
- Data Platform Modernization docs
- Market/Growth Engine docs
- Context/memory/self-improvement docs
- Infrastructure/deployment/ops docs
- Phase prompts and templates
- Build reports

## Remove Legacy
- Old product-specific pages/components/routes
- Old product-specific prompts/specs
- Old abandoned demo data
- Hard-coded references to the previous app idea
- Old process-specific assets that conflict with the new Conductor direction
- Generated artifacts from the abandoned branch that are not reusable

## Review Required
- Anything imported by current runtime code
- Anything containing data, credentials, or tokens
- Anything that may be useful as a generic reusable pattern
- Anything with unclear ownership/IP status
- Anything required by tests or build scripts

## Rule
When unsure, keep it and add it to the cleanup report as REVIEW_REQUIRED.
