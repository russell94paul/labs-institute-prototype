# Decision: DEC-001 — Default Tenancy Model

## Context
Conductor needs a multi-tenant data architecture. The choice affects every table, query, migration, and isolation boundary in the platform.

## Options
1. **Shared schema + RLS (recommended)** — One database, one schema, `tenant_id` on every row, PostgreSQL RLS policies enforce isolation. Lowest operational overhead, simplest migrations, strongest fit for MVP through meaningful scale. Highest blast radius if misconfigured.
2. **Schema-per-tenant** — One database, each tenant gets its own schema. Cleaner export/restore, but migration drift risk and harder connection pooling.
3. **Database-per-tenant** — Strongest data boundary. Per-tenant backup/encryption/retention is easier. Highest operational overhead, expensive for small tenants.
4. **Hybrid: pooled default + bridge-by-exception** — Start with shared schema + RLS, add `tenants.isolation_mode` field for future upgrade to dedicated schema/DB/stack per tenant.

## Recommendation
Option 4 (hybrid). Implement shared schema + RLS now, but include `tenants.isolation_mode` in the tenant registry so the platform can offer enterprise isolation tiers without a redesign.

## Research Source
Topic 01 — Multi-Tenant SaaS, RLS & Client Portals (Sections 3-4)

## Affects
- Database schema design (every table)
- `engine/server.py` — request middleware
- `engine/sessions.py` — session tenant context
- All pipeline/agent/dashboard modules
- Future Snowflake analytics layer

## Status
Proposed

## Decided by
(pending)
