---
name: ns-phase3
description: NeuroSpect Phase 3 — Prop Shield (Prop Risk + Tradovate Protection)
---

You are working on **NeuroSpect Phase 3** (Prop Shield). This is the **FIRST REVENUE** phase.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\neurospect\api\app\routers\tradovate.py` — existing Tradovate integration
4. Read `C:\Users\PaulRussell\repos\neurospect\api\app\services\tradovate.py` — Tradovate service
5. Read `C:\Users\PaulRussell\repos\neurospect\api\app\services\crypto.py` — credential encryption
6. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\broker_credential.py` — broker credentials
7. Read Phase 1 BrokerAccount model (from Phase 1 deliverables)
8. Read Phase 2 behavior metrics service (for tilt detection integration)

## Goal

Build the paid wedge that generates NeuroSpect's first revenue. Prop Shield monitors trading accounts against prop firm rules, tracks trailing drawdown, detects tilt behavior, and issues lockout warnings — protecting traders from blowing their funded accounts. This is the strongest near-term monetizable feature because prop traders have acute, daily pain around rule tracking.

## Deliverables

1. **PropRuleConfig model** — per-account rule configuration:
   - Daily loss limit (absolute $ or % of account)
   - Trailing drawdown limit (with high-water mark tracking)
   - Max contracts / position limits
   - Max daily trades
   - Forbidden trading hours
   - Consistency rule (max single-day profit as % of total)
2. **Rule engine service** — real-time calculation from trade/fill data:
   - Current daily P&L vs limit
   - Current trailing drawdown vs limit
   - Position size vs max contracts
   - Distance-to-breach for each rule (absolute and %)
3. **Lockout state machine** — warning → soft_lock → hard_lock → manual_reset
   - Soft lock: 80% of limit reached → alert, UI warning
   - Hard lock: limit reached → prominent UI banner, optional trading halt signal
   - Manual reset: user acknowledges and resets after review
4. **Tilt lockout integration** — from Phase 2 behavior metrics:
   - 3+ consecutive losses → tilt warning
   - Revenge trading detected → suggested cooldown
   - Configurable auto-cooldown period
5. **Risk dashboard UI**:
   - Rule status cards with distance-to-breach meters
   - Lockout history timeline
   - Daily P&L progress bar against limit
   - Trailing drawdown visualization
6. **Multi-account support** — different rules per account (sim vs eval vs funded)
7. **Alert system** — Discord webhook and/or email when approaching limits
8. **Prop firm presets** — pre-configured rule templates:
   - Apex Trader Funding (150K, 100K, 50K accounts)
   - TopStep
   - FTMO
   - Earn2Trade
   - MyFundedFutures
9. **Stripe billing integration** — Mentor ($29/mo) and Trader ($99/mo) tiers
10. **Tests** for rule engine, lockout state machine, and distance-to-breach calculations

## Key Constraints

- Lockouts are **advisory only**. NeuroSpect cannot prevent order execution.
- Required disclaimer: "Prop Shield monitors your trading data and alerts you to rule status, but cannot guarantee prevention of rule violations. Always verify with your prop firm's dashboard."
- Do not execute live trades or modify orders — read-only monitoring
- Do not implement NeuroFund or rewards yet
- Use feature flags for lockout functionality during rollout
- Lockouts must be explainable and auditable (log every state transition with timestamp and trigger)

## Acceptance Criteria

- [ ] User can configure prop rules per account (or select from presets)
- [ ] Rule engine calculates distance-to-breach from trade data in real-time
- [ ] Lockout state machine transitions correctly through warning → soft → hard → reset
- [ ] Risk dashboard shows all rule statuses with visual meters
- [ ] Tilt detection from Phase 2 integrates with soft lockout suggestions
- [ ] Alerts fire at configurable thresholds (default 80%)
- [ ] Prop firm presets load correct rules for Apex/TopStep/FTMO/E2T/MFF
- [ ] Stripe integration accepts Mentor and Trader subscriptions
- [ ] Tests cover daily loss, trailing drawdown, max position, and tilt lockout scenarios
- [ ] Advisory disclaimer is displayed on risk dashboard

## When done

Say: "Phase 3 complete — Prop Shield is live and billing is operational. This is the first revenue milestone. Run `/ns-phase4` in a new session for ICT Event Intelligence."
