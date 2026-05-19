# Current Client Migration Notes

## Migration Inventory

| Category | What we have | Missing | Risk | Priority | Owner | Evidence/Source | Client approval needed? | Notes |
|----------|-------------|---------|------|----------|-------|----------------|------------------------|-------|
| Source APIs | | | | | | | | |
| Prefect flows | | | | | | | | |
| Snowflake schemas | | | | | | | | |
| Snowflake tables/views | | | | | | | | |
| Power BI workspaces | | | | | | | | |
| Power BI reports | | | | | | | | |
| Semantic models | | | | | | | | |
| Credentials/access (references only) | | | | | | | | |
| Dashboards | | | | | | | | |
| Known failures | | | | | | | | |
| Must-not-break metrics | | | | | | | | |
| Current SLAs | | | | | | | | |
| Support processes | | | | | | | | |
| Compliance constraints | | | | | | | | |

## Migration Principles

1. **No functionality regression** — every current dashboard, pipeline, and report must work identically or better after migration.
2. **Dual-run before cutover** — run old and new pipelines in parallel until parity is validated.
3. **Client communication** — clients must be informed and approve any changes that affect their access or data.
4. **Credential isolation** — never copy credentials between systems. Request fresh credentials through secure workflows.
5. **Rollback plan** — every migration phase must have a documented rollback procedure.

## Per-Client Migration Status

### [Client Name]

**Status**: Not started / In progress / Dual-run / Cutover complete

| Phase | Status | Start date | End date | Blocker | Notes |
|-------|--------|-----------|----------|---------|-------|
| Inventory | | | | | |
| Gap analysis | | | | | |
| Credential requests | | | | | |
| Pipeline migration | | | | | |
| Dual-run | | | | | |
| Parity validation | | | | | |
| Client approval | | | | | |
| Cutover | | | | | |
| Old system decommission | | | | | |
