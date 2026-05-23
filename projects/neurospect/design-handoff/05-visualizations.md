# NeuroSpect Marketing Site — Visualization & Interaction Specs

## Design Philosophy for Visualizations

Every visualization should:
- Feel like a **real trading platform**, not a marketing mockup
- Be **interactive** — hover, click, toggle, expand
- Use **real-looking data** (illustrative but plausible NQ futures data)
- Show **why NeuroSpect matters** through the data itself
- Have smooth, polished transitions that feel premium
- Reinforce the tier progression story (Discretionary → Quant → Hybrid → S-Tier)

---

## 1. AI Coach Chat Demo (Landing Page)

**Current:** Static HTML mockup of a chat conversation

**Enhancement goals:**
- Typing animation on AI responses (character by character or word by word)
- Message bubbles slide in from bottom with stagger
- Checklist items animate in one by one (pass/fail icons pop with a micro-animation)
- Source citation links pulse subtly on first appearance
- Optional: multiple example conversations that auto-cycle (carousel of 3 different ICT scenarios)
- The chat should feel ALIVE — like the AI is actually responding in real-time

**Suggested scenarios to cycle through:**
1. FVG stop sweep analysis (current)
2. "Should I take this Silver Bullet setup?" — pre-session prep with real-time checklist
3. "Why do I keep losing on Wednesdays?" — journal-driven coaching with day-of-week insight

---

## 2. Equity Curve Chart (Performance Page)

**Current:** Chart.js line chart with 4 tier curves over 20 trading days, clickable trade markers

**Tier colors:**
- Tier 1 (Discretionary): Slate `rgba(100, 116, 139)`
- Tier 2 (Quant): Purple `rgba(139, 92, 246)`
- Tier 3 (Hybrid): Cyan `rgba(6, 182, 212)`
- Tier 4 (S-Tier): Emerald `rgba(16, 185, 129)`

**Data:** 20 trading days (May 2026 NQ futures), starting equity $25,000 per tier. Tier 4 ends highest, Tier 1 lowest. 8 annotated trade markers on specific dates.

**Enhancement goals:**
- Lines should draw on progressively when scrolled into view (animated from left to right)
- Trade markers (amber dots on Tier 1 line) should pulse to indicate clickability
- On marker click, a slide panel opens from the right showing per-tier trade outcomes
- Tier toggle buttons should animate the line in/out (not just hide/show)
- Tooltip should feel premium: dark glass background, per-tier color coding, marker callout
- Consider: animated vertical crosshair that follows mouse on hover
- Consider: background candle/bar chart texture (very subtle, 5% opacity) to reinforce "trading terminal" feel
- The chart area should have a subtle neon glow matching the dominant line color

**Interaction flow:**
1. User scrolls down → chart area enters viewport
2. Lines animate from left to right over 1.5s
3. Trade markers appear with a pop/pulse
4. User hovers → crosshair + tooltip with all 4 tier values
5. User clicks amber marker → slide panel opens with trade detail
6. User toggles tier buttons → lines fade in/out smoothly

---

## 3. Trade Detail Slide Panel (Performance Page)

**Current:** Right-side slide panel (440px) triggered by chart marker clicks

**Content per marker:**
- Trade title, date, session, setup type
- Market context paragraph
- 4 tier outcome cards (each showing: action entered/skipped, result win/loss/BE, PnL, explanation bullets, mistakes for Tier 1)
- "What Tier 1 Needed" solution block (amber card)

**Enhancement goals:**
- Panel slides in with spring physics (slight overshoot + settle)
- Tier outcome cards stagger in from right
- PnL numbers should count up/down to their value
- Win results have subtle green pulse, loss results have subtle red pulse
- Backdrop overlay dims the chart behind
- Consider: mini sparkline per tier showing equity around that trade date
- Close on Escape key, backdrop click, or X button

---

## 4. Day-of-Week Bar Chart (Performance Page, Analytics Tabs)

**Current:** Chart.js grouped bar chart (4 tiers x 5 days)

**Enhancement goals:**
- Bars should grow upward from baseline on tab open
- Negative bars (loss days) grow downward with red tint
- On hover, highlight all bars for that day and dim others
- Consider: small win-rate percentage overlay on each bar
- Consider: animated gradient fill on bars instead of flat color

---

## 5. Analytics Tab System (Performance Page)

**Current:** 5 tabs (Day of Week, Sessions, Setups, Mistakes, Risk) with panel switching

**Tabs:** Day of Week | Sessions | Setups | Mistakes | Risk

**Enhancement goals:**
- Tab indicator should slide smoothly between positions (animated underline)
- Panel content should cross-fade (not just show/hide)
- Tables should have row hover highlighting
- Consider: micro-charts inline in table cells (small sparklines for trends)
- Mistakes panel: severity badges should pulse on "high" severity items
- Risk panel: consistency score and recovery factor should have circular progress indicators

---

## 6. Tier Accordion (Performance Page)

**Current:** 4 expandable panels, one open at a time, chevron rotation

