# NeuroSpect Live Trading Simulator — Design Spec

## Overview

A real-time trading simulation that runs all 4 trader tiers simultaneously against the same market events. As price action unfolds, each tier makes decisions (enter, skip, exit) with visible reasoning. Wins and losses are logged with full analysis — mistakes identified, concepts to review, improvement actions.

This is the **flagship visualization** of the entire marketing site. It demonstrates every NeuroSpect capability in one interactive experience.

## Why This Matters

- Shows the product in action, not just describes it
- Every trader recognizes themselves in Tier 1 (the mistakes feel personal)
- The progression from Tier 1 → Tier 4 makes the upgrade path visceral
- The post-trade analysis proves the AI coaching is real and specific
- Nothing like this exists in trading SaaS marketing today

---

## Page: `/simulator`

New standalone page. Should feel like stepping into a trading terminal.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Nav (fixed)                                                │
├─────────────────────────────────────────────────────────────┤
│  Hero: "Watch Four Traders. Same Market. Different Tools."  │
│  [Start Simulation] [Speed: 1x / 2x / 5x]                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │              PRICE CHART (candlestick)               │   │
│  │         NQ Futures — 5-min candles                   │   │
│  │         Annotations: FVG zones, OBs, MSS markers    │   │
│  │         Entry/exit markers per tier (color-coded)    │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────┬──────────┬──────────┬──────────┐             │
│  │  TIER 1  │  TIER 2  │  TIER 3  │  TIER 4  │             │
│  │  Discr.  │  Quant   │  Hybrid  │  S-Tier  │             │
│  │          │          │          │          │             │
│  │ Status   │ Status   │ Status   │ Status   │             │
│  │ P&L      │ P&L      │ P&L      │ P&L      │             │
│  │ Trades   │ Trades   │ Trades   │ Trades   │             │
│  │ Win Rate │ Win Rate │ Win Rate │ Win Rate │             │
│  │          │          │          │          │             │
│  │ [Latest  │ [Latest  │ [Latest  │ [Latest  │             │
│  │  reason] │  reason] │  reason] │  reason] │             │
│  └──────────┴──────────┴──────────┴──────────┘             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          TRADE LOG (scrolling table)                  │   │
│  │  Time | Tier | Action | Entry | Exit | P&L | Result  │   │
│  │  ─────────────────────────────────────────────────── │   │
│  │  10:02 | T1 | Long  | 18450 | 18420 | -$600 | LOSS  │   │
│  │    └─ Analysis: Entered FVG without checking HTF...  │   │
│  │    └─ Mistake: Ignored bearish order block at 18470  │   │
│  │    └─ Review: Module 3, Lesson 2 — OB identification │   │
│  │    └─ Improvement: Always check HTF PD arrays...     │   │
│  │                                                      │   │
│  │  10:02 | T3 | Skip  |  —    |  —   |  $0   | SKIP   │   │
│  │    └─ Reasoning: NeuroQuant confluence score 0.3...   │   │
│  │                                                      │   │
│  │  10:15 | T1 | Short | 18430 | 18380 | +$1000| WIN   │   │
│  │    └─ Analysis: Good displacement + FVG alignment    │   │
│  │    └─ Note: Would have been filtered out by T2-T4... │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │       LEARNING PANEL (losses only, expandable)       │   │
│  │                                                      │   │
│  │  Trade #3 — Tier 1 Loss (-$600)                      │   │
│  │  ┌───────────────────────────────────────────────┐   │   │
│  │  │ What Happened:                                │   │   │
│  │  │ Entered long at FVG without confirming HTF    │   │   │
│  │  │ bias. Price was in a bearish OB from the      │   │   │
│  │  │ 1H timeframe.                                 │   │   │
│  │  ├───────────────────────────────────────────────┤   │   │
│  │  │ Mistakes:                                     │   │   │
│  │  │ • No HTF bias confirmation                    │   │   │
│  │  │ • Ignored conflicting PD array (bearish OB)   │   │   │
│  │  │ • Stop placed at FVG low, not swing low       │   │   │
│  │  ├───────────────────────────────────────────────┤   │   │
│  │  │ What Higher Tiers Did:                        │   │   │
│  │  │ T2: Skipped — quant filter flagged low prob.  │   │   │
│  │  │ T3: Skipped — confluence score 0.3/1.0        │   │   │
│  │  │ T4: Skipped — regime detection: bearish       │   │   │
│  │  ├───────────────────────────────────────────────┤   │   │
│  │  │ Concept to Review:                            │   │   │
│  │  │ "HTF-LTF Alignment" — Module 3, Lesson 4     │   │   │
│  │  │ Always confirm the higher timeframe bias      │   │   │
│  │  │ before entering on a lower timeframe signal.  │   │   │
│  │  ├───────────────────────────────────────────────┤   │   │
│  │  │ Improvement Action:                           │   │   │
│  │  │ Add an HTF bias check to your pre-trade       │   │   │
│  │  │ checklist. NeuroSpect Mentor can automate     │   │   │
│  │  │ this with the Entry Model Validator.          │   │   │
│  │  └───────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Waitlist CTA]                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Simulation Engine

