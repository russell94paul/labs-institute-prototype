# LABS Institute Growth & Gig Intelligence Platform

## Repo-Ready Product Specification

**Status:** Draft v1  
**Primary use case:** LABS Institute electronic music agency / artist-growth platform  
**Product type:** Multi-tenant music agency operating system with AI planning, simulation, portals, contracts, marketing, and analytics  
**Important naming rule:** Do **not** refer to this as Ortho. The current product/company direction is **LABS Institute**.

---

# 1. Product Vision

LABS Institute should have an intelligent operating system that helps the team manage DJs, artists, clients, promoters, venues, partner agencies, contracts, resources, marketing, events, and gig logistics from one controlled workspace.

The platform should not be a generic CRM. It should behave like a **music-agency decision engine**.

The core promise:

> LABS Institute can enter any opportunity, simulate the best path, generate a roadmap, assign the right tasks to the right portals, control the marketing, manage the contract, and track the financial and artist-growth outcome from one intelligent platform.

---

# 2. Strategic Product Positioning

## Recommended positioning

**LABS Institute Growth & Gig Intelligence Platform** is a centralized operating system for electronic music agencies that combines:

- artist onboarding
- artist resource management
- booking opportunity analysis
- lead scoring
- gig planning
- contract and billing workflows
- controlled marketing and social scheduling
- client/promoter collaboration
- external agency collaboration
- AI-generated roadmaps
- cost/revenue simulation
- ROI and artist-growth analytics

## Differentiation

Most tools solve only one slice of the agency workflow:

- CRM tools manage contacts and leads.
- Event tools manage events.
- Social tools schedule posts.
- Contract tools manage signatures.
- Spreadsheets track costs and revenue.
- Project management tools track tasks.

This platform should combine those workflows into a **music-specific, portal-driven, AI-assisted operating system**.

The strongest differentiator is the combination of:

1. **Master Simulator**
2. **AI Roadmap Builder**
3. **Role-based portals**
4. **Automated task/dependency generation**
5. **Controlled marketing and artist activity sharing**
6. **Financial, operational, marketing, and artist-growth analytics**

---

# 3. Core Platform Areas

| Platform Area | Purpose |
|---|---|
| **LABS HQ** | CEO/internal command center for everything happening across the agency |
| **Artist Roster OS** | Artist profiles, onboarding, assets, uploads, availability, resources |
| **Opportunity Board** | Leads, gigs, promoters, venues, festivals, brands, external agency opportunities |
| **AI Roadmap Builder** | Guided decision flow for gigs, campaigns, artist growth, tours, and releases |
| **Master Simulator** | Scenario engine for cost, revenue, ROI, artist growth, risk, and marketing strategy |
| **Client Portal** | Client/promoter-facing workspace with filtered info, tasks, approvals, documents |
| **Artist Portal** | Artist-facing workspace for uploads, approvals, availability, tasks, resources |
| **External Agency Portal** | Shared deal room for partner agencies, managers, promoters, and collaborators |
| **Marketing Control Center** | Campaign planning, post-style selection, approval workflows, social scheduling |
| **Contract & Billing Hub** | Contracts, invoices, deposits, balances, deal terms, settlement tracking |
| **Analytics Overview** | Executive, financial, artist, marketing, operations, and lead analytics |
| **Resource Library** | Templates, riders, brand assets, contract docs, onboarding guides, process docs |

---

# 4. Primary User Types

## Internal LABS users

- CEO / founder
- booking manager
- artist manager
- marketing manager
- operations coordinator
- finance/admin user
- legal/contract reviewer

## External users

- DJs / artists
- promoters
- venues
- festivals
- brand clients
- external booking agencies
- artist managers
- designers
- photographers/videographers
- production suppliers

---

# 5. Portal Strategy

## Recommendation

Build **one platform** with **role-based and entity-level portal views**.

Do **not** build separate apps for every user group. Use one multi-tenant platform where access is filtered by:

- organization
- workspace
- role
- entity
- event/gig
- contract
- artist
- client/company
- task visibility
- document visibility

## Portal types

