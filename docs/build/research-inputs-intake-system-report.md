# Research + Inputs Intake System — Build Report

**Date**: 2026-05-18
**Phase**: Research + Inputs Intake System
**Status**: Complete

---

## Files Created (37 total)

### docs/inputs/ (9 files)
| File | Purpose |
|------|---------|
| `README.md` | Directory guide and rules |
| `01-product-vision.md` | North Star vision, thesis, differentiators |
| `02-target-users.md` | User personas and segments |
| `03-use-cases.md` | Core use cases |
| `04-client-onboarding-flows.md` | Onboarding journey design |
| `05-current-aldc-service-inventory.md` | Service inventory template |
| `06-current-client-migration-notes.md` | Migration inventory table |
| `07-security-compliance-needs.md` | Security requirements |
| `08-demo-script.md` | Demo flow, screens, success criteria |
| `09-questions-for-deep-research.md` | Research question index |

### docs/research/ (12 files)
| File | Purpose |
|------|---------|
| `README.md` | Full research workflow guide |
| `research-index.md` | Topic index with links |
| `research-status.md` | Kanban status board |
| `synthesis-log.md` | Synthesis operation log |
| `syntheses/README.md` | Synthesis naming convention |
| `decisions/README.md` | Decision file format |
| `prompts/01-multi-tenant-saas-rls-client-portals.md` | Deep Research prompt |
| `prompts/02-agent-orchestration-dag-parallelization.md` | Deep Research prompt |
| `prompts/03-ai-product-onboarding-decision-simulation.md` | Deep Research prompt |
| `prompts/04-data-platform-modernization-factory.md` | Deep Research prompt |
| `prompts/05-context-memory-vector-db-self-improvement.md` | Deep Research prompt |
| `prompts/06-secure-credential-artifact-workflows.md` | Deep Research prompt |
| `prompts/07-market-intelligence-growth-engine.md` | Deep Research prompt |

### docs/prompts/ (2 files)
| File | Purpose |
|------|---------|
| `ingest-new-research-output.md` | Claude ingestion prompt |
| `synthesize-research-into-roadmap.md` | Roadmap synthesis prompt |

### config/ (1 file)
| File | Purpose |
|------|---------|
| `research-topics.json` | Machine-readable topic registry |

### local-inputs/ (2 files)
| File | Purpose |
|------|---------|
| `README.md` | Local inputs guide |
| `research-inbox/README.md` | Inbox instructions and expected filenames |

### docs/build/ (6 files)
| File | Purpose |
|------|---------|
| `change-manifest.md` | All files created/modified |
| `blockers.md` | Current blockers |
| `approval-requests.md` | Pending approvals |
| `parallelization-status.md` | Parallel work tracking |
| `rollback/research-inputs-intake-system-rollback.md` | Rollback instructions |
| `research-inputs-intake-system-report.md` | This report |

## Files Modified (1 total)

| File | Change |
|------|--------|
| `.gitignore` | Added `local-inputs/research-inbox/*` and `!local-inputs/research-inbox/README.md` |

---

## How to Use the Workflow

### Running Deep Research

1. Open `docs/research/research-status.md` to see what's pending
2. Pick the next priority topic (start with 01 or 02)
3. Open the corresponding file in `docs/research/prompts/`
4. Copy the "Deep Research Prompt" section
5. Paste into ChatGPT Deep Research and run
6. Save the output using the expected filename to `local-inputs/research-inbox/`

### Ingesting Research Output

1. After saving a research file to `local-inputs/research-inbox/`
2. Tell Claude Code: "Read and follow the prompt in `docs/prompts/ingest-new-research-output.md`"
3. Claude will create a synthesis, update tracking files, and extract decisions
4. Review the synthesis in `docs/research/syntheses/`

### Synthesizing into Roadmap

1. After 2-3 topics are synthesized and reviewed
2. Tell Claude Code: "Read and follow the prompt in `docs/prompts/synthesize-research-into-roadmap.md`"
3. Claude will create roadmap, phase dependencies, and risk register updates
4. Review before any implementation changes

---

## Next Manual Action for Paul

1. **Review the product vision** in `docs/inputs/01-product-vision.md` — refine or approve
2. **Run Deep Research for Topic 01** (Multi-Tenant SaaS) — copy prompt from `docs/research/prompts/01-multi-tenant-saas-rls-client-portals.md`
3. **Run Deep Research for Topic 02** (Agent Orchestration) — can run in parallel with Topic 01
4. **Fill in service inventory** in `docs/inputs/05-current-aldc-service-inventory.md` when ready

## Next Claude Action After Research Is Added

Run `docs/prompts/ingest-new-research-output.md` to synthesize the research output.

---

## Rollback Instructions

See `docs/build/rollback/research-inputs-intake-system-rollback.md` for full rollback procedures.

Quick rollback: `git revert <commit-hash>` if committed as a single commit.

---

## Risks / Limitations

| Risk | Mitigation |
|------|-----------|
| Deep Research quality varies | Synthesis step extracts and validates — bad research gets flagged |
| Research topics may have wrong priorities | Priorities are configurable in `config/research-topics.json` — adjust after reviewing |
| Raw research files could contain sensitive info | Inbox is gitignored; ingestion prompt checks for secrets |
| Product vision is a draft | Marked for review in `docs/build/approval-requests.md` |
| No product features were implemented | By design — this phase is documentation and workflow only |
