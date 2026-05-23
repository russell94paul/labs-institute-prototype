---
tags: [distributed-workflow, active, neurospect, kickoff]
aliases: [Neurospect Kickoff Tracker]
sources: []
created: 2026-04-18
updated: 2026-04-18
---

# Neurospect Kickoff — Workstream Tracker

First session of the Neurospect project under the distributed-workflow pattern. Three jobs: migrate the project entity page out of the ALDC wiki into this one, pick a transcript ingestion path for the mentor's Google Drive videos, and scaffold the ICT course KB.

> **Cross-wiki note:** This tracker is in the Neurospect wiki. The pattern docs it follows live in the ALDC wiki and are referenced **by absolute path**, never by wikilink. See [[../../../CLAUDE]] § *Isolation Rule*.

## Goal

By end of the kickoff session(s), this wiki should have:

1. **Migrated project entity page** — `entities/projects/neurospect.md` contains the content currently at `C:\Users\PaulRussell\repos\wiki\entities\projects\neurospect.md`. The ALDC-side file is removed and its `index.md` entry is removed (confirm with Paul before deleting).
2. **A chosen transcript ingestion path** — written into `concepts/architecture/transcript-pipeline.md`. Decision between (a) manual download from Google Drive + local Whisper transcription, (b) Google Drive API + auto-detected captions / Whisper fallback, (c) something else. Trade-offs documented; chosen path has a 1-page execution plan.
3. **ICT course KB scaffold** — `concepts/business-logic/ict-*.md` skeleton pages exist for the top-level concepts the mentor's curriculum is organised around (best-guess from Paul's existing notes; structure can shift as transcripts are ingested). Each file has frontmatter and a TOC stub — no body yet.
4. **Updated `index.md` and `log.md`** in this wiki reflecting the above.

"Done" = all four bullets complete and a checkpoint block is appended to `daily/2026-04-18.md`.

## Lane

