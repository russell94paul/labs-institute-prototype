---
name: ns-phase7
description: NeuroSpect Phase 7 — Edge Forensics
---

You are working on **NeuroSpect Phase 7** (Edge Forensics).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read Phase 2 analytics service — `api/app/services/analytics.py` (trade breakdown data)
4. Read Phase 2 behavior metrics service (tilt, discipline, consistency)
5. Read Phase 4 event models — `api/app/models/market_event.py` (event-trade associations)
6. Read Phase 5 EdgeLab experiment runner (for "promote to backtest" workflow)
7. Read Phase 6 AI coach — `api/app/coach/claude_client.py` (for AI-powered hypothesis enrichment)

## Goal

Turn repeated losses and mistake patterns into testable improvement hypotheses. Edge Forensics connects analytics (Phase 2), events (Phase 4), backtesting (Phase 5), and AI review (Phase 6) into a loss-diagnosis pipeline. This is where NeuroSpect becomes uniquely defensible — generic journals can't do this because they lack the event engine and backtest infrastructure.

## Deliverables

1. **Loss cluster detection** (`api/app/edgelab/forensics/cluster_detector.py`):
   - Group losing trades by: setup type, session, instrument, day of week, market conditions
   - Identify statistically over-represented loss clusters (chi-squared or binomial test)
   - Minimum sample size requirements (N >= 10 per cluster)
2. **Structured mistake taxonomy** (`api/app/models/mistake_taxonomy.py`):
   - Categories: premature_entry, no_displacement, wrong_session, counter_trend, revenge_trade, oversize, moved_stop, no_htf_bias, missed_exit, holding_through_news
   - Auto-detection rules for each category (from trade data + events)
   - Manual override (user can tag or untag mistakes)
3. **Pattern mining** (`api/app/edgelab/forensics/pattern_miner.py`):
   - Find correlations between losses and contextual factors:
     - Which ICT events were present/absent at entry?
     - What was the behavior state (tilt score, recent streak)?
     - What regime was the market in (if regime data available)?
     - What time/session/day was it?
   - Output: ranked list of loss-correlated factors with effect size
4. **Hypothesis generator** (`api/app/edgelab/forensics/hypothesis_generator.py`):
   - Convert loss patterns into structured, testable hypotheses
   - Format: "You lose {X}% of {setup} trades when {condition}. Hypothesis: {filter_rule} would improve win rate by {estimated}%."
   - AI enrichment: use Claude to generate human-readable explanations and improvement suggestions
5. **"Promote to backtest" workflow**:
   - One-click from hypothesis → EdgeLab experiment
   - Auto-generates strategy modification (add filter condition from hypothesis)
   - Runs A/B backtest: original strategy vs modified strategy
6. **Forensics API** (`api/app/routers/forensics.py`):
   - `GET /api/forensics/clusters` — loss clusters for user
   - `GET /api/forensics/hypotheses` — generated hypotheses
   - `POST /api/forensics/hypotheses/{id}/promote` — promote to EdgeLab experiment
   - `GET /api/forensics/improvement` — improvement tracking over time
7. **Forensics dashboard** (`app/src/pages/forensics.tsx`):
   - Loss cluster visualization (grouped bar chart by category)
   - Hypothesis cards with evidence, confidence, and "Test this" button
   - Improvement timeline (NeuroScore / win rate / discipline score over months)
8. **Tests** for clustering, taxonomy auto-detection, and hypothesis generation

## Key Constraints

- Hypotheses are "testable" not "proven" — no guaranteed improvement claims
- Frame as analytical tool: "Edge Forensics identifies patterns in your trading data that may represent improvement opportunities"
- Minimum sample sizes enforced — no hypotheses from < 10 trades
- Effect sizes must be meaningful (not just statistically significant)
- Do not auto-execute hypothesis-modified strategies in live trading
- Premium feature: Research tier ($199/mo) and above

## Acceptance Criteria

- [ ] Loss cluster detection identifies statistically significant loss patterns
- [ ] Mistake taxonomy auto-detects at least 5 categories from trade + event data
- [ ] Pattern mining produces ranked loss-correlated factors with effect sizes
- [ ] Hypothesis generator creates structured, testable hypotheses with evidence
- [ ] "Promote to backtest" creates an EdgeLab experiment with modified strategy
- [ ] Forensics dashboard shows clusters, hypotheses, and improvement timeline
- [ ] Minimum sample size enforced (no hypotheses from < 10 trades)
- [ ] Tests cover clustering edge cases, taxonomy detection, and hypothesis format

## When done

Say: "Phase 7 complete — Edge Forensics turns losses into testable hypotheses. Run `/ns-phase8` in a new session for NeuroScore + Leaderboard."
