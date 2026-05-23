# Multi-Tenant Security and RLS

Hierarchy:

```text
Tenant -> Organization -> Workspace -> Project -> Runs / Artifacts / Approvals / Context / Portal
```

Principals:
- internal user
- client portal user
- agent principal
- service account
- connector/integration

Rules:
- no cross-tenant access by default
- portal users only see portal-safe data
- agents receive minimum required context
- secrets are references only
- all sensitive actions are audited