| Portal | Main user | Purpose |
|---|---|---|
| **LABS HQ Portal** | Internal LABS team | Master dashboard and operational control center |
| **Artist Portal** | DJs/artists | Upload assets, approve posts, manage availability, complete onboarding |
| **Client/Promoter Portal** | Clients, venues, promoters | Submit booking details, approve assets, pay deposits, complete event tasks |
| **External Agency Portal** | Partner agencies/managers | Shared event, contract, and task workspace |
| **Lead Portal** | New DJs, clients, promoters | Intake forms, qualification, scoring, next-step routing |
| **Event/Gig Portal** | All approved stakeholders | Event-specific timeline, documents, tasks, approvals, logistics |
| **Marketing Portal** | Internal/external marketing collaborators | Campaign tasks, approvals, assets, scheduled posts |
| **Contract Portal** | Legal/finance/client/artist users | Versioned contracts, signatures, billing milestones, permissions |

## Sensitive data rules

External users should never see:

- internal LABS profit margin
- private negotiation notes
- alternative simulations unless explicitly shared
- other artists' confidential rates
- private risk analysis
- internal strategy notes
- unrelated contracts
- unrelated artist or client records

---

# 6. LABS HQ Command Center

The HQ dashboard should answer:

- What opportunities are active?
- Which gigs are confirmed?
- Which contracts are blocked?
- Which deposits are unpaid?
- Which artists need attention?
- Which campaigns are waiting for approval?
- Which client tasks are overdue?
- Which opportunities should be prioritized?
- Which events need simulation?
- Which roadmap needs approval?
- Which gigs are financially risky?

## Recommended dashboard widgets

- active opportunities
- confirmed gigs
- pending contracts
- unpaid deposits
- blocked tasks
- urgent client actions
- urgent artist actions
- upcoming announcements
- upcoming shows
- highest-value leads
- highest-risk gigs
- top artist momentum
- revenue forecast
- profit forecast
- marketing calendar
- roadmap approval queue

---

# 7. Opportunity / Lead Board

The Opportunity Board should manage incoming leads and potential gigs.

## Lead stages

1. New lead
2. Needs review
3. Qualified
4. Artist fit analysis
5. Simulation needed
6. Roadmap draft
7. Proposal drafted
8. Proposal sent
9. Negotiation
10. Contract pending
11. Confirmed
12. Lost
13. Archived

## Opportunity card fields

- opportunity name
- source
- client/promoter
- location
- event date
- venue
- budget
- target audience
- genre/subgenre
- recommended artists
- artist availability
- estimated revenue
- estimated cost
- estimated profit
- ROI estimate
- artist growth score
- brand value score
- client relationship score
- risk score
- required next action
- missing information
- simulation status
- roadmap status
- contract status

## Lead scoring dimensions

- budget fit
- genre fit
- location fit
- timeline feasibility
- artist availability
- client/promoter quality
- profit potential
- artist-growth value
- LABS brand value
- relationship value
- risk level
- repeat opportunity potential

---

# 8. Master Simulator

The Master Simulator is the main wow-factor feature.

It should allow LABS to compare multiple possible ways to execute an opportunity.

## Optimization goals

The user should be able to select an optimization target:

- maximize ROI
- maximize net profit
- maximize artist growth
- maximize LABS brand visibility
- maximize client satisfaction
- reduce operational risk
- maximize long-term relationship value
- maximize territory expansion
- balance all goals

## Constraint options

The simulator should support constraints such as:

- budget cap
- minimum profit margin
- maximum risk level
- selected artist priority
- required location
- required date range
- artist availability
- venue capacity
- marketing budget cap
- required marketing channels
- required client deliverables
- preferred lineup style
- contract status
- deposit status
- timeline deadline
- client approval requirements

## Simulator input categories

### Gig basics

- event type
- city/location
- venue
- venue capacity
- date
- time window
- expected attendance
- ticket price
- client budget
- artist lineup
- number of DJs
- set times
- genre/subgenre
- event maturity

### Revenue inputs

- client fee
- ticket revenue estimate
- bar/venue split
- sponsorship revenue
- brand partnership revenue
- merchandise potential
- upsell opportunities
- future booking likelihood
- LABS commission percentage
- deposit amount
- balance due
- payment schedule

### Cost inputs

- artist/DJ fee
- travel
- accommodation
- hospitality
- equipment
- visuals
- photographer/videographer
- designer
- paid ads
- content creation
- PR
- guestlist cost
- venue cost
- production cost
- insurance
- legal/contract cost
- internal staff time
- contingency buffer

### Marketing inputs

- organic social only
- paid social ads
- artist-led content
- venue-led content
- promoter-led content
- scene partner campaign
- influencer push
- press/editorial campaign
- email/newsletter
- teaser campaign
- ticket urgency campaign
- recap campaign
- release tie-in campaign