### Data Model

The simulation runs off a pre-scripted event timeline (not live market data). Each event represents a moment in a trading session.

```typescript
type SimulationEvent = {
  id: string;
  timestamp: string;           // "2026-05-12T10:02:00"
  candle: {
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  };
  annotations?: {
    type: "fvg" | "ob" | "mss" | "displacement" | "liquidity_sweep" | "breaker";
    direction: "bullish" | "bearish";
    priceLevel: number;
    label: string;
  }[];
  tierActions: {
    tier1: TierAction;
    tier2: TierAction;
    tier3: TierAction;
    tier4: TierAction;
  };
};

type TierAction = {
  action: "wait" | "enter_long" | "enter_short" | "exit" | "skip" | "stop_hit" | "tp_hit";
  reasoning: string;            // Real-time reasoning text
  confirmations?: string[];     // What confirmed the entry
  warnings?: string[];          // What the tier noticed but lower tiers missed
  tradeResult?: {
    result: "win" | "loss" | "breakeven";
    pnl: number;
    rMultiple: number;
    entryPrice: number;
    exitPrice: number;
    stopPrice: number;
    targetPrice: number;
  };
  analysis?: {
    whatHappened: string;
    mistakes: string[];
    whatHigherTiersDid: string[];
    conceptToReview: {
      name: string;
      module: string;
      lesson: string;
      summary: string;
    };
    improvementAction: string;
  };
};
```

### Playback

- Simulation starts paused. User clicks "Start Simulation"
- Events play at configurable speed: 1x (real-time feel), 2x, 5x
- Each event:
  1. New candle draws on chart
  2. Annotations appear (FVG zones highlight, OB boxes draw)
  3. Tier status cards update with reasoning text (typing animation)
  4. If a tier enters: entry marker appears on chart, trade log row animates in
  5. If a tier exits: exit marker appears, P&L updates, result logged
  6. If loss: learning panel expands with full analysis
- User can pause, rewind, skip forward
- Simulation covers one full NY AM session (~2 hours compressed)

### Simulation Scenarios

Pre-script 2-3 complete scenarios that can be selected:

| Scenario | Session | Key Events | Teaching Moments |
|---|---|---|---|
| **Silver Bullet Day** | NY AM (Tue) | Clean displacement + FVG, then liquidity sweep | T1 enters too early, gets swept. T3/T4 wait for confirmation. |
| **Choppy Wednesday** | NY AM (Wed) | Multiple false signals, no clean setup | T1 overtrades (3 losses). T2-T4 skip all or take 1 high-prob trade. |
| **Trend Day** | NY AM (Thu) | Strong directional move after London sweep | All tiers enter, but T1 exits too early. T4 holds to full target. |

---

## Chart Component

### Candlestick Chart

- 5-minute NQ candles
- Dark background matching site theme
- Candles: green/emerald for bullish, red for bearish
- Volume bars at bottom (subtle, 20% opacity)

### Annotations (drawn on chart as events arrive)

| Annotation | Visual |
|---|---|
| Fair Value Gap (FVG) | Shaded rectangle between candle bodies, bullish=cyan tint, bearish=red tint |
| Order Block (OB) | Bordered rectangle at candle range, dashed border |
| Market Structure Shift (MSS) | Horizontal line with label, breaks previous swing |
| Displacement | Thick vertical bar highlighting the displacement candle |
| Liquidity Sweep | Arrow pointing to the swept level |
| Breaker | OB that has been broken, hatched fill pattern |

### Entry/Exit Markers

| Tier | Entry Marker | Exit Marker |
|---|---|---|
| Tier 1 (Discretionary) | Slate triangle (up=long, down=short) | Slate X (loss) or circle (win) |
| Tier 2 (Quant) | Purple triangle | Purple X or circle |
| Tier 3 (Hybrid) | Cyan triangle | Cyan X or circle |
| Tier 4 (S-Tier) | Emerald triangle | Emerald X or circle |

---

## Tier Status Cards (4-column panel)

