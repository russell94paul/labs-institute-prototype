You are the autonomous conductor for this repo.

Your mission is to spin up the UI and build the first working product slice for the LABS Institute Growth & Gig Intelligence Platform.

This is not a generic CRM. It is a music-agency operating system for LABS Institute that helps the team manage DJs, artists, clients, promoters, venues, gigs, contracts, marketing, resources, opportunity analysis, roadmap planning, and financial/growth simulation.

Primary source documents:
- docs/product/labs-institute-growth-gig-intelligence-platform.md
- docs/product/mvp-scope.md
- docs/workflows/master-simulator.md
- docs/workflows/roadmap-builder.md
- docs/architecture/data-model.md
- docs/architecture/permissions-model.md
- docs/build/backlog.md
- docs/build/acceptance-criteria.md
- docs/build/orchestrator-guardrails.md

If some of these files are placeholders or incomplete, use:
- docs/product/labs-institute-growth-gig-intelligence-platform.md

as the main source of truth.

Important naming:
- Do not call the product Ortho.
- Use LABS Institute as the company direction.
- Suggested product name in the UI: LABS Growth OS or LABS Institute Growth OS.

Build goal:
Create a polished UI foundation that demonstrates the core product vision and can later be connected to real backend services.

Do not attempt to build every backend integration yet. Use mock data, typed data models, and deterministic simulation logic first.

First autonomous build scope:

1. Inspect the repo
- Identify framework, package manager, app structure, styling system, and routing pattern.
- Do not replace the existing app architecture unless absolutely necessary.
- Prefer existing conventions.
- If the app is Next.js, use the existing app/router or pages/router structure.
- If the app is Vite/React, use the existing route/component structure.
- If Tailwind or shadcn/ui exists, use it.
- If no UI system exists, create a clean minimal design system.

2. Spin up the UI
- Install dependencies if needed.
- Run the dev server or equivalent local command.
- Fix obvious startup errors.
- Do not spend excessive time on unrelated broken legacy code.
- If there are blockers, document them in a build report and continue with the safest implementation path.

3. Create the LABS app shell
Build a high-quality app shell with:
- left sidebar navigation
- top header
- workspace switcher or LABS Institute label
- search placeholder
- notification placeholder
- user/account placeholder
- responsive layout
- clean dashboard cards
- consistent spacing and typography

Primary nav items:
- HQ Dashboard
- Artists
- Opportunities
- Roadmaps
- Master Simulator
- Client Portals
- Marketing
- Contracts
- Analytics
- Resources
- Settings

4. Build typed mock data models
Create TypeScript types or equivalent models for:
- Artist
- Company
- Contact
- Lead
- Opportunity
- Gig
- Roadmap
- RoadmapStep
- RoadmapTask
- SimulationScenario
- Contract
- MarketingCampaign
- ArtistAsset
- ClientTask
- DashboardMetric

Create mock data for:
- 5 artists/DJs
- 5 opportunities
- 3 client/promoter companies
- 3 gigs
- 3 roadmap examples
- 4 simulation scenarios
- 4 marketing campaigns
- 3 contracts
- analytics metrics

Keep the mock data realistic for an electronic music agency:
- DJs
- clubs
- festivals
- promoters
- Irish / UK / European locations
- techno / electronic music context
- fees, costs, risk, growth scores, marketing activity

5. Build HQ Dashboard
The HQ Dashboard should show:
- active opportunities
- confirmed gigs
- pending contracts
- unpaid deposits
- blocked client tasks
- upcoming marketing deadlines
- projected revenue
- projected profit
- highest-risk gig
- best growth opportunity
- top artist momentum

Include cards and tables:
- KPI cards
- priority alerts
- upcoming gigs
- opportunity pipeline preview
- blocked dependencies
- recommended next actions

6. Build Artists area
Create an Artists page with:
- roster list
- artist profile cards
- fee range
- location
- genre
- growth score
- availability status
- recent activity
- assets status
- next recommended action

Create an Artist detail view if routing allows:
- profile overview
- onboarding checklist
- recent uploads
- upcoming gigs
- marketing assets
- tasks
- growth analytics
- notes placeholder

7. Build Opportunity Board
Create an Opportunity Board with stages:
- New Lead
- Needs Review
- Qualified
- Simulation Needed
- Proposal Drafted
- Negotiation
- Contract Pending
- Confirmed
- Lost

Each opportunity card should show:
- client/promoter
- city/location
- date
- budget
- recommended artist
- estimated revenue
- estimated profit
- artist growth score
- risk score
- missing information
- next action

8. Build Master Simulator
This is a core wow-factor module.

Create a Master Simulator page where the user can:
- select optimization goal:
  - Maximize ROI
  - Maximize Artist Growth
  - Maximize LABS Brand Visibility
  - Reduce Operational Risk
  - Maximize Client Satisfaction
  - Balanced Recommendation
- select constraints:
  - budget limit
  - location
  - artist priority
  - minimum profit margin
  - maximum risk level
  - required marketing channel
  - preferred lineup type
