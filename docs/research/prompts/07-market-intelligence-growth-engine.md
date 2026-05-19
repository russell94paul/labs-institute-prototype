# Deep Research Prompt: Market Intelligence & Growth Engine

## Purpose

Research how to build a market intelligence and growth strategy module, informing Conductor's competitive analysis, pricing, growth experiments, and feature prioritization capabilities.

## When to Run

Run last (Priority 7). This is a growth/strategy layer that builds on top of the core platform.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research how to build a market intelligence and growth strategy module inside a product-building platform. The system should identify competitors, market gaps, positioning options, pricing options, feature opportunities, growth channels, referral/incentive strategies, and launch plans. It should translate market gaps into product features with cost, value, risk, and ROI estimates.**

Context: I'm building a product orchestration platform (called "Conductor") that manages the full lifecycle of software products. Beyond just building products, I want Conductor to help users make strategic decisions: what to build, how to position it, how to price it, and how to grow it.

This module would sit alongside the build orchestration engine and feed into the onboarding/decision simulation flow. When a user is deciding what to build, market intelligence should inform the recommendations.

I need to understand:

1. **Market research workflow** — how to systematically research a market as part of the product development process. What data sources to use (public APIs, web scraping, industry reports). How to structure competitive analysis. How to keep research current.

2. **Competitor model** — how to model competitors: features, pricing, positioning, strengths, weaknesses, market share, funding, team size. How to track competitors over time. How to identify direct vs. indirect competitors.

3. **Market gap to feature framework** — how to translate identified market gaps into specific product features. How to estimate the value, cost, risk, and ROI of addressing each gap. How to prioritize gaps. How to validate that a gap is real (not just perceived).

4. **Growth experiment model** — how to design, run, and evaluate growth experiments within the platform. A/B testing frameworks. Growth metrics (acquisition, activation, retention, referral, revenue). How to integrate experiment results into product decisions.

5. **Pricing strategy model** — frameworks for pricing a B2B SaaS platform with AI components. Usage-based vs. seat-based vs. tier-based. How to model pricing sensitivity. How AI compute costs affect pricing. How to handle enterprise vs. self-service pricing.

6. **Incentive/rewards risk model** — if the platform offers referral bonuses, partner incentives, or loyalty rewards, how to model the financial risk. Fraud prevention. Cap structures. Tax implications. When incentives help vs. when they create perverse incentives.

7. **Growth channels** — which growth channels work for B2B SaaS product platforms. Content marketing, partnerships, integrations, marketplaces, events, outbound sales. How to evaluate channel economics (CAC, LTV, payback period).

8. **Launch plan framework** — how to plan a product launch. Pre-launch, launch, post-launch phases. Beta programs. Waitlists. Launch metrics. How to handle a soft launch vs. hard launch.

9. **UI/dashboard ideas** — how to present market intelligence to product owners. Competitive landscape visualizations. Feature gap matrices. Pricing comparison tools. Growth dashboards.

Provide your output as a structured report with:
- Market research workflow (steps, tools, cadence)
- Competitor model (schema, tracking strategy)
- Market gap to feature framework (process, scoring)
- Growth experiment model (design, metrics, evaluation)
- Pricing strategy model (frameworks, calculations)
- Incentive/rewards risk model (financial model, safeguards)
- UI/dashboard ideas (mockup descriptions)

Reference existing tools: Crayon, Klue, SEMrush, Mixpanel, Amplitude, Baremetrics, ProfitWell. Identify patterns to borrow.

---

## Expected Output Filename

`07-market-intelligence-growth-engine.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Market intelligence module design
- Pricing model
- Growth strategy
- Feature prioritization framework
- Onboarding recommendation enrichment
- Competitive positioning
