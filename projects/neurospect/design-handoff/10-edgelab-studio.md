# NeuroSpect EdgeLab Studio — Design Spec

## Overview

An interactive dashboard page that demonstrates three core EdgeLab capabilities in a live "research terminal" experience. The user starts with a base NSLM model, injects features, runs simulations, compares results, and watches the system adapt to market conditions in real time.

This page answers: **"What does AI-native trading research actually look like?"**

Nothing like this exists in trading product marketing today. It makes EdgeLab's value tangible — not through descriptions, but through an interactive workflow the user controls.

---

## The Three Engines

### 1. EdgeLab Feature Discovery Engine

**Formerly:** "Feature Researcher"

**What it does:** Analyzes historical trade outcomes to discover what distinguishes winning trades from losing trades. Automatically engineers, ranks, adds, or removes features to improve model performance.

**How it works:**
1. Ingests all trades from a model's backtest run
2. Segments trades into wins, losses, and breakevens
3. For each losing trade, identifies the market conditions at entry: regime, session, setup quality, HTF alignment, displacement strength, FVG fill percentage, time in kill zone, volatility percentile, etc.
4. Finds patterns: "85% of losses occurred when displacement strength was below 0.6 AND the session was NY Lunch"
5. Proposes new features that would have filtered those losses (e.g., `displacement_strength_threshold`, `session_quality_filter`)
6. For winning trades, identifies what conditions were consistently present and proposes features to weight those conditions higher
7. Runs a simulation with the proposed features and compares to baseline
8. If improvement is statistically significant, adds features to the Feature Library

**Concrete feature examples it discovers:**

| Feature | Type | Description | Discovery Source |
|---|---|---|---|
| `displacement_strength` | Continuous (0-1) | Measures the magnitude of displacement candle relative to ATR. Higher = stronger conviction. | 78% of losses had displacement < 0.4 |
| `fvg_fill_percentage` | Continuous (0-1) | How much of the FVG was filled before entry. 0 = untouched, 1 = fully filled. | Winners averaged 0.15 fill; losers averaged 0.62 |
| `htf_bias_alignment` | Binary (0/1) | Whether the LTF entry direction matches the HTF bias (1H+ timeframe). | 91% of T4 wins had alignment; only 52% of T1 losses did |
| `session_quality_score` | Continuous (0-1) | Composite of: kill zone active, volume above session average, spread normal. | Losses concentrated in low-quality sessions (score < 0.3) |
| `ob_proximity` | Continuous (pts) | Distance from nearest opposing order block. Closer = more risk. | Losses were 3x more likely when within 20 pts of opposing OB |
| `consecutive_loss_flag` | Binary (0/1) | Whether the trader has 2+ consecutive losses in the session. | Overtrading after loss accounts for 34% of T1 losses |
| `sweep_recency` | Continuous (candles) | Candles since last liquidity sweep. Fresh sweeps = higher probability. | 72% of wins occurred within 8 candles of a sweep |
| `smt_divergence_present` | Binary (0/1) | Whether SMT divergence confirms the entry direction. | Trades with SMT confirmation: 71% win rate vs 48% without |
| `adr_percentile` | Continuous (0-100) | Where current day's range sits relative to 20-day ADR. | Entries above 80th percentile ADR had 2.3x more losses |
| `time_in_killzone` | Continuous (min) | Minutes remaining in the active kill zone at entry. | Entries in last 10 min of kill zone: 62% loss rate |

### 2. Regime-Adaptive Optimization Engine

**Formerly:** "Market Regime Detector"

**What it does:** Classifies the current market environment into one of several regimes, then automatically adjusts model parameters to optimize performance for that specific regime.

**Regime classifications:**

| Regime | Code | Characteristics | Model Adjustment |
|---|---|---|---|
| **Trending Bull** | `TREND_BULL` | Strong directional move up, shallow pullbacks, HTF bullish structure | Widen targets, tighten entry filters, favor continuation setups |
| **Trending Bear** | `TREND_BEAR` | Strong directional move down, shallow pullbacks, HTF bearish structure | Widen targets, tighten entry filters, favor reversal sweeps |
| **Range-Bound** | `RANGE` | Price oscillates between support/resistance, no clear direction | Tighten targets, require stronger displacement, favor OB bounces |
| **High Volatility Expansion** | `HV_EXPAND` | Wide candles, gaps, news-driven, fast moves | Widen stops, reduce position size, require 2+ confirmations |
| **Low Volatility Compression** | `LV_COMPRESS` | Tight candles, coiling, pre-breakout | Skip most setups, wait for expansion trigger |
| **Transition** | `TRANSITION` | Regime shifting, conflicting signals, structure breaking | Reduce size, require maximum confluence, shorten hold time |