### Artist-growth inputs

- artist career stage
- current city traction
- social growth trend
- streaming momentum
- recent releases
- recent gigs
- similar artist pull
- audience overlap
- press value
- content value
- strategic territory value
- repeat booking likelihood

### Risk inputs

- contract risk
- payment risk
- cancellation risk
- artist availability risk
- travel risk
- venue reliability
- promoter reliability
- low-ticket-sales risk
- brand mismatch risk
- reputation risk
- operational complexity
- timeline pressure

## Simulator outputs

Each scenario should generate:

- gross revenue
- total cost
- net profit
- profit margin
- ROI
- break-even attendance
- cost per attendee
- revenue per attendee
- cashflow pressure
- deposit risk
- commission yield
- artist growth score
- territory expansion score
- audience match score
- content value score
- brand elevation score
- marketing impact score
- client relationship score
- execution complexity score
- risk score
- pros
- cons
- trade-offs
- recommendation summary
- confidence level

## Example simulation comparison

| Scenario | Revenue | Cost | Profit | ROI | Artist Growth | Risk | Summary |
|---|---:|---:|---:|---:|---:|---:|---|
| Established DJ only | High | Medium | High | Strong | Medium | Low | Safest profit option |
| Emerging DJ only | Medium | Low | Medium | Strong | High | Medium | Better artist-growth option |
| Established + emerging lineup | High | High | Medium | Moderate | High | Medium | Best balanced option |
| Premium marketing push | High upside | High | Variable | Variable | High | Higher | Best for brand visibility |

---

# 9. AI Roadmap Builder

The Roadmap Builder should turn an opportunity into a structured plan.

It should guide the LABS team through decisions and generate tasks, approvals, timelines, and portal-specific requirements.

## Roadmap types

- gig roadmap
- artist-growth roadmap
- marketing campaign roadmap
- tour/location roadmap
- client booking roadmap
- new DJ onboarding roadmap
- release/promo roadmap
- brand partnership roadmap

## Roadmap flow

### Step 1: Choose roadmap type

Examples:

- gig roadmap
- artist growth roadmap
- marketing campaign roadmap
- release roadmap
- client booking roadmap

### Step 2: Select primary goal

Examples:

- maximize profit
- grow a specific DJ
- build LABS brand visibility
- enter a new city
- win a client relationship
- reduce operational risk
- generate content
- support a release
- build long-term roster value

### Step 3: Select artist or lineup

Show for each artist:

- fee
- availability
- location
- growth score
- recent activity
- genre fit
- social reach
- previous gig data
- risk level
- recommended use case

### Step 4: Select location and event context

Inputs:

- city
- venue
- expected capacity
- event type
- promoter/client
- target audience
- date range
- local scene strength
- travel complexity

### Step 5: Build lineup and set times

Inputs:

- headline DJ
- support DJs
- local opener
- set durations
- running order
- genre flow
- crowd-building strategy

### Step 6: Add contract and billing assumptions

Inputs:

- client fee
- artist fee
- deposit
- balance
- payment due dates
- cancellation terms
- commission
- expense responsibility
- travel included or separate

### Step 7: Choose marketing strategy

Options:

- organic only
- paid ads
- artist-led content
- venue-led content
- promoter-led content
- scene partner/influencer push
- press/editorial
- email campaign
- teaser campaign
- ticket urgency campaign
- recap campaign

### Step 8: Generate task roadmap

The system generates:

- internal LABS tasks
- artist tasks
- client tasks
- promoter tasks
- marketing tasks
- contract tasks
- billing tasks
- logistics tasks
- approval tasks
- post-event tasks

Each task should include:

- owner
- due date
- dependency
- portal visibility
- status
- priority
- required file/input
- escalation rule

### Step 9: Simulate scenarios

Generate multiple plans:

- high ROI plan
- high artist-growth plan
- low-risk plan
- premium brand plan
- balanced recommendation

### Step 10: Request approval

Approval types:

- internal LABS approval
- artist approval
- client approval
- marketing approval
- contract approval
- finance/billing approval

## AI recommendation at each step

At every roadmap step, AI should provide:

- recommended option
- reasoning
- trade-offs
- risk warning
- missing information
- suggested next action

---

# 10. Client Portal Automation

When a roadmap is finalized, the system should automatically create a client-facing workspace.

The client portal should only expose information relevant to the client.

## Client sees