- compare multiple simulation scenarios

Each scenario should show:
- revenue estimate
- cost estimate
- net profit
- profit margin
- ROI
- artist growth score
- LABS brand score
- marketing impact score
- client relationship score
- risk score
- execution complexity
- pros
- cons
- trade-offs
- recommendation summary

Use deterministic scoring logic for now. Do not call a real AI API unless the repo already has a safe abstraction for it.

The simulator should feel interactive:
- user changes optimization goal
- scenario rankings update
- recommended scenario changes
- summary explanation updates

9. Build AI Roadmap Builder
Create a Roadmap Builder page with a guided step flow.

Steps:
1. Roadmap Type
2. Goal
3. Artist / Lineup Selection
4. Location & Event Context
5. Pricing & Billing
6. Contract Requirements
7. Marketing Strategy
8. Generated Tasks
9. Approval Request

At each step, show:
- selected option
- AI-style recommendation
- reasoning
- trade-offs
- risks
- missing information
- suggested next action

Do not call real AI yet. Use structured deterministic recommendations based on selected data.

When roadmap is finalized, show generated outputs:
- internal LABS tasks
- artist portal tasks
- client portal tasks
- marketing tasks
- contract/billing milestones
- dependency timeline
- approval requests

10. Build Client Portal preview
Create a Client Portals page showing client-facing workspaces.

Each client portal card should show:
- client/promoter name
- event/gig
- pending tasks
- contract status
- invoice/deposit status
- marketing approvals
- blocked items

Create a client portal detail preview if routing allows:
- event summary
- lineup
- tasks assigned to client
- files requested
- approvals needed
- messages placeholder
- contract/payment status

Client must not see:
- LABS internal profit margin
- artist negotiation notes
- alternate private simulation scenarios
- internal risk commentary unless explicitly shared

11. Build Marketing Control Center
Create a Marketing page with:
- campaign calendar/list
- campaign cards
- post drafts
- approval status
- selected post style
- platforms
- scheduled date
- required assets
- blocked approvals

Post-style options:
- Dark techno
- Underground
- Premium agency
- Festival energy
- Minimal announcement
- Ticket push
- Last-chance urgency
- Artist spotlight
- Behind-the-scenes
- New release
- Local scene focused
- International positioning

12. Build Contracts page
Create a Contracts page with:
- contract list
- status
- related gig
- related artist/client
- deposit status
- signature status
- next deadline
- risk flag

Statuses:
- Draft
- Internal Review
- Sent
- Client Review
- Artist Review
- Signed
- Deposit Pending
- Active
- Completed
- Archived

13. Build Analytics Overview
Create an Analytics page with sections:
- Financial Analytics
- Artist Growth Analytics
- Marketing Analytics
- Operations Analytics
- Lead/Opportunity Analytics
- Client Relationship Analytics

Include charts/tables if charting library exists. If not, use cards and progress bars.

Metrics to include:
- gross revenue
- net profit
- profit margin
- ROI
- projected revenue
- unpaid deposits
- artist growth score
- territory expansion score
- audience match score
- content value score
- marketing reach estimate
- engagement estimate
- contract turnaround time
- blocked dependencies
- client responsiveness
- lead conversion rate

14. Build Resources page
Create a Resources page with:
- artist onboarding resources
- contract templates
- marketing templates
- rider templates
- brand assets
- client documents
- internal SOPs

15. Add guardrails
Do not implement:
- real payment processing
- real e-signatures
- real social publishing
- real scraping
- real email sending
- real legal document generation
- real AI API calls
- sensitive personal data handling

Unless the repo already has safe, approved integrations for those systems.

For now, build:
- UI
- mock data
- typed models
- deterministic simulation
- deterministic AI-style recommendations
- clear extension points

16. Acceptance criteria
The first build is complete when:
- app starts successfully
- LABS navigation exists
- HQ Dashboard exists
- Artists page exists
- Opportunity Board exists
- Master Simulator exists
- Roadmap Builder exists
- Client Portal preview exists
- Marketing page exists
- Contracts page exists
- Analytics page exists
- mock data is centralized and typed
- simulator can rank scenarios by selected optimization goal
- roadmap builder can generate tasks and approvals from selected options
- UI looks polished enough for a stakeholder demo
- no sensitive or real external integrations are hardcoded
- code follows existing repo conventions
- README or build report explains what was added

17. Build report
At the end, create or update:

docs/build/labs-ui-build-report.md

Include:
- what was built
- files changed
- how to run the app
- known limitations
- next recommended build phase
- any blockers
- any assumptions made

18. Next phase recommendation
After completing this UI foundation, recommend the next build phase:
- persistence/database schema
- auth and role-based access
- real portal permissions
- roadmap persistence
- simulator backend service
- contract/document storage
- marketing approval workflow
- notification system
- integration planning

Work autonomously.
Make sensible decisions.
Prefer a working demo over incomplete over-engineering.
Preserve existing repo structure.
Use the docs as product truth.