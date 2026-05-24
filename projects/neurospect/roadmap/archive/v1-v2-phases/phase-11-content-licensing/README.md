---
phase: 11
name: "Content Licensing & IP Strategy"
status: not_started
track: "C (Business & Operations)"
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
parallel_with: [0, 1]
gates: [1]
created: 2026-05-10
updated: 2026-05-10
---

# Phase 11: Content Licensing & IP Strategy

Secure legal rights to instructor content before building any RAG or fine-tuning pipeline. This is existential risk — without content rights, the product cannot exist.

## Why This Phase Exists

Neither the v1 nor v2 plan had a concrete strategy for securing legal rights to instructor content. You can't build a RAG system on content you don't have permission to use. This phase gates Phase 1 (Knowledge Base & RAG MVP) — content ingestion cannot begin without executed agreements.

## Goals

1. **Content audit** — Inventory all ICT content sources (YouTube transcripts, mentorship recordings, course materials, community posts) and classify by IP ownership and licensing status
2. **Legal framework** — Establish content licensing agreement templates covering: exclusive vs non-exclusive rights, derivative work rights (RAG, fine-tuning, embedding), revenue sharing, termination clauses, content update obligations
3. **First instructor agreement** — Execute a signed content licensing agreement with the first instructor (ICT or alternative)
4. **IP protection strategy** — Define how NeuroSpect protects its own IP (fine-tuned models, feature engineering, EdgeLab research) and how instructor IP is segregated
5. **Content pipeline compliance** — Establish automated checks that content entering the RAG pipeline has valid licensing metadata

## Deliverables

| Deliverable | Description | Gate? |
|---|---|---|
| Content inventory spreadsheet | All known content sources, ownership, current licensing status | No |
| Content licensing agreement template | Reviewed by legal counsel, covers RAG + fine-tuning + embedding rights | Yes |
| Signed first instructor agreement | Executed agreement with first content provider | **Yes — gates Phase 1** |
| IP segregation architecture | Technical design for keeping instructor content isolated per agreement terms | No |
| Licensing metadata schema | Frontmatter/database fields tracking license status per content chunk | No |
| Fair use / public content analysis | Legal opinion on which publicly available content (YouTube, free courses) can be used under fair use or ToS | No |

## Exit Criteria

1. At least one signed content licensing agreement executed
2. Legal counsel has reviewed agreement template
3. Content inventory covers 80%+ of known ICT content sources
4. Licensing metadata schema defined and documented
5. IP segregation requirements documented for Phase 1 ingestion pipeline

## Risks

- **Instructor declines** — First instructor may not agree to terms. Mitigation: have backup instructor candidates; design platform to be methodology-agnostic from day 1.
- **Fair use gray area** — YouTube transcripts and public content may have unclear IP status. Mitigation: get legal opinion; err on the side of explicit licensing.
- **Revenue share disputes** — Instructor may want disproportionate revenue share. Mitigation: establish clear value-add metrics; benchmark against industry norms (20-30% platform share).
- **Content update obligations** — Agreement may require incorporating instructor updates. Mitigation: define update cadence and scope in agreement.

## Dependencies

- **Blocks:** Phase 1 (RAG MVP cannot ingest content without licensing)
- **Parallel with:** Phase 0 (Research & Validation)
- **Requires:** Legal counsel engagement (external)

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
