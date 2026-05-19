# Use Cases

## Core Use Cases

### UC-1: New Product Build
A product owner starts a new product build from scratch. They answer onboarding questions, receive AI recommendations for architecture, features, timeline, and budget. They adjust sliders to explore trade-offs, approve a plan, and Conductor orchestrates the build through phases.

### UC-2: Existing Product Improvement
A product owner wants to add features, fix issues, or optimize an existing product already managed by Conductor. The platform uses memory and context from the original build to make informed recommendations.

### UC-3: Data/Service Migration
A data engineer migrates an existing client from a legacy service stack to the Conductor-managed platform. The workflow includes inventory, gap analysis, dual-run, parity validation, and cutover.

### UC-4: Client Portal Access
A client stakeholder logs into their portal to view progress, approve decisions, upload credentials securely, and review deliverables.

### UC-5: AI-Guided Decision Making
At any decision point, the platform provides AI-generated options with cost, risk, timeline, and ROI estimates. The user can simulate different scenarios before committing.

### UC-6: Secure Credential Handoff
A client needs to provide API keys, OAuth tokens, or database credentials. The platform generates a secure request, the client uploads through a vault-integrated portal, and credentials are never exposed in logs, chat, or agent memory.

### UC-7: Build Orchestration
Conductor breaks an approved plan into phases and tasks, assigns them to agents or humans, manages dependencies, handles blockers, and tracks progress through a DAG-based pipeline.

### UC-8: Self-Improvement Loop
After each build, Conductor evaluates what worked and what didn't. Successful patterns are promoted to reusable templates. Failed patterns are quarantined. The platform gets better over time.

## Open Questions

- [ ] Which use cases are in scope for MVP?
- [ ] What is the minimum viable version of UC-4 (client portal)?
- [ ] How do UC-5 decisions persist and influence future recommendations?