- event summary
- confirmed artist/lineup
- client tasks
- required approvals
- contract status
- invoice/payment status
- asset requests
- marketing deadlines
- announcement date
- ticket link request
- venue detail request
- guestlist instructions
- production/rider requirements
- messages from LABS

## Client does not see

- internal LABS margin
- artist negotiation notes
- alternative simulation scenarios
- private artist strategy
- internal risk analysis
- other client information
- other artist private information

## Auto-generated client tasks

| Task | Assigned to | Dependency |
|---|---|---|
| Upload venue logo | Client | Required before poster design |
| Confirm announcement date | Client | Required before social scheduling |
| Approve lineup copy | Client | Required before first public announcement |
| Pay deposit | Client | Required before final confirmation |
| Provide ticket link | Client | Required before campaign launch |
| Confirm green room details | Client | Required before final advance |
| Approve final poster | Client | Required before campaign launch |

When the client completes a task, it should appear in LABS HQ for review.

---

# 11. Artist Portal Automation

The Artist Portal should feel like a professional growth hub.

## Artist onboarding checklist

- artist name
- legal name if required internally
- artist bio
- press photos
- logo
- EPK
- music links
- social links
- genre/subgenre
- booking fee range
- availability
- technical rider
- hospitality rider
- travel requirements
- payment details
- contract preferences
- content permissions
- emergency contact
- recent releases
- recent gigs

## Recent activity upload types

Artists can upload:

- new tracks
- mixes
- photos
- videos
- posters
- gig recaps
- release announcements
- press mentions
- playlist adds
- live clips

## Upload visibility options

Each upload can be marked as:

- private/internal only
- share with LABS
- share with artist profile
- share with client/promoter
- include in EPK
- include in campaign
- approved for paid ads
- approved for social scheduling
- needs approval before use

## AI suggestions after upload

The AI should suggest:

- best caption style
- best platform
- best posting time
- whether to add to EPK
- whether to include in a current campaign
- whether to tag venue/promoter
- whether to request approval
- whether to create follow-up content

---

# 12. Marketing Control Center

The Marketing Control Center should allow LABS to manage controlled marketing for the agency and its artists.

## Core features

- campaign calendar
- campaign brief generator
- post-style selector
- caption generator
- social scheduler
- approval workflows
- asset library
- campaign performance dashboard
- content rights tracking
- artist/client/promoter tagging
- automated reminders
- post-event recap generator

## Post-style taxonomy

- dark techno
- underground
- premium agency
- festival energy
- minimal announcement
- ticket push
- last-chance urgency
- artist spotlight
- behind-the-scenes
- new release
- professional press copy
- local scene focused
- international positioning

## Campaign strategy types

| Strategy | Best for | Risk |
|---|---|---|
| Organic artist-led | Authentic growth | Lower reach |
| Paid conversion | Ticket sales | Requires budget and tracking |
| Scene partner push | Local credibility | Depends on partner responsiveness |
| Premium brand campaign | LABS positioning | Slower direct ROI |
| Recap-first campaign | Long-term content library | Less useful before the gig |
| Release tie-in | Artist growth | Needs strong release asset |

---

# 13. Contract & Billing Hub

The platform should support contract workflows without exposing sensitive data to the wrong users.

## Contract types

- artist management agreement
- booking agreement
- performance agreement
- promoter agreement
- venue agreement
- co-promotion agreement
- brand partnership agreement
- NDA
- rider attachment
- invoice/payment terms

## Contract features

- template library
- contract metadata
- version history
- approval status
- internal notes
- external comments
- e-signature integration later
- signed PDF storage
- renewal/reminder dates
- cancellation terms
- deposit requirements
- balance due dates

## Billing features

- client fee
- artist fee
- LABS commission
- invoice status
- deposit status
- balance status
- payment due dates
- expenses
- settlement
- artist payout
- profit/loss per gig
- revenue by artist
- revenue by client
- revenue forecast

---

# 14. Task & Dependency Engine

The platform should generate and track tasks based on the approved roadmap.

## Task fields

- title
- description
- owner type
- owner ID
- portal visibility
- due date
- priority
- status
- required artifact
- dependency IDs
- blocker status
- escalation rule
- approval requirement

## Dependency example

A poster cannot be approved until:

- artist photo is uploaded
- venue logo is uploaded
- event title is confirmed
- lineup is confirmed
- ticket link is provided
- announcement date is approved

