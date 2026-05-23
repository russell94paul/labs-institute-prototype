---
tags: [roadmap, v3, transition]
created: 2026-05-15
updated: 2026-05-15
---

# Pre-Roadmap v3: Trader Workspace as Core Product Layer

## Strategic Insight

The trader account, journal, performance analytics, and improvement metrics should be an **explicit core product layer** (Trader Workspace / Trader OS), not features scattered across phases.

## Trader Workspace Feature Map

| Area | Features |
|---|---|
| **Trader Account** | Profile, broker connections, account type: sim/eval/funded/live |
| **Trading Journal** | Trade notes, screenshots, setup tags, emotions, mistakes, rule adherence |
| **Performance Analytics** | PnL, win rate, expectancy, drawdown, profit factor, average R/R, session stats |
| **Behavior Metrics** | Tilt score, revenge trading detection, overtrading, rule breaks, discipline score |
| **Strategy Analytics** | Best/worst setups, ICT event performance, time-of-day edge, instrument edge |
| **AI Trade Review** | Post-trade feedback, mistake detection, improvement suggestions |
| **Progress Tracking** | Weekly/monthly reports, goals, improvement plan, trader score history |
| **Leaderboard Eligibility** | Verified stats feeding NeuroScore and NeuroFund Elite eligibility |

## Revised Phase Order

```
trader account + verified trading data
→ journal + analytics
→ prop risk protection
→ ICT event tagging
→ backtesting
→ AI trade review
→ edge forensics
→ NeuroScore
→ NeuroFund Elite eligibility
→ advanced ML
```

The journal/analytics layer becomes the **data engine** for everything else.

## Key Metrics

| Category | Metrics |
|---|---|
| Performance | Net PnL, win rate, loss rate, avg win, avg loss, expectancy, profit factor, max drawdown, avg R/R, avg hold time |
| Session | Best/worst session, instrument, setup |
| Behavior | Tilt events, overtrading count, revenge trading flags, rule breach count, consistency score, discipline score |