**Parameter adjustments per regime:**

| Parameter | Trending | Range | HV Expand | LV Compress |
|---|---|---|---|---|
| `min_displacement_strength` | 0.5 | 0.7 | 0.8 | 0.4 |
| `target_r_multiple` | 3.0R | 1.5R | 2.0R | 1.0R |
| `max_position_size` | 100% | 75% | 50% | 25% |
| `min_confluence_score` | 0.6 | 0.7 | 0.8 | 0.9 |
| `stop_atr_multiplier` | 1.5x | 1.0x | 2.0x | 0.8x |
| `max_trades_per_session` | 4 | 3 | 2 | 1 |
| `fvg_fill_tolerance` | 40% | 25% | 20% | 50% |

**Dynamic condition modifiers** (override or adjust base regime parameters):

| Condition | Detection | Modifier |
|---|---|---|
| **Day of Week** | Calendar | Mon/Fri: reduce size 25%. Tue-Thu: full size. |
| **Economic News** | Calendar feed | 30 min before/after high-impact news: pause trading or require 2x confluence |
| **SMT Divergence** | NQ vs ES comparison | If present: boost confluence score +0.15. If absent and required: block entry. |
| **Session Liquidity Swept** | Sweep detector | PDH/PDL swept: enable expansion setups. Not swept: wait for sweep first. |
| **Price Cycle Phase** | APD detector | Consolidation: wait. Accumulation: prepare. Manipulation: alert. Distribution: enter or exit. |

### 3. NSLM Feature Studio

**Formerly:** "NSLM Model Injection"

**What it does:** Injects quantitative features as structured parameters into NSLM prompts, then runs iterative simulations to find optimal feature values. Integrates ICT domain knowledge to generate bespoke feature suggestions that combine quantitative rigor with ICT conceptual reasoning.

**How it works:**
1. Start with a base NSLM prompt (e.g., "Evaluate this NQ setup for a long entry")
2. Inject feature parameters into the prompt context:
   ```
   Current conditions:
   - displacement_strength: 0.72
   - htf_bias_alignment: true
   - regime: TREND_BULL
   - session_quality_score: 0.85
   - fvg_fill_percentage: 0.12
   - smt_divergence: present
   ```
3. NSLM evaluates the setup with full ICT reasoning + quantitative features
4. Run N iterations with different feature values to find:
   - Which features NSLM weights most heavily in its reasoning
   - At what thresholds NSLM flips from "enter" to "skip"
   - Which feature combinations produce the highest-quality reasoning
5. NSLM proposes new features based on ICT concepts it identifies as missing:
   ```
   "The current feature set doesn't capture the relationship between 
   the displacement candle's close and the nearest HTF order block. 
   Suggest: `displacement_to_ob_ratio` — measures whether displacement 
   carried price through or stopped at the OB level."
   ```
6. New features are validated via EdgeLab backtest and added to the Feature Library if they improve performance

**Feature Library integration:**

| Category | Features | Source |
|---|---|---|
| **ICT Structural** | FVG count, OB proximity, MSS recency, sweep depth | ICT detectors |
| **ICT Contextual** | Kill zone active, session quality, daily bias alignment, HTF structure | Session + bias detectors |
| **Quantitative** | ATR percentile, volume z-score, spread ratio, momentum score | Standard quant features |
| **NSLM-Derived** | Setup confidence, reasoning coherence, checklist completeness | NSLM structured outputs |
| **Regime** | Current regime, regime duration, transition probability | Regime detector |
| **Composite** | Confluence score (ICT gates + ML confidence + NSLM reasoning) | All sources combined |

---

## Page: `/research`

**Title:** "EdgeLab Research Studio"
**Nav position:** After Performance, before Workflows