If any dependency is missing, LABS HQ should show the item as blocked.

---

# 15. Analytics Overview

The analytics layer should have separate views for different purposes.

## CEO overview

- monthly revenue
- projected revenue
- gross profit
- net margin
- active opportunities
- confirmed gigs
- pending contracts
- unpaid deposits
- blocked tasks
- highest-value leads
- highest-risk gigs
- top artist momentum
- best client relationships

## Financial analytics

- gross revenue
- total cost
- net profit
- profit margin
- ROI
- break-even attendance
- cost per attendee
- revenue per attendee
- cashflow pressure
- unpaid deposit risk
- commission yield
- downside exposure
- upside potential

## Artist analytics

- gigs booked
- revenue generated
- average fee
- growth score
- city/territory traction
- social momentum
- campaign performance
- content activity
- repeat bookings
- next recommended move

## Client analytics

- revenue by client
- repeat booking rate
- payment reliability
- average deal size
- responsiveness
- approval speed
- future opportunity score

## Marketing analytics

- post frequency
- campaign reach
- engagement
- best post styles
- best platform by artist
- ticket conversion estimate
- approval delays
- top-performing assets

## Operations analytics

- tasks completed on time
- blocked dependencies
- contract turnaround time
- client response time
- artist response time
- average time from lead to confirmed gig
- average time from confirmed gig to settlement

---

# 16. Automation Map

## High-priority automation

| Automation | Value |
|---|---|
| Lead intake scoring | Helps prioritize opportunities faster |
| Artist fit scoring | Recommends the best DJ or lineup for a lead |
| Roadmap generation | Converts a lead into a structured plan |
| Scenario simulation | Compares ROI, growth, risk, and marketing options |
| Task generation | Creates internal, client, artist, and marketing tasks automatically |
| Dependency tracking | Prevents blocked campaigns and missed deadlines |
| Client information requests | Automatically asks clients for missing details |
| Artist onboarding reminders | Keeps artist data and assets complete |
| Marketing caption generation | Speeds up content planning |
| Approval reminders | Reduces delays before public announcements |
| Contract/payment reminders | Reduces financial and legal risk |
| Post-event reporting | Turns completed gigs into learning and follow-up actions |

## Human approval checkpoints

Automation should not publish, send, or finalize sensitive actions without approval.

Require approval for:

- public social posts
- client proposals
- contract sending
- contract signing
- final pricing
- artist fee changes
- invoice sending
- simulation recommendation acceptance
- roadmap finalization
- external portal visibility changes

---

# 17. Core Data Model

## Main entities

```text
User
Organization
Workspace
Role
Permission
Artist
ArtistProfile
ArtistAsset
SocialAccount
Company
Contact
Lead
Opportunity
Event
Gig
Venue
Roadmap
RoadmapStep
RoadmapTask
SimulationScenario
Contract
ContractVersion
Deal
Invoice
Payment
Task
TimelineMilestone
MarketingCampaign
MarketingAsset
PostDraft
PostApproval
PostSchedule
Message
Comment
Notification
Resource
Document
AuditLog
```

## Roadmap object model

```text
Roadmap
- id
- type
- goal
- status
- selected_artists
- selected_location
- selected_client
- selected_opportunity
- selected_strategy
- simulation_results
- recommended_scenario
- approval_status
- created_by
- finalized_at

RoadmapStep
- roadmap_id
- step_type
- decision
- recommendation
- tradeoffs
- selected_option
- risk_notes

RoadmapTask
- roadmap_id
- owner_type
- owner_id
- portal_visibility
- title
- due_date
- dependency_ids
- status
- required_artifact

SimulationScenario
- roadmap_id
- optimization_goal
- revenue_estimate
- cost_estimate
- profit_estimate
- roi_score
- artist_growth_score
- brand_score
- risk_score
- recommendation_summary
```

---

# 18. MVP Scope

## MVP goal

Build the foundation that proves the platform can manage LABS workflows and generate roadmap-driven portal tasks.

## MVP modules

1. Authentication and role-based access
2. Organization/workspace model
3. Artist profiles
4. Artist onboarding checklist
5. Company/contact CRM
6. Lead and opportunity board
7. Basic gig planner
8. Roadmap Builder v1
9. Simulator v1 with manual inputs
10. Task and dependency engine v1
11. Client portal v1
12. Artist portal v1
13. Document/resource uploads
14. Contract metadata tracking
15. Marketing campaign planner v1
16. HQ dashboard v1
17. Audit log v1

