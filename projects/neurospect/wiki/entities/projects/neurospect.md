---
tags: [entity, project, neurospect, trading, journal, ai-assistant, ict]
aliases: [Neurospect, NeuroSpect]
sources: []
created: 2026-04-16
updated: 2026-04-26
deployment_status: live
phase3_status: complete
phase4_status: complete
tradingview_webhook_status: verified_end_to_end
journaling_ux_phase1_status: in_progress
---

# Neurospect

Neurospect is a trading journal and AI-powered trade analysis platform designed specifically for ICT (Inner Circle Trader) / Smart Money Concepts traders. It goes beyond generic journaling to capture decision structure, market narrative, execution quality, and behavioral patterns, with the goal of becoming a personalized trading intelligence system.

**One-line vision**: "NeuroSpect helps ICT traders turn smart-money concepts into clearer narratives, better execution, and fewer low-quality trades."

## Vision / Goal

Start as an ICT trade journal and analytics platform that captures narrative, context, and execution quality deeply enough to later become a personalized trading intelligence system. The core principle: do not build "just a journal" -- build a system that captures what the trader saw, why they took the trade, what the market context was, how they executed, what happened after, and what pattern it belongs to.

The strongest product framing is not "track trades" but:
- Identify their real edge
- See which ICT setups actually work for them
- Spot recurring mistakes
- Improve execution discipline
- Convert screenshots and narratives into a personal playbook

## Current State

**Phase 4 (AI Coach frontend) is implemented.** Both the backend (`api/`) and frontend (`app/`) are fully functional in local development with the complete AI Coach pipeline — TradingView webhook → Claude coaching → live panel with polling. (As of 2026-05-02, all three modules — wiki, api, app — live in a single `neurospect` monorepo; see [[processes/distributed-workflow/active/monorepo-migration]].)

What's built:
- FastAPI backend with Discord OAuth2 (JWT-based SPA pattern) + debug login for local dev
- ICT-specific trade journal: CRUD, screenshots (Cloudflare R2), 7 analytics endpoints
- AI Coach: TradingView webhook ingestion, Claude API coaching calls, polling endpoints, TV token management
- Postgres schema: 12 ENUMs, 5 tables, full Alembic migration chain
- React 19 + TypeScript frontend (`app/`): auth flow, trade CRUD UI, analytics dashboard
- Screenshot upload (per-phase drag-and-drop), thumbnail grid, lightbox viewer
- Analytics dashboard: summary cards, breakdown tables, day-of-week chart, mistake chart, R-distribution histogram
- **AI Coach frontend:** `/coach` live panel (bias badge, narrative, strategy cards with checklist, invalid strategies, alerts, freshness pill, dynamic 2s/10s polling) + `/coach/setup` (token management with rotate/revoke Dialogs, Pine script download + preview, TradingView setup instructions)
- ICT course knowledge base: 5 modules, 7 entry models with machine-readable YAML strategy blocks
- Claude system prompt + strategies.json for live coaching

Extensive design research from the planning phase (v2) covering event-sourced journal architecture, AI trade analysis, behavioral analytics, broker API integration, rule engines, Discord bot architecture, and trading mentor industry analysis remains documented but is not yet implemented. A v2-moonshot track explores more ambitious future features.

## Architecture (v2 Design)

### Backend: Event-Sourced Journal

The backend is fundamentally an **event-normalization and reconciliation system**:
- **Append-only event log** with idempotent ingestion (broker feeds are inherently eventful)
- **Canonical schema**: Accounts, Instruments, Orders, Fills, Positions, Events, Tags, Audit Logs
- **Trade lifecycle state machine** supporting partial fills, cancels/replaces, OCO/bracket orders, scaling in/out
- **Dual storage**: OLTP (write-heavy journal data) + OLAP/time-series (rolling metrics, heatmaps, attribution)
- **Raw broker payload retention** in object storage for auditability
- **Postgres core** with JSONB for flexible broker payloads, partitioned event tables

### AI Assistant

- **Chart pattern recognition**: Time-series motifs, shapelets, wavelet multi-resolution analysis, 2D CNNs on candlestick images, transformer models
- **Trade classification**: Supervised ML on trade features (price, indicators, volume, time-of-day) with walk-forward validation
- **Risk assessment**: Per-trade (MAE/MFE, slippage) and portfolio-level (VaR/ES, scenario stress tests)
- **Composite trade quality scoring**: Multi-dimensional score (entry validity, position sizing, stop adherence, target achievement, risk/reward) with cohort benchmarking
- **NLP trade reasoning**: LLM-based extraction of structured intent from free-text trader notes (entry, stop, target, rationale)
- **Feedback modes**: Real-time alerts and post-trade review reports with explainability (saliency maps, natural-language rationales)

## Key Decisions

1. **ICT-specific, not generic**: The platform speaks ICT language (liquidity sweeps, MSS/BOS, FVGs, order blocks, premium/discount, kill zones, SMT) rather than offering generic trading analytics
2. **Structured trade schema**: ICT-specific fields (HTF bias, draw on liquidity, setup type, displacement quality, FVG presence, session/kill zone) alongside standard fields
3. **Narrative builder**: Pre-trade thesis capture (bias, dealing range, liquidity target, invalidation) compared against actual market behavior post-trade
4. **Event sourcing + projections**: Append-only broker events table with derived current-state tables, because broker feeds are eventful and reprocessing is inevitable
5. **Screenshot-first journaling**: Visual chart capture at multiple points (before entry, entry, exit, higher timeframe) because ICT trading is highly visual and screenshots become future training data

