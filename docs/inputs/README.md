# Product Inputs

These are non-secret product inputs that guide Conductor's roadmap, onboarding design, and platform architecture.

## Rules

- **Do NOT add** credentials, API keys, raw client secrets, `.env` values, or private data to any file in this directory.
- Reference credentials by name only (e.g., "GEP Snowflake service account") — never paste actual values.
- These files are committed to the repo and visible to all collaborators.

## Contents

| File | Purpose |
|------|---------|
| `01-product-vision.md` | North Star vision, thesis, differentiators |
| `02-target-users.md` | User personas and segments |
| `03-use-cases.md` | Core use cases and workflows |
| `04-client-onboarding-flows.md` | Onboarding journey design |
| `05-current-aldc-service-inventory.md` | Current service inventory template |
| `06-current-client-migration-notes.md` | Migration inventory and gap analysis |
| `07-security-compliance-needs.md` | Security and compliance requirements |
| `08-demo-script.md` | Demo flow, screens, success criteria |
| `09-questions-for-deep-research.md` | Questions to feed into Deep Research |

## How these are used

1. Product inputs inform the Deep Research prompts in `docs/research/prompts/`.
2. Research outputs are synthesized and fed back into these inputs to refine them.
3. The Bootstrap Console / Build Studio reads these to generate phases and tasks.
