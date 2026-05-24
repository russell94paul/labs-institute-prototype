---
tags: [research, neurofusion, architecture, ml, ensemble]
created: 2026-05-23
updated: 2026-05-23
status: active
phases: [6, 11, 3-NG]
---

# NeuroFusion Architecture Research

Cross-cutting research into the NeuroFusion-13 architecture — a Knowledge-Fused Ensemble Intelligence (KFEI) system that combines 13 distinct signal types into a unified quant trading platform.

NeuroSpect is a **quant trading platform** — the core is systematic/algorithmic (EdgeLab, NSLM, NeuroQuant, NeuroTrader Agent). The discretionary coaching layer (AI coach on past trades) is a separate feature, not part of the NeuroFusion model. NeuroFusion-13 powers the advanced tier for systematic signal generation, strategy discovery, and automated decision-making.

This research spans Phases 5 (EdgeLab), 11 (Advanced ML), and 3-NG (NeuroGraph). Findings inform architectural decisions across all three.

## The NeuroFusion-12 Signal Architecture

| # | Signal | Type | Question It Answers |
|---|---|---|---|
| 1 | VectorDB (NeuroCore) | Semantic retrieval | "What does the knowledge base say?" |
| 2 | DSLM (NSLM) | Domain LLM reasoning | "What does ICT methodology reason?" |
| 3 | Quant Model (EdgeLab) | Statistical prediction | "What do the numbers predict?" |
| 4 | Knowledge Graph (NeuroGraph) | Temporal/relational | "What patterns has this trader shown?" |
| 5 | Causal Engine | Causal inference | "What *causes* this outcome?" |
| 6 | Conformal Predictor | Calibrated uncertainty | "How reliable is this prediction?" |
| 7 | Adversarial Debate | Multi-agent reasoning | "What's the counter-argument?" |
| 8 | Synthetic Scenarios | Generative stress-test | "What *could* break this?" |
| 9 | Active Learning | Uncertainty sampling | "Where does human input help most?" |
| 10 | Federated Network | Collective intelligence | "What do all traders collectively show?" |
| 11 | Contrastive Regimes | Self-supervised discovery | "What market state are we actually in?" |
| 12 | Program Synthesis | Strategy discovery | "What patterns exist that humans haven't found?" |

**Data Sources (feed into multiple signals, not signals themselves):**

| Source | What It Provides | Feeds Into |
|---|---|---|
| Fundamental Events | Economic calendar (FOMC, NFP, CPI, PPI, Fed Chair), earnings reports, dividend dates, contract rollover, options expiry | Signals 3, 4, 5, 8, 11, 13 |
| Market Data | OHLCV bars, tick data, session context, volume profile | Signals 3, 4, 5, 8, 11, 12 |
| ICT Wiki Corpus | 135+ pages of ICT/Smart Money methodology, entry models, course content | Signals 1, 2 |
| Trade Journal | User's trades, behavior metrics, outcomes | Signals 3, 4, 5, 9 |

## Key Hypothesis

The ensemble is novel because fusion happens at the **reasoning level** (each signal contributes a different *kind* of intelligence) rather than the **prediction level** (stacking model outputs). No known system combines all 12 signal types.

## Research Structure

```
neurofusion/
├── README.md                        # This file
├── deep-research-prompts.md         # 5 ChatGPT deep research prompts
├── core-signals/                    # Findings on signals 1-4
│   ├── vectordb-retrieval/          # Hybrid retrieval techniques
│   ├── domain-specific-lm/          # DSLM + quant hybrid
│   ├── knowledge-graph/             # Persistent intelligence graphs
│   └── discretionary-trading-tech/  # Novel trading technology
├── extended-signals/                # Findings on signals 5-12
│   ├── causal-discovery/
│   ├── conformal-prediction/
│   ├── adversarial-debate/
│   ├── synthetic-scenarios/
│   ├── active-learning/
│   ├── federated-learning/
│   ├── contrastive-regimes/
│   └── program-synthesis/
├── architecture/                    # Fusion architecture design
│   ├── signal-fusion-design.md      # How signals combine
│   ├── papers.md                    # Key papers and references
│   └── competitive-landscape.md     # What exists, what doesn't
└── data/                            # Raw research outputs
```

## Research Status

| Area | Status | Source |
|---|---|---|
| Deep research prompts | Ready to run | ChatGPT Deep Research |
| Core signals (1-4) | Pending | Prompts 1-4 |
| Extended signals (5-12) | Pending | Prompt 5 |
| Fusion architecture | Concept stage | Internal design |
| Competitive landscape | Pending | Prompt 1 |

## Naming

- **Architecture:** Knowledge-Fused Ensemble Intelligence (KFEI)
- **Brand:** NeuroFusion Architecture
- **Full stack:** NeuroFusion-12
- **Academic:** Compound Neuro-Symbolic Trading Intelligence (CNSTI)