## Phased Roadmap

> **Superseded for forward planning.** The horizon-based roadmap at [[concepts/roadmap/README]] is the canonical forward-planning artefact. The v1 phased plan below is kept for historical reference — most of Phase 1 (and parts of Phase 2/3) have already shipped; see *Current State* above for what's actually built.

### Phase 1 -- MVP
- Manual trade journal with ICT-specific structured schema
- Screenshot uploads with markup tools
- Basic analytics dashboard (by setup type, session, instrument, bias alignment)
- Pre-trade narrative form and post-trade ICT review form
- Mistake tagging and setup quality grading
- Personal playbook page

### Phase 2 -- Sticky Product
- Broker import / automatic trade sync
- Chart screenshot markup tools
- Replay mode for trade review
- Rule violation tracking
- Confidence/emotion tracking
- Auto-generated weekly reviews
- Top mistake and best-condition insights

### Phase 3 -- AI Intelligence Layer
- Auto-tagging from chart/image/context
- AI-generated ICT trade reviews in ICT language
- Personal edge detection
- A+ setup scoring
- Execution warnings
- Narrative consistency analysis
- Personalized coaching feed

## Moonshot Ideas

> **Superseded for forward planning.** The catalogue below is preserved as a research record. Forward-planning decisions on these (and on newer brainstormed ideas) live in [[concepts/roadmap/README]] under the *Strategic* and *Research* horizons.

The v2-moonshot track explores 10 ambitious future directions, with the top 4:

1. **Execution Guardian**: Detects likely self-sabotage (revenge trading, FOMO, plan deviation) and adds friction (cooldowns, forced checklists, reduced-size mode)
2. **Regime Shift Detector**: Identifies when the market environment has structurally changed and strategies should adapt
3. **Autonomous Catalyst Mapper**: Maps second- and third-order effects from news across asset classes in real time
4. **Personalized Market Twin**: Builds a live simulation of the trader's behavior, risk tolerance, and patterns

ICT-specific moonshots include: Narrative-to-Execution Engine, A+ Setup Filter, Liquidity Map OS, Kill Zone Decision Assistant, Market Structure Interpreter, Personal ICT Coach, Replay Tutor, SMT + Intermarket Intelligence Layer, Entry Model Builder, and ICT Trade Review Engine.

## ICT Strategy Context

The platform's data model and AI layer are built around ICT / Smart Money Concepts. The key concept areas are documented as skeleton pages below and will be fleshed out as mentor video transcripts are ingested.

- [[concepts/business-logic/ict-market-structure]] — MSS, BOS, displacement, HTF bias
- [[concepts/business-logic/ict-liquidity]] — draw on liquidity, pools, BSL/SSL, premium/discount
- [[concepts/business-logic/ict-narratives]] — day-of-week framing, dealing ranges, pre-trade thesis
- [[concepts/business-logic/ict-entry-models]] — FVGs, order blocks, kill zones, OTE
- [[concepts/business-logic/ict-smt]] — SMT divergence, intermarket analysis

## Open Questions / Next Steps

- ~~Choosing technology stack~~ — **resolved:** Python/FastAPI + Postgres + Render + Discord OAuth. See [[concepts/architecture/tech-stack]].
- ~~Phase 3 (frontend)~~ — **complete.** See [[concepts/architecture/phase3-frontend-structure]].
- ~~Phase 4 (AI Coach frontend)~~ — **complete.** See [[concepts/architecture/phase4-coach-frontend]].
- **Deployment — live, fully operational (2026-04-26).** Backend on Render (Python 3.13, gunicorn + UvicornWorker, Alembic migrations in startCommand), frontend on Cloudflare Pages. Discord OAuth working. Trade journal saving. TradingView webhook → Claude → coach panel verified end-to-end. R2 screenshots working. `TRADINGVIEW_IP_ALLOWLIST` enabled. Webhook secret and user token rotated.
- **Journaling UX Phase 1 — in progress (2026-04-26).** Tab-based trade form (Pre-Trade / Entry / Post-Trade) implemented in `app/`. Pre-Trade fields split into 6 prominent + Advanced collapsible (6 optional fields). Defaults: trade_date = today, instrument = NQ. Pine script static mirror synced v5→v6. Pushed to monorepo `main` 2026-05-02 (was awaiting push at the time of the merge).
- Broker API integration strategy (which brokers first, auth flows, rate limiting)
- Discord bot integration for community features
- Data pipeline for market context snapshots at trade entry time
- Model training data strategy for chart pattern recognition
- Multi-account / prop-firm tracking requirements

## See Also

- [[concepts/architecture/transcript-pipeline]] — how mentor video transcripts are ingested
- [[concepts/business-logic/ict-market-structure]]
- [[concepts/business-logic/ict-liquidity]]
- [[concepts/business-logic/ict-narratives]]
- [[concepts/business-logic/ict-entry-models]]
- [[concepts/business-logic/ict-smt]]
