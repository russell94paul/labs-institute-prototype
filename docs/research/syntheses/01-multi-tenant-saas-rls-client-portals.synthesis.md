# Synthesis: 01 — Multi-Tenant SaaS, RLS & Client Portals

**Source report:** `local-inputs/research-inbox/01-multi-tenant-saas-rls-client-portals.report.md`
**Synthesized:** 2026-05-19
**Research date:** 2026-05-19

---

## Key Findings

1. **Pooled shared schema + PostgreSQL RLS is the correct starting architecture.** A single PostgreSQL database with mandatory `tenant_id` on every tenant-owned table, enforced by RLS, provides the best balance of security, simplicity, and migration cost from the current JSON-file state.

2. **Tenant isolation is not authentication.** Every database query, object-storage read, secret fetch, pipeline event, and agent tool call must be constrained by tenant context — not just login.

3. **RLS is defense-in-depth, not the only check.** API-layer authorization (RBAC + ABAC), object-storage signed URLs, secret broker access grants, and agent tool allowlists are all required alongside RLS.

4. **Control plane must be separate from application plane.** Tenant lifecycle, identity/SSO config, billing, operator access, and audit policy live in the control plane. Projects, pipelines, agents, and artifacts live in the application plane. Both planes respect tenant boundaries.

5. **Secrets must be references, never values.** The database stores vault paths; a secrets broker mediates all access with tenant/project/run scope, approval gates, and audit events. Raw secrets must never enter logs, prompts, vector stores, or artifacts.

6. **Bridge isolation model preserves future flexibility.** Adding `tenants.isolation_mode` now (defaulting to `pooled_shared_schema`) avoids a data model rewrite when enterprise clients need dedicated schemas, databases, or worker pools.

7. **Agent principals are not superusers.** Each agent is modeled as a principal with tenant/project/run scope, tool allowlists, and no direct database or secret access.

8. **Approval workflows are essential for high-risk actions.** Deployments, credential access, scope changes, and data exports require explicit approval with timeout, escalation, and audit trail.

9. **Audit logging must be SOC 2-oriented.** Structured JSON events covering auth, RBAC decisions, project changes, agent tool calls, secrets access, and approvals. Append-only storage with hash chaining for tamper resistance.

10. **Snowflake RLS is for analytics, not app authorization.** Row access policies on analytics copies complement but do not replace PostgreSQL RLS for transactional data.

---

## Architecture Implications

- **Database migration required:** Move from JSON files to PostgreSQL with `tenant_id` on every table, RLS policies, and tenant-aware indexes.
- **New modules needed:** Control plane service (tenant registry, identity, operator grants), secrets broker, approval service, audit event pipeline.
- **Session context pattern:** Every transaction sets `app.tenant_id`, `app.user_id`, `app.actor_type` via `set_config()` before any tenant-owned query.
- **Separate database roles:** Migration role owns tables; application role (`conductor_app`) has no `BYPASSRLS`.
- **Agent runtime changes:** Agent sessions must set RLS context; agent tool calls pass through authorization gateway.
- **Object storage:** Tenant-prefixed keys, server-generated signed URLs, no client-supplied keys.

---

## Roadmap Implications

- **P0 (before client data):** Tenant registry, RLS foundation, audit events, secrets broker interface, two-tenant isolation tests.
- **P1 (client portal MVP):** Tenant-scoped SPA routes, OIDC-ready identity, secure sessions, project dashboard, approval UI, credential upload, member management.
- **P2 (agent/pipeline boundaries):** Agent principals, tool authorization, per-run secret grants, pipeline RLS, concurrency limits.
- **P3 (compliance hardening):** Append-only audit, hash chaining, SSO/SAML, MFA, operator grants, retention/export, legal hold.
- **P4 (scale/bridge):** Tenant placement model, dedicated schema/DB provisioning, dedicated workers, Snowflake row access policies.

The 5-week minimal build plan in the report is aggressive but feasible if DB migration tooling is established first.

---

## New Risks

| Risk | Severity | Notes |
|---|---|---|
| RLS misconfiguration or bypass | Critical | Requires separate app role, `FORCE RLS`, migration lint, and automated two-tenant tests |
| Connection pool context leakage | High | Must use transaction-local `set_config(..., true)` and reset connections |
| IDOR across tenants | High | API must resolve resource ownership server-side, not trust URL parameters |
| Secret leakage to AI prompts/memory | Critical | Requires broker, handles, prompt filters, and artifact scanning |
| Migration creates table without RLS | High | CI lint query must fail on unprotected tenant tables |
| Operator access abuse | Medium | Time-boxed grants, reason/ticket required, complete audit trail |
| Noisy neighbor pipeline resource consumption | Medium | Per-tenant concurrency limits, rate limiting, dedicated workers for large tenants |

---

## Decisions Required

1. **DEC-001: Default tenancy model** — Shared schema + RLS vs. schema-per-tenant vs. hybrid. Report recommends shared schema + RLS.
2. **DEC-002: Database technology** — PostgreSQL is assumed. Confirm or choose alternative.
3. **DEC-003: Secret management backend** — Vault vs. AWS Secrets Manager vs. other. Report covers both patterns.
4. **DEC-004: Identity/SSO provider** — OIDC/SAML provider selection, magic link for MVP.
5. **DEC-005: Audit storage backend** — PostgreSQL + append-only object storage vs. dedicated audit service.
6. **DEC-006: Client portal auth pattern** — OIDC SSO vs. magic link vs. password+MFA for initial release.
7. **DEC-007: Operator access model** — Time-boxed grants with approval vs. permanent admin bypass.

---

## Implementation Recommendations

1. Start with the P0 foundation: `tenants`, `users`, `tenant_memberships`, `projects` tables with RLS from day one.
2. Create a Python transaction middleware (`with_tenant_context`) that sets RLS context in every request.
3. Build the secrets broker abstraction early, even if backed by local dev storage initially.
4. Add a CI migration lint that rejects any tenant-owned table without RLS.
5. Create automated two-tenant isolation tests as the foundational test suite.
6. Use the proposed RBAC model (8 roles) with `tenant_memberships` and `project_memberships`.
7. Model agents as first-class principals from the start — do not retrofit later.

---

## Phase Changes

- The multi-tenant foundation (P0) should be the **next build phase** after the pipeline DAG engine, as it affects every subsequent module.
- Client portal (P1) can begin in parallel with agent boundary work (P2) if the RLS foundation is solid.

---

## Open Questions

1. What is the timeline for migrating from JSON files to PostgreSQL?
2. Will Conductor initially deploy single-tenant (ALDC internal) before multi-tenant?
3. What is the target identity provider for the first external client?
4. Should the Snowflake analytics layer be built alongside the portal or deferred?
5. What is the minimum compliance posture for the first external client (SOC 2 Type I, contractual, informal)?
