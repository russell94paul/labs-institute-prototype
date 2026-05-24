---
name: ns-phase3-neurograph
description: NeuroSpect Phase 3-NG — NeuroGraph Planning (Data Source Discovery + Architecture)
---

You are working on **NeuroSpect Phase 3-NG** (NeuroGraph Planning). This is a **plan-mode-first** phase to design the persistent trading intelligence graph before building it.

**Start this phase in plan mode.** Do not implement until the data source mapping is approved.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\wiki\CLAUDE.md` — wiki corpus structure
4. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\models\trade.py` — trade data model (100+ fields)
5. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\models\enums.py` — 17 ICT enums
6. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\wiki\concepts\entry-models\` — 7 strategy YAMLs
7. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\wiki\concepts\business-logic\` — 8 ICT concept docs
8. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\wiki\concepts\course\` — 5 course modules
9. Read Zeus Memory architecture at `C:\Users\PaulRussell\repos\wiki` for pattern reference

## What is NeuroGraph

A **persistent, connected knowledge graph** for trading intelligence. Every trade, event, feature, model evaluation, coaching interaction, and behavior pattern becomes a node. Relationships between them become edges. The graph compounds with every interaction — the longer you use NeuroSpect, the smarter it gets about YOUR trading.

**NeuroGraph IS:**
- A connected knowledge graph (nodes = entities, edges = relationships)
- Seeded with data sources on first build (wiki, ICT concepts, instrument metadata)
- Temporal and regime-aware (knows WHEN and UNDER WHAT CONDITIONS something was learned)
- Queryable by every component (Mentor, EdgeLab, Forensics, NeuroScore, Prop Shield)
- The compounding moat — switching to a competitor means losing all accumulated intelligence

**NeuroGraph IS NOT:**
- NeuroCore (which retrieves static wiki content via RAG)
- A simple database log
- A trading signal generator

## Goal (Plan Mode)

Map all potential data sources, design the graph schema (node types, edge types, properties), identify what can be seeded immediately vs what accumulates over time, and produce an implementation plan.

## Phase 3-NG Plan Deliverables

### 1. Data Source Inventory

Identify and catalog every data source NeuroGraph can connect to:

**Internal Sources (already in the codebase):**
- Trade journal entries (100+ fields, 17 enums)
- Wiki corpus (36K+ lines, 111 files)
- 7 ICT entry model YAML specs
- 5 course modules (18 lessons)
- Tradovate fills and account data
- Analytics calculations (7 endpoints)
- Behavior metrics (Phase 2: tilt, discipline, consistency)

**Future Internal Sources (built in later phases):**
- ICT events (Phase 4: FVGs, sweeps, OBs, market structure)
- EdgeLab experiments (Phase 5: backtests, features, Monte Carlo)
- Coaching conversations (Phase 6: questions, answers, citations)
- Edge Forensics hypotheses (Phase 7)
- NeuroScore calculations (Phase 8)
- NSLM evaluations (Phase 11)

**External Sources to Evaluate:**
- Market data feeds (OHLCV, tick data, session context)
- Economic calendar (news events, FOMC, NFP, CPI)
- Broker APIs (account balance, positions, margin)
- Social sentiment (Twitter/X trading sentiment, optional)
- Prop firm APIs (if available — rule status, account health)
- Instrument reference data (tick size, session times, contract specs)
- Volatility indices (VIX, MOVE, etc.)
- Correlation data (NQ/ES/YM relationships)
- COT reports (Commitment of Traders, weekly)
- Dark pool / institutional flow (if accessible, premium data)

### 2. Graph Schema Design

Define node types, edge types, and properties:

**Node Types (entities in the graph):**
- `Trade` — individual trade with outcome, setup, context
- `Setup` — ICT setup type (E&R, Consolidation, Breaker, etc.)
- `Event` — detected ICT event (FVG, sweep, OB, MSS)
- `Session` — trading session (London, NY AM, NY PM, Asia)
- `Instrument` — NQ, ES, YM, GC
- `Regime` — market regime at time of trade
- `Feature` — quantitative feature (displacement z-score, FVG distance, etc.)
- `Pattern` — recurring behavioral pattern (tilt trigger, winning streak)
- `Concept` — ICT concept from wiki (seeded from wiki corpus)
- `Lesson` — course lesson or coaching insight
- `Experiment` — EdgeLab backtest result
- `Model` — NSLM prompt/model version
- `Hypothesis` — Edge Forensics hypothesis

**Edge Types (relationships):**
- `trade → used_setup` — which setup was traded
- `trade → during_session` — when it happened
- `trade → in_regime` — market conditions
- `trade → near_event` — ICT events at entry/exit
- `trade → produced_pattern` — behavioral patterns detected
- `setup → requires_concept` — concepts needed for this setup
- `feature → predicts_outcome` — feature-outcome correlations
- `experiment → tested_setup` — what was backtested
- `hypothesis → explains_pattern` — forensics connections
- `concept → taught_in_lesson` — educational graph

### 3. Seed Strategy

What to populate immediately (before any user trades):
- All wiki concepts as `Concept` nodes
- All 7 entry models as `Setup` nodes with `requires_concept` edges
- All course lessons as `Lesson` nodes with `taught_in_lesson` edges
- Instrument metadata as `Instrument` nodes
- Session definitions as `Session` nodes
- Known feature definitions as `Feature` nodes

### 4. Accumulation Strategy

How the graph grows over time:
- Every trade close → create `Trade` node + edges to setup, session, regime, events
- Every coaching session → create/update `Lesson` nodes, `Concept` access patterns
- Every EdgeLab experiment → create `Experiment` node + edges to features, setups
- Every behavior metric update → create/update `Pattern` nodes
- Confidence scoring: new nodes start at 0.5, reinforced patterns increase, contradicted ones decrease
- Decay: unused connections fade over time unless reinforced

### 5. Query Patterns

How components will query NeuroGraph:
- **Mentor:** "What does this trader struggle with?" → traverse Pattern + Concept nodes
- **EdgeLab:** "Has this strategy been tested before?" → traverse Experiment + Setup nodes
- **Forensics:** "What conditions correlate with this loss pattern?" → traverse Trade + Event + Regime nodes
- **NeuroScore:** "Is this trader improving?" → time-series over Pattern confidence scores
- **Prop Shield:** "What precedes this trader's tilt episodes?" → traverse Pattern + Trade + Session nodes
- **Launch Modal:** "What parameters worked best for this phase?" → traverse Experiment + Model nodes

### 6. Technology Decision

Evaluate graph storage options:
- **PostgreSQL + JSONB** (simple, no new infra, graph queries via recursive CTEs)
- **pgvector + relational** (hybrid: vector search for semantic, relations for graph)
- **Neo4j** (native graph DB, most powerful queries, new infrastructure)
- **NetworkX in-memory** (fast for small graphs, no persistence)

Recommendation: Start with PostgreSQL + JSONB (same DB, no new infra). Migrate to Neo4j only if graph queries become a bottleneck.

## Key Constraints

- Plan mode first — no implementation until data source mapping is approved
- Must work with zero data (graceful for new users, seeded with wiki/concepts)
- Must support deletion (GDPR/privacy)
- Must not generate trading recommendations — only provides context
- Seeded data is read-only (wiki concepts don't change based on user behavior)
- User-generated data is personal (multi-tenant from day one)

## Acceptance Criteria (Plan Phase)

- [ ] Complete data source inventory (internal + external) with feasibility ratings
- [ ] Graph schema document (all node types, edge types, properties)
- [ ] Seed strategy document (what's loaded on first build)
- [ ] Accumulation strategy document (how graph grows per interaction)
- [ ] Query patterns document (how each component uses NeuroGraph)
- [ ] Technology recommendation with tradeoffs
- [ ] Implementation plan with effort estimates
- [ ] External data source API research (availability, cost, rate limits)

## NeuroFusion-13 Research Context

Before implementation, read the following SIHRE research reports for techniques that should be incorporated:
- `research/neurofusion/data/prompt-3-knowledge-graph.md` — temporal knowledge graph design, confidence decay and reinforcement, GNN architecture for trading intelligence, and graph query patterns relevant to NeuroGraph schema and accumulation strategy

## When done

Say: "NeuroGraph planning complete. Data sources mapped, schema designed, seed strategy defined. Review the plan, then start implementation with `/ns-phase3-neurograph-build`."
