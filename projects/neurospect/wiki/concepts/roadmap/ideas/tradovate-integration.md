---
tags: [roadmap-idea, neurospect, next, broker]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: next
status: backlog
---

# Tradovate Integration (Prop Accounts)

Import trades from Tradovate; surface prop-firm account state (balance, drawdown, daily P&L) inside Neurospect; foundation for live risk monitoring and multi-account analytics.

## Why it matters

Most ICT/SMC retail traders working through prop firms (Topstep, Apex, etc.) execute on Tradovate. Without broker data, the journal is manual entry and analytics drift from reality. Tradovate's API is documented, OAuth-based, and covers fills + account state — feasible scope for a single workstream.

## Dependencies

- Existing trade schema ([[concepts/architecture/trade-schema]]) — confirm it accommodates broker-sourced fills (likely needs a `source` field and broker-event idempotency keys; matches the v2 event-sourced design Paul already documented).
- Tradovate API auth model + rate limits.

## Open questions

- Single-broker or pluggable-broker abstraction from day one? (Pluggable is more work but pays off if we add NinjaTrader, Rithmic, etc.)
- How do we handle the demo / live / funded account distinction natively?
- Real-time tick stream or end-of-session pull?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/trade-schema]]
- [[concepts/roadmap/ideas/multi-account-portfolio-analytics]]
- [[concepts/roadmap/ideas/overtrading-risk-limits]]
- [[concepts/roadmap/ideas/reduce-journaling-friction]]
