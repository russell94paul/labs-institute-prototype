---
phase: 16
name: "Team Scaling & Org Design"
status: not_started
track: "C (Business & Operations)"
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
parallel_with: [6, 7, 8]
gates: []
created: 2026-05-10
updated: 2026-05-10
---

# Phase 16: Team Scaling & Org Design

Plan for growth beyond the founding 2-engineer team. The v2 plan is an 18-month, 2-engineer roadmap — but what happens when you need to hire?

## Why This Phase Exists

The current plan has no org design, no role definitions, and no hiring timeline. Phases 7-9 (EdgeLab, NeuroQuant, NeuroTrader) introduce significant complexity — ML engineering, quant research, DevOps, and potentially a dedicated frontend engineer. Hiring reactively is expensive and slow. This phase ensures you hire proactively and intentionally.

## Goals

1. **Role definitions** — Define the first 5 roles you'd hire for, with clear responsibilities and requirements
2. **Hiring triggers** — Identify specific product/business milestones that trigger each hire (not dates, but signals)
3. **Org design** — How the team structure evolves from 2 → 5 → 10 people
4. **Onboarding process** — How new engineers get productive in the monorepo (CLAUDE.md, wiki, roadmap, skills)
5. **Knowledge transfer plan** — Reduce bus factor; ensure no single person is a bottleneck for any critical system
6. **Advisory board / fractional roles** — Identify expertise gaps that don't need full-time hires (legal, compliance, quant research, marketing)

## Hiring Roadmap

| Role | Trigger | Phase | Priority |
|---|---|---|---|
| **Fractional legal counsel** | Phase 11-12 starts | 11-12 | P0 |
| **ML/AI Engineer** | Phase 7 (EdgeLab) starts, 2-person team bottlenecked on ML + product work | 7 | P1 |
| **Frontend/Product Engineer** | Phase 3 (Product MVP) scope exceeds 1 engineer's capacity | 3-6 | P1 |
| **DevOps / Infrastructure** | Phase 5-6 (Beta/Launch) — production reliability requirements exceed part-time capacity | 5-6 | P2 |
| **Quant Researcher** | Phase 8 (NeuroQuant) — hybrid model research needs domain expertise | 8 | P2 |
| **Community / Marketing** | Phase 13 (GTM) — user acquisition requires dedicated effort | 13 | P2 |
| **Customer Support** | Post-launch — user volume exceeds founder capacity | 6+ | P3 |

## Org Evolution

```
Phase 0-3 (Now):
  Paul (Backend/AI/Data) + Vlad (Frontend/Product/Infra)
  + Fractional legal counsel

Phase 4-6 (Beta → Launch):
  Paul + Vlad + Frontend/Product Engineer
  + Fractional legal + Fractional marketing

Phase 7-8 (EdgeLab → NeuroQuant):
  Paul + Vlad + ML Engineer + Frontend Engineer
  + DevOps (fractional → full-time)
  + Quant Researcher (fractional)

Phase 9+ (NeuroTrader → Scale):
  Engineering team: 5-7 engineers
  Operations: Community manager, support
  Advisory: Legal, compliance, quant
```

## Deliverables

| Deliverable | Description | Gate? |
|---|---|---|
| Role definition documents | Job descriptions for first 5 hires with responsibilities, requirements, and comp ranges | No |
| Hiring trigger matrix | Specific milestones that trigger each hire decision | No |
| Org chart evolution plan | Visual org design for 2 → 5 → 10 people | No |
| Onboarding checklist | Step-by-step for new engineer: repo setup, CLAUDE.md tour, wiki orientation, skill walkthrough | No |
| Knowledge transfer audit | Identify single-person dependencies; document mitigation plan | No |
| Advisory board candidates | List of 3-5 potential advisors (fintech legal, quant, marketing) with outreach plan | No |
| Compensation framework | Salary bands, equity allocation plan, advisor compensation | No |

## Exit Criteria

1. Role definitions written for first 3 hires
2. Hiring trigger matrix complete and reviewed
3. Onboarding checklist tested with at least 1 person
4. Knowledge transfer audit identifies and documents all single-person dependencies
5. At least 1 advisory relationship established (legal counsel)

## Dependencies

- **Parallel with:** Phases 6-8
- **Requires:** Revenue or funding to justify hires (Phase 6+)
- **Informs:** All future phase timelines (more people = faster execution)

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
