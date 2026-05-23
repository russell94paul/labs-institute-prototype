---
tags: [roadmap, planning, neurospect, strategic]
aliases: [Neurospect Roadmap, Product Roadmap]
sources: []
created: 2026-04-25
updated: 2026-04-25
---

# Neurospect Roadmap

Forward-looking product roadmap for Neurospect. The destination is a **vertical AI platform for retail and prop-firm traders**: one place that absorbs the work currently spread across journaling tools, charting platforms, broker UIs, Discord communities, and risk dashboards — with an ICT-fluent AI coach as the connective tissue.

> **Operating principle:** Production stability before new features. Until the existing build (trade journal, analytics, AI Coach, course KB) is deployed, polished, and proven on real users, new feature scope stays in this backlog. The Now horizon is non-negotiable.

> **Isolation Rule reminder:** This roadmap is Neurospect-only. ALDC business context does not belong here. See [[CLAUDE]] § *Isolation Rule*.

## What's already built

For grounding (full detail in [[entities/projects/neurospect]]):

- **Build Phases 1–4 shipped** locally: FastAPI backend, ICT-specific trade journal, screenshots, 7-view analytics dashboard, AI Coach pipeline (TradingView → Claude → polling panel).
- **Course & KB complete**: 5 modules, 7 entry models with machine-readable YAML strategy blocks.
- **Deployment Phase 1 complete**: prompt files bundled, gunicorn + requirements.txt, DB shim, render.yaml ([[processes/distributed-workflow/active/deployment]]).

The original v1 phased plan in [[entities/projects/neurospect]] is **superseded by this document** for forward planning. The "what's built" list there remains the source of truth for current state.

---

## Horizons

The roadmap uses horizons rather than dated phases. Items move horizons as evidence accrues; only **Now** is committed.

| Horizon | Confidence | Typical window |
|---|---|---|
| **Now** | committed | 0–4 weeks |
| **Next** | high — building on what exists | 1–4 months |
| **Later** | medium — high-value expansion | 4–9 months |
| **Strategic** | low — defines product ceiling | 9+ months |
| **Research** | exploratory — shape unknown | unscheduled |
| **Compliance-Sensitive** | gated on legal review | unscheduled |

## Status

Every idea page carries a lifecycle status in its frontmatter. The status, not the horizon, tells you whether work is active.

| Status | Meaning |
|---|---|
| `backlog` | captured here; not actively worked |
| `designing` | spec being written under `concepts/architecture/` (or `concepts/business-logic/`) |
| `in-progress` | active workstream tracker exists under `processes/distributed-workflow/active/` |
| `shipped` | implemented and reconciled per [[CLAUDE]] § *Architecture Doc Integrity* |
| `paused` | was active, set aside; reason captured in the idea page |
| `dropped` | decided not to pursue; reason captured in the idea page |

When status changes, update the idea page frontmatter, the status pill in the relevant horizon section below, and (where applicable) link forward to the spec or tracker.

---

## Now — Production Stabilization

**No new features in this horizon.** The job is to get what's built into a state where real users can rely on it.

- **Finish deployment** — Render dashboard setup, Cloudflare Pages, Discord OAuth wiring, R2 screenshots, end-to-end verification. Tracked in [[processes/distributed-workflow/active/deployment]].
- **Beta hardening** — error monitoring (Sentry), structured logging review, rate limiting, abuse protection, basic uptime monitoring.
- **Polish on real usage** — fix bugs surfaced by Paul + initial beta users; tighten the trade form, analytics, and coach UX.
- **Sync rule discipline** — keep the wiki AI Coach prompts in lock-step with `neurospect-api/app/coach/prompts/` (see deployment tracker §1a).

**Exit criteria:** TradingView webhook → Claude → frontend coaching panel works end-to-end on production. Trade journal CRUD + screenshots + analytics work for at least one external beta trader. Error rate stable. *Then* the Next horizon unlocks.

## Next — Reduce Friction, Close the Original Plan

Items that finish the original v1 plan and pick up the highest-value, lowest-risk new ideas. Each one lowers the cost of using Neurospect daily.

- [[concepts/roadmap/ideas/reduce-journaling-friction]] — voice journaling, auto-populated trade fields, guided prompts, templates · *backlog*
- [[concepts/roadmap/ideas/tradovate-integration]] — broker import for prop accounts; foundation for live risk + multi-account analytics · *backlog*
- [[concepts/roadmap/ideas/chrome-screenshot-extension]] — capture chart screenshots into Neurospect with one click · *backlog*
- [[concepts/roadmap/ideas/mistake-driven-action-items]] — turn mistake tags from the journal into concrete improvement tasks · *backlog*
- [[concepts/roadmap/ideas/multi-account-portfolio-analytics]] — multi-account / prop-firm filters across the existing analytics dashboard · *backlog*
- **Replay mode for trade review** *(original v1 Phase 2; no idea page yet — capture before scoping.)*
- **Auto-generated weekly review** *(original v1 Phase 2; no idea page yet.)*

## Later — Risk, Discipline & AI Expansion

Behavioural and intelligence layers. Most of these depend on **Next** items having shipped (broker data, multi-account, mistake action items).

