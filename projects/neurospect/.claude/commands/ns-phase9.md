---
name: ns-phase9
description: NeuroSpect Phase 9 — NeuroFund Elite Rewards MVP (Compliance-Safe)
---

You are working on **NeuroSpect Phase 9** (NeuroFund Elite Rewards MVP). This is a **compliance-critical** phase.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read Phase 8 NeuroScore service — `api/app/services/neuroscore.py`
4. Read Phase 8 leaderboard — `api/app/routers/leaderboard.py`
5. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\user.py` — user model
6. Read `C:\Users\PaulRussell\repos\neurospect\roadmap\roadmap-change-integration\roadmap-changes-v2.md` — NeuroFund compliance language reference

## Goal

Create the NeuroFund Elite rewards MVP as a premium opt-in eligibility and rewards program. Company-sponsored, funded from NeuroSpect revenue. This is NOT a fund, NOT pooled user capital, NOT an investment vehicle.

## Compliance Language Reference

### APPROVED Language (use these exact patterns)
- "Company-sponsored trader allocation and rewards program funded from NeuroSpect revenue"
- "Premium members may become eligible for company-sponsored rewards, challenge reimbursements, grants, and future internal allocation consideration"
- "NeuroSpect may select qualified traders for challenge sponsorships"
- "May allocate", "may be eligible for", "consideration"

### FORBIDDEN Language (never use, flag if found anywhere)
- "Pooled user capital" / "subscriber money invested" / "investment pool"
- "Fund returns" / "members receive returns"
- "Your subscription is invested"
- "Community trading pool"
- "Guaranteed rewards" / "guaranteed returns"
- "Copy top traders" (without separate legal review)
- "Subscribers fund traders"

## Deliverables

1. **Elite eligibility flag** on user model — `is_elite_eligible: bool`, `elite_status: enum`
2. **Activation threshold** — program does not activate until 50 verified Elite-eligible members
3. **Elite eligibility criteria**:
   - Active Quant tier ($349/mo) subscription
   - NeuroScore >= 75 (sustained for 30+ days)
   - 90+ verified trades
   - 60+ trading days
   - Zero hard lockout breaches in last 90 days
   - Account type: funded or live (not sim or eval)
4. **Reward eligibility state machine**:
   - `not_eligible` — doesn't meet criteria
   - `tracking` — meets criteria, building track record
   - `qualified` — sustained qualification for 60+ days
   - `under_review` — admin reviewing for selection
   - `selected` — chosen for reward/sponsorship
   - `not_selected` — reviewed but not selected this cycle
5. **Monthly leaderboard seasons** — snapshot NeuroScore at end of each month, reset season rankings
6. **Challenge sponsorship eligibility** — NeuroSpect may sponsor eval challenge fees for selected traders
7. **Admin review workflow** (`api/app/routers/admin.py`):
   - View all qualified traders with NeuroScore breakdown
   - Add review notes per trader
   - Transition eligibility state (qualified → under_review → selected/not_selected)
   - Audit trail for every state transition
8. **Elite dashboard** (`app/src/pages/elite.tsx`):
   - Eligibility status and progress
   - Criteria checklist (which criteria met, which pending)
   - NeuroScore trend chart
   - Season ranking
   - Approved marketing copy (see compliance language above)
9. **Public marketing copy** — all user-facing text uses APPROVED language only
10. **Tests** for eligibility calculation, state machine transitions, and activation threshold

## Key Constraints

- **No pooled user capital** — rewards are company-funded from revenue
- **No return promises** — use "may be eligible for", never "will receive"
- **No managed account functionality** — NeuroSpect does not trade on behalf of users
- **No automatic payout system** — all selections require admin review
- **Admin review required** — no algorithmic auto-selection for rewards
- Add `COMPLIANCE_TODO` comment tags in code wherever reward/eligibility language appears
- Legal counsel review before any marketing copy goes live
- 50-member activation threshold before program launches
- Feature flag the entire NeuroFund Elite system for gradual rollout

## Acceptance Criteria

- [ ] Users can be flagged as Elite eligible based on criteria
- [ ] Activation threshold (50 members) is enforced — program inactive until threshold met
- [ ] Eligibility state machine transitions correctly through all 6 states
- [ ] Admin can review, annotate, and transition trader status
- [ ] Audit trail records every state transition with timestamp, admin, and reason
- [ ] All user-facing copy uses APPROVED language only
- [ ] No FORBIDDEN language exists anywhere in codebase (grep verify)
- [ ] Elite dashboard shows eligibility progress and criteria checklist
- [ ] Monthly seasons snapshot correctly
- [ ] Tests cover eligibility edge cases, state transitions, and threshold logic
- [ ] `COMPLIANCE_TODO` tags present wherever reward language is used

## When done

Say: "Phase 9 complete — NeuroFund Elite rewards MVP is live with compliance-safe language. Run `/ns-phase10` in a new session for the Allocation Watchlist pipeline."
