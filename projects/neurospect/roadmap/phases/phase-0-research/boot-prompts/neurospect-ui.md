# NeuroSpect Interactive Marketing Site (neurospect-ui/) — Boot Prompt

_Generated 2026-05-13. Primary marketing codebase — replaces site/ (Astro SSG)._

## What This Is

React 18 CDN-based interactive marketing site. No build step — React and Babel loaded from CDN, JSX compiled in-browser. Richer interactivity than the original Astro site: SVG equity curves, candlestick chart simulator, typing-animation AI coach demo, interactive course system, architecture diagram with hover states.

## Tech Stack

- React 18.3.1 (UMD from unpkg CDN)
- Babel 7.29.0 (in-browser JSX transpilation)
- Custom CSS with design tokens (no Tailwind)
- Fonts: Inter (body), JetBrains Mono (data), Orbitron (display)
- No package.json, no build tooling, no bundler

## Relationship to Other Codebases

- `neurospect-ui/` = marketing site (this)
- `site/` = DEPRECATED (original Astro SSG marketing site)
- `app/` = product application (React 19 + TS, separate)
- `design-handoff/` = design specs that informed both codebases

## File Inventory

### Entry Points
- `NeuroSpect v2.html` — Main v2 entry point with hash routing
- `NeuroSpect v2 standalone-src.html` — Portable version
- `NeuroSpect.html` — Original v1 (1.7MB bundled, legacy)

### V2 Components (primary)
- `v2/v2-shell.jsx` — Sidebar router, shared components, SVG icons
- `v2/v2-home-course.jsx` — Home + course pages
- `v2/v2-backtesting.jsx` — Backtesting/EdgeLab interface
- `v2/v2-pages.jsx` — Features, performance, architecture pages
- `v2/v2-compare-deep.jsx` — Comparison + pricing pages
- `v2/v2-styles.css` — V2 design system

### V1 Components (still loaded)
- `ns-nav-hero.jsx` — Navigation, hero, scroll reveal
- `ns-features.jsx` — EdgeLab Research Studio features
- `ns-course.jsx` — Interactive course with modules
- `ns-performance.jsx` — SVG equity curve visualization
- `ns-simulator.jsx` — Candlestick chart simulator
- `ns-coach.jsx` — AI coaching demo with typing animation
- `ns-coach-compare.jsx` — Coach comparison interface
- `ns-platform-arch.jsx` — Architecture diagram
- `tweaks-panel.jsx` — Design system controls

### Data Files
- `ns-data.js` — Trading days, tier metadata, equity curves, KPIs, trade markers, components, pricing
- `ns-course-data.js` — 5-module curriculum with lessons, concepts, rules
- `ns-features-data.js` — EdgeLab engines, workflow steps, feature dimensions
- `ns-competitors-data.js` — Competitor comparison data

### Content
- `uploads/course/` — Course markdown content
- `uploads/entry-models/` — Entry model documentation
- `uploads/ict-*.md` — ICT concept reference files
- `uploads/neurospect-adaptive-edge-engine-design-doc.md` — Historical design doc (canonical name is now "EdgeLab Research Studio")

## Pages (V2 Hash Routes)
- `#home` — Landing page with hero, stats, pain points
- `#course` — Interactive ICT course (5 modules)
- `#backtesting` — EdgeLab backtesting interface
- `#performance` — Equity curve comparison (4 tiers)
- `#architecture` — 6-component platform architecture
- `#features` — EdgeLab Research Studio (3 engines)
- `#compare` — Competitive comparison
- `#pricing` — 6 pricing tiers

## Design System
- Background: pure black
- Primary accent: cyan (#06b6d4)
- Neon card system: glassmorphic cards with colored border glow (cyan, purple, amber, emerald, rose, red)
- CSS custom properties for all tokens
- Scroll-triggered reveal animations via IntersectionObserver

## App Navigation
A "Launch App" link should be present in the nav, pointing to the product app (app.neurospect.ai or localhost:5173 for dev).

## Known Issues Fixed
- "Sovereign Architect" renamed to "S-Tier Trader" (2026-05-13)
- "Adaptive Edge Engine" renamed to "EdgeLab Research Studio" (2026-05-13)
