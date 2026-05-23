# NeuroLLM: AI Trading Coach Platform — Complete Product & Technical Plan

---

## Executive Summary

**Current state:** NeuroSpect is a deployed, production trading journal + AI coaching platform for ICT traders. Phases 1-4 are live: FastAPI backend on Render, React 19 frontend on Cloudflare Pages, Discord OAuth, TradingView webhook → Claude Sonnet coaching, trade journal with 17 ICT-specific enums, 7 analytics views, and a 36K-line wiki with 5 course modules and 7 machine-readable entry models.

**Proposed pivot:** NeuroLLM.md proposes a B2B2C platform where trading instructors deploy personalized AI coaches trained on their content (RAG → LoRA fine-tuning → chart analysis → practice trading → automated trading).

**This plan's recommendation:** **Yes, proceed — but modify the approach significantly.**

The core modification: **Two parallel tracks.** Track A: Build a single-instructor ICT AI coaching product (Phases 0-6, ~31 weeks to revenue). Track B: Build the backtesting/NeuroQuant/NeuroTrader Agent pipeline (Phases 7-9, ~36 additional weeks). Track B can begin during Track A's beta phase. The null test at Phase 7C is a hard gate — if ICT strategies don't show statistically significant edge, Phase 9 (automated trading) pivots to better analytics and coaching tools instead.

**Product components:**
- **NeuroLLM** — Platform and company brand
- **NeuroSpect** — Consumer-facing AI coaching product (RAG + ICT knowledge + trade journal)
- **NeuroCortex** — Knowledge/retrieval layer (hybrid 3-signal search, cross-wiki intelligence, all knowledge sources indexed)
- **Backtesting Platform** — Event-driven ICT strategy evaluation with Monte Carlo + walk-forward
- **NeuroQuant** — Hybrid LLM + ML system (ICT features + quant features + regime detection + model ensemble)
- **NeuroTrader Agent** — Automated trading agent (shadow → paper → live progression with 5-layer safety)

**Key numbers:**
- Coaching MVP cost: $6-107/month
- Full platform cost (all systems): $150-700/month
- Timeline to coaching revenue: ~31 weeks (8 months)
- Timeline to backtesting platform: ~43 weeks (11 months)
- Timeline to paper trading agent: ~63 weeks (16 months)
- Timeline to live trading (conditional): ~68 weeks (17 months)
- Team: 2 engineers, no additional hires needed through Phase 8

---

## 1. Current Repo Assessment

### What's Built and Deployed

| Component | Status | Technology | Reusability for NeuroLLM |
|---|---|---|---|
| Backend API | Live on Render | FastAPI, SQLAlchemy async, PostgreSQL 16, Alembic | 100% — extend, don't replace |
| Frontend | Live on Cloudflare Pages | React 19, TypeScript, Vite, TanStack Query, shadcn/ui | 100% — add chat UI alongside existing |
| Auth | Live | Discord OAuth2, JWT | 100% — works as-is |
| AI Coach | Live | Anthropic SDK, Claude Sonnet 4.6, prompt caching | 90% — extend for RAG + multi-turn chat |
| Trade Journal | Live | 100+ ICT-specific fields, 17 enums, 5 tables | 100% — keep for journaling, add agent tools on top |
| Analytics | Live | 7 endpoints, summary/breakdown/mistakes/R-distribution | 100% — reuse, add AI-specific metrics later |
| Screenshots | Live | Cloudflare R2, presigned URLs | 100% — extend for chart review |
| Broker Integration | Partial | Tradovate REST (auth + fills, not orders) | 100% — sufficient for MVP |
| Wiki/KB | Complete | 111 markdown files, 36K lines, YAML frontmatter | HIGH — this IS the RAG corpus |
| Course Content | Complete | 5 modules, 18 lessons, 7 entry models with YAML | HIGH — machine-readable, ready to embed |
| Source Transcripts | Complete | 32 immutable transcripts (4 volumes + streams) | MEDIUM — needs chunking/embedding, lower priority than structured KB |

### Key Architecture Files

- `api/app/coach/claude_client.py` — Core Claude integration; extend for RAG + multi-turn
- `api/app/coach/prompt_loader.py` — System prompt assembly; extend for dynamic RAG injection
- `api/app/coach/prompts/system-prompt-template.md` — Full ICT system prompt with strategy library
- `api/app/coach/prompts/strategies.json` — Machine-readable ICT strategy library (already loaded into Claude)
- `api/app/models/trade.py` — ICT trade data model (100+ fields)
- `api/app/models/enums.py` — 17 ICT-specific enums
- `wiki/concepts/business-logic/` — 8 core ICT concept docs (liquidity, structure, entry models, narratives, SMT, deviations, order flow, live commentary)
- `wiki/concepts/entry-models/` — 7 strategies with checklist YAML blocks
- `wiki/concepts/course/` — 5 modules, 18 lessons

### What's Strong

1. **The wiki corpus is real, structured, and deep.** 36K lines of curated ICT content with YAML frontmatter, cross-references, and source traceability. The "4-8 weeks of editorial curation" mentioned in NeuroLLM.md has largely been done — the `concepts/` directory IS the curated knowledge base.
2. **Machine-readable strategy blocks exist.** The 7 entry models have YAML blocks designed for the AI Coach system prompt. These are directly usable for both RAG retrieval and deterministic rule validation.
3. **The Claude integration is production-grade.** Prompt caching, structured JSON output, error handling, latency tracking — all proven in production.
4. **The async architecture is ideal for AI workloads.** FastAPI + SQLAlchemy async handles concurrent LLM calls naturally.

### What Needs Work

1. **No vector database or embedding pipeline.** Currently using static prompt injection (strategy library baked into system prompt), not dynamic RAG retrieval.
2. **No multi-turn chat.** The existing coaching pipeline is webhook → one-shot Claude call → polling. Need a conversational chat endpoint.
3. **No conversation persistence.** Coaching events are stored but not as chat sessions with message history.
4. **No subscription/billing.** Single-user system with no tiers or payment processing.

---

## 2. NeuroLLM Feasibility Assessment

### Recommendation: **Modify the approach significantly, then proceed**

The NeuroLLM spec is 60% correct. Here's the breakdown:

| Aspect | Verdict | Reasoning |
|---|---|---|
| Phase sequencing (RAG → SFT → Vision → Detection → RL) | **Correct** | Each phase genuinely requires the previous phase's infrastructure |
| Risk calibration | **Correct** | Unusually honest about 0% adversarial pass rate, look-ahead bias, ICT non-validation |
| B2B2C multi-instructor platform | **Premature** | Codebase is deeply ICT-specific; methodology-agnostic abstraction = full rewrite |
| Phase 1 (RAG coaching) | **Strong, build now** | Wiki corpus is RAG-ready; existing Claude integration handles this |
| Phase 2 (LoRA fine-tuning) | **Conditional** | Blocked on instructor providing 200+ coaching examples (a relationship problem, not a technical one) |
| Phase 3 (Chart analysis) | **Deprioritize** | 0% adversarial pass rate; hybrid approach (structured text + supplementary vision) is really just a rule-validation tool — call it what it is |
| Phase 4 (Practice trading) | **High-value but large** | Custom detection engine is 3-6 months of engineering; chart replay is buy-not-build |
| Phase 5 (Automated trading) | **Separate entirely** | Different infrastructure, different regulatory requirements, null test should be a standalone research project |

### What to Modify

1. **Drop the multi-instructor platform abstraction from MVP.** Build for one ICT instructor. If it works, refactor for multi-instructor as a Phase 7 workstream. This saves 4-8 weeks of unnecessary abstraction work.

2. **Skip Phase 2 (fine-tuning) until data exists.** A well-crafted system prompt with "speak in ICT terminology, be direct, reference specific price levels" gets 80% of the voice without any fine-tuning. Only invest in LoRA when the instructor has provided 200+ coaching examples AND users report the generic voice is a barrier.

3. **Rename Phase 3 from "chart analysis" to "structured trade review."** The hybrid approach (structured text input → rule validation → optional vision cross-check) is the correct design, but calling it "chart analysis" sets user expectations for a vision-first feature that doesn't work reliably.

4. **Move Phase 5 (automated trading) to a separate repo and research project.** The null test is a good idea but should not be in the product roadmap — it's a research gate.

### Assumptions Requiring Validation Before Building

| Assumption | How to validate | Risk if wrong |
|---|---|---|
| The instructor will provide content access and participate | Direct conversation; written agreement | Project cannot start |
| ICT wiki content is retrieval-friendly after embedding | Build test RAG pipeline with 5 concept docs, test 20 questions | Phase 1 quality is poor |
| Students will pay $29-149/month for AI coaching | Landing page with pricing → waitlist signups; interview 10 ICT traders | No revenue |
| 200+ coaching examples can be collected from the instructor | Ask directly; estimate effort | Phase 2 (fine-tuning) delayed indefinitely |
| The instructor has IP rights to their content | Verify contractually | Legal liability |

---

## 3. ICT Knowledge Modeling Plan

### Concept Classification

| Concept | Type | Operationalizable? | Data Requirements | Encoding Difficulty |
|---|---|---|---|---|
| **Market Structure** (STH/ITH/LTH, BOS, MSS) | Structural | YES — swing classification is rule-based | OHLCV + swing detection algo | Medium — subjectivity in swing classification |
| **Liquidity** (BSL/SSL, DOL, equal highs/lows) | Structural | YES — price level identification | OHLCV + level detection | Low — well-defined price levels |
| **Fair Value Gaps** (BISI/SIBI, IOFED, BAG) | Structural | YES — gap detection on 3-candle patterns | OHLCV | Low — precise 3-candle rule |
| **Order Blocks** | Structural | PARTIAL — requires "displacement" judgment | OHLCV + context | HIGH — "displacement" is subjective |
| **Breaker Blocks** | Structural | PARTIAL — depends on OB validity | OHLCV + OB detection | HIGH — chained subjectivity |
| **Displacement** | Qualitative | DIFFICULT — "significant impulse" is undefined | OHLCV + volatility context | VERY HIGH — no universal threshold |
| **Premium/Discount** | Structural | YES — 50% of range is deterministic | OHLCV + range bounds | Low |
| **Kill Zones** | Temporal | YES — fixed time windows | Clock | None — pure time lookup |
| **Sessions** | Temporal | YES — fixed time windows | Clock | None |
| **SMT Divergence** | Relational | YES — cross-instrument divergence | Multi-instrument OHLCV | Medium — need NQ+ES+YM simultaneously |
| **Bias Formation** | Composite | PARTIAL — combines HTF FVG + opening price | Multiple timeframe OHLCV | Medium — multi-timeframe alignment |
| **Entry Confirmation** | Composite | PARTIAL — combines multiple concepts | All above | HIGH — full system integration |
| **Invalidation** | Rule-based | YES — defined per entry model | Trade parameters + OHLCV | Low — clear stop/invalidation rules per model |
| **Risk Management** | Rule-based | YES — position sizing, R-multiple | Account data + trade parameters | Low |
| **Power of Three (AMD)** | Narrative | DIFFICULT — retrospective pattern recognition | OHLCV + session context | VERY HIGH — only identifiable after the fact |
| **Day-of-Week Protocol** | Rule-based | YES — specific rules per weekday | Calendar + price data | Low — well-documented rules |

