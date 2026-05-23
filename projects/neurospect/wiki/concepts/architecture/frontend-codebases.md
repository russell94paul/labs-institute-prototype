---
tags: [architecture, frontend, neurospect]
corpus_type: development
created: 2026-05-13
updated: 2026-05-13
---

# Frontend Codebases

NeuroSpect has three frontend codebases, each serving a different purpose.

## Active Codebases

### neurospect-ui/ — Marketing Site

**Status:** Active, primary marketing codebase
**Tech:** React 18.3.1 (CDN), Babel 7.29.0 (in-browser JSX), custom CSS
**Purpose:** Interactive marketing site, waitlist capture, product demos
**Deployment:** Static HTML files (Cloudflare Pages or similar)

Pages: home, course, backtesting, performance, architecture, features, compare, pricing
Key features: SVG equity curves, candlestick simulator, typing AI coach demo, interactive course modules, architecture diagram

### app/ — Product Application

**Status:** Active, in development
**Tech:** React 19 + TypeScript, Vite
**Purpose:** The actual trading platform — journal, coaching, analytics, EdgeLab, NeuroQuant
**Deployment:** Cloudflare Pages or similar (with API backend)

Pages: login, dashboard, coach, trades, new-trade, settings, trade-detail, coach-setup, auth-callback

## Deprecated

### site/ — Original Marketing Site

**Status:** Deprecated (2026-05-13), replaced by neurospect-ui/
**Tech:** Astro 5.8 + Tailwind 3.4 + Chart.js
**Reason for deprecation:** neurospect-ui/ provides richer interactivity (SVG charts, candlestick simulator, typing animations) with a simpler deployment model (no build step).

## Relationship

```
neurospect-ui/ (marketing) ──[Launch App]──→ app/ (product)
                                              ↑
                              app.neurospect.ai or localhost:5173
```

The marketing site links to the product app via a "Launch App" nav button. They are separate deployments with no shared runtime.

## See Also

- Boot prompt: `roadmap/phases/phase-0-research/boot-prompts/neurospect-ui.md`
- Design specs: `design-handoff/`
