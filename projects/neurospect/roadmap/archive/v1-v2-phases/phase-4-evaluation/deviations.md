---
phase: 4
name: "Evaluation, Reliability & Prompt Infrastructure"
created: 2026-05-09
updated: 2026-05-10
---

# Phase 4 Deviations

## Deviation: Expanded scope to include Prompt Versioning Module (4B)

- **Planned:** Evaluation & Reliability only — eval suite, load testing, security audit, instructor review, monitoring (weeks 22-24)
- **Actual:** Split into 4A (Evaluation & Reliability) + 4B (Prompt Versioning Module). 4B adds prompt registry, A/B testing, regression detection, per-strategy tuning, audit trail, rollback, multi-model routing.
- **Why:** Prompt versioning is evaluation infrastructure. EdgeLab (Phase 7) depends on prompt/model version registries. Building it in Phase 4 means it's ready before Phase 7, and the coaching product (Phase 5 beta) benefits from A/B testing and rollback before real users.
- **Impact on future phases:** Phase 7 (EdgeLab) can consume the prompt registry directly rather than building from scratch. Phase 7 scope for "NSLM prompt version registry" becomes an extension of the Phase 4 module, not a greenfield build.
- **Timeline impact:** Extended from 3 weeks (22-24) to 5 weeks (22-26)
- **Date:** 2026-05-10
- **Engineer:** Paul Russell
