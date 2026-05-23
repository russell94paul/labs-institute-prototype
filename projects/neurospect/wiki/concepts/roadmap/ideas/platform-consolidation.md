---
tags: [roadmap-idea, neurospect, strategic, integration]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: strategic
status: backlog
---

# Platform Consolidation: Discord + TradingView + Tradovate

Long-term goal: Neurospect absorbs the daily workflow currently spread across Discord (community/signals/accountability), TradingView (charts/alerts/Pine), and Tradovate (execution/account data). The trader doesn't switch tabs.

## Why it matters

Defines the product ceiling. Each integration on its own is a feature; together they're a product moat. Determines how every other roadmap item is scoped.

## Sub-tracks

- **Discord** — community/signals/accountability surfaces; Discord OAuth already in place; bot for in-Discord journaling.
- **TradingView** — beyond webhooks: drawn-on-chart annotations, multi-symbol Pine indicator suite, alert templates per setup.
- **Tradovate** — beyond import: order placement, account-rule enforcement at the broker layer.

## Dependencies

- [[concepts/roadmap/ideas/tradovate-integration]] (Next horizon) is the gateway.
- TradingView Premium / API limits; Discord bot rate limits.

## Open questions

- Build order — which integration earns the strategic bet first based on user feedback?
- Multi-broker abstraction or Tradovate-first.

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/tradingview-connector]]
- [[concepts/roadmap/ideas/tradovate-integration]]
- [[concepts/roadmap/ideas/vertical-ai-platform]]
