# Claude Design Prompt — EdgeLab Research Studio

Use this prompt with Claude to generate high-fidelity design mockups for the `/research` page.

---

## Prompt

Design a premium dark-theme interactive research terminal page for NeuroSpect, an AI-native trading research platform. This page demonstrates three research engines through a live dashboard experience.

### Brand

- Background: pure black (#000000)
- Primary accent: cyan (#06b6d4)
- Secondary accents: emerald (#10b981), purple (#8b5cf6), amber (#f59e0b)
- Cards: charcoal glass (rgba(30, 30, 35, 0.85)) with 1px border (rgba(255, 255, 255, 0.06)), 16px border radius, colored glow on hover
- Typography: Inter for text (white headings, slate-300 body, slate-500 secondary), JetBrains Mono for data/numbers
- Semantic colors: emerald-400 for positive/wins, red-400 for negative/losses, amber-400 for warnings
- Design inspiration: Bloomberg terminal meets Linear app meets Vercel dashboard — data-dense but breathable

### Page Structure

Design these sections in order:

**1. Hero**
Headline: "Your Trading Edge, Engineered."
Subhead: "Watch EdgeLab discover features, adapt to market regimes, and optimize NSLM prompts — in real time."
Two buttons: [Launch Research Terminal] (primary cyan) and [How It Works] (ghost)
Small amber badge: "Interactive Demo — Illustrative Data"

**2. Three Engine Overview Cards** (3-column grid)
Three glassmorphism cards with colored top borders:
- "Feature Discovery Engine" (cyan border) — "Analyzes wins and losses. Engineers features that filter bad trades and amplify good ones." Icon: magnifying glass + chart
- "Regime-Adaptive Optimization" (emerald border) — "Detects 6 market regimes. Auto-tunes parameters for each condition." Icon: adaptive/wave
- "NSLM Feature Studio" (amber border) — "Injects features into NSLM prompts. Runs iterations to find optimal values." Icon: code/brain

**3. Feature Discovery Section**
Before/After comparison. Two stacked cards:
- BEFORE card (slate/neutral): "Base Model — 38 trades | 42% WR | PF 1.1 | -$3,200 max DD" with a pattern callout: "85% of losses had displacement strength < 0.4"
- Arrow/transition
- AFTER card (cyan glow): "+ 3 features — 22 trades | 64% WR | PF 2.1 | -$1,100 max DD" with: "16 low-quality trades filtered. Net improvement: +$4,200"

Below: a data table with 10 features. Columns: Feature name (mono font), Type (pill badge), Discovery Insight (the pattern that revealed it). Each row is a card-style row with subtle hover.

**4. Regime-Adaptive Section**
6 regime selector cards in a horizontal row (scrollable on mobile):
- Trending Bull (emerald, up arrow)
- Trending Bear (red, down arrow)  
- Range-Bound (amber, sideways arrows)
- HV Expansion (purple, lightning bolt)
- LV Compression (slate, diamond)
- Transition (cyan, wave)

Below: parameter adjustment table that changes when a regime is selected. Columns: Parameter | Default | Regime Value | Delta (with colored up/down indicators).

Below the table: 5 small "Dynamic Condition" modifier cards in a row:
- Day of Week | Economic News | SMT Divergence | Session Liquidity | Price Cycle
Each shows one key modifier (e.g., "Mon: -25% size", "NFP: Pause trading")

**5. NSLM Feature Studio — The Interactive Research Terminal**
This is the centerpiece. It should look like a real research IDE/terminal.

Split layout: LEFT panel (35%) + RIGHT panel (65%).

LEFT PANEL:
- "Base Model" card at top: "NSLM v2.1 — ICT Setup Evaluator" with baseline stats
- "Injected Features" section: list of features with sliders (continuous 0-1) and toggles (binary). Each feature has a name in mono font and a remove (X) button. An "+ Add Feature" dropdown at the bottom shows available features.
- "Dynamic Conditions" section: 6 dropdown selectors (Regime, Day, News, SMT, Liquidity Swept, Price Cycle)
- Two action buttons: [Run Simulation] (primary) and [Run Parameter Sweep] (secondary)
- [+ Add to Comparison] (ghost)

RIGHT PANEL:
- Simulation results card with KPI row: Trades | Win Rate | Profit Factor | Sharpe — each showing value + delta from baseline (green up arrows or red down arrows)
- Below KPIs: an equity curve chart. Two lines: baseline (slate dashed) and current run (cyan solid). Dark grid, subtle.
- Below chart: "Filtered Trades" summary card — how many trades were filtered, how many would have been losses, net benefit.
- Below that: a comparison table (appears when multiple runs are saved) — rows for each metric, columns for each saved run. Progressive improvement left to right.
- At bottom: "NSLM Reasoning Sample" — a terminal-style card with monospace text showing the NSLM evaluating a specific trade, checking each feature gate (✓/✗), and giving its ICT reasoning. At the bottom, a "Suggested New Feature" callout with an [Add to Feature Library] button.

**6. Parameter Sweep Panel** (shows below terminal when sweep is run)
Table: parameter value in column 1, then Trades, WR, PF, Sharpe, Net PnL for each value step. Optimal zone row highlighted in cyan. Diminishing returns zone in amber. Overfitting zone in red.
Chart: line graph of Net PnL vs parameter value, with the optimal zone shaded.

**7. Feature Library**
Full-width searchable table. Filter pills at top: All | ICT | Quant | NSLM | Regime | Composite.
Table rows: Feature name (mono), Type (pill), Category (colored badge), Impact (5-bar rating), Description.
Each row is hover-interactive (shows expanded detail on click).

**8. Bottom CTA**
"Stop Guessing. Start Engineering Your Edge."
Two buttons: [Join Waitlist] and [See Pricing]
Disclaimer: "Illustrative research demo. Not financial advice."

### Key Design Requirements

- The terminal section (5) is the hero moment — it should feel like opening a Bloomberg terminal for the first time. Dense with data but organized. Make it feel powerful.
- All numbers in JetBrains Mono. Positive values in emerald, negative in red.
- Cards should have subtle colored glow borders matching their engine color (cyan for Feature Discovery, emerald for Regime, amber for NSLM).
- The equity curve chart should be the Chart.js dark theme style: black background, very subtle grid lines (white at 6% opacity), cyan line with fill gradient to transparent.
- Parameter sweep optimal zone should use a gradient highlight (cyan center → transparent edges).
- NSLM reasoning should look like a terminal/code block: dark charcoal background, monospace text, checkmarks in emerald, X marks in red.
- Mobile: terminal splits vertically (model panel on top, results below). Feature table scrolls horizontally.
- Animate: cards fade-in on scroll, KPI numbers count up on load, equity curve draws left-to-right, parameter sweep table rows stagger in.

### What NOT to do

- No light mode
- No stock photos
- No generic SaaS look
- No cluttered dashboards — use progressive disclosure (tabs, accordions, expandable rows)
- No unrealistic numbers — keep performance improvements realistic (not "1000% gains")
- No missing disclaimers — every section with numbers needs "illustrative data" label
