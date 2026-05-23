---
phase: 4
name: "Evaluation, Reliability & Prompt Infrastructure"
status: not_started
track: "A (Coaching)"
assigned: []
started: null
completed: null
tickets_total: 1
tickets_done: 0
created: 2026-05-09
updated: 2026-05-10
---

# Phase 4: Evaluation, Reliability & Prompt Infrastructure

Automated eval suite, load testing, security audit, instructor review, monitoring, and the prompt versioning module that becomes infrastructure for EdgeLab (Phase 7+).

## Goals

### 4A: Evaluation & Reliability

- Automated nightly evaluation pipeline
- Load testing (50 concurrent users)
- Security audit
- Instructor reviews 50+ AI responses
- User feedback mechanism (thumbs up/down)
- Monitoring and cost alerting

### 4B: Prompt Versioning Module

Build the prompt versioning infrastructure that coaching uses immediately and EdgeLab depends on later.

- **Prompt registry** — catalog all prompts (coaching, analysis, agent) with version, status, and lineage metadata
- **Version tracking** — each prompt version is immutable and traceable; new versions link to their predecessor
- **A/B testing framework** — run prompt variants against the same inputs, measure output quality against trade outcomes and coaching ratings
- **Regression detection** — automated comparison when model versions change (e.g., Claude 4.6 → 4.7); flag quality degradation before it reaches users
- **Per-strategy prompt tuning** — version and specialize prompts by ICT strategy (FVG, Order Blocks, Liquidity Sweeps, etc.)
- **Audit trail** — every coaching response traceable to exact prompt version, model, and inputs
- **Rollback** — one-step revert to last known good prompt version
- **Multi-model routing** — same logical prompt, optimized variants per model (Opus vs Sonnet vs Haiku), selected at runtime

This module starts as a filesystem + git approach (organized `prompts/` directory with frontmatter) and graduates to a Python module (`api/app/prompts/`) with database-backed registry by the end of Phase 4.

### Why Phase 4

Phase 4 is the natural home because:
1. The folder structure is used informally during Phases 1-3
2. Phase 4 is already about evaluation — prompt versioning is evaluation infrastructure
3. EdgeLab (Phase 7) depends on prompt/model version registries — they must exist before Phase 7 begins
4. The coaching product (Phase 5 beta) benefits from A/B testing and rollback before real users arrive

## Exit Criteria

### Evaluation & Reliability
1. Hallucination rate < 10%
2. Latency < 5s (p95) under load (50 concurrent users)
3. Instructor approves 85%+ of AI responses

### Prompt Versioning Module
1. All active prompts registered with version metadata
2. A/B test pipeline functional — can compare two prompt versions against the same inputs and measure quality difference
3. Regression detection runs automatically on model version changes
4. Audit trail queryable — given a coaching response, trace to exact prompt version
5. Rollback demonstrated — revert a prompt and verify coaching output changes
6. Module API consumed by coaching (Mentor) and ready for EdgeLab integration

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
