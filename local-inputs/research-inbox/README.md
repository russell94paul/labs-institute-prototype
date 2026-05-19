# Research Inbox

Drop Deep Research output files here for Claude to ingest.

## Expected filenames

| Topic | Filename |
|-------|----------|
| 01 — Multi-Tenant SaaS | `01-multi-tenant-saas-rls-client-portals.report.md` |
| 02 — Agent Orchestration | `02-agent-orchestration-dag-parallelization.report.md` |
| 03 — AI Onboarding | `03-ai-product-onboarding-decision-simulation.report.md` |
| 04 — Data Modernization | `04-data-platform-modernization-factory.report.md` |
| 05 — Context & Memory | `05-context-memory-vector-db-self-improvement.report.md` |
| 06 — Secure Credentials | `06-secure-credential-artifact-workflows.report.md` |
| 07 — Market Intelligence | `07-market-intelligence-growth-engine.report.md` |

## After saving a file here

Run the ingestion prompt in Claude Code:

```
Read and follow the prompt in docs/prompts/ingest-new-research-output.md
```

## Important

- Files in this directory (except this README) are gitignored
- Do NOT place credentials or secrets in research files
- Do NOT delete files after ingestion — they serve as source-of-truth for the raw research
