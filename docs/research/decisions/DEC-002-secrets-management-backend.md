# Decision: DEC-002 — Secrets Management Backend

## Context
Conductor agents and pipelines need access to tenant credentials (API keys, OAuth tokens, DB passwords). The platform must never store raw secrets in JSON state, logs, prompts, or artifacts.

## Options
1. **HashiCorp Vault** — Industry standard for secret lifecycle, dynamic credentials, leasing, audit. Operational overhead of running/hosting Vault.
2. **AWS Secrets Manager** — Managed service, IAM-based access, rotation support. Ties to AWS; session tags can scope per-tenant.
3. **Local dev storage + broker abstraction** — Start with encrypted local files or environment variables behind a secrets broker interface. Swap in Vault/AWS later.

## Recommendation
Option 3 for MVP. Build the secrets broker abstraction now (tenant/project/run context verification, RBAC checks, audit events, short-lived leases). Back it with local dev storage initially. Swap in Vault or AWS Secrets Manager when deploying for external clients.

## Research Source
Topic 01 — Multi-Tenant SaaS, RLS & Client Portals (Section 11)

## Affects
- `engine/server.py` — secret broker integration
- Agent runtime — secret leases per tool call
- Pipeline tasks — credential injection
- Audit logging — `secret.access_granted`, `secret.used_by_task` events
- Client portal — credential upload UX

## Status
Proposed

## Decided by
(pending)
