# Decision: DEC-010 — Evaluation Harness MVP Scope

## Context
The report recommends a full evaluation pipeline: evidence validation, contradiction checks, scope classification, leakage scans, replay tests, and human review. Building the complete harness before there are enough memories to evaluate is premature. We need to decide what evaluation capabilities ship first.

## Options
1. **Evidence + contradiction only** — Check that every candidate links to source evidence and search for conflicting memories. No replay tests, no automated scoring. Human review for anything flagged.
2. **Evidence + contradiction + automated scoring** — Add confidence, utility, freshness, and risk score computation. Still no replay tests, but automated gates can promote/quarantine based on scores.
3. **Full harness including replay** — Build the golden task suite and run memory vs. no-memory comparisons from the start. Most rigorous but highest build cost.
4. **No automated evaluation** — All promotion and quarantine is manual (human review only). Simplest but doesn't scale.

## Recommendation
Option 1 (evidence + contradiction only). This enforces the report's "no memory without evidence" rule and catches conflicts, while keeping the MVP simple. Add automated scoring (Option 2) once there are enough memories to calibrate thresholds. Replay testing (Option 3) should wait until the golden task suite is built from real historical tasks.

## Research Source
Topic 05 — Context, Memory, Vector DB & Self-Improvement (Sections 9, 10)

## Affects
- Memory promotion workflow
- Human review queue design
- Evaluation pipeline complexity
- Golden task suite planning (deferred)

## Status
Proposed

## Decided by
(pending)
