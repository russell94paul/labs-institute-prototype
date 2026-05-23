---
name: ns-phase0
description: NeuroSpect Phase 0 — Marketing + Demo + Technical Validation
---

You are working on **NeuroSpect Phase 0** (Marketing + Demo + Technical Validation).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\roadmap\phases\phase-0-marketing-demo\README.md`
3. Read `C:\Users\PaulRussell\repos\neurospect\roadmap\phases\phase-0-marketing-demo\deviations.md`
4. Read `C:\Users\PaulRussell\repos\neurospect\neurospect-ui\index.html` — current marketing site shell
5. Read `C:\Users\PaulRussell\repos\neurospect\docs\neurospect_product_overview_user_guide.md` (first 200 lines — product context)

## Goal

Validate market interest, build the waitlist, and demonstrate the full NeuroSpect product vision through an interactive marketing site and demos — before writing production features. Phase 0B establishes CI/CD, error monitoring, and audits the existing data model to prepare for Phase 1's data foundation work.

## Sub-phases

| Sub-Phase | Scope | Status |
|---|---|---|
| **0A — Marketing & Demo** | Marketing site (`neurospect-ui/`), live simulator, ICT course, EdgeLab studio, product guide, design handoffs | Substantially complete |
| **0B — Technical Validation** | CI/CD pipeline, Sentry error tracking, data model audit for Phase 1, schema validation | Not started |

## Deliverables

### 0A (Marketing — largely done)
1. Marketing site with 6+ pages deployed to Cloudflare Pages
2. Live trading simulator (`/simulator`) — NEU-27
3. Interactive ICT Course (`/course`) — 5 modules, 18 lessons, 4 assessment types
4. EdgeLab Research Studio (`/research`) — 3 interactive engines
5. Product guide at `docs/neurospect_product_overview_user_guide.md`
6. Design handoff package in `design-handoff/`
7. App nav link from `app/` to `neurospect-ui/`

### 0B (Technical Validation — revised scope)
1. GitHub Actions CI/CD pipeline (lint + test on PR)
2. Sentry error tracking integrated into `api/`
3. Data model audit: review `api/app/models/trade.py` (100+ fields), `enums.py` (17 enums), `broker_credential.py` for Phase 1 readiness
4. Schema validation: document what fields need extending for BrokerAccount, account types, trade verification
5. Competitive teardown documented

## Key Constraints

- 0A: Marketing copy must avoid performance promises. Disclaimers on simulator page.
- 0B: Do NOT implement the RAG prototype in this phase — RAG is deferred to Phase 6.
- 0B: Do NOT implement billing or subscriptions yet.
- 0B: The data model audit is a document, not code changes. Changes happen in Phase 1.

## Acceptance Criteria

- [ ] Marketing site live with waitlist capturing signups
- [ ] CI/CD runs on every PR (lint + test)
- [ ] Sentry capturing errors in API
- [ ] Data model audit document exists listing Phase 1 schema changes needed
- [ ] All marketing pages functional in `neurospect-ui/`

## When done

Say: "Phase 0 complete. The marketing site is live and CI/CD is operational. This is a natural session boundary — start a new session with `/ns-phase1` for the Trading Data Foundation."
