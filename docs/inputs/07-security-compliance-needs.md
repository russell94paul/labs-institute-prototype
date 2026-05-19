# Security & Compliance Needs

## Requirements to Research

- [ ] SOC 2 Type II requirements and timeline
- [ ] HIPAA applicability (any health data clients?)
- [ ] GDPR applicability (any EU-based clients or data subjects?)
- [ ] Data residency requirements per client
- [ ] Encryption at rest and in transit requirements
- [ ] Audit log retention requirements
- [ ] Incident response plan requirements
- [ ] Penetration testing requirements
- [ ] Vendor security assessment questionnaire readiness

## Credential Security Principles

1. No raw secrets in chat, logs, prompts, agent memory, or vector DB
2. Vault-integrated credential storage (HashiCorp Vault, AWS Secrets Manager, or equivalent)
3. Time-limited access tokens where possible
4. Audit trail for all credential access
5. Client-initiated credential upload through secure portal

## Multi-Tenant Isolation

- Row-level security (RLS) at the database layer
- Tenant-scoped API tokens
- Workspace isolation in build environments
- Network-level isolation where required
- Separate encryption keys per tenant (evaluate need)

## Open Questions

- [ ] What compliance frameworks are required for initial clients?
- [ ] What is the budget for security tooling and audits?
- [ ] Do any clients require on-prem or air-gapped deployments?
- [ ] What is the incident response SLA?
