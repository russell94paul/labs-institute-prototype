---
tags: [roadmap-idea, neurospect, next, analytics]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: next
status: backlog
---

# Multi-Account & Portfolio Analytics

Filters across the existing analytics dashboard for multiple accounts (personal, prop firm A, prop firm B), strategy, instrument, timeframe, setup type, mistake category. Adds a portfolio-level performance view aggregated across accounts.

## Why it matters

Most active prop traders run 2–10 accounts simultaneously. Today the journal assumes a single trading identity. Multi-account filters surface where the edge actually lives and which firm/strategy combination is paying off.

## Dependencies

- [[concepts/roadmap/ideas/tradovate-integration]] (or any broker import) for trustworthy multi-account data.
- Schema additions: `account_id`, `firm`, possibly `account_type` ENUM.

## Open questions

- How are funded vs. evaluation vs. demo accounts treated in aggregate metrics?
- Currency normalisation for portfolio view if accounts span instruments with different point values.

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/trade-schema]]
- [[concepts/roadmap/ideas/tradovate-integration]]
