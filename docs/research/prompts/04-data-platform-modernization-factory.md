# Deep Research Prompt: Data Platform Modernization Factory

## Purpose

Research best practices for modernizing an existing managed data service stack, informing Conductor's migration workflow, parity testing, and dual-run strategy.

## When to Run

Run after Topics 1 and 2 (Priority 4). This is directly relevant to the ALDC proof case.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research best practices for modernizing an existing managed data service that currently uses API connectors, Prefect pipelines, Snowflake data warehouse, data models, and Power BI dashboards. The goal is to migrate current clients to an optimized platform without functionality regression.**

Context: I'm building a product orchestration platform (called "Conductor") and the first proof case is migrating my own company's (ALDC) data service stack onto it. 

Current architecture:
- API connectors pull data from client source systems
- Prefect orchestrates data pipeline flows (extract, transform, load)
- Snowflake is the data warehouse (multiple schemas, some with RLS)
- Power BI provides dashboards and reports to clients
- Credentials are currently managed manually (1Password, environment variables)
- Some pipelines are undocumented; some have known failure modes

Multiple clients share the infrastructure but with per-client schemas and workspaces. The migration must be zero-downtime for existing clients.

I need to understand:

1. **Target architecture** — what does a modern, well-architected version of this stack look like? How do the components (connectors, orchestration, warehouse, BI) map to Conductor's platform model? What should be consolidated, what should be separated?

2. **Migration phases** — how to break a migration like this into phases. What order to migrate components. How to handle dependencies between components during migration (e.g., a new pipeline writing to Snowflake while old Power BI reports still read from it).

3. **Current-state inventory template** — what information needs to be captured about every existing service, pipeline, table, report, and credential before migration begins. How to automate inventory capture vs. manual documentation.

4. **Artifact gap analysis template** — how to identify what's missing, undocumented, or broken in the current state. How to prioritize gaps (critical path vs. nice-to-have). How to handle services that work but nobody understands.

5. **Parity testing framework** — how to validate that the migrated system produces identical results to the old system. Data comparison strategies for large datasets. Report comparison strategies. How to handle acceptable differences vs. regressions.

6. **Dual-run strategy** — how to run old and new pipelines in parallel during migration. How to compare outputs. How long to dual-run. How to handle divergence. Cost implications of running two systems.

7. **Rollback strategy** — how to roll back a migration phase if something goes wrong. What needs to be preserved for rollback to work. How to test rollback procedures.

8. **Operational monitoring plan** — what to monitor during and after migration. Health checks, data freshness, pipeline success rates, report accuracy. Alerting thresholds. Client-facing status pages.

Provide your output as a structured report with:
- Target architecture (with diagram description)
- Migration phases (ordered, with dependencies)
- Current-state inventory template
- Artifact gap analysis template
- Parity testing framework
- Dual-run strategy
- Rollback strategy
- Operational monitoring plan

Reference real migration case studies where possible. Include specific Snowflake, Prefect, and Power BI considerations.

---

## Expected Output Filename

`04-data-platform-modernization-factory.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Migration workflow design
- Service inventory templates (see `docs/inputs/05-current-aldc-service-inventory.md`)
- Parity testing approach
- Dual-run infrastructure
- Client communication during migration
- Rollback procedures
- Operational monitoring
