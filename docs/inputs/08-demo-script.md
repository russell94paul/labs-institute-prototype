# Conductor Demo Script

## Demo Flow

```
User opens Conductor
  → Chooses: New Product / Existing Product / Data Migration
  → Answers onboarding questions
  → Sees AI recommendations
  → Adjusts budget / timeline / user sliders
  → Sees roadmap scenarios
  → Approves selected plan
  → Conductor creates phases
  → Bootstrap / Build Studio runs phases
  → Progress appears on board / DAG
  → Blockers and approvals appear
  → Final product is built / deployed
```

## Demo Narrative

### Scene 1: Entry (30 seconds)
"This is Conductor — a platform that builds, migrates, and operates software products. Let me show you what happens when a new client comes in."

**Screen**: Landing / project selection screen

### Scene 2: Onboarding (2 minutes)
"The client tells us what they need. Conductor asks smart questions and starts forming a plan."

**Screen**: Onboarding questionnaire with adaptive questions
- Select "Data Migration" path
- Fill in: source systems, current pain points, compliance needs, timeline constraints

### Scene 3: AI Recommendations (1 minute)
"Based on the answers, Conductor recommends an architecture, estimates cost and timeline, and flags risks."

**Screen**: Recommendation panel with architecture diagram, cost estimate, risk summary

### Scene 4: Decision Simulation (2 minutes)
"The client can explore trade-offs. What if we increase the budget? What if we need SOC 2 compliance? What if we add 5 more data sources?"

**Screen**: Slider panel with real-time scenario updates
- Adjust budget slider → see timeline and feature scope change
- Toggle compliance → see cost and timeline increase
- Add data sources → see architecture complexity change

### Scene 5: Plan Approval (30 seconds)
"The client approves the plan. Conductor breaks it into phases."

**Screen**: Roadmap view with phases, dependencies, milestones

### Scene 6: Build Orchestration (2 minutes)
"Each phase runs as a pipeline. Agents and humans work in parallel. Dependencies are managed automatically."

**Screen**: DAG view with running/completed/blocked tasks
- Show a completed phase
- Show a running phase with progress
- Show a blocked task waiting for client approval

### Scene 7: Blocker Resolution (1 minute)
"When something needs human input — a credential, an approval, a design decision — Conductor asks and waits."

**Screen**: Approval request panel, credential request portal

### Scene 8: Delivery (1 minute)
"The product is built, tested, and deployed. The client sees it in their portal."

**Screen**: Client portal with deployed product, dashboards, health metrics

## Screens Needed

1. Landing / project selection
2. Onboarding questionnaire (adaptive)
3. AI recommendation panel
4. Decision simulator with sliders
5. Roadmap / phase view
6. DAG pipeline view
7. Approval / blocker resolution panel
8. Credential request portal
9. Client portal with deployed product
10. Progress dashboard / health metrics

## Success Criteria

- [ ] Demo completes in under 10 minutes
- [ ] Each screen transition is smooth and logical
- [ ] AI recommendations feel intelligent and specific (not generic)
- [ ] Decision simulator shows meaningful trade-offs
- [ ] DAG view accurately reflects real pipeline state
- [ ] At least one "wow" moment where the platform does something unexpected and valuable

## Wow-Factor Moments

1. **Instant architecture recommendation** — AI suggests a complete architecture in seconds based on answers
2. **Live trade-off simulation** — Sliders update cost/timeline/scope in real time
3. **Self-improvement callback** — "This migration pattern worked well for your last client, applying it here"
4. **Credential security** — Show that credentials are requested but never visible in the platform
5. **Parallel execution** — Multiple agents working simultaneously on different phases

## Risks / Open Questions

- [ ] How realistic can the AI recommendations be for a demo?
- [ ] Do we need real data or can we use synthetic/demo data?
- [ ] How do we handle the gap between demo UI and actual implementation state?
- [ ] Should the demo use a real Claude Code session or a recorded/simulated one?
- [ ] What is the minimum viable demo for investor/client conversations?
