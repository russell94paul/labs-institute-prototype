---
phase: 0
name: "Marketing + Demo"
status: in_progress
assigned: [paul]
started: 2026-05-10
completed: null
tickets_total: 6
tickets_done: 1
goal: "Validate market interest, build waitlist, demo full product vision through interactive marketing site and demos. Technical validation: CI/CD, Sentry, data model audit."
deliverables:
  - "Marketing site with 6+ pages deployed to Cloudflare Pages"
  - "Live trading simulator (/simulator)"
  - "Interactive ICT Course (5 modules, 18 lessons, 4 assessment types)"
  - "EdgeLab Research Studio (3 interactive engines)"
  - "CI/CD pipeline (lint + test on PR)"
  - "Sentry error tracking in API"
  - "Data model audit for Phase 1 readiness"
constraints:
  - "Marketing copy must avoid performance promises"
  - "Do NOT implement RAG prototype — deferred to Phase 6"
  - "Do NOT implement billing — that is Phase 3"
  - "Data model audit is a document, not code changes"
acceptance_criteria:
  - "Marketing site live with waitlist capturing signups"
  - "CI/CD runs on every PR"
  - "Sentry capturing errors in API"
  - "Data model audit document exists"
  - "All marketing pages functional in neurospect-ui/"
created: 2026-05-09
updated: 2026-05-23
---

# Phase 0: Marketing + Demo

Validate market interest, build waitlist, demo product vision. Two sub-phases: 0A (marketing site, demos, course, EdgeLab studio) and 0B (CI/CD, Sentry, data model audit).

0A is substantially complete. 0B has not started.

See `/ns-phase0` for full implementation guide.

## Deviations

Captured in `deviations.md` as implementation progresses.