Wiki: Neurospect (`C:\Users\PaulRussell\repos\neurospect-wiki\`)

Owned paths (write here):

- `entities/projects/neurospect.md` (new — migration target)
- `concepts/business-logic/ict-*.md` (new skeletons)
- `concepts/architecture/transcript-pipeline.md` (new — pipeline decision doc)
- `sources/neurospect/` (raw material when transcripts arrive in a later session)
- `index.md`, `log.md`, `daily/2026-04-18.md` (this wiki's shared files only)

**Forbidden:** any write to the ALDC wiki **except** the one-time deletion of `C:\Users\PaulRussell\repos\wiki\entities\projects\neurospect.md` and the removal of its `index.md` entry, performed only after the migration is complete and Paul has confirmed.

## Required Context

Read at boot:

- `../../../CLAUDE.md` — this wiki's schema, Isolation Rule, conventions.
- This tracker (you are here).

Cross-wiki references (read by **absolute path**, never wikilink):

- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md`
- `C:\Users\PaulRussell\repos\wiki\entities\projects\neurospect.md` — the page being migrated. Read fully before migrating.

## Plan-Mode Rule

- **Enter plan mode** for the kickoff session and for any later session that introduces a new component (transcript pipeline implementation, course-KB schema redesign, live-commentary engine, app code repo).
- **Skip plan mode** for routine ingest sessions once the transcript pipeline exists and is approved.

## Session Log

_Initial bootstrap — no work executed in this session._

### 2026-04-18 — bootstrap

- did: created this tracker; lane set to Neurospect-wiki only with the documented one-time exception for the migration cleanup.
- decided: kickoff is plan-mode-first; the three Goal bullets are sequenced as (1) migration → (2) pipeline decision → (3) course-KB scaffold, but plan mode may reorder if a clearer dependency emerges.
- next: open a fresh Claude session pointed at the Neurospect wiki using the boot prompt below; enter plan mode and propose the structure for the migrated `entities/projects/neurospect.md` and the pipeline decision doc.

### 2026-04-22 — stream/YouTube ingest (KB updated)

- did: ran stream + YouTube ingest session. Read all 13 source files (11 streams, 2 YouTube weekly reviews). Created ict-live-commentary.md (new page). Updated ict-narratives, ict-liquidity, ict-entry-models, ict-smt with live application context. Updated index.md, log.md, daily/2026-04-22.md.
- decided: kickoff workstream is fully complete. KB now has both structured class content (Vols 1–4) and live application context (stream + YouTube). Three parallel workstreams are active.
- next: begin course-and-kb workstream (see [[course-and-kb]] tracker).

### 2026-04-22 — app planning

- did: transcribed 11 stream tape-reading videos and 2 YouTube videos (Whisper medium, CPU). Fixed YouTube path bug in transcribe_batch.py. Spawned three new workstream trackers: course-and-kb.md, ai-coach.md, journal-analytics.md. Updated kickoff Next Phase section and index.md.
- decided: kickoff workstream is complete. Three parallel workstreams now active — sequence is course-and-kb first, then ai-coach Phase 1-2, then build backend shared between ai-coach and journal-analytics.
- next: once YouTube transcripts finish, run stream/YouTube ingest session (boot prompt below), then begin course-and-kb workstream.

### 2026-04-20 — transcript ingest (Vols 1–4)

- did: installed openai-whisper + ffmpeg; ran Whisper medium (CPU overnight) on 12 videos; extracted 8 PDF notes; saved 20 source files to sources/neurospect/. Fully populated all 5 ICT skeleton pages and created ict-deviations.md, ict-order-flow.md, entities/people/mrwitness-axl.md. Updated index.md and log.md.
- decided: Vol 1–4 ingest complete for available material; 5 videos confirmed missing from Drive (Vol 1 Cls 4, Vol 2 Cls 2, Vol 3 Cls 1+3, Vol 4 Cls 3) — content gaps noted in daily/2026-04-20.md.
- next: transcribe stream/YouTube videos, then ingest them.

### 2026-04-18 — kickoff execution

- did: migrated `entities/projects/neurospect.md` from ALDC wiki (removed ALDC wikilinks, added ICT concept cross-refs); created `concepts/architecture/transcript-pipeline.md`; scaffolded 5 ICT skeleton pages (`ict-market-structure`, `ict-liquidity`, `ict-narratives`, `ict-entry-models`, `ict-smt`); updated `index.md` and `log.md`.
- decided: blocker 1 resolved — default ICT scope (top-level only); blocker 2 resolved — manual + Whisper chosen (no GCP setup exists); upgrade trigger to Drive API set at ~20 videos.
- next: confirm with Paul before deleting `C:\Users\PaulRussell\repos\wiki\entities\projects\neurospect.md` and its `index.md` entry. After that, begin transcript ingest when first video is ready — follow `concepts/architecture/transcript-pipeline.md` runbook.

## Decisions Log

- 2026-04-18 — Neurospect lives in its own sub-wiki at `C:\Users\PaulRussell\repos\neurospect-wiki\`, fully decoupled from the ALDC wiki per Paul's preference. Only allowed cross-wiki coupling is one-way: ALDC research → Neurospect (currently the distributed-workflow pattern docs by absolute path).
- 2026-04-18 — Pattern docs are not duplicated into this wiki. The kickoff session must follow them by absolute-path reference.
- 2026-04-18 — Transcript ingestion path: manual download + local Whisper (large-v3 model). No GCP/OAuth setup exists at kickoff. Upgrade trigger to Drive API automation: corpus > 20 videos. See `concepts/architecture/transcript-pipeline.md`.
- 2026-04-18 — ICT skeleton scope: 5 top-level pages only (market-structure, liquidity, narratives, entry-models, smt). Sub-concepts deferred to transcript-driven creation.

## Pending Wiki Updates

_All updates from this session applied directly (no parallel writers in this wiki)._

### Applied 2026-04-18

- `index.md`: added `[[entities/projects/neurospect]]` under Entities → Projects.
- `index.md`: added 5 ICT concept entries under Concepts → Business Logic.
- `index.md`: added `[[concepts/architecture/transcript-pipeline]]` under Concepts → Architecture.
- `log.md`: appended 3 rows (migrate, create, scaffold).

## Blockers / Open Questions

- 2026-04-18 — Open question for Paul: any of the existing ICT concepts you'd like the kickoff session to *not* skeleton today (i.e., reserve for a later, more deliberate pass)? Default: scaffold the obvious top-level concepts only (e.g. day-of-week framing, draws on liquidity, narratives, market structure) and leave nuanced sub-concepts for transcript-driven creation.
- 2026-04-18 — Open question: Drive API auth — do you have a Google Cloud project / OAuth client already set up, or is this a from-scratch task? Affects the trade-off in the pipeline decision.

## Cross-Lane Requests

_None._

## Boot Prompts

### A — Stream / YouTube Ingest (run once YouTube transcription completes)

**Recommended model:** Sonnet 4.6 (default). No plan mode needed.

````
You are running the stream and YouTube ingest session for the Neurospect wiki.
All transcripts are already saved in `sources/neurospect/` — your job is to read
and ingest them into the KB.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md` (Isolation Rule).
2. Read `processes/distributed-workflow/active/kickoff.md` (this tracker).
3. Read `index.md` to orient yourself.

Files to ingest (all in sources/neurospect/):
- 11 stream files: 2026-04-20-stream-*.md  (source_type: stream_transcript)
- 2 YouTube files: 2026-04-20-youtube-*.md (source_type: youtube_transcript)

What to do:
- Read each file thoroughly.
- Extract ICT concepts, real-world examples, and trade setups that appear.
- Update the relevant `concepts/business-logic/ict-*.md` pages with any new
  examples, nuances, or live application context not already captured.
- Stream content = live pre-market commentary + live trade setups. It is lower-level
  than structured classes — use it to add worked examples and live framing, not new
  concept definitions.
- Create `concepts/business-logic/ict-live-commentary.md` if stream content warrants
  a dedicated page (e.g. pre-market narrative framework, live news framing, HOD/LOD
  calling process).
- Update `index.md` and append to `log.md`.

At session end, append a `## Distributed Workflow Checkpoint` to `daily/YYYY-MM-DD.md`
and update this tracker's Session Log.
````

### B — Future Class Ingest (use when missing videos become available)

**Recommended model:** Sonnet 4.6 (default). No plan mode needed.

````
You are ingesting newly available class videos for the Neurospect wiki.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`.
2. Read `processes/distributed-workflow/active/kickoff.md`.
3. Read `index.md` and `log.md` to see what's already been ingested.

Missing classes (confirm which are now available):
- Vol 1 Class 4 — Reversal (PDF notes exist; video missing)
- Vol 2 Class 2 — Session Power of Three (PDF notes exist; video missing)
- Vol 3 Class 1 — Unknown topic
- Vol 3 Class 3 — Unknown topic
- Vol 4 Class 3 — Likely "Six Sisters" (referenced in Vol 4 Class 2)

Transcription: run `transcribe_batch.py` in the downloads folder — it skips existing
files and picks up any new ones automatically.

Ingest: read the new transcript(s), extract concepts, update the relevant
`concepts/business-logic/ict-*.md` pages and/or `concepts/entry-models/` pages
if new strategies are introduced.
````

## Next Phase Trackers

Kickoff is complete. Three active workstreams spawned:

1. **[[course-and-kb]]** — ICT course construction + entry models library (do first)
2. **[[ai-coach]]** — AI trading coach / Claude + TradingView integration (depends on course-and-kb)
3. **[[journal-analytics]]** — Trade journal + analytics module (parallel to ai-coach, shares backend)

**Recommended sequence:** course-and-kb → ai-coach Phase 1-2 (strategy JSON + system prompt) → journal-analytics Phase 1 (schema) → build both Phase 2+ together on a shared backend.

## See Also

- `../../../CLAUDE.md` (Isolation Rule)
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md` (the pattern this tracker follows)
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md` (lifecycle and checkpoint procedure)
