---
tags: [roadmap-idea, neurospect, next, extension]
aliases: []
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: next
status: backlog
---

# Chrome Extension for Trade Screenshots

Browser extension that captures or copies chart screenshots (TradingView, Tradovate, broker DOMs) directly into a Neurospect trade entry — pre-entry, entry, exit, and HTF context shots.

## Why it matters

Screenshot upload is already supported in the journal but the round-trip (snip → save → upload) is high-friction. An extension makes it one click and routes the image to the right trade phase. Compounds with [[concepts/roadmap/ideas/reduce-journaling-friction]].

## Dependencies

- Existing screenshot endpoints (`neurospect-api`).
- Auth model for the extension (use the same JWT issued to the SPA).

## Open questions

- MV3 constraints around capturing iframe content (TradingView lives in iframes).
- Per-phase auto-routing — does the extension prompt for phase, or does it pick the active phase from the in-app trade detail view?
- Firefox/Edge support or Chrome-only v1?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/phase3-frontend-structure]]
- [[concepts/roadmap/ideas/reduce-journaling-friction]]
