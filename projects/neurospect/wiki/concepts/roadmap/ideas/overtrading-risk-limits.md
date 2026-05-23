---
tags: [roadmap-idea, neurospect, later, risk]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: later
status: backlog
---

# Overtrading & Risk Limit System

Detect overtrading behaviour and enforce trader-survival rules: daily loss limits, max trades per day, cooldowns after losses, drawdown awareness, account-protection thresholds aligned with prop-firm rules.

## Why it matters

In prop trading, the rules that kill accounts are universal (daily loss limit, max contracts, news embargo). Most blow-ups are behavioural, not analytical. Building this in turns Neurospect from a review tool into a live discipline layer — a much stickier value prop.

## Dependencies

- Live broker data ([[concepts/roadmap/ideas/tradovate-integration]]).
- Account-rule schema (per-firm thresholds).

## Open questions

- Hard block vs. friction (cooldown timer, forced checklist) vs. notification-only?
- Per-firm preset rule sets (Topstep, Apex, etc.) vs. user-defined?
- How does the risk system interact with the AI Coach — does the coach refuse to evaluate setups when a daily loss limit is hit?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/roadmap/ideas/tradovate-integration]]
- [[concepts/roadmap/ideas/trader-psychology-profiler]]
- [[entities/projects/neurospect]] § *Moonshot Ideas* — Execution Guardian