### Layout — The Research Terminal

```
┌──────────────────────────────────────────────────────────────┐
│  Nav (fixed)                                                  │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  HERO                                                          │
│  "Your Trading Edge, Engineered."                              │
│  Sub: "Watch EdgeLab discover features, adapt to market        │
│  regimes, and optimize NSLM prompts — in real time."           │
│                                                                │
│  [Launch Research Terminal]  [How It Works]                     │
│  Badge: "Interactive Demo — Illustrative Data"                 │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  THREE ENGINES OVERVIEW (3 column cards)                       │
│                                                                │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐  │
│  │ FEATURE DISCOVERY │ │ REGIME-ADAPTIVE  │ │ NSLM FEATURE │  │
│  │ ENGINE            │ │ OPTIMIZATION     │ │ STUDIO       │  │
│  │                    │ │                  │ │              │  │
│  │ Analyzes wins &    │ │ Detects market   │ │ Injects      │  │
│  │ losses. Engineers   │ │ conditions.      │ │ features     │  │
│  │ features that       │ │ Auto-tunes       │ │ into NSLM    │  │
│  │ filter bad trades   │ │ parameters per   │ │ prompts.     │  │
│  │ and amplify good    │ │ regime.          │ │ Iterates     │  │
│  │ ones.               │ │                  │ │ to find      │  │
│  │                    │ │                  │ │ optimal      │  │
│  │ [neon-card-cyan]   │ │ [neon-card-      │ │ values.      │  │
│  │                    │ │  emerald]        │ │              │  │
│  │                    │ │                  │ │ [neon-card-  │  │
│  │                    │ │                  │ │  amber]      │  │
│  └──────────────────┘ └──────────────────┘ └──────────────┘  │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  FEATURE DISCOVERY ENGINE (Section 1)                          │
│                                                                │
│  "How EdgeLab Turns Losses Into Features"                      │
│                                                                │
│  Before/After visualization:                                   │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ BEFORE: Base Model (no feature filtering)                │  │
│  │ ┌─────────────────────────────────────────────────────┐ │  │
│  │ │  38 trades | 42% WR | PF 1.1 | -$3,200 max DD      │ │  │
│  │ │  Loss pattern: "85% of losses had displacement       │ │  │
│  │ │  strength < 0.4 AND session quality < 0.3"           │ │  │
│  │ └─────────────────────────────────────────────────────┘ │  │
│  │                         ↓                                │  │
│  │  Feature Discovery scans 38 trades...                    │  │
│  │  Found: 3 features that separate wins from losses        │  │
│  │                         ↓                                │  │
│  │ AFTER: + displacement_strength + session_quality          │  │
│  │        + htf_bias_alignment                               │  │
│  │ ┌─────────────────────────────────────────────────────┐ │  │
│  │ │  22 trades | 64% WR | PF 2.1 | -$1,100 max DD      │ │  │
│  │ │  16 low-quality trades filtered out                  │ │  │
│  │ │  Net PnL improved +$4,200                            │ │  │
│  │ └─────────────────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
│  FEATURE TABLE (10 rows)                                       │
│  ┌──────────────────┬──────┬──────────────────────────────┐   │
│  │ Feature           │ Type │ Discovery Insight             │   │
│  │ displacement_str  │ 0-1  │ 78% of losses < 0.4          │   │
│  │ fvg_fill_pct      │ 0-1  │ Winners avg 0.15, losers 0.62│   │
│  │ htf_bias_align    │ 0/1  │ 91% of T4 wins had alignment │   │
│  │ session_quality   │ 0-1  │ Losses in sessions < 0.3     │   │
│  │ ob_proximity      │ pts  │ 3x loss rate within 20 pts   │   │
│  │ ...               │      │                               │   │
│  └──────────────────┴──────┴──────────────────────────────┘   │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  REGIME-ADAPTIVE OPTIMIZATION (Section 2)                      │
│                                                                │
│  "Same Strategy. Six Different Markets.                        │
│   Parameters That Adapt."                                      │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ REGIME CARDS (6 columns, scrollable on mobile)           │  │
│  │                                                           │  │
│  │ [TREND ↑] [TREND ↓] [RANGE ↔] [HV ⚡] [LV ◇] [TRANS ~] │  │
│  │  Bull      Bear      Bound     Expand   Compress Transit │  │
│  │                                                           │  │
│  │ Click a regime to see parameter adjustments below:        │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
│  PARAMETER TABLE (updates when regime selected)                │
│  ┌──────────────────────┬─────────┬─────────┬─────────────┐  │
│  │ Parameter             │ Default │ Regime  │ Delta       │  │
│  │ min_displacement      │ 0.5     │ 0.7     │ +0.2 ↑      │  │
│  │ target_r_multiple     │ 2.0R    │ 1.5R    │ -0.5R ↓     │  │
│  │ max_position_size     │ 100%    │ 75%     │ -25% ↓      │  │
│  │ min_confluence_score  │ 0.6     │ 0.7     │ +0.1 ↑      │  │
│  │ ...                   │         │         │             │  │
│  └──────────────────────┴─────────┴─────────┴─────────────┘  │
│                                                                │
│  DYNAMIC CONDITION MODIFIERS (cards below table)               │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ Day of │ │Econ    │ │ SMT    │ │Session │ │ Price  │     │
│  │ Week   │ │News    │ │Diverg. │ │Liq.   │ │ Cycle  │     │
│  │ Mon:   │ │NFP:    │ │Present:│ │Swept: │ │Consol: │     │
│  │ -25%   │ │Pause   │ │+0.15   │ │Enable │ │Wait    │     │
│  │ size   │ │trading │ │conflu. │ │expan. │ │        │     │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
│                                                                │
│  PERFORMANCE BY REGIME (bar chart or heatmap)                  │
│  Shows PnL / win rate / PF per regime with vs without          │
│  adaptive optimization.                                        │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  NSLM FEATURE STUDIO (Section 3)                               │
│                                                                │
│  "Open the Model. Inject Features. Run Experiments."           │
│                                                                │
│  This is the interactive research terminal demo.               │
│  (See detailed wireframe below)                                │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  FEATURE LIBRARY (Section 4)                                   │
│                                                                │
│  "Every Feature, Cataloged and Ranked"                         │
│  Searchable/filterable table of all features.                  │
│                                                                │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  CTA + Waitlist                                                │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## NSLM Feature Studio — Interactive Research Terminal

This is the flagship interactive section. It should feel like a real research IDE.

### Terminal Layout

```
┌──────────────────────────────────────────────────────────────┐
│  NSLM Feature Studio                                          │
│  "Open the Model. Inject Features. Run Experiments."          │
│                                                                │
│  ┌─ WORKSPACE ──────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │  ┌─ MODEL PANEL (left 35%) ────────────────────────────┐ │ │
│  │  │                                                      │ │ │
│  │  │  BASE MODEL                                          │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │ NSLM v2.1 — ICT Setup Evaluator              │   │ │ │
│  │  │  │ Base prompt: "Evaluate this NQ setup..."       │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │ Baseline performance:                          │   │ │ │
│  │  │  │ 38 trades | 42% WR | PF 1.1 | Sharpe 0.45    │   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  │                                                      │ │ │
│  │  │  INJECTED FEATURES                                   │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │ + displacement_strength    [0.6]  [slider]    │   │ │ │
│  │  │  │ + htf_bias_alignment       [ON]   [toggle]    │   │ │ │
│  │  │  │ + session_quality_score    [0.4]  [slider]    │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │ [+ Add Feature ▾]                              │   │ │ │
│  │  │  │   displacement_strength                        │   │ │ │
│  │  │  │   fvg_fill_percentage                          │   │ │ │
│  │  │  │   ob_proximity                                 │   │ │ │
│  │  │  │   consecutive_loss_flag                        │   │ │ │
│  │  │  │   sweep_recency                                │   │ │ │
│  │  │  │   smt_divergence_present                       │   │ │ │
│  │  │  │   adr_percentile                               │   │ │ │
│  │  │  │   time_in_killzone                             │   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  │                                                      │ │ │
│  │  │  DYNAMIC CONDITIONS                                  │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │ Regime:     [TREND_BULL ▾]                    │   │ │ │
│  │  │  │ Day:        [Tuesday ▾]                       │   │ │ │
│  │  │  │ News:       [None ▾]                          │   │ │ │
│  │  │  │ SMT:        [Present ▾]                       │   │ │ │
│  │  │  │ Liq Swept:  [PDL Swept ▾]                     │   │ │ │
│  │  │  │ Price Cycle: [Manipulation ▾]                  │   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  │                                                      │ │ │
│  │  │  [▶ Run Simulation]  [▶▶ Run Sweep]                 │ │ │
│  │  │  [+ Add to Comparison]                               │ │ │
│  │  │                                                      │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                           │ │
│  │  ┌─ RESULTS PANEL (right 65%) ─────────────────────────┐ │ │
│  │  │                                                      │ │ │
│  │  │  SIMULATION RESULTS                                  │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │ Run: NSLM v2.1 + 3 features                  │   │ │ │
│  │  │  │ Regime: TREND_BULL | Conditions: SMT+Swept    │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │ ┌────────┬────────┬────────┬────────┐         │   │ │ │
│  │  │  │ │Trades  │WR      │PF      │Sharpe  │         │   │ │ │
│  │  │  │ │22      │64%     │2.1     │1.45    │         │   │ │ │
│  │  │  │ │vs 38   │vs 42%  │vs 1.1  │vs 0.45 │         │   │ │ │
│  │  │  │ │↓ -42%  │↑ +22pp │↑ +91%  │↑ +222% │         │   │ │ │
│  │  │  │ └────────┴────────┴────────┴────────┘         │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │  EQUITY CURVE (Chart.js line)                  │   │ │ │
│  │  │  │  ┌────────────────────────────────────────┐   │   │ │ │
│  │  │  │  │  ── Baseline (slate, dashed)            │   │   │ │ │
│  │  │  │  │  ── With Features (cyan, solid)         │   │   │ │ │
│  │  │  │  │                                          │   │   │ │ │
│  │  │  │  │          ╱‾‾‾‾‾╲                        │   │   │ │ │
│  │  │  │  │     ╱‾‾‾╱       ╲_____╱‾‾‾‾‾            │   │   │ │ │
│  │  │  │  │  __╱                                     │   │   │ │ │
│  │  │  │  │  ╱  ╲_╱‾╲___╱‾╲___╱‾                    │   │   │ │ │
│  │  │  │  └────────────────────────────────────────┘   │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │  FILTERED TRADES (what was removed)            │   │ │ │
│  │  │  │  ┌────────────────────────────────────────┐   │   │ │ │
│  │  │  │  │ 16 trades filtered out:                 │   │   │ │ │
│  │  │  │  │  12 would have been losses (-$4,800)    │   │   │ │ │
│  │  │  │  │   3 would have been breakevens          │   │   │ │ │
│  │  │  │  │   1 would have been a win (-$320)       │   │   │ │ │
│  │  │  │  │  Net filter benefit: +$4,480            │   │   │ │ │
│  │  │  │  └────────────────────────────────────────┘   │   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  │                                                      │ │ │
│  │  │  COMPARISON VIEW (when multiple runs added)          │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │           │ Baseline│ +Disp  │ +Disp+HTF│+All│   │ │ │
│  │  │  │ Trades    │ 38      │ 28     │ 22       │ 18 │   │ │ │
│  │  │  │ Win Rate  │ 42%     │ 54%    │ 64%      │ 72%│   │ │ │
│  │  │  │ PF        │ 1.1     │ 1.6    │ 2.1      │ 2.8│   │ │ │
│  │  │  │ Sharpe    │ 0.45    │ 0.92   │ 1.45     │ 1.9│   │ │ │
│  │  │  │ Max DD    │ -$3,200 │ -$2,100│ -$1,100  │-$80│   │ │ │
│  │  │  │ Net PnL   │ +$1,850 │ +$3,900│ +$6,050  │+$8K│   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  │                                                      │ │ │
│  │  │  NSLM REASONING SAMPLE                               │ │ │
│  │  │  ┌──────────────────────────────────────────────┐   │ │ │
│  │  │  │  Trade #7 — NSLM evaluation with features:    │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │  "Setup: NQ long at 18,420 FVG retrace.       │   │ │ │
│  │  │  │   displacement_strength: 0.72 ✓ (above 0.6)   │   │ │ │
│  │  │  │   htf_bias_alignment: true ✓                   │   │ │ │
│  │  │  │   session_quality: 0.85 ✓ (above 0.4)         │   │ │ │
│  │  │  │   regime: TREND_BULL ✓                         │   │ │ │
│  │  │  │   smt_divergence: present ✓                    │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │   Verdict: ENTER — 5/5 feature gates passed.   │   │ │ │
│  │  │  │   Confluence score: 0.91.                      │   │ │ │
│  │  │  │   ICT reasoning: Sweep of PDL confirmed        │   │ │ │
│  │  │  │   bullish intent. FVG retrace to discount.     │   │ │ │
│  │  │  │   OTE zone entry. Kill zone active."           │   │ │ │
│  │  │  │                                                │   │ │ │
│  │  │  │  SUGGESTED NEW FEATURE:                        │   │ │ │
│  │  │  │  "displacement_to_ob_ratio — measures whether  │   │ │ │
│  │  │  │   displacement carried through or stopped at   │   │ │ │
│  │  │  │   the nearest HTF order block."                │   │ │ │
│  │  │  │  [Add to Feature Library]                      │   │ │ │
│  │  │  └──────────────────────────────────────────────┘   │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                │
│  PARAMETER SWEEP VIEW                                          │
│  (appears when "Run Sweep" is clicked)                         │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Sweep: displacement_strength from 0.3 to 0.9 (step 0.1)  │ │
│  │                                                            │ │
│  │  Value │ Trades │ WR    │ PF   │ Sharpe │ Net PnL         │ │
│  │  0.3   │ 35     │ 43%   │ 1.1  │ 0.48   │ +$1,920         │ │
│  │  0.4   │ 30     │ 50%   │ 1.4  │ 0.82   │ +$3,100         │ │
│  │  0.5   │ 26     │ 58%   │ 1.8  │ 1.12   │ +$4,600  ← opt │ │
│  │  0.6   │ 22     │ 64%   │ 2.1  │ 1.45   │ +$6,050  ← opt │ │
│  │  0.7   │ 16     │ 69%   │ 2.4  │ 1.62   │ +$5,200         │ │
│  │  0.8   │ 10     │ 70%   │ 2.3  │ 1.40   │ +$3,800         │ │
│  │  0.9   │ 5      │ 80%   │ 3.1  │ 1.10   │ +$2,100         │ │
│  │                                                            │ │
│  │  Chart: line graph showing PnL vs parameter value          │ │
│  │  Optimal zone highlighted in cyan                          │ │
│  │  Diminishing returns zone in amber                         │ │
│  │  Overfitting warning zone in red                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### Interaction Flow

