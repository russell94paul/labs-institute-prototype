---
tags: [architecture, frontend, ai-coach, react, neurospect]
aliases: [Coach Frontend Architecture, Phase 4 Frontend]
sources: []
created: 2026-04-24
updated: 2026-04-24
---

# Phase 4 — AI Coach Frontend Architecture

Canonical architecture doc for the AI Coach frontend (Phase 4). Reconciled against shipped code in `app/src/`. The companion backend doc is [[concepts/architecture/tradingview-connector]].

## Routes

Both routes live under `ProtectedLayout` in `src/App.tsx`.

| Path | Page | Purpose |
|---|---|---|
| `/coach` | `CoachPage` | Live coaching panel — polls latest event |
| `/coach/setup` | `CoachSetupPage` | TV token management + Pine script distribution |

`/coach/setup` is linked from a button in the `/coach` page header. It is **not** a sidebar item — the sidebar has a single "AI Coach" nav item pointing at `/coach`.

## Sidebar

`src/components/layout/sidebar.tsx` — `Sparkles` icon from lucide-react. Appended to `navItems` after "New Trade".

## Hooks

### `src/hooks/use-coaching.ts`

- **`useLatestCoachingEvent()`** — `GET /api/coach/events/latest`. Query key `['coach', 'latest']`.
  - 404 response → returns `null` (not an error). Caught via `HTTPError` from ky.
  - Dynamic `refetchInterval`: 2 000 ms when `status === 'pending'`, 10 000 ms otherwise.
  - `refetchIntervalInBackground` not set (defaults to false — polling stops on hidden tabs).
- **`useCoachingEvent(id)`** — `GET /api/coach/events/{id}`. `enabled: !!id`. Kept for future deep-linking.

### `src/hooks/use-tv-token.ts`

- **`useTvToken()`** — `GET /api/coach/tv-token`. Query key `['coach', 'tv-token']`. 404 → `null`.
- **`useRotateTvToken()`** — `POST /api/coach/tv-token`. On success: invalidate `['coach', 'tv-token']`.
- **`useRevokeTvToken()`** — `DELETE /api/coach/tv-token`. On success: invalidate `['coach', 'tv-token']`.

## Types & Constants

### `src/types/api.ts` (coach additions)

```typescript
type CoachBias = 'bullish' | 'bearish' | 'neutral' | 'stand_aside';
type Confidence = 'high' | 'medium' | 'low';
type CoachingEventStatus = 'pending' | 'complete' | 'error';

interface ChecklistItem { id: string; met: boolean; note: string }
interface ValidStrategy { strategy_id: string; confidence: Confidence; checklist: ChecklistItem[]; missing: string[]; watch_for: string }
interface Layer3Response { bias: CoachBias; narrative: string; valid_strategies: ValidStrategy[]; invalid_strategies: string[]; alerts: string[] }
interface CoachingEvent { id: string; status: CoachingEventStatus; instrument: string; alert_timestamp: string; request_payload: Record<string, unknown>; response_payload: Record<string, unknown> | null; error_message: string | null; claude_latency_ms: number | null; created_at: string; completed_at: string | null }
interface TvTokenResponse { token: string; webhook_url: string; created_at: string }
```

Note: `CoachBias` (not `Bias`) avoids collision with the existing `BiasType` trade type (`'bullish' | 'bearish' | 'neutral'`).

### `src/lib/constants.ts` (coach additions)

- `COACH_BIAS_LABELS: Record<CoachBias, string>` — display labels
- `COACH_BIAS_STYLES: Record<CoachBias, string>` — Tailwind classes (bullish=green, bearish=red, neutral=slate, stand_aside=amber), matching status-badge color vocabulary
- `CONFIDENCE_LABELS: Record<Confidence, string>`
- `CONFIDENCE_STYLES: Record<Confidence, string>` (high=green, medium=amber, low=slate)
- `STRATEGY_LABELS: Record<string, string>` — all 7 strategy IDs from `concepts/ai-coach/strategies.json`

## Component Tree

### `/coach` page

```
CoachPage
└── CoachingPanel (src/components/coach/coaching-panel.tsx)
    ├── [loading]  → Skeleton card
    ├── [null/404] → empty-state Card with link to /coach/setup
    ├── [pending]  → EventMeta + animate-pulse text + Skeleton cards
    ├── [error]    → EventMeta + red Card (error_message in <pre> + retry hint)
    └── [complete] → EventMeta + BiasBadge + narrative Card + AlertsBanner + StrategyCard[] + InvalidStrategies
```

