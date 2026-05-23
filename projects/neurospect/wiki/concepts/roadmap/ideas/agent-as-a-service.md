---
tags: [roadmap-idea, neurospect, research, exploratory]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: research
status: backlog
---

# Agent-as-a-Service

Surface Neurospect's coaching/analysis agents to external products or users — e.g., embed an ICT coach into another tool, or expose a research agent that other traders can call.

## Why it matters

Logged for completeness. Concrete use cases are not yet clear. Worth tracking because the underlying agent infrastructure (Claude pipeline, prompt caching, strategy library) is reusable beyond the Neurospect UI.

## Dependencies

- Mature agent surface inside Neurospect first.

## Open questions

- Which agent capability has external pull (live coaching vs. trade review vs. journal extraction)?
- B2B vs. B2C distribution model.
- Pricing — per-call API vs. embedded SDK vs. white-label.

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/tradingview-connector]]
- [[concepts/ai-coach/system-prompt-template.md]]
