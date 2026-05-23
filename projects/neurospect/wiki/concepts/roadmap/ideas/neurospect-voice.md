---
tags: [roadmap-idea, neurospect, later, ai, voice]
aliases: [Voice Coach]
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: later
status: backlog
---

# NeuroSpect Voice

> **Naming note:** "NeuroSpect Voice" is a placeholder. Better names may be picked later.

Voice-based trading psychology coach. Holds reflective sessions with the trader, stores user memories across sessions, asks questions calibrated to the trader's profile, and frames every interaction in the trader's own ICT vocabulary.

## Why it matters

Psychology work is the part of trading most likely to be skipped, because it's the part with the highest activation energy. Voice removes the activation energy. Persistent memory turns every session into context for the next one. This is the surface where Neurospect stops being a journal and starts being a coach.

## Dependencies

- [[concepts/roadmap/ideas/trader-psychology-profiler]] for personalisation that isn't generic.
- A persistent user-memory layer (separate from `coaching_events` — long-lived facts, not per-event reasoning).
- STT + TTS pipeline.

## Open questions

- Memory model: episodic (per-session summaries) vs. semantic (extracted facts) vs. both?
- Real-time conversation vs. async voice messages?
- Do we use a custom system prompt from the AI Coach pipeline or a separate "psychology coach" prompt?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/architecture/tradingview-connector]]
- [[concepts/ai-coach/system-prompt-template.md]]
- [[concepts/roadmap/ideas/trader-psychology-profiler]]