**Step 1: Open Base Model**
- Page loads showing the base NSLM v2.1 with baseline stats
- No features injected yet
- "This is your starting point. A raw ICT setup evaluator."

**Step 2: Add First Feature**
- User clicks "+ Add Feature" → dropdown shows available features
- Selects `displacement_strength` → slider appears (default 0.5)
- Adjusts slider to 0.6
- Clicks "Run Simulation"
- Results panel animates in: improved metrics, equity curve overlays baseline
- Delta indicators show improvement (+12pp win rate, etc.)

**Step 3: Add More Features**
- User adds `htf_bias_alignment` (toggle ON) and `session_quality_score` (slider 0.4)
- Clicks "Run Simulation" again
- Results update with cumulative improvement
- "Add to Comparison" saves this run for side-by-side

**Step 4: Run Parameter Sweep**
- User clicks "Run Sweep" on `displacement_strength`
- Sweep table shows results for 0.3 → 0.9
- Chart shows the optimal zone and diminishing returns
- User sees: "0.5-0.6 is the sweet spot — higher filters too aggressively"

**Step 5: Dynamic Conditions**
- User changes regime to "RANGE" → parameter adjustments auto-apply
- Metrics change to show regime-specific performance
- "In range-bound markets, tighter displacement threshold prevents false breakout entries"