## MVP simulator should include

- revenue estimate
- cost estimate
- net profit
- profit margin
- ROI
- artist growth score
- risk score
- recommended scenario
- trade-off summary

## MVP should not try to do everything

Defer these until later:

- full social publishing integrations
- e-signature integrations
- payment processing
- automatic venue/festival scraping
- advanced ML forecasting
- ticketing integrations
- full financial settlement automation
- cross-platform social analytics ingestion

---

# 19. V2 Roadmap

V2 should add stronger automation and integrations.

- AI scoring improvements
- campaign strategy comparison
- social scheduling integrations where feasible
- e-signature integration
- invoice/payment provider integration
- calendar integration
- Gmail/email integration
- opportunity scanner
- artist momentum analytics
- client responsiveness analytics
- approval escalation rules
- post-event report generator

---

# 20. V3 Roadmap

V3 should move toward a full agency growth engine.

- ticketing integrations
- settlement automation
- tour routing
- territory expansion intelligence
- competitor/public market intelligence
- advanced forecast models
- white-label external portals
- public artist pages
- agency-wide revenue forecasting
- automated client proposal generation
- advanced content performance optimization

---

# 21. Orchestrator Build Strategy

For autonomous building, the orchestrator needs more than a product idea. It needs structured source documents, acceptance criteria, and staged implementation tasks.

## Recommended source-of-truth documents

Keep the repo documentation modular.

```text
docs/
  README.md
  product/
    labs-institute-growth-gig-intelligence-platform.md
    personas.md
    feature-map.md
    mvp-scope.md
  research/
    labs-institute/
      deep-research.md
      source-notes.md
      assumptions.md
      competitor-matrix.md
  architecture/
    system-architecture.md
    data-model.md
    permissions-model.md
    portal-architecture.md
    integration-plan.md
  workflows/
    roadmap-builder.md
    master-simulator.md
    artist-onboarding.md
    client-portal.md
    contract-billing.md
    marketing-control-center.md
  decisions/
    ADR-001-one-platform-role-based-portals.md
    ADR-002-roadmap-as-core-entity.md
    ADR-003-simulator-v1-manual-inputs.md
  build/
    implementation-plan.md
    backlog.md
    acceptance-criteria.md
    test-plan.md
prompts/
  labs/
    deep-research-prompt.md
    orchestrator-boot-prompt.md
```

## Best practice for adding the research doc

Adding the research doc to a subfolder is a good idea, but it should not be the only input to the orchestrator.

Recommended location:

```text
docs/research/labs-institute/deep-research.md
```

Then create a distilled summary:

```text
docs/research/labs-institute/assumptions.md
```

The orchestrator should use the distilled files for decisions, not only the raw research.

## Why this is better

Raw research can be long, messy, and contradictory. The orchestrator will build more reliably if the research is converted into:

- verified facts
- assumptions
- product implications
- rejected ideas
- build priorities
- risks
- acceptance criteria

## Recommended orchestrator input hierarchy

The orchestrator should read in this order:

1. `docs/README.md`
2. `docs/product/labs-institute-growth-gig-intelligence-platform.md`
3. `docs/product/mvp-scope.md`
4. `docs/architecture/data-model.md`
5. `docs/architecture/permissions-model.md`
6. `docs/workflows/master-simulator.md`
7. `docs/workflows/roadmap-builder.md`
8. `docs/build/backlog.md`
9. `docs/build/acceptance-criteria.md`
10. `docs/research/labs-institute/assumptions.md`
11. `docs/research/labs-institute/deep-research.md`

## Orchestrator guardrails

Add a file such as:

```text
docs/build/orchestrator-guardrails.md
```

It should say:

- Build MVP first.
- Do not build V2/V3 features until MVP acceptance criteria pass.
- Do not expose sensitive internal financials to external portals.
- Do not publish social posts without approval.
- Do not send contracts or invoices without approval.
- Use mocked integrations first.
- Keep simulator v1 explainable and manually configurable.
- Preserve audit logs for sensitive actions.
- Treat research claims as unverified unless moved into `assumptions.md` or cited in product docs.

---

# 22. Recommended Initial Build Order

## Phase 1: Foundation

- auth
- organizations
- users
- roles
- permissions
- workspaces
- audit logs
- core navigation

## Phase 2: Core records

- artists
- artist profiles
- artist assets
- companies
- contacts
- venues
- leads
- opportunities