### Concepts That Should NEVER Be Fully LLM-Delegated

1. **Kill zone / session time calculations** — deterministic, must be exact
2. **Position sizing and risk calculations** — arithmetic, cannot tolerate hallucination
3. **R-multiple computations** — exact math
4. **Order execution** — regulatory + reliability
5. **Opening price identification** — lookup, not inference
6. **Premium/discount calculation** — arithmetic on range bounds

### What the Wiki Needs Before RAG Deployment

The structured KB docs (`concepts/business-logic/`, `concepts/entry-models/`, `concepts/course/`) are already information-dense and well-structured. The raw transcripts (`sources/neurospect/`) need processing but are lower priority.

**Immediate (Phase 0-1):**
- Chunk structured KB docs at `##` section headers (~300-600 tokens per chunk)
- Build ICT terminology normalization dictionary (50+ terms: CHoCH, CISD, FVG, OTE, BISI, SIBI, etc.)
- Tag chunks with metadata: `source_file`, `section`, `tags`, `chunk_type` (concept/rule/example/checklist)
- Parse YAML strategy blocks separately for deterministic rule validation

**Later (Phase 2+):**
- Process raw transcripts: de-duplicate, normalize terminology, chunk at paragraph breaks
- Tag transcript chunks with lower retrieval priority than structured KB
- Build contradiction resolution: when multiple transcript versions disagree, flag and resolve with instructor

---

## 4. Wiki Transformation Plan

### Current State Assessment

| Dimension | Score | Notes |
|---|---|---|
| Content depth | 9/10 | 5 modules, 18 lessons, 8 business-logic docs, 7 entry models |
| Structure | 8/10 | Well-organized directories, consistent formatting |
| Metadata | 8/10 | YAML frontmatter with tags, aliases, sources, dates |
| Machine-readability | 7/10 | Entry models have YAML blocks; concept docs are prose |
| Cross-referencing | 7/10 | Wikilinks between pages; source traceability |
| Examples | 6/10 | Some worked examples in course lessons; need more |
| Visual content | 3/10 | Only 4 chart images; most concepts described in text |

### Transformation Strategy

The wiki should serve as **all of the above** — knowledge base for RAG, structured playbook, dataset generator, and evaluation corpus. The format is already close to ideal.

**Recommended storage format: Keep markdown + YAML frontmatter as the source of truth.** Generate derived formats (embeddings, JSONL for training, structured playbooks) via pipelines. Do not abandon the wiki format — it's version-controlled, human-readable, and already mature.

```
Source of Truth:           Derived Formats:
wiki/concepts/*.md    →    pgvector embeddings (for RAG retrieval)
                      →    strategies.json (for deterministic validation, already exists)
                      →    eval_dataset.jsonl (for quality testing)
                      →    training_pairs.jsonl (for future LoRA SFT)
```

### Chunking Strategy

| Content Type | Chunking Method | Target Size | Priority |
|---|---|---|---|
| Business-logic docs | Split at `##` headers | 300-600 tokens | 1 (highest) |
| Entry model explanations | Split at `##` headers | 300-600 tokens | 1 |
| Entry model YAML blocks | Keep as single chunk | Variable (up to 1000 tokens) | 1 |
| Course lessons | Split at `##` headers | 300-600 tokens | 1 |
| Live commentary protocols | Split at `##` headers | 300-600 tokens | 1 |
| Raw transcripts (Vol 1-4) | Split at paragraph breaks, 500-token window with 100-token overlap | 500 tokens | 2 (lower) |
| Stream transcripts | Split at paragraph breaks | 500 tokens | 3 (lowest — contextual, not reference) |

### Semantic Tagging Schema

Each chunk gets metadata stored in a JSONB column alongside its embedding:

```json
{
  "source_file": "concepts/business-logic/ict-liquidity.md",
  "section": "## Draw on Liquidity",
  "tags": ["concept", "liquidity", "DOL"],
  "chunk_type": "concept",      // concept | rule | example | checklist | transcript
  "priority": 1,                // 1 = structured KB, 2 = raw transcript
  "module": null,               // for course content: "module-1", "module-2", etc.
  "entry_model": null,          // for entry models: "consolidation", "london", etc.
  "ict_concepts": ["BSL", "SSL", "DOL", "FVG"],  // ICT terms mentioned
  "created": "2026-04-18",
  "updated": "2026-04-22"
}
```

### Evaluation Dataset Requirements

Before beta, create 100-200 question-answer pairs spanning all concepts:

```jsonl
{"question": "What makes a valid order block?", "expected_answer": "The last opposing candle before displacement...", "source": "concepts/business-logic/ict-entry-models.md#order-blocks", "concepts": ["OB", "displacement"], "difficulty": "basic"}
{"question": "When should I avoid trading during NFP week?", "expected_answer": "Monday through Wednesday of NFP week...", "source": "concepts/business-logic/ict-live-commentary.md#economic-calendar", "concepts": ["news", "NFP"], "difficulty": "advanced"}
```

---

## 5. Recommended Product Architecture

### System Architecture

```
                              FRONTEND
                        React 19 / Vite / TS
                        (Cloudflare Pages)
                              |
                        REST + SSE (streaming)
                              |
                        API LAYER (FastAPI, Render)
                   /     |      |       \        \
            Auth    Journal  Coach    Analytics  Billing
           (Discord  (CRUD   (Chat    (SQL       (Stripe
            OAuth2)  + R2)   + RAG)   queries)   webhooks)
                               |
                     AGENT ORCHESTRATION
                     (Anthropic SDK + custom tool loop)
                     /       |          \
              RAG          Tool         Conversation
            Pipeline     Execution       Memory
               |            |              |
           pgvector    Deterministic     PostgreSQL
           (same DB)   Rules Engine     (sessions +
               |       (kill zones,      messages)
          Embedding    opening prices,
           Pipeline    strategy
          (OpenAI      validation)
           3-small)
               |
          Wiki Corpus
         (structured KB
          + transcripts)
```

### MVP Features (Phase 1: Weeks 4-9)

**What the agent can do:**
- Answer ICT questions grounded in the wiki corpus with citations
- Maintain multi-turn conversational context within a session
- Cite specific course modules and concepts
- Refuse to answer outside its knowledge domain
- Validate ICT setup checklists against deterministic rules
- Continue existing webhook-based live coaching (unchanged)
- All existing journal, analytics, screenshot features remain

**New backend:**
1. `POST /api/coach/chat` — streamed chat endpoint (SSE)
2. pgvector on existing PostgreSQL — wiki chunk embeddings + similarity search
3. `chat_sessions` and `chat_messages` tables — conversation persistence
4. Extended `prompt_loader.py` — inject RAG-retrieved passages alongside static strategy library

**New frontend:**
1. Chat panel — conversational UI with message history, citations, confidence indicators
2. Session management — new session, session history list

### V1 Features (Phases 2-3: Months 3-5)

- Structured trade review (user describes markup → rule validation → optional vision cross-check)
- Agent tool calls: `get_user_trades()`, `get_analytics_summary()`, `get_economic_calendar()`, `get_session_context()`, `validate_ict_rules()`
- Economic calendar integration (Forex Factory RSS)
- Post-trade AI reviews from journal entries
- Pattern analysis across user's trading history
- Voice journaling (Whisper transcription → field extraction → form pre-fill)
- Subscription tiers (Free/Student $29/Pro $79) via Stripe

### Future Features (Phase 7+)

- LoRA fine-tuned instructor voice (conditional on 200+ coaching examples)
- Practice trading (TradingView Lightweight Charts replay + custom detection engine)
- Multi-instructor support (separate RAG namespaces, separate models)
- Cross-session user memory
- Discord coaching bot
- Real-time market data streaming

---

## 6. Integration vs Migration Decision

### Recommendation: **Option B — New services inside the existing monorepo**

| Option | Verdict | Reasoning |
|---|---|---|
| **A: Integrate into existing codebase** | Partially | The chat endpoint, RAG pipeline, and pgvector extend the existing `api/` naturally. Don't create a separate service for what is essentially a new router + retrieval layer. |
| **B: New services in monorepo** | **Best** | Add `agent/` for RAG pipeline and embedding generation as a separate concern. Keep `api/` as the API gateway. `wiki/` stays as knowledge source. |
| **C: Migrate to new architecture** | Overkill | The existing infrastructure (Render, Cloudflare Pages, PostgreSQL) handles this scale. New architecture = new deployment complexity for zero benefit at 2-engineer scale. |

### Proposed Monorepo Structure

```
neurospect/
├── CLAUDE.md                    # Monorepo routing
├── NeuroLLM.md                  # Strategic spec (reference)
├── wiki/                        # Knowledge base (unchanged)
│   ├── CLAUDE.md
│   ├── concepts/
│   ├── sources/
│   └── ...
├── api/                         # FastAPI backend (extended)
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── models/
│   │   │   ├── trade.py         # Existing
│   │   │   ├── coaching_event.py # Existing
│   │   │   ├── chat_session.py  # NEW: conversation persistence
│   │   │   ├── chat_message.py  # NEW: message history
│   │   │   ├── wiki_chunk.py    # NEW: embedded chunks + metadata
│   │   │   └── subscription.py  # NEW: Stripe tier tracking
│   │   ├── routers/
│   │   │   ├── trades.py        # Existing
│   │   │   ├── chat.py          # NEW: conversational coaching endpoint
│   │   │   ├── billing.py       # NEW: Stripe webhook + subscription
│   │   │   └── ...
│   │   ├── coach/
│   │   │   ├── claude_client.py # Extended: RAG context injection
│   │   │   ├── prompt_loader.py # Extended: dynamic retrieval
│   │   │   ├── rag/             # NEW: retrieval pipeline
│   │   │   │   ├── embedder.py  # Chunk embedding via OpenAI
│   │   │   │   ├── retriever.py # pgvector similarity search
│   │   │   │   ├── ingestor.py  # Wiki markdown → chunks → embeddings
│   │   │   │   └── evaluator.py # RAG quality testing
│   │   │   └── tools/           # NEW: agent tool definitions
│   │   │       ├── trade_tools.py    # get_user_trades, get_analytics
│   │   │       ├── market_tools.py   # get_session_context, get_calendar
│   │   │       └── ict_rules.py      # validate_ict_setup (deterministic)
│   │   └── ...
│   └── scripts/
│       ├── ingest_wiki.py       # NEW: one-time wiki ingestion
│       └── run_eval.py          # NEW: RAG evaluation runner
├── app/                         # React frontend (extended)
│   ├── CLAUDE.md
│   ├── src/
│   │   ├── pages/
│   │   │   ├── chat.tsx         # NEW: coaching chat page
│   │   │   └── ...
│   │   ├── components/
│   │   │   ├── chat/            # NEW: chat UI components
│   │   │   │   ├── ChatPanel.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   ├── CitationLink.tsx
│   │   │   │   └── SessionSidebar.tsx
│   │   │   └── ...
│   │   └── hooks/
│   │       ├── use-chat.ts      # NEW: chat session management
│   │       └── ...
│   └── ...
├── evals/                       # NEW: evaluation datasets
│   ├── ict_qa_pairs.jsonl       # Ground-truth Q&A for RAG testing
│   ├── backtest_baselines/      # Null test results, baseline comparisons
│   └── README.md
└── docs/                        # Planning docs
```

