# Decision: DEC-009 — Memory Extraction Trigger

## Context
Memories must be extracted from build/test outcomes, agent runs, and human reviews. The extraction can happen inline during the agent run (synchronous) or after the run completes (asynchronous). This affects latency, data freshness, and system complexity.

## Options
1. **Async post-build extraction** — A background job processes completed run logs, test results, and diffs after the pipeline stage or session completes. Memories are always based on known outcomes.
2. **Inline extraction with async promotion** — Extract candidate memories during the run (e.g., after each stage), but defer evaluation and promotion to a background job. Faster candidate creation, but candidates may lack outcome context.
3. **Event-driven extraction** — The event system (P0-events) emits events; a subscriber extracts memories from relevant event streams. Decoupled from pipeline execution.

## Recommendation
Option 1 (async post-build). The report emphasizes that memories should be based on outcome evidence — knowing whether a build succeeded or failed is critical for extraction quality. Inline extraction creates candidates without outcome context, leading to lower-quality memories. Option 3 is architecturally elegant but adds complexity; it can be adopted later once the event system matures.

## Research Source
Topic 05 — Context, Memory, Vector DB & Self-Improvement (Sections 3.3, 12.1)

## Affects
- Pipeline completion hooks
- Memory extraction pipeline design
- Event system integration (future)
- System resource usage (background job scheduling)

## Status
Proposed

## Decided by
(pending)
