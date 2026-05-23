---
phase: 14
name: "Retention, Analytics & Coaching Quality"
status: not_started
track: "C (Business & Operations)"
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
parallel_with: [4, 5, 6]
gates: []
created: 2026-05-10
updated: 2026-05-10
---

# Phase 14: Retention, Analytics & Coaching Quality

Build the measurement and feedback systems that prove coaching works and keep users engaged. Trading education has notoriously high churn — most retail traders quit within 6-12 months.

## Why This Phase Exists

Neither plan addresses what happens after users sign up. No engagement loops, no re-activation strategy, no coaching quality measurement beyond "does the RAG retrieve the right content." Without this, you'll acquire users and lose them. This phase ensures you can answer: "Is the coaching actually making traders better?"

## Goals

1. **Churn model** — Understand why users leave and predict who's at risk before they cancel
2. **Engagement loops** — Design product features that create habitual usage (daily coaching, trade review rituals, streak tracking)
3. **Coaching quality evaluation** — Measure whether coaching responses are accurate, helpful, and actually improve trading outcomes
4. **A/B testing framework** — Test coaching approaches, prompts, and features against measurable outcomes
5. **User outcome tracking** — Track whether users who engage with coaching improve their trading results over time
6. **Re-activation campaigns** — Win back churned or dormant users with targeted interventions

## Deliverables

| Deliverable | Description | Gate? |
|---|---|---|
| Churn prediction model | Identify leading indicators of churn (login frequency, question volume, trade frequency) | No |
| Engagement loop design | Product features: daily coaching prompt, trade review ritual, weekly progress report, streak system | No |
| Coaching quality rubric | Scoring framework: accuracy, helpfulness, source-groundedness, actionability, safety (no harmful advice) | Yes |
| Automated coaching evaluation | Nightly eval pipeline: sample responses scored against rubric by LLM judge + instructor spot-check | No |
| A/B testing infrastructure | Feature flag system for testing coaching prompts, UI variants, engagement features | No |
| User outcome dashboard | Track: win rate trend, P&L trend, journal consistency, concept mastery progression per user | No |
| Cohort analysis framework | Compare retention and outcomes across signup cohorts, pricing tiers, and engagement levels | No |
| Re-activation playbook | Email/notification sequences for dormant users (7-day, 30-day, 90-day) | No |

## Key Metrics

| Metric | Target | Measurement |
|---|---|---|
| 7-day retention | > 50% | Users who return within 7 days of signup |
| 30-day retention | > 30% | Users active in their 4th week |
| Monthly churn rate | < 10% | Paid subscribers who cancel per month |
| Coaching accuracy | > 85% | Instructor-validated response accuracy |
| Coaching helpfulness | > 4.0/5 | User rating per coaching interaction |
| NPS | > 30 | Quarterly survey |
| Time-to-value | < 10 minutes | Time from signup to first useful coaching interaction |

## Engagement Loop Design

```
Daily Loop:
  Morning → AI sends market context briefing
  Pre-session → AI suggests what to watch for (based on user's level + ICT concept progression)
  Post-session → AI prompts for trade review journal entry
  Evening → AI delivers daily coaching summary + progress nudge

Weekly Loop:
  Monday → Weekly goal setting (AI-suggested based on recent trades)
  Friday → Weekly performance review + concept mastery update
  Sunday → Week-ahead preparation (economic calendar, key levels)

Monthly Loop:
  Month-end → Comprehensive progress report
  Milestone → Concept mastery badges / level progression
```

## Coaching Quality Evaluation Framework

| Dimension | Weight | Evaluation Method |
|---|---|---|
| Factual accuracy | 30% | LLM judge + instructor spot-check |
| Source-groundedness | 20% | Citation verification against wiki content |
| Actionability | 20% | Does the response give concrete next steps? |
| Pedagogical quality | 15% | Does it teach, not just answer? |
| Safety | 15% | No reckless advice, proper risk disclaimers |

## Exit Criteria

1. Churn prediction model identifies at-risk users with > 70% accuracy
2. At least 3 engagement loops implemented and instrumented
3. Coaching quality rubric documented and automated evaluation running nightly
4. A/B testing infrastructure operational with at least 1 experiment completed
5. User outcome tracking deployed (even if correlation data takes months to accumulate)

## Dependencies

- **Parallel with:** Phases 4-6
- **Requires:** Active users (Phase 5 beta), coaching product functional (Phase 3)
- **Feeds into:** Phase 8 (coaching quality data informs NSLM evaluation)

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
