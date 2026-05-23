# NeuroSpect — Technical Reference (Extracted from Site + Roadmap)

_Compiled 2026-05-13. Source of truth for external content generation._

---

## Product Identity

**Name:** NeuroSpect
**Category:** AI-native trading research and coaching platform
**Target Market:** ICT (Inner Circle Trader) and Smart Money Concepts traders
**Positioning:** "The first platform where your setups are computable, your edge is provable, and your automation is earned — not toggled."
**Not:** A ChatGPT wrapper. A generic journal. A simple backtester.

---

## Product Hierarchy

```
NeuroSpect (company / product brand)
├── NeuroSpect Mentor   — Consumer-facing AI coaching product
├── NeuroCore           — Knowledge/retrieval layer (hybrid 3-signal search)
├── NSLM                — NeuroSpect Language Model (ICT-aware DSLM family)
├── NeuroSpect EdgeLab  — Research, backtesting, feature engineering, model evaluation engine
├── NeuroQuant          — Production model layer (regime-aware scoring, ensembles)
└── NeuroTrader Agent   — Automated trading agent (Shadow → Paper → Live)
```

### Component Details

| Component | Layer | Color | What It Does | Data It Consumes | Data It Produces |
|---|---|---|---|---|---|
| **NeuroSpect Mentor** | Consumer | Cyan (#06b6d4) | AI coaching with source-grounded citations, deterministic entry model validation, personalized to trader's journal | NeuroCore retrievals, NSLM reasoning, trade journal, psychology profile | Coaching conversations, mistake tags, action items, checklist results |
| **NeuroCore** | Intelligence | Purple (#8b5cf6) | Hybrid 3-signal search (BM25 + semantic/pgvector + entity/tag) via Reciprocal Rank Fusion | Wiki content (36K+ lines), trade journal, EdgeLab experiments, market data, agent signals | Retrieved passages with citations, cross-wiki intelligence, entity relationships |
| **NSLM** | Intelligence | Amber (#f59e0b) | ICT-aware language model family. Prompt-versioned, model-versioned, evaluated through EdgeLab. Produces structured reasoning, setup classifications, and features. | Curated ICT content, structured playbooks, evaluation feedback, injected feature parameters | Setup evaluations, trade thesis, structured outputs (confidence scores, checklist results), bespoke feature suggestions |
| **EdgeLab** | Research | Emerald (#10b981) | Event-driven backtesting, quant feature engineering, NSLM prompt/model experimentation, hybrid model evaluation | Market data (OHLCV), ICT detector outputs, NSLM structured outputs, feature store, strategy YAML specs | Backtest results, feature importance rankings, experiment comparisons, model candidates, promoted models |
| **NeuroQuant** | Research | Rose (#ec4899) | Production model scoring. Regime-aware ensembles. Confluence decisions: ICT gates (binary) + ML confidence (probability) + NSLM reasoning (coherence). | Promoted models from EdgeLab, validated features, regime classifications | Confluence scores, regime classifications, position sizing signals, model performance metrics |
| **NeuroTrader Agent** | Automation | Red (#ef4444) | Automated trading with 5-layer safety architecture. Shadow → Paper → Live progression. Gated by EdgeLab evidence. | NeuroQuant scoring, market data, risk limits, safety layer outputs | Trade executions, post-trade analysis, agent self-improvement signals |

### Data Flow

```
1. INGEST    → ICT content, transcripts, trade journal → NeuroCore hybrid index
2. RETRIEVE  → NeuroCore retrieves context → NSLM generates ICT-aware responses
3. RESEARCH  → EdgeLab backtests strategies → evaluates NSLM versions → promotes to NeuroQuant
4. EXECUTE   → NeuroTrader uses NeuroQuant scoring → 5 safety layers → human oversight
```

### Component Integration Map

| From | To | Integration |
|---|---|---|
| NeuroCore | Mentor | Retrieval — provides source-grounded passages for coaching responses |
| NSLM | Mentor | Generation — produces ICT-aware reasoning with feature-gate checks |
| NeuroCore | EdgeLab | Data — provides historical knowledge for experiment context |
| EdgeLab | NSLM | Evaluation — tests NSLM prompt/model versions against historical outcomes |
| EdgeLab | NeuroQuant | Promotion — validated models/features graduate to production |
| NeuroQuant | NeuroTrader | Scoring — provides confluence scores and regime signals for trade decisions |
| Trade Journal | Mentor | Personalization — journal data feeds coaching responses and mistake detection |
| Trade Journal | EdgeLab | Analysis — trade outcomes feed feature discovery and model evaluation |
| NeuroTrader | EdgeLab | Learning — agent's trade outcomes feed back into model improvement |
| Mentor | Trade Journal | Automation — coaching insights auto-tag journal entries with mistake categories |

---

## Data Sources & Data Warehousing

### Primary Data Sources

| Source | Type | Storage | Used By |
|---|---|---|---|
| ICT Wiki (36K+ lines) | Structured markdown | PostgreSQL + pgvector embeddings | NeuroCore, NSLM training |
| Mentor Transcripts | Raw text | PostgreSQL + pgvector | NeuroCore, NSLM fine-tuning |
| Trade Journal | Structured records (100+ fields, 17 enums) | PostgreSQL | Mentor, EdgeLab, Psychology Profiler |
| Market Data (OHLCV) | Time series (NQ, ES, Forex) | Parquet on R2 (Cloudflare) | EdgeLab backtesting, NeuroTrader |
| EdgeLab Experiments | Structured results | PostgreSQL | NeuroQuant, NSLM evaluation |
| NSLM Prompt Versions | Versioned prompts + metadata | PostgreSQL | EdgeLab, Mentor |
| NSLM Model Versions | Model artifacts + eval results | PostgreSQL + R2 | EdgeLab, NeuroQuant |
| Broker Data (Tradovate) | Trade fills, positions, account data | PostgreSQL (via API) | Journal auto-fill, risk engine |
| Economic Calendar | Event data | External API cache | Regime engine, risk engine |

### Database Schema (Key Tables)

**Core:** `trades`, `trade_journal_entries`, `users`, `conversations`, `coaching_messages`
**EdgeLab:** `edgelab_experiments`, `edgelab_runs`, `edgelab_run_trades`, `backtest_metrics`, `monte_carlo_results`, `walk_forward_results`
**Features:** `feature_definitions`, `feature_snapshots`
**NSLM:** `nslm_prompt_versions`, `nslm_model_versions`, `nslm_evaluation_runs`, `nslm_structured_outputs`
**Analytics:** `trader_profiles`, `psychology_assessments`, `mistake_patterns`

### Search Architecture (NeuroCore)

Three signals fused via Reciprocal Rank Fusion:
1. **Keyword/BM25** (PostgreSQL tsvector) — exact ICT jargon matches
2. **Semantic** (pgvector embeddings, text-embedding-3-small) — conceptual similarity
3. **Entity/Tag** — instrument, session, strategy, concept references

---

## Analytics Surfaces

| Where | What's Shown | Tier |
|---|---|---|
| **Trade Journal Dashboard** | PnL, win rate, R-distribution, day-of-week, session breakdown, mistake frequency | All paid |
| **Psychology Profiler** | Revenge trading detection, hesitation patterns, overtrading clusters, tilt sequences | Mentor+ |
| **Entry Model Validator** | Per-setup checklist pass/fail rates, setup quality scores, best/worst setups | Mentor+ |
| **Strategy Performance Reports** | Backtest equity curves, Monte Carlo fan charts, walk-forward efficiency | Trader+ |
| **EdgeLab Experiment Dashboard** | Experiment list, backtest detail, feature browser, NSLM prompt comparison | Research+ |
| **Feature Library** | Feature definitions, importance rankings, regime sensitivity, impact scores | Research+ |
| **NeuroQuant Scoring Panel** | Real-time confluence scores, regime classification, model ensemble outputs | Quant+ |
| **NeuroTrader Monitor** | Shadow/paper/live trade log, agent reasoning, safety layer triggers, concordance rate | Quant+ |
| **Risk Dashboard** | Drawdown curves, daily loss tracking, prop firm rule compliance, position sizing | Trader+ |
| **Session Analytics** | PnL by session (Asia/London/NY AM/Lunch/PM), best setups per session, avoided trades | All paid |

---

## How Trade Data Flows Through the Platform

```
TRADE EXECUTION (Broker)
    │
    ▼
JOURNAL AUTO-FILL ──────────────────────── Trade Journal Dashboard
    │                                       (PnL, win rate, R-dist)
    ▼
MENTOR ANALYSIS ────────────────────────── Coaching Conversations
    │ (reads journal, detects mistakes)     (personalized feedback)
    │
    ▼
PSYCHOLOGY PROFILER ────────────────────── Psychology Dashboard
    │ (pattern detection across entries)    (tilt, revenge, hesitation)
    │
    ▼
EDGELAB FEATURE DISCOVERY ──────────────── Feature Library
    │ (wins vs losses → new features)       (ranked, categorized)
    │
    ▼
EDGELAB BACKTESTING ────────────────────── Experiment Dashboard
    │ (test with new features)              (equity curves, Monte Carlo)
    │
    ▼
NSLM EVALUATION ────────────────────────── Prompt Comparison
    │ (compare prompt versions)             (A/B test results)
    │
    ▼
NEUROQUANT PROMOTION ───────────────────── Scoring Panel
    │ (validated models go to production)   (confluence scores)
    │
    ▼
NEUROTRADER AGENT ──────────────────────── Agent Monitor
    │ (uses scoring for execution)          (trade log, reasoning)
    │
    ▼
POST-TRADE ANALYSIS ────────────────────── Back to Journal
    (agent learns, feeds EdgeLab)           (continuous improvement loop)
```

---

## Pricing Tiers

| Tier | Price | Target | Key Unlocks |
|---|---|---|---|
| **Free** | $0 | Curious learners | 5 coaching Q/day, read-only glossary, basic journal |
| **Mentor** | $29/mo | Active ICT students | Unlimited coaching, full journal, voice journaling, psychology profiler, entry model checklists |
| **Trader** | $99/mo | Serious traders | + Backtesting (3/mo), Monte Carlo, broker auto-fill, risk engine, prop firm presets |
| **Research** | $199/mo | Strategy researchers | + Unlimited backtesting, walk-forward, EdgeLab experiments, feature library, NSLM prompt comparison |
| **Quant** | $349/mo | Quant-curious | + Hybrid models, feature engineering, regime detection, NeuroQuant, NeuroTrader shadow |
| **Team** | $499/mo | Educators/teams | + Private KBs, custom NSLM, API access, multi-user, revenue share |

---

## Trader Tiers (Workflow Personas)

### Tier 1: Discretionary ICT Trader
**Profile:** Knows ICT concepts, trades manually, journals inconsistently. Emotional decisions and overtrading erode edge.
**Workflow:** Study → Prepare → Execute → Journal → Review → Improve
**Components:** Mentor, NeuroCore, Journal, Course KB, Risk Limits
**Key Metrics:** 38 trades, 42% WR, PF 1.18, Sharpe 0.42, Max DD -$3,200, 24 mistakes

### Tier 2: Quant Trader
**Profile:** Systematic with statistical filters. Consistent execution but misses ICT-specific context.
**Workflow:** Define Strategy → Backtest → Validate → Null Test → Feature Engineer → Train → Evaluate → Deploy/Reject
**Components:** EdgeLab, Feature Store, Model Registry, NeuroQuant
**Key Metrics:** 24 trades, 55% WR, PF 1.72, Sharpe 0.91, Max DD -$1,800, 8 mistakes

### Tier 3: Hybrid Trader
**Profile:** ICT + quant confluence. NSLM-assisted grading. Selective and process-driven.
**Workflow:** Study → Research → Prepare → Execute → Journal → Review → Improve
**Components:** All Tier 1 + EdgeLab, NeuroQuant, NSLM
**Key Metrics:** 20 trades, 62% WR, PF 2.41, Sharpe 1.38, Max DD -$1,200, 4 mistakes

### Tier 4: S-Tier Trader
**Profile:** Full stack. EdgeLab-validated, NeuroQuant-scored, NeuroTrader-assisted. Maximum selectivity.
**Workflow:** Research → Validate → Promote → Shadow → Paper → Limited Live → Monitor → Iterate
**Components:** Everything + NeuroTrader Agent, 5-Layer Safety, Kill Switch
**Key Metrics:** 16 trades, 71% WR, PF 4.28, Sharpe 2.14, Max DD -$820, 2 mistakes

---

## EdgeLab Research Engines

### 1. Feature Discovery Engine
Analyzes trade outcomes → discovers win/loss patterns → auto-engineers features

**10 Core Features:**
| Feature | Type | What It Measures |
|---|---|---|
| `displacement_strength` | 0-1 | Displacement candle magnitude vs ATR |
| `fvg_fill_percentage` | 0-1 | How much FVG was filled before entry |
| `htf_bias_alignment` | 0/1 | LTF entry matches HTF bias |
| `session_quality_score` | 0-1 | Kill zone + volume + spread composite |
| `ob_proximity` | pts | Distance to nearest opposing order block |
| `consecutive_loss_flag` | 0/1 | 2+ consecutive session losses |
| `sweep_recency` | candles | Candles since last liquidity sweep |
| `smt_divergence_present` | 0/1 | SMT confirms entry direction |
| `adr_percentile` | 0-100 | Day's range vs 20-day ADR |
| `time_in_killzone` | min | Minutes remaining in active kill zone |

### 2. Regime-Adaptive Optimization Engine
6 regimes with per-regime parameter tuning + 5 dynamic condition modifiers

**Regimes:** Trending Bull, Trending Bear, Range-Bound, HV Expansion, LV Compression, Transition

**Dynamic Conditions:** Day of Week, Economic News, SMT Divergence, Session Liquidity Swept, Price Cycle Phase

### 3. NSLM Feature Studio
Inject features into NSLM prompts → run simulations → sweep parameters → discover optimal values → NSLM suggests new bespoke features

**Feature Categories:** ICT Structural, ICT Contextual, Quantitative, NSLM-Derived, Regime, Composite

---

## ICT Knowledge Base

**5 Course Modules (18 lessons):**
1. Foundations (Liquidity, FVGs, Practice)
2. Price Delivery (4 APD stages, Consolidation, Expansion, Reversals)
3. Session Context & Bias (Power of Three, Kill Zones, Deviations, Daily Bias)
4. Market Structure (Swings, Fractality, Structure Deviations, Model 2022/OTE)
5. Order Flow & SMT (HTF/LTF Order Flow, SMT Divergence)

**7 Entry Models:**
Consolidation, Daily Bias, Expansion & Retracement, London, Model 2022 OTE, Reversal/Raid on Stops, SMT Confirmation

**Minimum Confluence (all strategies):** HTF FVG bias confirmed + Opening price aligned + Kill zone active + PDA in discount + 1M entry or below

---

## Key Statistics

- 36K+ lines of curated ICT content
- 7 machine-readable entry models with YAML checklists
- 5 structured course modules, 18 lessons
- 100+ ICT-specific journal fields
- 17 specialized trading enums
- 7 analytics views
- 8 ICT pattern detectors (Swing, FVG, OB, Market Structure, Session, SMT, Bias, Consolidation)
- 6 market regime classifications
- 5 safety layers for automated trading
- 10K Monte Carlo iterations in < 30 seconds

---

## Competitive Advantage (14 capabilities unique to NeuroSpect)

1. ICT-aware reasoning
2. Trade thesis generation
3. Event-driven ICT backtesting
4. Journal intelligence
5. NSLM prompt/model experimentation
6. Quant feature engineering
7. Hybrid ICT + quant modeling
8. Personalized coaching
9. Risk review
10. Setup validation
11. Model/version comparison
12. Workflow memory
13. Source-grounded knowledge
14. Shadow/paper trading roadmap

No single competitor covers more than 3 of these. NeuroSpect covers all 14.