**Phase 7+ additions to `api/`:**

```
api/app/
├── backtest/                    # NEW (Phase 7): Backtesting engine
│   ├── engine.py                # Event-driven backtest simulator
│   ├── ict_detectors.py         # SwingDetector, FVGDetector, OBDetector, etc.
│   ├── strategy_compiler.py     # YAML strategy blocks → executable StrategySpec
│   ├── monte_carlo.py           # Permutation-based Monte Carlo simulation
│   ├── walk_forward.py          # Walk-forward optimization with overfitting guards
│   ├── risk_analysis.py         # VaR, CVaR, drawdown analysis, Kelly criterion
│   └── data_pipeline.py         # Polygon.io → Parquet → R2
├── neuroquant/                  # NEW (Phase 8): Hybrid LLM + Quant
│   ├── features/
│   │   ├── ict_features.py      # ICT-specific feature engineering
│   │   └── quant_features.py    # Traditional statistical features
│   ├── regime/
│   │   ├── detector.py          # HMM + rule-based regime detection
│   │   └── labeler.py           # Post-hoc state labeling
│   ├── models/
│   │   ├── baseline.py          # Logistic regression
│   │   ├── lgbm_model.py        # LightGBM production model
│   │   └── ensemble.py          # Regime-conditional model selection
│   ├── llm_scorer.py            # Claude-based narrative coherence scoring
│   └── confluence.py            # Combined decision: ICT gates + ML + LLM
├── agent/                       # NEW (Phase 9): NeuroTrader Agent
│   ├── state_machine.py         # Agent states (IDLE → SCANNING → ... → EXITED)
│   ├── market_monitor.py        # Polygon.io WebSocket for live bars
│   ├── execution.py             # Paper + Live execution managers
│   ├── risk_manager.py          # Pre-trade gates, circuit breakers, position sizing
│   ├── learning.py              # Post-trade analysis, retraining triggers, calibration
│   └── config.py                # AgentConfig, AgentMode, safety defaults
├── models/
│   ├── backtest_run.py          # NEW: Backtest result persistence
│   ├── backtest_trade.py        # NEW: Individual backtest trades
│   ├── agent_config.py          # NEW: Versioned agent configuration
│   ├── agent_session.py         # NEW: Daily session logs
│   ├── agent_signal.py          # NEW: Every detected signal (traded or not)
│   └── ...
└── routers/
    ├── backtests.py             # NEW: Launch, view, compare backtests
    ├── neuroquant.py            # NEW: Features, regime, models, evaluate
    ├── agent.py                 # NEW: Agent config, status, halt, history
    └── ...
```

**New database tables (9 total):**

| Table | Phase | Purpose |
|---|---|---|
| `backtest_runs` | 7 | Backtest metadata + aggregate results |
| `backtest_trades` | 7 | Individual trades from backtests |
| `monte_carlo_results` | 7 | Monte Carlo simulation outputs |
| `wfo_results` | 7 | Walk-forward optimization results |
| `agent_configs` | 9 | Versioned agent configuration |
| `agent_sessions` | 9 | Daily session logs |
| `agent_signals` | 9 | Every signal detected (traded or not) |
| `agent_performance` | 8 | Rolling stats per strategy × regime |
| `wiki_chunks` | 1 | Embedded wiki content for RAG |

**New Python dependencies:**

| Package | Phase | Purpose |
|---|---|---|
| `polars` | 7 | Columnar data (10-100x faster than pandas for backtesting) |
| `polygon` | 7 | Market data API client |
| `pyarrow` | 7 | Parquet file support |
| `scikit-learn` | 8 | Logistic regression, calibration, preprocessing |
| `lightgbm` | 8 | Gradient boosted trees (production ML model) |
| `hmmlearn` | 8 | Hidden Markov Models for regime detection |
| `websockets` | 9 | WebSocket client for live market data |

**Key principle:** Everything stays in the monorepo's `api/` service. At 2-engineer scale, microservices add deployment complexity for zero benefit. The backtesting engine, NeuroQuant models, and agent all run as modules within the FastAPI app. Background tasks (backtests, agent loop) use Render background workers or FastAPI BackgroundTasks.

---

## 7. RAG vs Fine-Tuning vs Agent Tools vs Hybrid

### Comparison Matrix

