# Deep Research Prompt: AI-Guided Onboarding & Decision Simulation

## Purpose

Research how to design an AI-guided product onboarding and decision simulator, informing Conductor's onboarding flow, recommendation engine, and scenario simulation UI.

## When to Run

Run after Topics 1, 2, and 5 are complete (Priority 5). This builds on the architecture and memory system decisions.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research how to design an AI-guided product onboarding and decision simulator for software product development.**

Context: I'm building a product orchestration platform (called "Conductor") where users start by answering onboarding questions about what they want to build. The platform then recommends product scope, features, architecture, infrastructure, compliance level, support level, timeline, and budget trade-offs. Users can adjust sliders to explore different scenarios before committing to a plan.

The platform supports three entry paths:
1. New product build from scratch
2. Improving an existing product
3. Migrating an existing data/service stack

The backend uses Claude (AI) for generating recommendations. The frontend is a vanilla HTML/CSS/JS SPA.

I need to understand:

1. **Onboarding flow design** — how to design an adaptive questionnaire that gathers enough information for meaningful recommendations without overwhelming the user. Progressive disclosure patterns. Conditional questions based on prior answers. How to handle incomplete information gracefully.

2. **Decision model** — how to model the multi-dimensional decision space (features, architecture, timeline, budget, compliance, risk, automation, support). How dimensions interact (adding compliance increases cost and timeline). How to handle constraints vs. preferences.

3. **Recommendation scoring model** — how to score and rank AI-generated recommendations. What makes a recommendation "good"? How to incorporate historical data (previous successful builds) into recommendations. How to explain recommendations to users (not just "trust the AI").

4. **Scenario simulator design** — how to build an interactive scenario simulator with sliders for budget, timeline, user count, scalability, compliance, automation, support, and risk tolerance. How slider changes propagate through the model to update all dependent variables. Real-time vs. batch recalculation. How to show meaningful differences between scenarios.

5. **Cost/ROI model** — how to estimate development costs, operational costs, time-to-market, and ROI for different product configurations. What inputs are needed. How accurate can estimates be. How to present uncertainty ranges rather than false precision.

6. **UI patterns** — what UI patterns work for multi-dimensional decision making. Radar charts, trade-off matrices, scenario comparison tables, slider panels. How to make complex trade-offs accessible to non-technical product owners. Mobile considerations.

7. **Data model** — how to store onboarding responses, recommendations, scenarios, and decisions. How to version scenarios so users can compare. How decisions feed into the pipeline/phase generation.

8. **Implementation roadmap** — what to build first for an MVP. What can be hardcoded vs. what needs to be dynamic from day one. How to validate that recommendations are useful before building the full simulator.

Provide your output as a structured report with:
- Onboarding flow (steps, questions, branching logic)
- Decision model (dimensions, interactions, constraints)
- Recommendation scoring model
- Scenario simulator design (architecture, UI, data flow)
- Cost/ROI model (inputs, calculations, output format)
- UI patterns (with mockup descriptions)
- Data model (schemas, relationships)
- Implementation roadmap (MVP → full product)

Reference existing products: Vercel's project setup, Stripe Atlas, AWS Well-Architected Tool, Figma's onboarding, Linear's project setup. Identify patterns to borrow.

---

## Expected Output Filename

`03-ai-product-onboarding-decision-simulation.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Onboarding UI design
- Recommendation engine architecture
- Decision simulator frontend
- Cost estimation model
- Phase/pipeline generation from approved plans
- Client portal onboarding experience