**Step 6: NSLM Reasoning**
- User clicks a specific trade row to see NSLM's full reasoning
- Shows feature-by-feature gate check + ICT narrative reasoning
- NSLM suggests a new feature → "Add to Feature Library" button

---

## Feature Library Section

Searchable, filterable table of all available features.

```
┌──────────────────────────────────────────────────────────────┐
│  FEATURE LIBRARY                                              │
│  "Every Feature, Cataloged and Ranked"                        │
│                                                                │
│  Filter: [All ▾] [ICT ▾] [Quant ▾] [NSLM ▾] [Regime ▾]     │
│  Search: [________________________]                            │
│                                                                │
│  ┌──────────┬──────┬────────┬──────────┬────────────────────┐ │
│  │ Feature   │ Type │Category│ Impact   │ Description         │ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ displace │ 0-1  │ ICT    │ ████░ Hi │ Displacement candle │ │
│  │ _strength│      │        │          │ magnitude vs ATR    │ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ htf_bias │ 0/1  │ ICT    │ █████ Hi │ LTF direction       │ │
│  │ _align   │      │        │          │ matches HTF bias    │ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ session  │ 0-1  │ ICT    │ ████░ Hi │ KZ active + volume  │ │
│  │ _quality │      │        │          │ + spread composite  │ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ regime   │ enum │ Regime │ ████░ Hi │ Current market       │ │
│  │ _state   │      │        │          │ regime classification│ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ smt_div  │ 0/1  │ ICT    │ ███░░ Med│ SMT divergence       │ │
│  │ _present │      │        │          │ confirms direction  │ │
│  ├──────────┼──────┼────────┼──────────┼────────────────────┤ │
│  │ ...20 more features...                                    │ │
│  └──────────┴──────┴────────┴──────────┴────────────────────┘ │
│                                                                │
│  Click any feature to see: full description, discovery source, │
│  optimal range, regime sensitivity, backtest impact chart.     │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### Data
- All simulation data is synthetic and deterministic
- Pre-computed results for each feature combination (no real-time ML)
- Stored in TypeScript data files like other pages
- Parameter sweep results are a lookup table, not computed on the fly

### Libraries
- Chart.js: equity curves, parameter sweep charts, bar charts
- lightweight-charts: any candlestick chart examples in feature descriptions
- Vanilla JS: feature add/remove, slider controls, tab switching, comparison table

### New files

```
site/src/
├── pages/
│   └── research.astro
├── components/
│   └── research/
│       ├── ResearchHero.astro
│       ├── EngineCards.astro           # 3-engine overview
│       ├── FeatureDiscovery.astro      # Before/after + feature table
│       ├── RegimeOptimization.astro    # Regime cards + parameter table
│       ├── FeatureStudio.astro         # Interactive research terminal
│       ├── ParameterSweep.astro        # Sweep results table + chart
│       ├── NslmReasoning.astro         # NSLM reasoning sample panel
│       ├── SimulationResults.astro     # Results panel with metrics + curve
│       ├── ComparisonTable.astro       # Side-by-side run comparison
│       ├── FeatureLibrary.astro        # Searchable feature catalog
│       └── ResearchCTA.astro           # Bottom CTA
├── data/
│   ├── features.ts                    # Feature definitions + metadata
│   ├── simulation-results.ts          # Pre-computed results per combination
│   ├── regime-parameters.ts           # Parameter adjustments per regime
│   └── sweep-results.ts              # Parameter sweep lookup tables
```

---

## Safety & Disclaimers

- "Illustrative research demo — not live model output"
- "Feature performance is based on synthetic backtests, not live trading"
- "Past backtest performance does not guarantee future results"
- "This demo shows the EdgeLab workflow, not actual NSLM predictions"

---

## Connection to Product Tiers

| Demo Element | NeuroSpect Feature | Available In |
|---|---|---|
| Feature Discovery | EdgeLab Feature Discovery Engine | Research ($199), Quant ($349) |
| Regime Detection | NeuroQuant Regime-Adaptive Optimization | Quant ($349) |
| NSLM Feature Studio | NSLM Feature Studio + Prompt Lab | Research ($199), Quant ($349) |
| Feature Library | EdgeLab Feature Store | Trader ($99)+, full in Research |
| Parameter Sweep | EdgeLab Experiment Runner | Research ($199)+ |
| Dynamic Conditions | NeuroQuant Condition Engine | Quant ($349) |

---

_All data is illustrative. Not financial advice. Trading involves risk._
