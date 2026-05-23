---
tags: [roadmap-idea, neurospect, next]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: next
status: backlog
---

# Mistake-Driven Action Items

Recurring mistake tags become concrete improvement tasks tied to playbooks, rules, or coaching prompts. "Took trade outside kill zone" three times in a week → action item: pre-trade kill-zone check enabled on next session.

## Why it matters

The journal already captures `mistake_tags` (TEXT[] in the trade schema). Today they're searchable but not actionable. Converting them into recurring tasks is the simplest path from "I journal" to "the journal changes my behaviour."

## Dependencies

- Existing mistake tagging in [[concepts/architecture/trade-schema]].
- Light task model (new table or reuse `coaching_events`?).

## Open questions

- Threshold for "recurring" — count, recency window, or model-driven?
- Should action items integrate with the AI Coach panel (next live session reads recent active items into the system prompt)?
- Manual override for trader to dismiss false positives.

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/trade-schema]]
- [[concepts/architecture/tradingview-connector]]
- [[concepts/roadmap/ideas/trader-psychology-profiler]]