| Dimension | RAG | Fine-Tuning (LoRA SFT) | Agent Tools | Deterministic Rules |
|---|---|---|---|---|
| **Solves** | Domain knowledge injection | Voice/style transfer | Real-time data access | Rule enforcement |
| **Accuracy** | High (bounded by retrieval quality) | N/A for knowledge | High (grounded outputs) | Perfect |
| **Hallucination risk** | 6-20% residual | Can increase if overtrained | Minimal | Zero |
| **Cost (inference)** | +$0.001-0.005/query | $0 if self-hosted | Negligible/tool call | Negligible |
| **Cost (setup)** | $50-200 one-time (embedding) | $500-2000 (GPU + data prep) | $0-500 (dev time) | $0 (code) |
| **Data requirements** | Existing corpus (HAVE IT) | 200-500 pairs (DON'T HAVE) | API credentials | Rule specs (HAVE IN YAML) |
| **Update cycle** | Minutes (re-embed) | Hours-days (retrain) | Immediate | Immediate (deploy) |

### Phased Hybrid Recommendation

**Month 1-2 (MVP): RAG + Deterministic Rules**
- Embed the wiki structured KB docs (8 business-logic + 7 entry models + 18 course lessons)
- Move kill zone, opening price, and strategy checklist validation from system prompt into deterministic Python functions callable as agent tools
- Claude Sonnet 4.6 via API with strong system prompt for voice approximation

**Month 3-4 (V1): + Agent Tools**
- Add tool calling: `get_user_trades()`, `get_analytics_summary()`, `get_economic_calendar()`, `get_session_context()`
- Personalized coaching based on the trader's own history

**Month 5+ (conditional): + Fine-Tuning**
- Only if instructor provides 200+ coaching examples AND users report generic voice is a barrier
- In practice, a well-crafted system prompt gets 80% of the voice without fine-tuning

### What Should NEVER Be Fully LLM-Delegated

- Order execution or trade signals (regulatory + reliability)
- Risk management decisions (stop placement, position sizing)
- Kill zone / session time calculations (deterministic, must be exact)
- R-multiple and PnL calculations (arithmetic)
- Financial advice of any kind

---

## 8. Data Strategy

### Internal Data

**Immediately usable (RAG corpus):**

| Content | Files | Tokens (est.) | RAG Readiness |
|---|---|---|---|
| 8 business-logic docs | `wiki/concepts/business-logic/` | ~8K | HIGH — information-dense, structured |
| 7 entry models + YAML | `wiki/concepts/entry-models/` | ~6K | HIGH — machine-readable checklists |
| 18 course lessons | `wiki/concepts/course/` | ~12K | HIGH — structured learning content |
| System prompt + strategies.json | `wiki/concepts/ai-coach/` | ~4K | ALREADY IN USE |

**Usable after processing:**

| Content | Files | Tokens (est.) | Action |
|---|---|---|---|
| 13 course video transcripts | `wiki/sources/neurospect/*-vol*` | ~100K | Skip for MVP; chunk + embed for V1 with lower priority |
| 11 stream transcripts | `wiki/sources/neurospect/*-stream*` | ~80K | Valuable for live commentary feature; not for Q&A RAG |
| Trade records | PostgreSQL `trades` table | N/A | Agent tool: query for personalized coaching |
| Coaching events | PostgreSQL `coaching_events` table | N/A | History context for follow-ups |

**Missing:**
- Instructor coaching examples (200+) — needed for fine-tuning, not for MVP
- Common student mistakes as structured data — partially implied in course content
- Chart annotations — zero exist
- Historical OHLCV data — zero in system, needed for Phase 4+
- Embeddings — none generated yet

### External Data Sources

#### Market Data (not needed for MVP)

| Source | NQ Futures? | Cost | Best For |
|---|---|---|---|
| **FirstRate Data** | Yes (CME) | $100-200 one-time | Phase 4 research: 3+ years of 1-min NQ CSVs |
| **Tradovate API** (existing integration) | Yes | $0 incremental | V1: recent price data via existing broker connection |
| **Databento** | Yes (CME) | $50-150/mo | Phase 4+: production tick data with clean API |
| **Polygon.io** | Limited futures | $200+/mo | Not recommended for futures |

**Recommendation:** Do not acquire market data until Phase 4. For V1, use Tradovate's existing integration for recent prices.

#### Economic Calendar

| Source | Cost | Notes |
|---|---|---|
| **Forex Factory RSS** | $0 | Comprehensive, free; scraping may break |
| **Trading Economics API** | $0-49/mo | Official API; upgrade if scraping is fragile |
| **MQL5 Calendar** | $0 | Structured JSON, filters by impact |

**Recommendation:** Start with Forex Factory RSS (free, comprehensive).

### Which Market First

**NQ (Nasdaq 100 E-mini futures).** The entire codebase is already built around it:
- System prompt specifies NQ
- ORG thresholds calibrated in NQ handles
- Stream transcripts are live NQ sessions
- The instructor trades NQ
- Supporting ES as secondary is trivial (same exchange, same sessions)

---

## 9. Ingestion and Storage Architecture

### Wiki Ingestion Pipeline

```
Wiki Markdown (concepts/ + course/ + entry-models/)
    ↓
Markdown Parser (extract frontmatter, split at ## headers)
    ↓
Section-Level Chunking (~500 tokens per chunk)
    ↓
Metadata Tagging (source_file, section, tags, chunk_type, priority)
    ↓
ICT Terminology Normalization (CHoCH, CISD, FVG, OTE → canonical forms)
    ↓
Embedding Generation (OpenAI text-embedding-3-small, 1536 dims)
    ↓
Store in pgvector (PostgreSQL extension, same DB)
```

### Storage Architecture

| Store | Technology | Purpose | MVP Cost |
|---|---|---|---|
| App database | PostgreSQL 16 (Render) | Users, trades, chats, wiki chunks + embeddings | $0-7/mo |
| Vector storage | pgvector (same PostgreSQL) | Similarity search on wiki chunks | $0 (included) |
| Object storage | Cloudflare R2 | Screenshots, chart images | ~$0 (free tier) |
| Cache | In-process LRU | System prompt, strategy library, hot embeddings | $0 |
| Queue | FastAPI BackgroundTasks | Claude API calls, embedding generation | $0 |
| Logs | Render built-in + Sentry (free) | Error tracking, request logs | $0 |
| Eval datasets | JSON files in repo (`evals/`) | RAG quality testing | $0 |

**Why pgvector over a dedicated vector DB:** The corpus is hundreds of chunks, not millions. pgvector handles this trivially on the existing PostgreSQL instance. Zero additional infrastructure cost. One database to back up and monitor. Upgrade to Pinecone/Weaviate only if corpus exceeds 100K chunks (extremely unlikely for a single instructor).

---

## 10. Recommended Tech Stack

### What to Keep (Already Built)

| Category | Technology | Status |
|---|---|---|
| Frontend framework | React 19 + TypeScript + Vite | Deployed |
| UI library | shadcn/ui + Tailwind v4 | Deployed |
| State management | TanStack Query | Deployed |
| Backend framework | FastAPI (Python 3.12+) | Deployed |
| ORM | SQLAlchemy 2.x async | Deployed |
| Database | PostgreSQL 16 | Deployed |
| Migrations | Alembic | Deployed |
| AI SDK | Anthropic Python SDK | Deployed |
| Auth | Discord OAuth2 + JWT | Deployed |
| Object storage | Cloudflare R2 | Deployed |
| Backend hosting | Render | Deployed |
| Frontend hosting | Cloudflare Pages | Deployed |

### What to Add

| Category | Recommended | Alternative | Why | Cost | Speed |
|---|---|---|---|---|---|
| Vector DB | pgvector (extension on existing PG) | Chroma, Pinecone | Zero new infrastructure; corpus is small | $0 | 1 day |
| Embedding model | OpenAI text-embedding-3-small | BGE-M3 (self-hosted) | $0.02/1M tokens; corpus costs <$0.10 to embed | ~$0 | 1 day |
| Chat streaming | FastAPI SSE (`StreamingResponse`) | WebSocket | Simpler for unidirectional LLM streaming | $0 | 2-3 days |
| Agent orchestration | Custom tool-calling loop on Anthropic SDK | LangGraph, CrewAI | Direct SDK usage is simpler for 2-engineer team; avoid abstraction overhead | $0 | 1-2 weeks |
| Charting (future) | TradingView Lightweight Charts (OSS) | Recharts (analytics only) | Purpose-built for candlestick charts | $0 | 2-4 weeks |
| Billing | Stripe Billing | Paddle, Lemon Squeezy | Industry standard; best docs; handles subscriptions | 2.9% + $0.30/txn | 1-2 weeks |
| Error monitoring | Sentry (free tier) | Render logs only | Free, FastAPI integration is 3 lines | $0 | 1 hour |
| CI/CD | GitHub Actions | Render auto-deploy (already configured) | Add test + lint before deploy | $0 | 1 day |
| Project tracking | Linear (free tier) | GitHub Projects | Best DX for 2-engineer team; keyboard-first, fast | $0 | 30 min |
| Economic calendar | Forex Factory RSS scrape | Trading Economics API ($49/mo) | Free, comprehensive | $0 | 2-3 days |
| Transcription (future) | OpenAI Whisper API | Local Whisper | $0.006/min, no GPU needed | Per-use | Already documented |

### Cost Model: No New Monthly Infrastructure Until V1

The MVP adds zero new monthly costs beyond existing Render + Cloudflare + Anthropic API usage. pgvector, SSE streaming, Sentry free tier, and the wiki embedding pipeline all run on existing infrastructure.

---

## 11. Infrastructure and Cost Estimates

### MVP Monthly Costs (Months 1-2)

| Category | Low | Medium | High | Notes |
|---|---|---|---|---|
| Claude Sonnet 4.6 API | $5 | $25 | $75 | 500-7,500 queries/mo; prompt caching reduces ~50% |
| OpenAI embeddings | $0.10 | $0.10 | $0.10 | One-time corpus embedding; negligible |
| PostgreSQL (Render) | $0 | $7 | $15 | Free tier → Starter |
| Backend hosting (Render) | $0 | $7 | $15 | Free tier → Starter |
| Frontend (Cloudflare Pages) | $0 | $0 | $0 | Free tier |
| Object storage (R2) | $0 | $0 | $1 | Free tier |
| Error tracking (Sentry) | $0 | $0 | $0 | Free tier |
| **TOTAL** | **$6** | **$40** | **$107** | |

### V1 Monthly Costs (Months 3-6)

| Category | Low | Medium | High | Notes |
|---|---|---|---|---|
| Claude Sonnet + Haiku | $17 | $85 | $280 | More queries, tool chains, Haiku for routing |
| Vision (chart review) | $0 | $5 | $20 | Phase 3 hybrid approach |
| Embeddings | $0.50 | $1 | $2 | Per-query + re-embedding |
| PostgreSQL | $15 | $25 | $50 | Standard plan for pgvector indexes |
| Backend hosting | $15 | $25 | $50 | Standard plan |
| Stripe fees | $0 | $50 | $200 | 2.9% + $0.30 on subscription revenue |
| R2 | $0 | $2 | $5 | More screenshots/charts |
| Market data (amortized) | $8 | $8 | $8 | FirstRate CSV one-time $100 |
| **TOTAL** | **$56** | **$201** | **$615** | |

### Scale Monthly Costs (100+ users, Month 9+)

| Category | Estimate | Notes |
|---|---|---|
| Claude Sonnet + Haiku | $500-1,500 | Prompt caching critical |
| Fine-tuned model hosting (if applicable) | $100-300 | Modal/RunPod serverless |
| Database | $50-100 | Larger plan, more connections |
| Backend hosting | $50-150 | Multiple workers |
| Market data (if Phase 4) | $200-400 | CME-licensed NQ |
| **TOTAL** | **$930-2,500** | |

### Cost-Saving Recommendations

1. **Prompt caching is the single biggest lever.** Already implemented via `cache_control: {"type": "ephemeral"}`. Saves ~50% of input tokens.
2. **Route simple queries to Claude Haiku.** "What kill zone am I in?" doesn't need Sonnet. 10x cheaper.
3. **Cache deterministic results aggressively.** Kill zones, opening prices, calendar lookups are pure functions of time.
4. **Stay on Render free/starter tiers as long as possible.** Cold starts (30s after 15min idle) are acceptable for beta.
5. **Don't buy market data until Phase 4 is being built.** $200-400/mo for CME data sitting unused is waste.
6. **Don't self-host models until 100+ active users.** API is cheaper below ~50K queries/month.

---

## 12. Product Strategy

### Product Positioning

**What is NeuroLLM?** An AI coaching platform that turns a trading educator's knowledge, voice, and teaching style into a personalized AI coach available 24/7 to every student.

**Who is it for?** (1) Trading educators who can't scale personalized coaching; (2) Trading students who want interactive feedback, not passive video consumption.

**What problem does it solve?** Trading education's scaling problem: an educator with 2M subscribers can record courses but can't personally review each student's analysis. Students practice in isolation with no feedback loop until they lose real money.

**Why now?** RAG for domain Q&A is production-proven (Khanmigo). LoRA SFT for voice at 200-500 examples is validated (Databricks, IBM). Trading education creators (50M+ YouTube subscribers across top 100) are entirely unserved by AI tooling.

### Ideal Customer Profile (Ranked)

1. **ICT/SMC learners** — First target. Instructor's 2M subscriber base = immediate distribution. Highest density, most underserved.
2. **Prop firm traders** — Adjacent. Proven budget ($50-200/month on eval attempts). Need structured coaching + accountability.
3. **Trading educators** (B2B) — 10K-500K followers, active Discord, paid courses. The platform's growth engine.
4. **Crypto/forex retail traders** — Larger TAM but less structured. Phase 2 expansion.

### Competitor Landscape

| Category | Key Players | NeuroLLM Differentiation |
|---|---|---|
| AI trading assistants | Price Action Lover, TradingGPT | Single methodology, no personalization, no instructor voice. NeuroLLM has exclusive instructor content + fine-tuned voice. |
| Trading education | Warrior Trading, Bear Bull Traders | No AI coaching. Passive content. Live rooms are synchronous (instructor must be present). |
| TradingView ecosystem | LuxAlgo (800K followers) | Detection tools, not coaching. LuxAlgo shows "here's an OB"; NeuroLLM says "that's not an OB because it didn't precede displacement." |
| Journaling tools | TradeZella ($29-49/mo), Tradervue, Edgewonk | Generic journaling, no methodology-specific fields, no AI coaching. NeuroSpect has 100+ ICT-specific fields. |
| ICT-specific AI | ICT GPTs (free ChatGPT store) | Anyone can build in an afternoon. No fine-tuning, no proprietary data, no persistent progress. |
| Backtesting | FX Replay ($47-97/mo), TV Replay | Replay without coaching. Practice trading + AI feedback (Phase 4) is the differentiation. |

### USP

- **Core:** "The only platform where a trading educator's knowledge becomes a personalized AI coach that scales to every student, 24/7"
- **Technical moat:** RAG on proprietary course content + fine-tuned instructor voice — cannot be replicated without the instructor's exclusive data
- **Data moat:** Compounds with each student interaction (correction signals, common questions, gap identification)
- **Community moat:** Students follow instructors, not platforms; switching costs are high once established

### Branding Recommendation

- **NeuroLLM** → Company/platform/B2B brand (educators and investors see this)
- **NeuroSpect** → Consumer-facing product brand (students see this)
- **Tagline:** "NeuroSpect — AI coaching powered by NeuroLLM"
- **Visual:** Dark mode default (traders live in dark UIs). Deep navy/charcoal base, electric blue accents, amber for warnings. Monospace for numbers, clean sans-serif for prose.
- **Tone:** Direct, domain-fluent, never generic. "Price is inside the 4H bullish FVG spanning 19800-19850 below the midnight open" — not "the price might be at a support level."
- **Trust positioning:** "Educational coaching" language everywhere. Never "financial advice," "trade signals," or "recommendations." Visible citations. Confidence scoring. "I don't know" when outside course content.

### Pricing Strategy

**Phase 1 Tiers (Coaching Product — at launch):**

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | 5 AI coaching questions/day, read-only glossary, basic journal |
| **Student** | $29/month | Unlimited coaching, full journal, basic analytics, conversation history |
| **Pro** | $79/month | + advanced analytics, agent tools (trade history queries, session context), priority responses, data export |

**Phase 2 Tiers (+ Backtesting — after Phase 7 ships):**

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | Same as above |
| **Student** | $29/month | Same as above |
| **Pro** | $99/month | Everything in Student + backtesting (3 runs/month), basic Monte Carlo, strategy performance breakdown |
| **Trader** | $199/month | Unlimited backtesting, walk-forward optimization, full Monte Carlo, risk analysis suite, all 7 ICT strategies, backtest comparison, monthly returns heatmap, MAE/MFE analysis |

**Phase 3 Tiers (+ NeuroQuant & NeuroTrader — after Phase 9 ships):**

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | Same |
| **Student** | $29/month | Coaching + journal |
| **Pro** | $99/month | + backtesting (3 runs/month), basic analytics |
| **Trader** | $199/month | Unlimited backtesting, full analytics suite, regime detection dashboard, model performance tracking |
| **Quant** | $349/month | Everything in Trader + NeuroQuant access (feature engineering, ML model training, custom regime detection, confluence scoring), NeuroTrader Agent shadow mode |
| **Quant Pro** | $499/month | Everything in Quant + NeuroTrader Agent paper trading, live trading (when available), priority compute for backtests, API access for custom integrations |

**Add-ons (any paid tier):**
- Extra backtest compute credits: $19/month (10 additional runs)
- Historical market data (additional instruments beyond NQ/ES): $29/month per instrument
- NeuroTrader Agent live trading (when available, Quant Pro only): included in tier but requires separate ToS acceptance and broker connection

**B2B (instructor):** $0 for first instructor (design partner). Then $199/month + 15-25% revenue share. $2,000-5,000 onboarding fee for content curation.

**Pricing rationale:**
- $29 (Student) — competitive with TradeZella/Tradervue but includes AI coaching they don't have
- $99 (Pro) — adds backtesting, which competitors charge $47-97/month for separately (FX Replay)
- $199 (Trader) — full quantitative analysis suite; no competitor offers ICT-specific backtesting + walk-forward + Monte Carlo
- $349 (Quant) — hybrid LLM+ML system is genuinely novel; targets serious prop firm traders
- $499 (Quant Pro) — includes automated trading capability; targets traders spending $200+/month on prop firm challenges who want systematic edge

**Unit economics (at scale):**
- Student tier: ~$1-5/mo LLM cost → 83-97% gross margin
- Pro/Trader tiers: ~$5-15/mo (LLM + backtesting compute) → 85-93% gross margin
- Quant tiers: ~$15-40/mo (LLM + ML inference + market data) → 88-92% gross margin
- NeuroTrader Agent: ~$30-65/mo (live monitoring + LLM calls + notifications) → 87% gross margin at $499

### Monetization: Phased Model

**Phase 1 (Launch):** Freemium subscription (Free → Student $29 → Pro $79). Revenue from coaching product.

**Phase 2 (+ Backtesting):** Expand tiers to Pro $99 / Trader $199. Revenue from quantitative analysis tools. This is a natural upsell — traders who use the coaching will want to backtest the strategies they're learning.

**Phase 3 (+ NeuroQuant + NeuroTrader):** Add Quant $349 / Quant Pro $499 tiers. This is the premium product — automated trading intelligence with hybrid LLM+ML. Targets serious traders spending $200+/month on tools and prop firm challenges.

**Revenue projection (conservative, single instructor):**

| Milestone | Users | Mix | Est. MRR |
|---|---|---|---|
| Beta (50 users) | 50 | 100% free | $0 |
| Launch +30 days | 100 paid | 60% Student, 30% Pro, 10% Trader | $5,240 |
| Launch +90 days | 300 paid | 50% Student, 30% Pro, 15% Trader, 5% Quant | $22,100 |
| Launch +180 days | 500 paid | 40% Student, 25% Pro, 20% Trader, 10% Quant, 5% Quant Pro | $57,550 |

**Per-instructor break-even:** ~50 paying students at blended $40 ARPU covers platform costs. NeuroQuant/NeuroTrader tiers dramatically increase ARPU for serious traders.

---

## 13. Go-to-Market Plan

### Launch Sequence

1. **Private alpha** (2-4 weeks): Paul + 3-5 hand-picked ICT traders → find bugs, tune prompts
2. **Private beta** (4-8 weeks): 20-50 students from instructor's community → validate engagement, retention, willingness to pay
3. **Waitlist launch**: Open waitlist, gated by instructor → build demand signal
4. **Open beta**: Remove waitlist → validate unit economics, measure conversion
5. **Paid launch**: Introduce paid tiers → revenue

### Beta Exit Criteria

- 7-day retention > 30%
- Hallucination rate < 10%
- "Sounds like instructor" score > 3.5/5
- 60%+ of beta users say they would pay $29/month

### Growth Channels

1. **Instructor's community** (primary) — Discord announcement, YouTube video "I built an AI version of myself"
2. **Student-generated content** — Screenshots of coaching interactions shared organically
3. **SEO** (long-term) — Public educational pages for ICT concepts → conversion to AI coach
4. **Discord bot** — AI coach accessible inside instructor's existing Discord server
5. **Content marketing** — Weekly "AI coach reviews my student's trade" shorts

---

## 14. Risk, Compliance, and Safety

### Critical Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **Financial advice classification** | CRITICAL | Educational framing only. System prompt prohibits trade recommendations. Pre-access disclaimer. Never "should I take this trade?" — redirect to educational response. |
| **Hallucinated ICT analysis** | HIGH | RAG grounding with citations. Confidence scoring. "I don't know" behavior. Instructor review queue. |
| **User trading losses** | HIGH | Paper trading first. No P&L responsibility. Never touches user funds. Persistent disclaimer on every interaction. |
| **Overconfidence** | MEDIUM | Calibrated language ("based on Module X, this appears to be..."). Vision is advisory, never authoritative. |
| **Regulatory exposure (SEC/FINRA)** | HIGH (Phase 5) | Phases 1-3 are educational (lower risk). Phase 5 triggers RIA registration. Budget for counsel before Phase 4. |
| **Model drift** | MEDIUM | Monitor quality metrics. Version models. Periodic re-evaluation. |
| **Content IP** | MEDIUM | Written content license agreement. Instructor retains IP. Exit clause with model destruction. |

### Required Product Safeguards

1. Educational disclaimer acknowledgment recorded before first coaching interaction
2. Every response cites a course module — never provides trade recommendations
3. Confidence scoring visible on every response
4. "I don't know" when outside course content
5. Persistent, non-dismissible disclaimer on every coaching interaction
6. Audit logs (coaching_events table with request/response payloads — already implemented)
7. Instructor review queue for AI response quality
8. Rate limiting (per-user, per-endpoint)

---

## 15. Project Tracking Recommendation

### Recommendation: **Linear** (free tier)

| Criteria | Linear | GitHub Projects |
|---|---|---|
| DX | Keyboard-first, fast, clean | Familiar but less opinionated |
| GitHub integration | Excellent (PR linking, branch sync) | Native |
| Issue hierarchy | Projects > Issues > Sub-issues | Projects > Issues (no sub-issues) |
| Automation | Built-in | Requires YAML |
| Cost | Free (250 issues) | Free |

**If zero new tools preferred:** Use GitHub Projects. Both work for 2 engineers.

### Conventions

- **Branches:** `feat/NLM-42-rag-retrieval-pipeline`, `fix/NLM-55-hallucination-on-order-blocks`
- **PRs:** `[NLM-42] Add RAG retrieval pipeline`
- **Sprints:** 2-week cycles, Monday start
- **Labels:** feature, bug, task, research, rag, fine-tuning, frontend, backend, content, compliance

---

## 16. Full Roadmap

### Phase 0: Research & Validation (Weeks 1-3)

**Goals:** Validate first customer, prototype RAG, select tech stack.

**Deliverables:**
- Instructor content access agreement
- RAG prototype with wiki content (retrieval quality benchmarked)
- Vector DB selected (pgvector recommended)
- Embedding model selected (text-embedding-3-small recommended)
- 50 Q&A evaluation pairs
- Competitive teardown (test Price Action Lover, ICT GPTs)
- Linear workspace set up

**Exit criteria:** RAG prototype returns relevant passages for 80%+ of test questions.

**Estimated effort:** 2 × 3 weeks = 6 engineer-weeks

### Phase 1: Knowledge Base & RAG MVP (Weeks 4-9)

**Goals:** Production RAG pipeline, ingested course content, working chat UI.

**Deliverables:**
- Ingestion pipeline (markdown → chunks → embeddings → pgvector)
- Retrieval pipeline (query → similarity search → top-K → re-rank)
- Chat API endpoint (`POST /api/coach/chat` with SSE streaming)
- Chat UI (message bubbles, citations, confidence indicators, session history)
- ICT terminology normalization dictionary (50+ terms)
- 100 Q&A evaluation pairs
- Existing webhook coaching unchanged

**Exit criteria:** Hallucination rate < 15% on eval dataset. Response latency < 5s (p95).

**Estimated effort:** 2 × 6 weeks = 12 engineer-weeks

### Phase 2: Market Context & Trade Integration (Weeks 10-15)

**Goals:** Agent tools for personalized coaching, economic calendar, trade review.

**Deliverables:**
- Agent tool system (get_user_trades, get_analytics, get_calendar, validate_ict_rules)
- Economic calendar integration (Forex Factory RSS)
- Post-trade AI review from journal entries
- Structured trade review workflow (text-based setup validation)
- Voice journaling prototype (Whisper → field extraction)
- LoRA fine-tuning pipeline (if coaching examples available — conditional)

**Exit criteria:** Agent can reference user's trading history in coaching responses.

**Estimated effort:** 2 × 6 weeks = 12 engineer-weeks

### Phase 3: Product MVP (Weeks 16-21)

**Goals:** Beta-ready product with onboarding, billing, and polish.

**Deliverables:**
- User onboarding flow (Discord OAuth → disclaimer → guided first question)
- Stripe integration (Free / Student $29 / Pro $79)
- Usage limiting (free tier: 5 questions/day)
- Conversation history (browse past sessions)
- Landing page
- Discord coaching bot (MVP)
- ToS + Privacy Policy drafted
- Admin: basic user activity + quality metrics page

**Exit criteria:** A user can sign up, subscribe, and get coaching. Free/paid tiers enforced.

**Estimated effort:** 2 × 6 weeks = 12 engineer-weeks

### Phase 4: Evaluation & Reliability (Weeks 22-24)

**Goals:** Harden for real users. Instructor review. Load testing.

**Deliverables:**
- Automated nightly evaluation (alert on quality regression)
- Load testing (50 concurrent users)
- Security audit (auth, data isolation, rate limiting)
- Instructor reviews 50+ AI responses
- User feedback mechanism (thumbs up/down)
- Monitoring and cost alerting (Sentry, token tracking)

**Exit criteria:** Hallucination < 10%. Latency < 5s (p95) under load. Instructor approves 85%+.

**Estimated effort:** 2 × 3 weeks = 6 engineer-weeks

### Phase 5: Private Beta (Weeks 25-28)

**Goals:** Real users, validate product-market fit.

**Deliverables:**
- 20-50 beta users active
- Weekly feedback loop
- Usage analytics (DAU, questions/user, retention)
- Iterated improvements from feedback

**Exit criteria:** 7-day retention > 30%. NPS > 20. 60%+ would pay $29/month.

**Estimated effort:** 2 × 4 weeks = 8 engineer-weeks

### Phase 6: V1 Launch (Weeks 29-31)

**Goals:** Paid tiers live, first revenue.

**Deliverables:**
- Stripe payment processing in production
- Landing page with beta social proof
- Instructor launch content published
- Support channel established

**Exit criteria:** First paid subscribers within 7 days. MRR trajectory toward 100 paying users in 60 days.

**Estimated effort:** 2 × 3 weeks = 6 engineer-weeks

### Phase 7: Backtesting & Evaluation Platform (Weeks 32-43)

**Goals:** Build a robust backtesting engine, ICT detection system, Monte Carlo simulation, walk-forward optimization, and performance analytics dashboard. This is the foundation for everything in Phases 8-9.

**Deliverables:**
- Custom event-driven backtest engine (no Zipline/Backtrader — ICT-specific logic conflicts with off-the-shelf frameworks)
- ICT pattern detection module: SwingDetector, FVGDetector, OrderBlockDetector, MarketStructureDetector, SessionDetector, SMTDetector, BiasDetector, ConsolidationDetector
- Strategy compiler: YAML strategy blocks from wiki → executable `StrategySpec` objects
- Monte Carlo simulation (permutation-based, 10K iterations)
- Walk-forward optimization with overfitting guards (deflated Sharpe, efficiency ratio)
- Risk analysis module (VaR, CVaR, drawdown analysis, Kelly criterion)
- Market data ingestion pipeline (Polygon.io → Parquet on R2)
- Performance analytics dashboard with 11+ chart types
- **Null test**: ICT features vs standard indicators — go/no-go gate for Phase 9

**Sub-phases:**

**7A (Weeks 32-35): Foundation**
- Polygon.io client + Parquet writer + R2 upload/download
- Core detectors: SwingDetector, FVGDetector, SessionDetector, OpeningPriceDetector
- Backtest engine core: bar replay, position management, stop/target execution, anti-look-ahead enforcement
- Database schema: `backtest_runs`, `backtest_trades` tables
- Strategy compiler: Consolidation Model (first strategy)

**7B (Weeks 36-39): Full Engine**
- Remaining ICT detectors: OrderBlockDetector, MarketStructureDetector, ConsolidationDetector, SMTDetector, BiasDetector
- Strategy compiler for all 7 entry models
- Monte Carlo simulation
- Walk-forward optimization
- Risk analysis module (VaR, CVaR, drawdown, Kelly)
- REST API endpoints for launching/viewing backtests

**7C (Weeks 40-43): Dashboard + Null Test**
- Frontend pages: `/backtests`, `/backtests/{id}`, `/backtests/{id}/monte-carlo`, `/backtests/{id}/walk-forward`, `/backtests/compare`
- Charts: equity curve, drawdown, R-distribution, monthly returns heatmap, rolling Sharpe, MAE/MFE scatter, Monte Carlo fan chart, WFO efficiency bars
- Run null test: ICT strategies vs random entries with same risk management
- Document results — if null test fails (p > 0.05), Phase 9 (live agent) is NOT viable

**Architecture:**
```
Market Data (Polygon.io) → Parquet files on R2
    ↓
ICT Detection Module (SwingDetector, FVGDetector, etc.)
    ↓
Strategy Compiler (YAML → StrategySpec)
    ↓
Backtest Engine (event-driven, anti-look-ahead)
    ↓
Results → PostgreSQL (backtest_runs, backtest_trades)
    ↓
Monte Carlo / Walk-Forward / Risk Analysis
    ↓
Performance Dashboard (React + Recharts)
```

**Anti-bias architecture:** The engine is structurally incapable of look-ahead bias — the strategy function receives only `bars[:current_idx+1]`. This is the single most important design decision.

**New database tables:** `backtest_runs`, `backtest_trades`, `monte_carlo_results`, `wfo_results`

**New Python dependencies:** `polars` (columnar data), `polygon` (market data API), `pyarrow` (Parquet support)

**Cost:** Polygon.io Starter $29/mo + R2 storage ~$0.50/mo = ~$30/mo

**Exit criteria:** All 7 ICT strategies backtested. Walk-forward efficiency ratio > 0.5 for at least 3 strategies. Null test completed and documented.

---

### Phase 8: NeuroQuant — Hybrid LLM + Quant System (Weeks 44-55)

**Goals:** Build a hybrid system combining ICT-specific features, traditional quantitative features, market regime detection, and ML models that select the right strategy for the current market conditions. The LLM provides narrative reasoning; the ML models provide statistical confidence; deterministic rules provide hard gates.

**Deliverables:**
- ICT feature engineering pipeline (FVG distance, OB proximity, session encoding, HTF bias, displacement quality, SMT signal, opening price position, consolidation metrics)
- Quantitative feature engineering (Parkinson volatility, ATR, returns distribution, volume profile, auto-correlation, opening range gap)
- Market regime detector (HMM-based + simple rule-based fallback)
- Signal models: Logistic regression baseline + LightGBM production + XGBoost comparison
- Regime-conditional model selection (trending → E&R model, choppy → consolidation model)
- Confluence scorer: combines ICT condition gates (binary) + ML confidence (probability) + LLM reasoning (narrative coherence)
- Model improvement loop: walk-forward retraining, confidence calibration (Platt scaling), performance tracking per strategy × regime
- Feature importance visualization and model comparison dashboard

**Architecture:**
```
ICT Features + Quant Features → Feature Engineering Pipeline
    ↓                               ↓
LLM Reasoning Layer           ML Signal Models (per regime)
(Claude: narrative             (LightGBM/XGBoost)
coherence, edge cases)              ↓
    ↓                         Model Ensemble
    ↓                         (regime-conditional selection)
    ↓                               ↓
    +-------→ Confluence Scorer ←---+
              (combined decision)
                    ↓
              Trade Signal (direction, confidence, strategy, regime)
```

**Key design decisions:**
- **ICT conditions are FILTERS (binary gates)**, ML provides CONFIDENCE (probability), LLM provides REASONING (narrative coherence check)
- **The LLM is NOT run on every backtest bar** (cost-prohibitive at 13.5M bars/year). LLM is for: (a) live/paper decisions (~5-20 calls/day), (b) post-hoc analysis of flagged trades, (c) borderline setups that pass ML but score 0.55-0.75
- **No deep learning** — with hundreds-to-thousands of trades (not millions), gradient-boosted trees outperform neural networks. LSTMs/Transformers need 10-100x more data.
- **No traditional indicators** (RSI, MACD, Bollinger) — ICT doesn't use them. All features are ICT-specific or raw statistical measures.

**Market regime detection:**
- **Simple (MVP):** Rule-based using ORG ratio and autocorrelation — maps directly to ICT's LRLR/HRLR classification
- **Production:** Hidden Markov Model (4 states: trending, ranging, high-volatility, low-volatility) fitted on daily bars using returns, realized volatility, autocorrelation, and range/close features
- ICT concepts behave differently per regime: FVGs stay open in trending (LRLR), fill in choppy (HRLR); E&R model works in trending; consolidation model works in ranging

**Model improvement loop:**
1. After each trade: record full context + features + decision rationale
2. Run LLM post-trade analysis (mirrors existing AI Coach post-trade review)
3. Update per-strategy, per-regime rolling statistics
4. Trigger model retraining every 100 new trades or 2 weeks (whichever first)
5. Confidence calibration via Platt scaling on recent predictions
6. Weekly automated review report (LLM-generated)

**New database tables:** `agent_performance` (rolling stats per strategy × regime)

**New Python dependencies:** `scikit-learn` (logistic regression, calibration, preprocessing), `lightgbm` (gradient boosted trees), `hmmlearn` (Hidden Markov Models)

**Cost:** LightGBM trains on CPU in seconds. No GPU needed. Claude API for LLM scoring: ~$5-20/mo at 50-100 calls/day.

---

### Phase 9: NeuroTrader Agent — Automated Trading (Weeks 56-68)

**Goals:** Build an automated trading agent that detects ICT setups on live market data, evaluates them through the NeuroQuant confluence scorer, executes trades (paper first, then optionally live), and learns from its results over time.

**PREREQUISITE:** Phase 7 null test must show statistically significant edge (p < 0.05) for ICT strategies. If null test fails, this phase pivots to "better coaching and analytics" — still valuable, just not automated trading.

**Deliverables:**
- Agent state machine (IDLE → SCANNING → SETUP_DETECTED → EVALUATING → WAITING_ENTRY → ENTERED → MANAGING → EXITED → LOGGING)
- Three operating modes: Shadow (signals only, no execution), Paper (simulated execution, real data), Live (real execution via Tradovate)
- Market monitor (Polygon.io WebSocket for live bars)
- Paper execution manager (simulated fills with realistic slippage)
- Live execution manager (Tradovate API bracket orders — entry + stop + target as one OSO)
- Risk management system (daily loss limits, consecutive loss limits, cooldown periods, drawdown-based size reduction, circuit breakers)
- Learning loop (automated post-trade LLM analysis, performance tracking, model retraining triggers, confidence calibration)
- Kill switch (one-click flatten all positions + cancel all orders)
- Discord webhook notifications (entries, exits, circuit breakers, daily summaries)
- Agent performance dashboard

**Safety architecture (5 layers):**

| Layer | Mechanism | Details |
|---|---|---|
| Mode enforcement | Shadow → Paper → Live progression | Live requires 30+ days profitable paper trading + explicit user approval |
| Risk manager | Pre-trade gate | Daily loss limit (3%), weekly loss limit (5%), max 3 consecutive losses, 30-min cooldown after loss, max 1 concurrent position |
| Circuit breakers | Intra-session | 10% drawdown → half size; 15% drawdown → halt |
| Bracket orders | Execution safety | Every live order is OSO (entry + stop + target). No naked orders. Stop never modified to increase risk. |
| Kill switch | Emergency | `POST /api/agent/halt` — immediately cancels all orders, flattens all positions, no confirmation required |

**Agent configuration:**
```python
AgentConfig(
    mode="shadow",                    # Start here, always
    instruments=["NQ"],               # One instrument first
    strategies=["consolidation-model", "expansion-retracement-model", "model-2022-ote"],
    risk_per_trade_pct=0.01,          # 1% risk per trade
    max_daily_loss_pct=0.03,          # 3% daily loss limit
    max_daily_trades=3,
    max_concurrent_positions=1,
    min_confidence=0.65,
    require_llm_confirmation=True,    # LLM must approve before entry
    cool_down_after_loss_minutes=30,
    max_consecutive_losses=3,
    halt_on_news_flag=True,
)
```

**Sub-phases:**

**9A (Weeks 56-59): Shadow Mode**
- Market monitor (Polygon.io WebSocket)
- Agent state machine (IDLE, SCANNING, SETUP_DETECTED)
- ICT pattern detection on live data (reuse backtest detectors)
- Signal logging to `agent_signals` table
- Discord notifications for detected setups
- Frontend: agent status page

**9B (Weeks 60-63): Paper Trading**
- Paper execution manager
- Full agent loop: detect → evaluate (NeuroQuant) → paper entry → manage → exit
- Risk manager with all circuit breakers
- Learning loop: post-trade LLM analysis, performance tracking
- Paper trading dashboard with equity curve

**9C (Weeks 64-68): Live Trading (conditional)**
- Live execution manager via Tradovate API (bracket orders)
- Kill switch endpoint + frontend button
- Enhanced notifications
- Weekly automated review reports
- **Gate:** minimum 30 days profitable paper trading AND positive walk-forward efficiency

**New database tables:** `agent_configs`, `agent_sessions`, `agent_signals`

**New dependencies:** `websockets` (market data stream)

**Cost:** Polygon.io (shared) + Tradovate data fees ($0-10/mo) + Claude API for agent ($10-30/mo) + Render background worker ($7-25/mo) = ~$17-65/mo additional

---

### Phase 10: Advanced Features (Weeks 69+)

- Second instructor onboarding (validates platform model)
- Chart analysis hybrid (text-primary, vision-supplementary)
- NeuroQuant Fund concept exploration (regulatory review required)
- Multi-market support (ES, GC, currencies)
- Advanced psychology profiling from journal + agent data
- Voice coaching (TTS of coaching responses)
- Multi-instructor architecture
- Mobile-optimized UI
- Strategy builder (user-defined ICT strategies → backtest → deploy to agent)

---

## 17. Two-Engineer Execution Plan

### Workstream Split

**Engineer A (Backend/AI/Data):** RAG pipeline, LLM integration, data ingestion, vector DB, fine-tuning, market data, evaluation, backend API extensions.

**Engineer B (Frontend/Product/Infrastructure):** React UI (chat, onboarding, subscription), Stripe, Discord bot, landing page, CI/CD, monitoring, DevOps.

### Parallelization

```
Phase 0 (Weeks 1-3):
  A: RAG prototype, vector DB eval, embedding benchmarks
  B: Linear setup, competitive teardown, chat UI design, landing page wireframe

Phase 1 (Weeks 4-9):
  A: Ingestion pipeline, retrieval pipeline, chat API
  B: Chat UI, onboarding flow, citation display, analytics
  Shared: Evaluation dataset, instructor coordination

Phase 2 (Weeks 10-15):
  A: Agent tools, economic calendar, LoRA pipeline (conditional)
  B: Trade review UI, voice journaling UI, market context display

Phase 3 (Weeks 16-21):
  A: Stripe backend, usage limiting, Discord bot backend
  B: Stripe frontend, subscription UI, landing page, admin

Phase 4 (Weeks 22-24):
  A: Automated eval, load testing, security audit
  B: Feedback UI, quality indicators, UX polish

Phase 5-6 (Weeks 25-31):
  Both: Bug fixes, iteration, launch coordination
```

### Critical Path

```
Track A (Coaching Product):
  Instructor commitment (GATE)
    → Content ingestion (Phase 1)
      → RAG pipeline (Phase 1)
        → Chat API (Phase 1)
          → Product MVP (Phase 3)
            → Beta (Phase 5)
              → Launch (Phase 6)

Track B (Trading Agent — can run in parallel from Phase 7):
  Market data acquisition
    → Backtest engine (Phase 7A)
      → All ICT detectors (Phase 7B)
        → NULL TEST (Phase 7C) ← GO/NO-GO GATE
          → NeuroQuant features + models (Phase 8)
            → Shadow agent (Phase 9A)
              → Paper trading (Phase 9B)
                → Live trading (Phase 9C) — conditional on paper results
```

Fine-tuning (LoRA) is OFF critical path. Null test at Phase 7C is a hard gate for Phase 9.

### First 30 Days

**Week 1-2:**
- A: RAG prototype on wiki content, test 20 questions, evaluate pgvector + embedding models
- B: Linear setup, competitive teardown, chat UI mockups, onboarding wireframe

**Week 3:**
- A: Finalize vector DB + embedding model, build evaluation framework (50 Q&A pairs)
- B: Design pricing UX, landing page wireframe, CI/CD setup

**Week 4:**
- A: Start production ingestion pipeline (wiki → chunks → embeddings)
- B: Start chat UI scaffolding (message bubbles, input, session sidebar)

### MVP Exit Criteria (Coaching Product — Phase 6)

ALL must be true:
1. Student can sign up and start a coaching conversation
2. AI answers from course content with citations
3. Hallucination rate < 10% on eval dataset
4. Instructor approves 85%+ of reviewed responses
5. Response latency < 5s (p95)
6. Free/paid tiers enforced
7. Trade journal functional
8. Error monitoring operational
9. System handles 20 concurrent users

### Backtesting Platform Exit Criteria (Phase 7)

ALL must be true:
1. All 7 ICT strategies compiled from YAML and backtestable
2. Walk-forward efficiency ratio > 0.5 for at least 3 strategies
3. Monte Carlo simulation runs 10K iterations in < 30 seconds
4. Null test completed and documented
5. Performance dashboard shows equity curve, drawdown, R-distribution, monthly returns, MAE/MFE

### NeuroTrader Agent Exit Criteria (Phase 9B → 9C gate)

ALL must be true for live trading:
1. 30+ days of paper trading completed
2. Paper trading shows positive expectancy (avg R > 0)
3. Walk-forward efficiency > 0.6 on all active strategies
4. Risk manager circuit breakers tested and verified
5. Kill switch tested end-to-end
6. Null test showed statistically significant edge (p < 0.05)
7. User explicitly approves live mode via authenticated confirmation

---

## 18. Initial GitHub Issues (Top 20)

1. **Set up pgvector on existing PostgreSQL** — P0, Phase 0
2. **Evaluate embedding models (OpenAI 3-small vs BGE-M3)** — P0, Phase 0, research
3. **Research chunking strategies for ICT content** — P1, Phase 0, research
4. **Build wiki content ingestion pipeline** — P0, Phase 1
5. **Build RAG retrieval pipeline (similarity search + re-ranking)** — P0, Phase 1
6. **Build coaching chat API endpoint (POST /api/coach/chat with SSE)** — P0, Phase 1
7. **Build chat coaching UI** — P0, Phase 1
8. **Create ICT terminology normalization dictionary** — P1, Phase 1
9. **Build evaluation framework for RAG quality** — P1, Phase 1
10. **Implement conversation persistence (chat_sessions + chat_messages)** — P1, Phase 1
11. **Migrate existing coaching pipeline to support RAG + direct chat** — P1, Phase 1
12. **Set up CI/CD pipeline (GitHub Actions)** — P1, Phase 0
13. **Research market data sources for NQ** — P1, Phase 2
14. **Implement agent tool system (trade queries, analytics, calendar)** — P1, Phase 2
15. **Implement user onboarding flow with disclaimer** — P1, Phase 3
16. **Integrate Stripe for subscription billing** — P1, Phase 3
17. **Implement free tier usage limits** — P1, Phase 3
18. **Set up Sentry error monitoring** — P1, Phase 0
19. **Build landing page** — P1, Phase 3
20. **Security audit (auth, data isolation, rate limiting)** — P0, Phase 4

---

## 19. Open Questions

1. **Has the instructor committed to content access?** This is the single gate for the entire project.
2. **Does the instructor have 200+ coaching examples?** Determines whether Phase 2 fine-tuning is feasible or deferred.
3. **What are the instructor's IP arrangements?** Need a content license agreement before ingesting.
4. **Should billing be per-instructor or platform-wide?** Affects Stripe integration design.
5. **Is Discord the only auth provider, or should we add email/password?** Discord works for ICT community; broader audience may need email auth.
6. **What is the compliance posture?** Budget for legal counsel before beta? Or launch with standard ToS and review later?
7. **Is the existing NeuroSpect journal preserved alongside the new coaching features, or does it become a secondary feature?** Recommendation: preserve it — it differentiates from generic chatbot competitors.

---

## 20. NeuroCortex — Knowledge Layer Architecture

### What NeuroCortex Is

NeuroCortex is the hybrid retrieval/intelligence layer that indexes ALL knowledge sources in the platform and makes them queryable via a unified search interface. It powers:
- RAG coaching (Phase 1) — answer ICT questions from the wiki corpus
- Cross-wiki intelligence — surface relevant content from one engineer's wiki to the other
- Agent reasoning (Phase 9) — provide context for NeuroTrader's decision-making
- Fine-tuning dataset generation — transform wiki content into training pairs
- Promotion workflow — identify mature personal wiki pages ready for the team wiki

### Knowledge Sources Indexed

| Source | Content Type | Corpus Tag | Index Priority |
|---|---|---|---|
| `wiki/` pages tagged `corpus_type: training` | ICT concepts, entry models, course lessons | `training` | 1 (highest) |
| `wiki/` pages tagged `corpus_type: both` | Mixed content | `training` + `development` | 1 |
| `wiki/` pages tagged `corpus_type: development` | Architecture, boot prompts, system prompt templates | `development` | 2 |
| `wiki/sources/` (raw transcripts) | Immutable mentor transcripts | `transcript` | 3 (lowest) |
| `paul-wiki/` | Paul's research, decisions, journal | `personal` | 2 |
| `vlad-wiki/` | Vlad's research, decisions, journal | `personal` | 2 |
| `initial-plan/` | Versioned plans | `planning` | 2 |
| PostgreSQL `trades` table | User trade journal entries | `trade_data` | On-demand |
| PostgreSQL `backtest_runs/trades` | Backtest results | `backtest` | On-demand |
| PostgreSQL `agent_signals` | Agent decisions and outcomes | `agent` | On-demand |

### Search Architecture

3-signal hybrid search fused via Reciprocal Rank Fusion (RRF):
1. **Keyword/BM25** (25% weight) — tsvector GIN index, catches exact ICT jargon
2. **Semantic** (60% weight) — pgvector HNSW index (1536-dim embeddings), conceptual similarity
3. **Entity/Tag** (15% weight) — tag matches on instruments, sessions, strategies, corpus_type

Optional cross-encoder reranking for precision on borderline results.

### Cross-Wiki Intelligence

When an engineer works on a component, NeuroCortex surfaces relevant content from the other engineer's wiki and the team wiki. Triggers:
- New file creation in a personal wiki → auto-search other wikis
- `/crossref` command → on-demand deep search
- Component tag matching → pages tagged with the same component name

### Wiki Content Tagging

Every `wiki/` page gets `corpus_type` in frontmatter: `training` (for LLM/RAG), `development` (for engineers), or `both`. The NeuroCortex pipeline reads this tag and routes content to the appropriate index.

### Personal Wiki Promotion Workflow

1. Add `promote: true` to frontmatter when a page matures
2. Wiki lint catches promoted pages and suggests moving to `wiki/`
3. After promotion, personal page becomes a stub linking to canonical version

---

## 21. Patterns to Replicate from Zeus Memory

Zeus Memory (ALDC's production knowledge system, 3.6M+ memories) has battle-tested patterns to reimplement independently in NeuroLLM. We are NOT using zeus-memory code — building from scratch using the same architectural patterns.

| Pattern | Zeus Implementation | NeuroLLM Application | Priority |
|---|---|---|---|
| **Hybrid 3-Signal Search (RRF)** | tsvector + pgvector + entity signals, RRF fusion | NeuroCortex search across all knowledge sources | P0 (Phase 1) |
| **pgvector + HNSW** | Sub-100ms queries on 3.5M+ rows | Wiki chunk embeddings + similarity search | P0 (Phase 1) |
| **Ingestion base class** | Abstract base with dedup (SHA256), batch processing, error recovery | Market data, wiki, calendar ingestion pipelines | P1 (Phase 1+7) |
| **Cross-encoder reranking** | Voyage rerank-2.5 second-pass reranking | Precision reranking for coaching Q&A | P2 (Phase 2) |
| **Entity extraction + knowledge graph** | LLM-powered entity extraction, profile synthesis, relationships | Instruments, sessions, ICT concepts as entities | P2 (Phase 8) |
| **Multi-tenant RLS** | PostgreSQL Row-Level Security with GUCs | Multi-instructor isolation (Phase 10) | P3 (Phase 10) |
| **Embedding queue + batch** | Async queue for embedding generation with retry | Wiki re-embedding, new content ingestion | P1 (Phase 1) |

---

## 22. `/sync` — Unified Project State Synchronization

A single Claude Code skill that keeps the entire project state in sync. **Must be offered to the user before every session ends.**

### What `/sync` Does (5 operations)

1. **Linear sync** — Compares Linear ticket statuses against git branches/PRs (via `gh` CLI + Linear API). Closes tickets for merged PRs. Flags stale in-progress tickets with no recent commits. Reports discrepancies.

2. **Boot prompt regeneration** — Rebuilds the current phase's `boot-prompt.md` dynamically from:
   - Phase definition (goals, scope, exit criteria from the plan)
   - Actual implementation state (what files exist, what was merged, what the code does)
   - Previous phase outputs (deviations from plan, decisions made, gotchas)
   - Active Linear tickets (assigned, blocked, done)
   
   Boot prompts are **generated, not hand-written**. They always reflect current reality, not original plan assumptions.

3. **Phase README update** — Updates the current phase's `phases/phase-N/README.md` with implementation context from this session: what was built, what deviated from plan, what the next phase should know. Captures deviations explicitly so downstream boot prompts inherit them.

4. **Cross-wiki intelligence flag** — Searches the other engineer's personal wiki for content relevant to what changed in this session. Surfaces matches as non-blocking suggestions: "Paul documented X in `paul-wiki/research/fvg-edge-cases.md` — may be relevant to your FVG detector work."

5. **Roadmap status update** — Updates the phase status table (in `initial-plan/` and personal wiki phase indexes) based on ticket completion percentages.

### Why Boot Prompts Must Be Generated

A Phase 3 boot prompt written during Phase 0 planning is stale by the time Phase 3 starts — Phase 1 and 2 implementation will have made decisions that deviate from the original plan. If the boot prompt still references the original plan, the engineer starts with wrong assumptions.

The chain rule: when Phase N finishes, `/sync` captures deviations in Phase N's README. When Phase N+1 starts, `/sync` generates Phase N+1's boot prompt including those deviations. The boot prompt always reflects what was **actually built**, not what was **originally planned**.

### End-of-Session Behavior

Every Claude Code session that modifies code, wiki content, or tickets should end with:

```
Would you like to run /sync before ending this session?
This will: update Linear tickets, regenerate boot prompts, 
update phase README, and check for cross-wiki relevant content.
```

This is documented as a mandatory offer in the root CLAUDE.md and both personal wiki CLAUDE.mds.

### Implementation

Starts as a Claude Code skill (`.claude/skills/sync.md`). Uses `gh` CLI for git/PR state, Linear API (or `linear` CLI) for ticket state, and file reads/writes for wiki and boot prompt updates.

Upgrade to a CI/CD-triggered endpoint when the team grows or when automation beyond end-of-session is needed.

---

## 23. Missing Requirements

- **User roles and permissions** — need student/instructor/admin roles (currently single-user)
- **Subscription/billing infrastructure** — no Stripe integration exists
- **Admin dashboard** — no internal management UI
- **Product analytics** — no DAU/retention/conversion tracking
- **Evaluation datasets** — no RAG test pairs exist yet
- **Legal pages** — no ToS, Privacy Policy, or educational disclaimer
- **Content license agreement** — no legal framework for instructor content
- **Feedback/correction pipeline** — no mechanism for users or instructor to flag incorrect responses
- **Prompt versioning** — no version tracking or A/B testing for system prompts
- **Model monitoring** — no quality metric tracking over time
- **Incident response** — no downtime communication or escalation process
- **Support process** — no customer support channel
- **Launch checklist** — no formal pre-launch verification list
- **Churn prevention** — no engagement nudges, re-engagement flows, or cancel feedback
- **Mobile optimization** — responsive but not deliberately designed for mobile
- **Multi-tenant data isolation** — current `user_id` scoping is insufficient for multi-instructor

---

## 24. Final Recommendation

### Should we pursue NeuroLLM as the new product direction?

**Yes, but modify the approach significantly.**

The NeuroLLM spec is strategically correct. The platform vision (coaching → backtesting → quant modeling → automated trading) is the right sequence. The modifications:

1. **Two parallel tracks after Phase 6.** Track A (coaching product) generates revenue. Track B (backtesting → NeuroQuant → NeuroTrader Agent) builds the trading intelligence platform. Track B can begin during Track A's beta/launch phase.

2. **The null test at Phase 7C is a hard gate.** If ICT strategies don't show statistically significant edge (p < 0.05) in walk-forward backtesting, the NeuroTrader Agent (Phase 9) pivots to "better analytics + coaching tools" — still valuable, but not automated trading. This protects the team from building a trading bot on an unvalidated premise.

3. **Shadow → Paper → Live progression is mandatory.** No shortcuts. 30+ days profitable paper trading before live. 5-layer safety architecture. Kill switch on every screen.

4. **NeuroQuant (hybrid LLM + quant) is the real differentiator.** The combination of ICT condition gates (binary) + ML confidence (probability) + LLM reasoning (narrative coherence) is novel. No competitor does this. ICT conditions filter, ML models score, LLM reasons about edge cases — each system handles what it's good at.

5. **Build backtesting FIRST, before any live trading.** Without robust backtesting with walk-forward validation and Monte Carlo simulation, the trading agent is gambling. The backtesting platform is independently valuable as a product feature even if the agent never goes live.

6. **Defer multi-instructor platform abstraction** until the first instructor proves unit economics.

### Next 10 Actions

1. **Confirm instructor content access** — Direct conversation, written agreement. GATE for everything else.
2. **Prototype RAG on existing wiki** — Build a test pipeline with 5 business-logic docs, run 20 ICT questions, measure retrieval precision. Takes 2-3 days.
3. **Enable pgvector on existing PostgreSQL** — One `CREATE EXTENSION` command. Zero cost.
4. **Set up Linear workspace** — Import Phase 0-1 issues. 30 minutes.
5. **Build ICT terminology normalization dictionary** — 50+ terms mapping Whisper variants to canonical ICT terms.
6. **Create 50 evaluation Q&A pairs** — Ground-truth dataset for RAG quality.
7. **Design chat UI mockups** — Reference existing coaching panel. Decide: separate page vs. integrated.
8. **Set up CI/CD** — GitHub Actions for pytest + ESLint + type-check. 1 day.
9. **Evaluate Polygon.io for market data** — Sign up for starter plan ($29/mo). Pull 1 year of NQ 1-minute data. Validate quality and API behavior. This feeds Phase 7.
10. **Build wiki ingestion pipeline** — Markdown → chunk → embed → pgvector. The first load-bearing deliverable.

### Decision Matrix

| Decision | Recommendation | Alternatives | Key Tradeoff |
|---|---|---|---|
| Build approach | Extend existing monorepo | Separate service, new architecture | Speed vs. separation. At 2-engineer scale, one deployment wins. |
| Vector DB | pgvector | Pinecone, Chroma, Weaviate | $0 vs. $50-200/mo. Corpus is hundreds of chunks. |
| Embedding model | OpenAI text-embedding-3-small | BGE-M3, text-embedding-3-large | $0.02/1M tokens. Small is sufficient for this corpus. |
| LLM for coaching | Claude Sonnet 4.6 via API | GPT-4o, self-hosted | Already integrated with prompt caching. |
| Backtesting engine | Custom event-driven (Python) | Zipline, Backtrader, VectorBT | ICT-specific logic conflicts with off-the-shelf frameworks. ~1200 lines of custom code. |
| Data processing | Polars | Pandas | 10-100x faster, lower memory, better API for columnar data. |
| Market data storage | Parquet on R2 | TimescaleDB, PostgreSQL | Cheapest ($0.015/GB/mo). Fast with Polars. No extra DB to manage. |
| ML models | LightGBM + scikit-learn | Deep learning (LSTM, Transformer) | With hundreds of trades (not millions), boosted trees outperform. No GPU needed. |
| Regime detection | HMM (hmmlearn) | Clustering, rule-based | HMM discovers states from data; rule-based MVP as fallback. |
| Agent execution | Tradovate API (bracket orders) | IBKR, Alpaca | Already have partial integration. OSO bracket = entry + stop + target. |
| Billing | Stripe Billing | Paddle, Lemon Squeezy | Industry standard. Handles subscriptions natively. |
| Project tracking | Linear | GitHub Projects, Jira | Best DX for 2 engineers. |
| Fine-tuning | Defer until 200+ examples exist | Build now | Don't build infrastructure for data you don't have. |
| Multi-instructor | Defer until first instructor proves revenue | Build now | Premature abstraction vs. shipping faster. |
| Live trading gate | Null test + 30 days paper | Go live immediately | Safety first. Non-negotiable. |

### Full Timeline Summary

| Phase | Weeks | Description | Key Deliverable |
|---|---|---|---|
| 0 | 1-3 | Research & Validation | RAG prototype, instructor commitment |
| 1 | 4-9 | Knowledge Base & RAG MVP | Chat coaching with citations |
| 2 | 10-15 | Market Context & Tools | Agent tools, economic calendar |
| 3 | 16-21 | Product MVP | Billing, onboarding, landing page |
| 4 | 22-24 | Evaluation & Reliability | Eval suite, load testing, security audit |
| 5 | 25-28 | Private Beta | 20-50 users, feedback loop |
| 6 | 29-31 | V1 Launch | First revenue |
| 7 | 32-43 | Backtesting Platform | Engine, Monte Carlo, WFO, **null test** |
| 8 | 44-55 | NeuroQuant | Features, regime detection, ML models, ensemble |
| 9 | 56-68 | NeuroTrader Agent | Shadow → Paper → Live (conditional) |
| 10 | 69+ | Advanced Features | Multi-instructor, strategy builder, mobile |