**Enhancement goals:**
- Panel expand should have smooth height animation (spring easing)
- Content inside should fade in as panel opens
- Color bar on left should glow when panel is open
- Consider: auto-expand the first tier on scroll into view
- Metric values should count up when panel first opens

---

## 7. Architecture Diagram (Architecture Page)

**Current:** Inline SVG with 6 component nodes, animated dashed connection lines with flowing particles, layer labels

**Component nodes:**
- NeuroSpect Mentor (top center, cyan)
- NeuroCore (left middle, purple)
- NSLM (right middle, amber)
- EdgeLab (left lower, emerald)
- NeuroQuant (right lower, rose)
- NeuroTrader (bottom center, red)

**Connections (with labels):**
- NeuroCore → Mentor: "retrieval"
- NSLM → Mentor: "generation"
- NeuroCore → EdgeLab: "data"
- EdgeLab → NSLM: "evaluation"
- EdgeLab → NeuroQuant: "promotion"
- NeuroQuant → NeuroTrader: "scoring"

**Enhancement goals:**
- Node hover should brighten the node's glow and highlight its connections (dim all others)
- Click a node → scroll to its detail card below and highlight it
- Particles should have a glowing trail/comet effect, not just a dot
- Connection labels should appear on hover (hidden by default to reduce clutter)
- Consider: data flow animation that shows a "request" traveling from Mentor → NeuroCore → back to Mentor (end-to-end flow storytelling)
- Consider: subtle parallax — nodes shift slightly on mouse move for depth
- Layer labels (CONSUMER, INTELLIGENCE, RESEARCH, AUTOMATION) should be more prominent
- The entire diagram should feel like a living system, not a static chart
- Consider: "Activate" button that triggers a full data-flow animation sequence

---

## 8. Capability Matrix (Compare Page)

**Current:** HTML table with checkmark/partial/no icons, horizontal scroll on mobile

**14 capabilities x 7 tools (6 competitors + NeuroSpect)**

**Enhancement goals:**
- NeuroSpect column should have a persistent glow/highlight
- On row hover, highlight the entire row and show which tools fail
- Consider: animate the checkmarks filling in column-by-column from left to right
- Footer summary row should have a progress bar per column showing coverage %
- Consider: filter/sort capability rows by category
- Mobile: consider a card-based layout instead of horizontal scroll table

---

## 9. Subscription Stack (Compare Page)

**Current:** 2-column layout: Before (8 tools with costs) vs After (NeuroSpect)

**Enhancement goals:**
- "Before" items should stack with a slight delay, each appearing with a red pulse
- After the stack builds, the total should count up to $125-$710
- Then the NeuroSpect card slides in from the right with a satisfying glow
- The price contrast should be visceral — maybe a visual "collapse" animation where the 8 tool cards compress into the single NeuroSpect card
- Consider: animated savings counter showing dollar difference

---

## 10. Workflow Before/After (Compare Page)

**Current:** 2 columns of 7 numbered steps with connector lines

**Enhancement goals:**
- Steps should draw in top-to-bottom with connector line animation
- "Before" steps appear in red/muted, "After" steps in brand cyan
- Connector lines should animate (dash flow)
- Context switch indicators between "Before" steps (small "switch" icon)
- Consider: side-by-side animation where both columns build simultaneously
- KPI cards below should count up when scrolled into view

---

## 11. Trader Maturity Progression (Performance Page)

**Current:** 4 tier cards showing trader progression

**Enhancement goals:**
- Cards should connect with an animated progression arrow
- Each tier card should have a mini metric (e.g., typical win rate, typical drawdown)
- Active tier should glow more prominently
- Consider: user can "select" a tier and the entire page filters to show that tier's data prominently

---

## 12. Pricing Cards (Pricing Page)

**Current:** 6 cards in a 3x2 grid, "Most Popular" badge on Trader

**Enhancement goals:**
- "Most Popular" card should have stronger glow and slight scale-up (1.02x)
- On hover, card lifts and glow intensifies
- Feature checkmarks should animate in on scroll
- Consider: toggle between monthly/annual pricing (with discount callout)
- Consider: feature comparison expansion — click "Compare all features" to see full matrix
- Price numbers should count up from $0 when scrolled into view

---

## Global Interaction Patterns

### Waitlist Form
- Input focus: border glows brand-500, subtle inner glow
- Submit: button should have loading state (spinner or progress)
- Success: form slides up and away, success message fades in with checkmark animation
- Consider: show waitlist position number ("You're #247 on the list")

### Scroll Progress
- Consider: thin progress bar at top of page (brand-500 gradient)
- Consider: section dots on right edge for long pages (Performance, Compare)

### Page Transitions
- If Astro View Transitions are enabled: cross-fade between pages with shared nav
- Consider: page-specific loading animations (chart sketch → render for Performance page)

### Mobile
- All charts must be touch-friendly (tap instead of hover)
- Slide panel should be full-screen on mobile
- Tab bar should be horizontally scrollable
- Consider: swipe between tabs on mobile