### `/coach/setup` page

```
CoachSetupPage
├── TokenCard (src/components/coach-setup/token-card.tsx)
│   ├── [no token]  → "Generate Token" button
│   └── [token]     → masked token, readonly webhook URL + copy, Rotate (Dialog), Revoke (Dialog)
├── PineScriptCard (src/components/coach-setup/pine-script-card.tsx)
│   └── Download button + Collapsible <pre> (fetches /neurospect-coach.pine at mount)
└── TvSetupInstructions (src/components/coach-setup/tv-setup-instructions.tsx)
    └── Numbered steps + security callout
```

### Shared coach components (`src/components/coach/`)

| File | Renders |
|---|---|
| `bias-badge.tsx` | Colored Badge from `COACH_BIAS_STYLES` |
| `confidence-pill.tsx` | Small Badge from `CONFIDENCE_STYLES` |
| `freshness-pill.tsx` | Green/Amber/Gray pill: <5m Fresh / 5–30m Stale(Xm) / ≥30m Stale(Xh) |
| `event-meta.tsx` | `instrument · relativeTime · FreshnessPill · Claude Xms` |
| `checklist-row.tsx` | CheckCircle2 (green, met) or Circle (muted) + title-cased id + note |
| `strategy-card.tsx` | shadcn Card: name + ConfidencePill + ChecklistRow list + missing bullets + watch_for callout |
| `invalid-strategies.tsx` | shadcn Collapsible (default closed); null if empty |
| `alerts-banner.tsx` | Amber Card with AlertTriangle per alert; null if empty |

## Polling Behavior

`useLatestCoachingEvent` uses TanStack Query's `refetchInterval` function form:

```typescript
refetchInterval: (query) => query.state.data?.status === 'pending' ? 2000 : 10000
```

This means:
- While a coaching call is in-flight (`status === 'pending'`): polls every 2s.
- Once complete or error (or no events yet / null): polls every 10s.
- When the browser tab is hidden: polling pauses (TanStack Query default — `refetchIntervalInBackground: false`).
- Navigating away from `/coach` unmounts the component, stopping the query. Navigating back restarts it.

## Pine Script Static Asset

`app/public/neurospect-coach.pine` is a copy of the canonical file at:
`neurospect-wiki/assets/pine/neurospect-coach.pine`

This is served as a static file by Vite (and any static host). The setup page's Download button links to `/neurospect-coach.pine`. The `<PineScriptCard>` collapsible `fetch`es this URL at mount to display the script content.

**Sync rule:** When the wiki Pine file is updated, manually re-copy it to `app/public/`. A note in `app/README.md` records this requirement.

## Status Rendering States

| `CoachingEvent.status` | UI |
|---|---|
| *(loading)* | Skeleton card |
| *(null / 404)* | Empty-state card with link to `/coach/setup` |
| `pending` | EventMeta + "Claude is thinking…" pulse + skeleton strategy cards |
| `complete` | Full panel: EventMeta, BiasBadge, narrative, AlertsBanner, StrategyCards, InvalidStrategies |
| `error` | EventMeta + red card: `error_message` in monospaced `<pre>` + "fire another alert" hint |

## TV Token UX

- **No token:** "Generate Token" button → `POST /api/coach/tv-token` → displays masked token + webhook URL.
- **Rotate:** confirmation Dialog → `POST /api/coach/tv-token` → old token revoked, new token shown. Webhook URL changes (it encodes the token).
- **Revoke:** confirmation Dialog → `DELETE /api/coach/tv-token` → returns to "No active token" state.
- **Copy webhook URL:** `navigator.clipboard.writeText()` with a transient "Copied" confirmation.
- Token display: `token.slice(0, 6) + '…' + token.slice(-6)` (never show full token in UI).

## See Also

- [[concepts/architecture/tradingview-connector]] — backend webhook, Claude call, polling endpoints
- [[concepts/architecture/phase3-frontend-structure]] — frontend project structure + trade journal patterns
- [[processes/distributed-workflow/active/ai-coach]] — full workstream tracker