## Phase 3: Workflow engine

- tasks
- dependencies
- timelines
- notifications
- status transitions
- portal visibility rules

## Phase 4: Roadmap Builder v1

- roadmap entity
- roadmap steps
- selected options
- AI recommendation placeholder layer
- task generation from roadmap
- approval workflow

## Phase 5: Master Simulator v1

- manual input form
- scenario creation
- ROI/profit calculations
- growth/risk scoring
- ranked scenario results
- recommendation summary

## Phase 6: Portals

- LABS HQ
- artist portal
- client portal
- event/gig portal
- basic external agency portal

## Phase 7: Marketing and contracts

- marketing campaigns
- post drafts
- approval workflow
- contract metadata
- billing milestones
- deposit/balance tracking

## Phase 8: Analytics

- CEO overview
- opportunity analytics
- artist analytics
- financial analytics
- operations analytics
- marketing analytics

---

# 23. MVP Acceptance Criteria

The MVP should be considered successful when the following flow works end-to-end:

1. LABS creates an artist profile.
2. Artist completes onboarding checklist in the artist portal.
3. A client/promoter submits or is entered as a new opportunity.
4. LABS reviews the opportunity on the Opportunity Board.
5. LABS generates a roadmap.
6. LABS selects artists, location, pricing assumptions, and marketing strategy.
7. The simulator creates multiple scenarios.
8. LABS selects a recommended scenario.
9. The roadmap generates tasks for LABS, artist, and client.
10. The client sees only their relevant tasks in the client portal.
11. The artist sees only their relevant tasks in the artist portal.
12. LABS can track blocked dependencies from HQ.
13. Contract and billing milestones are tracked.
14. A marketing campaign plan is created.
15. The gig can be marked completed.
16. The system generates a basic post-event summary.

---

# 24. Testing Strategy

## Unit tests

- permission checks
- role access
- simulator formulas
- scoring logic
- task dependency logic
- roadmap status transitions
- approval rules

## Integration tests

- opportunity to roadmap
- roadmap to tasks
- tasks to portals
- contract milestones to dashboard
- marketing campaign to approval queue

## End-to-end tests

1. New artist onboarding
2. New client opportunity
3. Opportunity simulation
4. Roadmap generation
5. Client task assignment
6. Artist task assignment
7. Contract milestone creation
8. Marketing approval workflow
9. Gig completion
10. Post-event report

## Security tests

- artist cannot see another artist's private data
- client cannot see internal margin
- external agency sees only shared records
- revoked user loses access
- sensitive action creates audit log
- unpublished posts cannot be published without approval

---

# 25. Open Questions

These should be answered through research or product discovery:

1. What exact services does LABS Institute provide today?
2. What artist roster or artist relationships are public and verified?
3. What tools does LABS currently use?
4. How does LABS currently manage contracts?
5. How does LABS currently manage artist resources and EPKs?
6. What is the most painful workflow: bookings, marketing, contracts, or artist onboarding?
7. Does LABS want this as an internal tool or future SaaS product?
8. Which social platforms matter most?
9. Should the first version integrate with live social APIs or use export/manual scheduling?
10. What contract templates are needed first?
11. How sensitive are artist fees and client deal terms?
12. What level of automation is acceptable before human approval is required?

---

# 26. Immediate Next Documents to Create

To make the repo orchestrator-ready, create these next:

1. `docs/product/mvp-scope.md`
2. `docs/architecture/data-model.md`
3. `docs/architecture/permissions-model.md`
4. `docs/workflows/master-simulator.md`
5. `docs/workflows/roadmap-builder.md`
6. `docs/build/backlog.md`
7. `docs/build/acceptance-criteria.md`
8. `docs/research/labs-institute/deep-research.md`
9. `docs/research/labs-institute/assumptions.md`
10. `prompts/labs/orchestrator-boot-prompt.md`

---

# 27. Recommendation

The research doc should go in a subfolder, but the best practice is to pair it with a distilled, build-facing set of documents.

Recommended approach:

1. Add the raw research to `docs/research/labs-institute/deep-research.md`.
2. Extract useful conclusions into `docs/research/labs-institute/assumptions.md`.
3. Update the product spec with confirmed findings.
4. Turn the MVP into a backlog with acceptance criteria.
5. Give the orchestrator the backlog and acceptance criteria as its primary build instructions.

This will help the orchestrator build autonomously without getting lost in a large research document.
