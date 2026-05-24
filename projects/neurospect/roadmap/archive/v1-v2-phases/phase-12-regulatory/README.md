---
phase: 12
name: "Regulatory & Compliance Framework"
status: not_started
track: "C (Business & Operations)"
assigned: []
started: null
completed: null
tickets_total: 0
tickets_done: 0
parallel_with: [2, 3]
gates: [3, 9]
created: 2026-05-10
updated: 2026-05-10
---

# Phase 12: Regulatory & Compliance Framework

Establish the legal and regulatory foundation before generating any trade signals, recommendations, or automated trading functionality.

## Why This Phase Exists

Both plans mention SEC/FINRA in passing but neither has an actual legal strategy. If you're generating trade signals — even in shadow mode — you may need RIA (Registered Investment Advisor) registration. Getting this wrong can shut down the product.

## Goals

1. **Regulatory classification analysis** — Determine whether NeuroSpect's coaching, signal generation, and automated trading features trigger SEC/FINRA registration requirements (RIA, broker-dealer, etc.)
2. **Disclaimer framework** — Build a comprehensive disclaimer system reviewed by legal counsel, covering: educational-only disclaimers, not-financial-advice language, risk warnings, performance disclaimers (no backtested-as-live misrepresentation)
3. **Compliance-by-design** — Embed regulatory guardrails into the product architecture so compliance is enforced technically, not just by policy
4. **State/jurisdiction analysis** — Determine which US states and international jurisdictions have additional requirements
5. **Data privacy compliance** — GDPR, CCPA, and financial data handling requirements for trade journal data

## Deliverables

| Deliverable | Description | Gate? |
|---|---|---|
| Regulatory classification memo | Legal counsel opinion on RIA/BD requirements for each product tier | Yes |
| Disclaimer framework | Template disclaimers for coaching, signals, backtesting, paper trading, live trading | Yes |
| Compliance architecture doc | Technical design: where disclaimers are shown, how signals are flagged, how live trading is gated | No |
| Privacy policy & ToS | GDPR/CCPA-compliant privacy policy and terms of service | **Yes — gates Phase 3 (Product MVP)** |
| State/jurisdiction matrix | Which jurisdictions NeuroSpect can operate in, and restrictions per tier | No |
| Compliance checklist per phase | What regulatory requirements must be met before each phase ships | No |
| RIA registration (if required) | File registration if legal counsel determines it's needed | **Yes — gates Phase 9 (NeuroTrader)** |

## Phased Compliance Requirements

| Phase | Compliance Needed |
|---|---|
| Phase 1-2 (Coaching) | Educational disclaimers, "not financial advice" language |
| Phase 3 (Product MVP) | Full ToS, Privacy Policy, cookie consent, data retention policy |
| Phase 5-6 (Beta/Launch) | Payment compliance (PCI via Stripe), refund policy |
| Phase 7 (EdgeLab) | Backtesting disclaimers ("past performance..."), anti-lookahead disclosure |
| Phase 8 (NeuroQuant) | Signal generation disclaimers, model performance transparency |
| Phase 9 (NeuroTrader) | Full regulatory analysis — RIA if required, broker-dealer analysis, risk disclosures, kill switch compliance |

## Exit Criteria

1. Regulatory classification memo delivered by legal counsel
2. Disclaimer framework covers all current and planned product tiers
3. Privacy policy and ToS reviewed by counsel and deployed
4. Compliance checklist created for each engineering phase
5. RIA determination made (register, exempt, or not applicable)

## Risks

- **Unintentional RIA status** — Coaching that's too specific could be classified as investment advice. Mitigation: legal review of coaching prompt templates; hard guardrails on specificity.
- **International jurisdiction complexity** — EU MiFID II, UK FCA, etc. may apply if serving international users. Mitigation: geo-restrict initially; expand jurisdictions incrementally.
- **Regulatory change** — SEC/FINRA rules for AI-generated financial content are evolving rapidly. Mitigation: build flexibility into compliance framework; schedule quarterly reviews.

## Dependencies

- **Blocks:** Phase 3 (ToS/Privacy), Phase 9 (RIA determination)
- **Parallel with:** Phases 2-3
- **Requires:** Legal counsel specializing in fintech/securities law (external)

## Deviations

_None yet. Captured in `deviations.md` as implementation progresses._
