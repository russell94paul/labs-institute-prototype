# Target Users

## User Personas

### Platform Operator
- **Who**: ALDC team members running Conductor for clients
- **Goals**: Efficient multi-tenant operations, cost visibility, incident response
- **Pain points**: Manual client onboarding, scattered credentials, no unified view of all client health
- **Key workflows**: Client onboarding, pipeline monitoring, credential management, billing

### Product Owner
- **Who**: Internal or client-side stakeholder defining product requirements
- **Goals**: Clear scope, realistic timelines, budget trade-offs, roadmap visibility
- **Pain points**: Scope creep, unclear cost implications, no way to simulate "what if" scenarios
- **Key workflows**: Onboarding questionnaire, decision simulator, roadmap review, approval gates

### Developer / AI Agent
- **Who**: Human developers or Claude Code agents executing build phases
- **Goals**: Clear task definitions, unblocked dependencies, relevant context
- **Pain points**: Missing context, unclear acceptance criteria, blocked by approvals or credentials
- **Key workflows**: Phase execution, code generation, testing, PR creation, deployment

### Client Stakeholder
- **Who**: Client team members who receive and use the built product
- **Goals**: Visibility into progress, approval authority, secure credential handoff
- **Pain points**: No portal access, email-based status updates, insecure credential sharing
- **Key workflows**: Portal login, progress dashboard, approval workflows, credential upload

### Data Engineer
- **Who**: Engineers responsible for data pipeline operations
- **Goals**: Reliable pipelines, clear migration path, parity validation
- **Pain points**: Undocumented pipelines, no inventory, risky cutovers
- **Key workflows**: Service inventory, gap analysis, dual-run validation, cutover

## Open Questions

- [ ] Which persona is the primary user for the MVP?
- [ ] Do client stakeholders need self-service capabilities in Phase 1?
- [ ] What level of technical sophistication should the onboarding flow assume?