- [[concepts/roadmap/ideas/overtrading-risk-limits]] — daily loss limits, max trades, cooldowns, drawdown awareness, account-protection rules · *backlog*
- [[concepts/roadmap/ideas/trader-psychology-profiler]] — type the trader from journal entries, behaviour patterns, and emotional triggers · *backlog*
- [[concepts/roadmap/ideas/neurospect-voice]] — voice-based ICT/psychology coach with persistent user memory · *backlog*
- [[concepts/roadmap/ideas/in-app-course-section]] — structured learning surface inside the app, sourced from the existing course KB · *backlog*
- [[concepts/roadmap/ideas/ui-design-exploration]] — differentiated UI/workflow patterns ("Clause" design exploration); runs in parallel · *backlog*
- **AI-generated ICT trade reviews** *(original v1 Phase 3.)*
- **Personal edge detection / A+ setup scoring** *(original v1 Phase 3.)*
- **Auto-tagging from chart/image/context** *(original v1 Phase 3.)*
- **Narrative consistency analysis** *(original v1 Phase 3.)*
- **Confidence/emotion tracking + rule violation tracking** *(original v1 Phase 2.)*

## Strategic — Platform Bets

Items that move Neurospect from "best ICT journal + coach" to "the trader's home base." These define the product ceiling and need real evidence before commitment.

- [[concepts/roadmap/ideas/platform-consolidation]] — deep, durable integrations with Discord, TradingView, Tradovate; trader does not switch tabs · *backlog*
- [[concepts/roadmap/ideas/vertical-ai-platform]] — strategic positioning as **the** vertical AI product for retail + prop-firm traders · *backlog*
- **Original v2 moonshots** that survive: Execution Guardian, Regime Shift Detector, Personalized Market Twin, Liquidity Map OS, Kill Zone Decision Assistant. Catalogued in [[entities/projects/neurospect]] § *Moonshot Ideas*.

## Research — Shape Unknown

Ideas worth tracking but not yet ready to scope. Capture, monitor, revisit.

- [[concepts/roadmap/ideas/agent-as-a-service]] — surfacing Neurospect's agent capabilities to external users/products; use cases unclear · *backlog*

## Compliance-Sensitive — Gated on Legal Review

These ideas have real product appeal **and** real regulatory or IP exposure. They stay here until counsel is engaged. Do not promise these to users or in marketing copy.

- [[concepts/roadmap/ideas/ai-live-audio-commentary]] — live market commentary / squawk-box-style audio. **Constraint:** no real-person voice cloning, no copyrighted YouTube content · *backlog*
- [[concepts/roadmap/ideas/neuro-quant-fund]] — automated strategy research; longer-term "Neuro-Fund" investment-vehicle concept. **Constraint:** investment-vehicle territory is heavily regulated · *backlog*

---

## Prioritization rationale

Items in **Next** were chosen because each one:

1. **Compounds existing assets.** Trade journal + mistake tags + analytics dashboard already exist; friction reduction, action items, and multi-account filtering each add a layer the trader sees immediately.
2. **Has a clear path to data.** Tradovate integration + Chrome extension produce inputs that feed every later horizon.
3. **Is feasible without new infrastructure.** Voice journaling reuses the AI Coach pipeline; mistake-driven action items reuse the journal schema.

Items in **Later** require **Next** to have shipped. Risk limits without live broker data is a UI gimmick; the psychology profiler without months of journal entries has nothing to profile; voice coaching without user-memory infrastructure is a chatbot.

Items in **Strategic** require evidence from **Later** that the AI coaching surface is genuinely valued — without that, platform consolidation is a feature checklist, not a product moat.

## Lifecycle: idea → spec → workstream → shipped

1. Idea captured here as a stub in `concepts/roadmap/ideas/` with `status: backlog`.
2. When an idea earns commitment, it enters **design**: a spec page is created under `concepts/architecture/` (or `concepts/business-logic/`). Idea page status flips to `designing` and links forward to the spec.
3. When implementation starts, a **tracker** is created at `processes/distributed-workflow/active/<workstream>.md`. Idea page status flips to `in-progress` and links to the tracker.
4. After implementation completes and the architecture doc is reconciled per [[CLAUDE]] § *Architecture Doc Integrity*, idea page status flips to `shipped`.
5. The idea page itself stays in `concepts/roadmap/ideas/` throughout. Spec is canonical for design; tracker is canonical for execution; idea page is the strategic origin record and lifecycle index.

Naming note: "NeuroSpect Voice", "Neuro-Quant", and "Neuro-Fund" are placeholders. Better names may be picked later.

## See Also

- [[concepts/roadmap/ideas/README]] — idea-backlog index
- [[entities/projects/neurospect]] — project entity, current state, original v1 plan, moonshot catalogue
- [[concepts/architecture/tech-stack]] — backend stack (constrains what's feasible Now/Next)
- [[concepts/architecture/trade-schema]] — journal data model (constrains journal-related ideas)
- [[concepts/architecture/tradingview-connector]] — AI Coach pipeline (constrains coaching-related ideas)
- [[concepts/architecture/phase3-frontend-structure]] — frontend layout (constrains UI ideas)
- [[concepts/architecture/phase4-coach-frontend]] — AI Coach UI (constrains voice-coaching ideas)
- [[concepts/business-logic/ict-live-commentary]] — conceptual foundation for live commentary feature
- [[processes/distributed-workflow/active/deployment]] — Now-horizon active work
- [[processes/distributed-workflow/active/ai-coach]] — AI Coach tracker
- [[processes/distributed-workflow/active/journal-analytics]] — Journal tracker
- [[processes/distributed-workflow/active/course-and-kb]] — Course & KB tracker
