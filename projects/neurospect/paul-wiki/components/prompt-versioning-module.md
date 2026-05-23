---
tags: [prompts, versioning, architecture, neuro-llm, nslm]
component: prompt-engine
status: planned
phase: 4
promote: false
created: 2026-05-10
updated: 2026-05-10
---

# Prompt Versioning Module

Design spec for a programmatic prompt versioning system. Near-term use: organized folder with frontmatter-based versioning. Long-term: a Python module that loads, versions, and serves prompts at runtime.

## Near-Term: `prompts/` Directory

Top-level monorepo directory for build-time and engineering prompts (separate from product prompts in `wiki/concepts/ai-coach/`).

```
prompts/
├── CLAUDE.md              # Conventions, frontmatter schema
├── index.md               # Registry
├── phases/
│   ├── phase-0/           # Prompts tied to Phase 0 work
│   └── phase-1/
├── ad-hoc/                # Not tied to a specific phase
└── meta/                  # Meta-prompts (prompt-engineering prompts)
```

Frontmatter schema per prompt:

```yaml
---
version: 2
phase: 1
purpose: RAG retrieval pipeline design
status: active | superseded | experimental
supersedes: phases/phase-0/rag-retrieval-v1.md
created: 2026-05-10
updated: 2026-05-10
---
```

## Long-Term: Prompt Versioning Module

A Python module (`api/app/prompts/` or standalone `prompt-engine/`) that manages prompts programmatically. Builds on top of the folder structure.

### What It Enables

#### Agent Performance & Self-Improvement
- **A/B test prompt variants** against real trade outcomes — measure whether prompt v3 produces better coaching responses than v2.
- **Per-strategy prompt tuning** — specialize prompts by ICT strategy (Fair Value Gaps vs Order Blocks vs Liquidity Sweeps).
- **Regression detection** — when a model upgrade changes behavior, compare outputs across prompt versions to catch degradation before users do.

#### NeuroTrader Agent Loop
- **Auditable prompt history** — which prompt version was active when the agent took a trade? Critical for post-trade LLM analysis and regulatory defensibility.
- **Automatic prompt evolution** — agent analyzes losing trades, proposes prompt modifications, versions them, tests in shadow mode before promotion. The versioning module is the backbone of that feedback loop.

#### NeuroQuant Confluence Scoring
- **Regime-bound prompt variants** — different market regimes (trending vs ranging vs volatile) may need different prompt strategies for LLM narrative reasoning. Version and bind prompt variants to regime states.

#### Operational Maturity
- **Rollback** — bad prompt goes live, one-line revert to last known good version.
- **Audit trail** — "why did the coach say X?" traces to exact prompt version, inputs, and model.
- **Multi-model routing** — same logical prompt, different optimized versions for Opus vs Sonnet vs Haiku, selected at runtime by task complexity.

### Core Insight

Git tracks *what changed*. A prompt versioning module tracks *what performed* — connecting prompt identity to downstream outcomes (trade results, coaching quality scores, agent decisions). That's the difference between version control and version *intelligence*.

This maps directly onto the NeuroTrader self-improvement loop: the agent can't learn from its mistakes if it can't identify which prompt version produced each decision.

## Open Questions

- Should product prompts (`wiki/concepts/ai-coach/`) migrate into this system, or stay separate?
- What's the storage backend — filesystem + git, or database-backed?
- How does this interact with the NeuroCore retrieval layer?
