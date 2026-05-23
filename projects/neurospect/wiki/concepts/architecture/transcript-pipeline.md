---
tags: [concept, architecture, neurospect, transcription, whisper]
aliases: [Transcript Pipeline, Ingestion Pipeline]
sources: []
created: 2026-04-18
updated: 2026-04-18
---

# Transcript Pipeline

Describes how mentor video content is converted into structured source material in `sources/neurospect/` for ingest into the knowledge base. Decision made at kickoff: manual download + local Whisper.

## Decision: Manual Download + Local Whisper

**Chosen path:** Download videos from Google Drive manually, run OpenAI Whisper locally, save transcript as a markdown file in `sources/neurospect/`, then run the standard ingest operation.

## Rationale

- No Google Cloud project or OAuth client exists at kickoff — Drive API auth is a multi-hour from-scratch task
- Corpus is small at kickoff; per-video manual effort is acceptable
- Whisper (medium or large-v3) produces high-quality transcripts sufficient for knowledge extraction
- Zero ongoing API cost; no rate limits; transcript stays local
- Upgrade path to Drive API is clear and can be triggered when corpus justifies it

## Options Considered

### Option A — Manual Download + Local Whisper (CHOSEN)

**How:** Download each video file from Google Drive via the browser. Run `whisper <file> --model large-v3 --output_format md` (or `medium` if GPU VRAM is limited). Save output to `sources/neurospect/<YYYY-MM-DD>-<slug>.md`.

**Pros:** ~30-min setup, no API keys, no rate limits, full local control.

**Cons:** Manual per-video step; no automation at scale.

### Option B — Google Drive API + Whisper Fallback

**How:** Authenticate via OAuth 2.0 (Google Cloud project required), list files in the mentor's shared Drive folder, download programmatically, check for existing captions/subtitles first, fall back to Whisper if none found.

**Pros:** Fully automated; detects new videos without manual intervention; can batch-process.

**Cons:** Requires GCP project + OAuth client setup from scratch (~3-5 hours); adds credential management complexity; ongoing maintenance if Drive API changes.

**When to revisit:** Once the corpus exceeds ~20 videos or new videos appear frequently enough that manual tracking becomes a burden.

### Option C — Platform-Native Captions (YouTube / Teachable / etc.)

**How:** If the mentor distributes via YouTube or a course platform, use `yt-dlp --write-subs` or the platform's own export to pull existing captions.

**Pros:** Zero transcription cost if captions already exist.

**Cons:** Quality varies (auto-captions miss ICT jargon); only applicable if distribution channel changes.

**When to use:** Check for existing captions before running Whisper on any video — if the platform exposes good subs, prefer them.

## Execution Runbook

1. Download the video file from Google Drive to a local temp directory.
2. Run Whisper:
   ```
   whisper <video-file> --model large-v3 --output_format md --output_dir sources/neurospect/
   ```
   Use `medium` if VRAM < 8 GB. Rename output to `YYYY-MM-DD-<slug>.md`.
3. Open the transcript and add a frontmatter block:
   ```yaml
   ---
   tags: [source, transcript, neurospect]
   aliases: []
   mentor: <mentor name>
   video_title: <title>
   video_date: YYYY-MM-DD
   source_url: <Google Drive link or N/A>
   created: YYYY-MM-DD
   ---
   ```
4. Save to `sources/neurospect/YYYY-MM-DD-<slug>.md`. **Do not edit the transcript body** — sources are immutable.
5. Run ingest: read the file, extract entities/concepts/processes, update or create wiki pages, update `index.md` and `log.md`.

## Upgrade Trigger: When to Switch to Drive API

Switch to Option B when **any** of the following is true:
- Corpus exceeds 20 videos
- New videos arrive faster than one manual download per week
- Batch re-transcription of the full corpus is needed

When triggering: create a `processes/operations/drive-api-setup.md` runbook and update this page's decision section.

## See Also

- [[entities/projects/neurospect]] — project overview and architecture
- [[concepts/business-logic/ict-market-structure]] — primary target of ingest operations
