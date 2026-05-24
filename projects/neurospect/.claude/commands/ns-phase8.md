---
name: ns-phase8
description: NeuroSpect Phase 8 — NeuroScore + Verified Leaderboard
---

You are working on **NeuroSpect Phase 8** (NeuroScore + Verified Leaderboard).

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\CLAUDE.md`
3. Read Phase 1 BrokerAccount model (account types, verification status)
4. Read Phase 2 behavior metrics service (tilt, discipline, consistency scores)
5. Read Phase 3 Prop Shield rule engine (rule adherence tracking)
6. Read Phase 2 analytics service — `api/app/services/analytics.py` (performance data)
7. Read `C:\Users\PaulRussell\repos\conductor\projects\neurospect\api\app\models\user.py` — user model

## Goal

Build a verified, risk-adjusted trader ranking system. NeuroScore considers not just profit but drawdown discipline, rule adherence, consistency, sample size, and tilt control. This is the prerequisite for NeuroFund Elite eligibility (Phase 9) and creates a competitive/aspirational dynamic that drives engagement and upgrades.

## Deliverables

1. **NeuroScore calculation engine** (`api/app/services/neuroscore.py`):
   - **Performance component** (40% weight): risk-adjusted returns (Sharpe-like), not raw PnL
   - **Drawdown discipline** (20%): max drawdown as % of peak, drawdown duration
   - **Rule adherence** (15%): prop rule breach rate (from Phase 3), ICT methodology compliance
   - **Consistency** (15%): variance of daily returns, streak analysis, no single-day > X% of total
   - **Tilt control** (10%): tilt events per period (from Phase 2), cooldown compliance
   - Weights are configurable but these are the defaults
   - Score range: 0-100
   - Minimum requirements: 50+ verified trades, 30+ trading days
2. **Verification requirements**:
   - Only broker-verified trades (import_source = tradovate_sync) count toward NeuroScore
   - Self-reported / manual trades do not count
   - Screenshot-based verification explicitly NOT accepted
3. **Account type labeling**:
   - Clear labels: Sim, Evaluation, Funded, Live
   - Leaderboard shows account type prominently
   - Separate leaderboard views per account type
4. **NeuroScore history model** — track score over time (weekly snapshots)
5. **Leaderboard API** (`api/app/routers/leaderboard.py`):
   - `GET /api/leaderboard` — top traders, filterable by account type, instrument, time period
   - `GET /api/leaderboard/me` — current user's rank and score breakdown
   - `GET /api/leaderboard/history/{user_id}` — NeuroScore over time
6. **Leaderboard UI** (`app/src/pages/leaderboard.tsx`):
   - Sortable table with NeuroScore, account type, trade count, consistency badge
   - Score breakdown tooltip (hover to see component scores)
   - "My Profile" card with percentile ranking
   - Account type filter tabs
   - Time period selector (30d / 90d / all-time)
7. **Peer comparison** — percentile ranking within same account-type cohort
8. **Tests** for score calculation, edge cases, and minimum requirements

## Scoring Detail

| Component | Weight | What It Measures | Source |
|---|---|---|---|
| Performance | 40% | Risk-adjusted returns (not raw PnL) | Trade records |
| Drawdown Discipline | 20% | Max DD control, DD duration | Trade records |
| Rule Adherence | 15% | Prop rule breach rate, methodology compliance | Phase 3 Prop Shield |
| Consistency | 15% | Return variance, no outlier-driven profits | Trade records |
| Tilt Control | 10% | Tilt events, cooldown compliance | Phase 2 behavior metrics |

## Key Constraints

- Do NOT rank users by profit alone — the whole point of NeuroScore is holistic assessment
- No screenshot-based verification — broker API verification only
- Account types must be clearly labeled (no mixing sim with funded)
- No implication that high NeuroScore equals future profitability
- Leaderboard visible on free tier (drives conversions) but score details require Quant tier
- Minimum 50 verified trades to appear on leaderboard
- Do NOT implement rewards or NeuroFund yet (Phase 9)

## Acceptance Criteria

- [ ] NeuroScore calculated from 5 weighted components
- [ ] Only broker-verified trades count toward score
- [ ] Minimum requirements enforced (50 trades, 30 days)
- [ ] Account types clearly labeled on leaderboard
- [ ] Leaderboard filterable by account type, instrument, time period
- [ ] Score history tracked over time (weekly snapshots)
- [ ] Percentile ranking within account-type cohort
- [ ] Tests cover scoring edge cases: zero trades, single trade, all wins, all losses, tilt-heavy, consistent-but-unprofitable

## When done

Say: "Phase 8 complete — NeuroScore and verified leaderboard are live. Run `/ns-phase9` in a new session for NeuroFund Elite Rewards MVP."