Each card shows real-time state:

| Field | Display |
|---|---|
| Status | "Watching" / "Analyzing" / "Entering Long" / "In Trade" / "Exiting" / "Skipped" |
| Current P&L | Running total, green/red |
| Trades | Win/Loss/Skip count |
| Win Rate | Percentage |
| Latest Reasoning | Typing animation showing AI reasoning in real-time |

### Reasoning Examples

**Tier 1 (entering a bad trade):**
> "FVG spotted on 5m. Displacement looks clean. Going long at 18,450. Stop below FVG."

**Tier 2 (skipping same trade):**
> "FVG detected but quant filter shows low probability. HTF momentum score: 0.28/1.0. Feature rank: bottom quartile. Skipping."

**Tier 3 (skipping with more detail):**
> "FVG valid but NeuroQuant confluence score 0.3/1.0. Bearish OB overhead at 18,470 creates conflict zone. Mentor checklist: 3/5 criteria met. Insufficient for entry."

**Tier 4 (skipping automatically):**
> "Regime: bearish (detected via 4H structure). Entry signal filtered. No trade executed. Safety layer 2 (regime filter) blocked."

---

## Trade Log Table

Scrolling table that grows as the simulation progresses. Each row is a trade event.

| Column | Content |
|---|---|
| Time | HH:MM timestamp |
| Tier | Color-coded tier badge |
| Action | Long / Short / Skip |
| Entry | Price |
| Exit | Price (or "—" if skipped) |
| P&L | Dollar amount, green/red |
| Result | WIN / LOSS / SKIP badge |

### Expandable Row (on click or auto-expand for losses)

Losses auto-expand to show the learning panel inline:
- What Happened (narrative)
- Mistakes (bullet list)
- What Higher Tiers Did (comparison)
- Concept to Review (module + lesson reference)
- Improvement Action (specific next step)

Wins show a brief note. Skips show the reasoning for skipping.

---

## Learning Panel (bottom section)

Aggregated view of all losses with full analysis. Acts as a "coaching session summary" after the simulation completes.

### Post-Simulation Summary

When simulation ends, show a summary card:

```
Session Complete — NY AM, May 12, 2026

            Tier 1      Tier 2      Tier 3      Tier 4
P&L         -$1,400     +$800       +$1,600     +$2,200
Trades      5           2           2           2
Win Rate    20%         50%         100%        100%
Mistakes    4           1           0           0
Grade       D           B+          A           A+

Key Insight: Tier 1 took 3 trades that higher tiers skipped.
Those 3 skipped trades account for -$2,100 in losses.
With NeuroSpect Mentor's entry model validation, 
Tier 1 would have avoided 2 of 3 losses.
```

---

## Interaction Design

### Controls

| Control | Behavior |
|---|---|
| Start/Pause | Toggle simulation playback |
| Speed (1x/2x/5x) | Adjust event playback rate |
| Scenario selector | Choose between 2-3 pre-scripted scenarios |
| Tier focus | Click a tier card to highlight only that tier's entries on chart |
| Reset | Return to beginning of simulation |

### Progressive Disclosure

- Chart annotations appear as events happen (not all at once)
- Tier reasoning appears as typing animation
- Trade log rows slide in from right
- Loss analysis expands with accordion animation
- Post-simulation summary fades in when complete

### Sound (optional, off by default)

- Subtle "tick" on new candle
- Entry chime (different pitch per tier)
- Loss "thud" (low, subtle)
- Win "ding" (bright, brief)

---

## Technical Considerations

- Candlestick chart: consider lightweight-charts (TradingView open source) or custom Canvas/SVG
- All data is pre-scripted (no live market feed needed)
- Event timeline is a JSON array loaded at page init
- Playback engine is a simple interval timer stepping through events
- Chart annotations are overlays, not part of the candle data
- Mobile: stack tier cards vertically, chart takes full width

---

## Connection to Product

Every element of the simulator maps to a real NeuroSpect feature:

| Simulator Element | NeuroSpect Feature |
|---|---|
| Tier reasoning text | NeuroSpect Mentor AI coaching |
| Entry model checklist | Deterministic rule validation |
| Mistake identification | Journal intelligence + psychology profiler |
| Concept to review | NeuroCore knowledge retrieval |
| Higher tier comparison | EdgeLab + NeuroQuant scoring |
| Regime detection (T4) | NeuroQuant regime-aware models |
| Auto-skip (T4) | NeuroTrader Agent safety layers |

The CTA after simulation: **"Stop being Tier 1. Start your journey to Tier 4."** → Join Waitlist
