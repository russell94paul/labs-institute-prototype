# Deep Research Prompt: Secure Credential & Artifact Workflows

## Purpose

Research best practices for secure client credential handling and artifact request workflows, informing Conductor's credential management, vault integration, and client approval flows.

## When to Run

Run after Topics 1 and 4 (Priority 6). Credential security is critical but depends on the tenancy and migration architecture decisions.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research best practices for secure client artifact requests, credential handoff, OAuth connection setup, API key management, secret vault integration, access expiration, audit logs, and client approval workflows. The platform should never store raw secrets in chat, vector DB, logs, prompts, build reports, or agent memory.**

Context: I'm building a product orchestration platform (called "Conductor") that builds and operates software products for multiple clients. During builds and operations, the platform frequently needs client credentials: API keys for source systems, OAuth tokens for SaaS integrations, database connection strings, service account credentials, etc.

Current problem: credentials are managed manually via 1Password sharing, environment variables, and Slack messages. This is insecure, unauditable, and doesn't scale.

The platform uses AI agents (Claude Code) that must NEVER see raw credentials. Credentials must flow from client → vault → runtime environment without appearing in any AI context, prompt, log, or stored artifact.

I need to understand:

1. **Secure credential flow** — end-to-end flow for how a credential gets from a client to a running pipeline without any human or AI seeing the raw value. What are the handoff points? Where are the risks?

2. **Artifact request model** — how to model a request for a credential or artifact. What metadata is needed (what credential, why it's needed, who's requesting, when it expires, what it unlocks). How requests map to approval workflows.

3. **Vault integration pattern** — how to integrate with secret vaults (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager). Common patterns for multi-tenant vault design. Dynamic secrets vs. static secrets. Lease management and rotation.

4. **Approval workflow** — how the client approves a credential request. Portal-based approval vs. email-based. Multi-step approval (client admin → security review). How to handle urgent requests. Timeout and escalation.

5. **Audit model** — what to log for credential operations. Who requested, who approved, when it was accessed, by what service, for how long. How to make audit logs tamper-proof. Retention requirements for SOC 2.

6. **Client portal UX** — how the credential request and upload experience works from the client's perspective. Upload form design. Status tracking. Expiration notifications. Revocation workflow.

7. **OAuth connection setup** — how to handle OAuth flows where the client needs to authorize the platform. Consent screens. Token storage. Refresh token rotation. What happens when tokens expire.

8. **Agent-safe credential injection** — how to inject credentials into a running agent session (Claude Code) without the credential appearing in the session's context, prompts, or outputs. Environment variable injection. Sidecar patterns. Proxy patterns.

9. **Security checklist** — comprehensive checklist for credential security. Common vulnerabilities. Testing strategies. Penetration testing for credential flows.

Provide your output as a structured report with:
- Secure credential flow (end-to-end diagram description)
- Artifact request model (schema, states, transitions)
- Vault integration pattern (architecture, multi-tenant design)
- Approval workflow (steps, roles, timeouts)
- Audit model (events, schema, retention)
- Client portal UX (screens, flows)
- Security checklist (prioritized)

Reference real implementations: GitHub's secret scanning, Stripe's key management, HashiCorp Vault patterns, AWS Secrets Manager best practices.

---

## Expected Output Filename

`06-secure-credential-artifact-workflows.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Credential management architecture
- Vault selection and integration
- Client portal credential upload flow
- Agent session environment injection
- Approval workflow design
- Audit logging infrastructure
- Compliance readiness (SOC 2)
