---
name: ns-phase10
description: NeuroSpect Phase 10 — Allocation Watchlist Pipeline
---

You are working on **NeuroSpect Phase 10** (Allocation Watchlist Pipeline).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\CLAUDE.md`
3. Read Phase 8 NeuroScore service — `api/app/services/neuroscore.py`
4. Read Phase 9 Elite eligibility models and admin workflow
5. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\roadmap\roadmap-change-integration\roadmap-changes-v2.md` — compliance language reference

## Goal

Create the company-sponsored allocation watchlist — an internal workflow for identifying traders who may be considered for challenge sponsorships, grants, or company-sponsored account allocation. This extends Phase 9's eligibility system with deeper qualification criteria, trader model cards, and admin review tools.

## Deliverables

1. **Allocation watchlist model** (`api/app/models/allocation_watchlist.py`):
   - trader_id, entry_date, status, qualification_criteria_snapshot JSONB
   - Status enum: `tracking` → `pre_qualified` → `under_review` → `watchlist` → `selected` → `not_selected` → `removed`
2. **Qualification criteria** (stricter than Phase 9 eligibility):
   - 60-90 days continuous verified trading history
   - Minimum 100 verified trades
   - NeuroScore >= 80 sustained for 60+ days
   - Zero hard lockout breaches in qualification period
   - Max drawdown < 8% of peak equity
   - Consistency score in top 20th percentile
   - Documented trading strategy (user must submit strategy description)
   - Account type: funded or live only
3. **Trader model card** (`api/app/models/trader_model_card.py`):
   - Risk profile summary (max DD, avg DD, worst week)
   - Strategy summary (primary setups, instruments, sessions)
   - Consistency evidence (equity curve, monthly returns, streak analysis)
   - NeuroScore history (last 6 months)
   - Behavior metrics summary (tilt events, discipline trend)
   - Edge Forensics highlights (identified edges, improvement trajectory)
4. **KYC/identity verification placeholder**:
   - Model fields for KYC status (not_started, pending, verified, rejected)
   - Integration point stub for future KYC provider
   - Do NOT implement actual KYC in this phase — just the model and status tracking
5. **Admin review workflow** (extend Phase 9 admin tools):
   - Watchlist view with qualification criteria breakdown
   - Side-by-side trader comparison
   - Review notes and decision tracking
   - Allocation readiness checklist
   - Status transition with reason and audit trail
6. **Allocation Watchlist API** (`api/app/routers/allocation.py`):
   - `GET /api/allocation/watchlist` — admin-only: list watchlist traders
   - `GET /api/allocation/watchlist/{id}` — trader model card + qualification detail
   - `PATCH /api/allocation/watchlist/{id}/status` — admin transition status
   - `GET /api/allocation/criteria` — public: show qualification requirements
7. **Trader-facing view** (`app/src/pages/allocation.tsx`):
   - Qualification progress (which criteria met, which pending)
   - Strategy submission form
   - Current watchlist status (if applicable)
   - Approved marketing copy only
8. **Tests** for qualification logic, status transitions, and model card generation

## Key Constraints

- Same compliance rules as Phase 9 — all APPROVED/FORBIDDEN language applies
- **No promise of allocation** — "may be considered for", "allocation consideration"
- **No managed account functionality** — NeuroSpect does not trade user funds
- **No letting users invest in traders** — this is purely internal review
- **No guaranteed selection** — admin discretion required
- KYC is a placeholder — actual identity verification is a future legal/compliance deliverable
- Admin-only watchlist management — traders can see their own status but cannot modify it
- "NeuroSpect may select qualified traders for challenge sponsorships, grants, or company-sponsored account allocation consideration"

## Acceptance Criteria

- [ ] Qualification criteria automatically evaluated against trader data
- [ ] Trader model card generated with risk profile, strategy summary, consistency evidence
- [ ] Watchlist status transitions work with audit trail
- [ ] Admin can compare traders side-by-side
- [ ] Strategy submission form captures trader's documented strategy
- [ ] KYC status fields exist (placeholder, not implemented)
- [ ] Trader-facing view shows qualification progress
- [ ] All user-facing copy uses APPROVED language only
- [ ] Tests cover qualification edge cases and status transitions

## When done

Say: "Phase 10 complete — Allocation Watchlist pipeline is operational. Run `/ns-phase11` in a new session for Advanced ML Research (plan-mode recommended)."
