---
tags: [roadmap-idea, neurospect, compliance-sensitive, audio, ai]
aliases: [Squawk Box]
sources: []
created: 2026-04-25
updated: 2026-04-25
horizon: compliance-sensitive
status: backlog
---

# AI Live Audio Commentary / Squawk-Box

Live market commentary or coaching audio during sessions — narrating ICT context, calling out HOD/LOD candidates, flagging kill-zone entries, in-the-moment psychology nudges.

## Why it matters

Squawk boxes are a paid product in institutional trading; nothing equivalent exists for retail ICT traders. AI-generated commentary that respects ICT framing could be a flagship surface.

## Compliance / risk notes

- **No real-person voice cloning** without explicit, written rights from that person. Includes mentor figures (MrWitness/AXL) — even with their permission, the legal posture must be airtight before shipping.
- **No commentary derived from copyrighted YouTube content** without licensing.
- **Acceptable framings:** synthetic original voices, user-selected personas (clearly labelled as AI), licensed educational commentary, or commentary inspired by publicly available trading concepts where legally appropriate (general ICT terminology is publicly known; specific instructor delivery is not).
- Live financial commentary that names instruments at sub-second latency may itself trigger investment-advice rules in some jurisdictions — needs counsel review before any live shipping.

## Dependencies

- TTS pipeline + low-latency streaming infra.
- Live market context feed.
- **Legal review before any user-facing release.**

## Open questions

- Licensed-content path vs. fully-synthetic path — which is feasible first?
- How is "this is AI commentary, not advice" disclaimer surfaced loudly enough?

## See Also

- [[concepts/roadmap/README]]
- [[concepts/business-logic/ict-live-commentary]]
- [[concepts/roadmap/ideas/neurospect-voice]]
