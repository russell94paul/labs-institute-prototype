# Deep Research Prompt: Multi-Tenant SaaS, RLS & Client Portals

## Purpose

Research best practices for designing a secure multi-tenant SaaS platform with client portals, informing Conductor's tenant isolation, data security, and client-facing portal architecture.

## When to Run

Run this first (Priority 1). The multi-tenant architecture is foundational — most other design decisions depend on the tenancy model.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research best practices for designing a secure multi-tenant SaaS platform with client portals, project workspaces, RBAC, row-level security, audit logs, secret handling, approval workflows, and tenant isolation.**

Context: I'm building a product orchestration platform (called "Conductor") that manages the full lifecycle of software products for multiple clients. Each client (tenant) gets a workspace with their own projects, pipelines, data, credentials, and team members. The platform uses AI agents to orchestrate builds, and a DAG pipeline engine for task execution.

The platform's data layer currently uses JSON files but will evolve to a database. The front end is a vanilla HTML/CSS/JS SPA. The backend is Python.

I need to understand:

1. **Multi-tenant architecture patterns** — schema-per-tenant vs. shared schema with RLS vs. database-per-tenant. Trade-offs for each at different scales (5 tenants, 50, 500+). How this affects query performance, backup/restore, schema migrations, and tenant-specific customization.

2. **Row-level security (RLS)** — how to implement RLS that works across the data layer (database), API layer (authorization), and UI layer (data filtering). Specific patterns for PostgreSQL and/or Snowflake. How RLS interacts with AI agent access (agents must only see data from their assigned tenant).

3. **Client portals** — best practices for building tenant-scoped portals where clients can view project progress, approve decisions, upload credentials securely, and manage their team. Authentication patterns (SSO, magic link, OAuth). Session management. What clients should and should not be able to see or do.

4. **RBAC** — role-based access control models that work for multi-tenant platforms. Roles like: platform admin, tenant admin, project owner, developer, viewer, client stakeholder. How roles interact with RLS. How to handle cross-tenant access for platform operators.

5. **Audit logging** — what events must be logged for SOC 2 compliance. Log format, retention, tamper-proofing. How to make audit logs queryable without exposing sensitive data.

6. **Secret handling** — how to handle client credentials (API keys, OAuth tokens, database passwords) in a multi-tenant platform. Vault integration patterns (HashiCorp Vault, AWS Secrets Manager). How to ensure secrets never appear in logs, chat, AI agent memory, vector databases, or build artifacts.

7. **Approval workflows** — patterns for multi-step approval workflows where clients must approve decisions, credential access, deployments, or scope changes. How to handle timeouts, escalation, and audit trails for approvals.

8. **Tenant isolation testing** — how to test that tenant isolation is working correctly. Penetration testing patterns. Automated tenant boundary tests. Chaos testing for isolation failures.

Provide your output as a structured report with:
- Recommended architecture (with diagram description)
- Data model (tables, relationships, RLS policies)
- RLS strategy (database + API + UI layers)
- Tenant isolation strategy
- Security risks and mitigations
- Implementation checklist (ordered by priority)
- Testing checklist

Include specific examples, not just principles. Reference real-world implementations where possible (Stripe, Salesforce, Slack, etc.).

---

## Expected Output Filename

`01-multi-tenant-saas-rls-client-portals.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox. Claude will:
1. Read the report
2. Extract key findings, architecture implications, risks, and decisions
3. Create a synthesis in `docs/research/syntheses/`
4. Update the research index and status

## Decision Areas This Affects

- Database architecture (schema design, RLS policies)
- API authorization model
- Client portal design
- Agent permission boundaries
- Credential management architecture
- Audit logging infrastructure
- Compliance readiness
