# Client Onboarding Flows

## Overview

Onboarding is the entry point for every Conductor engagement. The flow adapts based on whether the user is building something new, improving something existing, or migrating a service.

## Flow Selection

```
User opens Conductor
  → New Product Build       → UC-1 onboarding flow
  → Existing Product        → UC-2 onboarding flow
  → Data/Service Migration  → UC-3 onboarding flow
```

## New Product Onboarding (UC-1)

### Step 1: Product Intent
- What problem does this product solve?
- Who are the primary users?
- What domain (data analytics, SaaS app, internal tool, etc.)?

### Step 2: Requirements Gathering
- Feature wishlist (free text + suggested categories)
- Compliance requirements (SOC2, HIPAA, GDPR, none)
- User scale (10s, 100s, 1000s, 10000s+)
- Integration requirements (APIs, databases, third-party services)

### Step 3: AI Recommendations
- Recommended architecture
- Suggested features (must-have, should-have, nice-to-have)
- Estimated timeline ranges
- Estimated cost ranges

### Step 4: Decision Simulation
- Budget slider
- Timeline slider
- Feature scope slider
- Compliance level slider
- Automation level slider
- Risk tolerance slider

### Step 5: Plan Review & Approval
- Generated roadmap with phases
- Cost breakdown
- Risk summary
- Approval gate

## Migration Onboarding (UC-3)

### Step 1: Current State Inventory
- Upload or fill `05-current-aldc-service-inventory.md`
- Identify all services, pipelines, databases, reports

### Step 2: Gap Analysis
- Auto-detect missing artifacts
- Flag undocumented pipelines
- Identify credential requirements

### Step 3: Migration Plan
- Phased migration strategy
- Dual-run approach
- Parity testing plan
- Cutover criteria

### Step 4: Risk Review & Approval
- Must-not-break items
- Rollback strategy
- Client communication plan

## Open Questions

- [ ] Should onboarding be a single session or multi-session?
- [ ] How much can AI pre-fill from existing documentation?
- [ ] What happens if the user abandons onboarding mid-flow?
