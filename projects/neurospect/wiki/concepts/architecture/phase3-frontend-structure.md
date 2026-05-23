---
tags: [architecture, frontend, neurospect, phase3]
aliases: [Frontend Architecture, Neurospect App Structure]
sources: []
created: 2026-04-23
updated: 2026-04-26 (1c)
---

# Phase 3 — Frontend Architecture

Canonical doc for the React frontend at `app/` (formerly the `neurospect-app` repo). The code in `app/` is the source of truth; this doc describes the architecture as implemented after Phase 3 Session 3.

## Tech Stack

| Layer | Choice | Version |
|---|---|---|
| Framework | React | 19 |
| Language | TypeScript | 5.x |
| Build tool | Vite | 6 |
| Routing | React Router | v7 (data router) |
| Server state | TanStack Query | v5 |
| Forms | React Hook Form + Zod | latest |
| HTTP client | ky | v1 |
| UI components | shadcn/ui (Radix + Tailwind) | latest |
| Charts | Recharts | latest |
| Utilities | date-fns, Lucide React | latest |

## Project Layout

```
app/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── sidebar.tsx        # Fixed left nav (Desktop + mobile Sheet); Settings link added in 1c
│   │   │   ├── user-menu.tsx      # Discord avatar + Logout dropdown
│   │   │   └── app-shell.tsx      # Flex container: sidebar | main + Outlet; ActiveTradeBadge + BrokerDisconnectedBanner added in 1c
│   │   ├── settings/              # Added in 1c
│   │   │   ├── settings-shell.tsx     # Sidebar nav ("Broker Connections") + children slot
│   │   │   ├── broker-credentials-form.tsx  # Token-paste form; POST /credentials/token
│   │   │   ├── broker-status-card.tsx       # Connection status, test button, disconnect
│   │   │   └── auto-fetch-toggle.tsx        # Manual / Automatic radio; persists to localStorage
│   │   ├── trade/
│   │   │   ├── status-badge.tsx   # Colored Badge per trade status/outcome
│   │   │   ├── mistake-tag-input.tsx # Tag input with suggestions
│   │   │   ├── pre-trade-fields.tsx  # Pre-trade RHF fieldset
│   │   │   ├── entry-fields.tsx      # Entry RHF fieldset; TradovateFillButton added in 1c
│   │   │   ├── post-trade-fields.tsx # Post-trade RHF fieldset; TradovateFillButton added in 1c
│   │   │   ├── trade-form.tsx        # Main form; handleEntryFillApplied / handleExitFillApplied added in 1c
│   │   │   ├── trade-card.tsx        # Compact list card
│   │   │   ├── trade-filters.tsx     # URL-driven filter bar
│   │   │   ├── tradovate-fill-button.tsx        # "Fetch from Tradovate" with disabled states + picker (added 1c)
│   │   │   ├── tradovate-fill-picker-dialog.tsx # Multi-fill picker dialog (added 1c)
│   │   │   └── active-trade-guard-dialog.tsx    # 409 guard modal for NewTradePage (added 1c)
│   │   ├── screenshot/
│   │   │   ├── screenshot-upload.tsx # Per-phase drag-and-drop upload zone
│   │   │   ├── screenshot-grid.tsx   # Thumbnail grid grouped by phase + delete
│   │   │   └── screenshot-viewer.tsx # shadcn Dialog lightbox
│   │   └── analytics/
│   │       ├── summary-cards.tsx     # 8-card stat grid
│   │       ├── breakdown-table.tsx   # Sortable table (setup, session, instrument)
│   │       ├── day-of-week-chart.tsx # Recharts BarChart with per-bar coloring
│   │       ├── mistake-chart.tsx     # Horizontal BarChart sorted by frequency
│   │       └── r-distribution.tsx   # Histogram with green/red/amber bucket colors
│   ├── hooks/
│   │   ├── use-trades.ts        # useTrades, useTrade, useCreateTrade, useUpdateTrade, useDeleteTrade
│   │   ├── use-screenshots.ts   # useScreenshots, useUploadScreenshot, useDeleteScreenshot
│   │   ├── use-analytics.ts     # useSummary, useBySetup, useBySession, useByInstrument,
│   │   │                        #   useByDayOfWeek, useMistakes, useRDistribution
│   │   ├── use-tradovate.ts     # useBrokerCredentials, useSaveBrokerToken, useTestBrokerCredentials,
│   │   │                        #   useDeleteBrokerCredentials, useFetchTradovateFills,
│   │   │                        #   useApplyTradovateFill (added 1c)
│   │   └── use-active-trade.ts  # useActiveTrade() → Trade | null (added 1c)
│   ├── lib/
│   │   ├── api.ts      # ky instance: baseUrl + Bearer injection + 401 → /login redirect
│   │   ├── auth.ts     # AuthProvider context: token/user/isLoading, login/debugLogin/logout
│   │   ├── constants.ts # All ENUM label maps + Select option arrays + COMMON_MISTAKE_TAGS
│   │   └── utils.ts    # cn(), formatDate(), formatDecimal(), formatPercent()
│   ├── pages/
│   │   ├── login.tsx          # Discord OAuth + Debug Login (VITE_DEBUG=true)
│   │   ├── auth-callback.tsx  # Exchanges OAuth code for JWT, stores token, nav to /dashboard
│   │   ├── dashboard.tsx      # Analytics dashboard (all 6 chart/table components)
│   │   ├── trades.tsx         # Trade list with URL-driven filters + pagination
│   │   ├── new-trade.tsx      # Create mode (TradeForm with no trade prop); ActiveTradeGuardDialog added in 1c
│   │   ├── trade-detail.tsx   # Edit mode (TradeForm + Screenshots section)
│   │   └── settings-broker.tsx # /settings/broker — SettingsShell + credentials form + status card + toggle (added 1c)
│   ├── types/
│   │   └── api.ts   # All TypeScript interfaces mirroring backend Pydantic schemas + 11 ENUM types
│   ├── App.tsx      # createBrowserRouter: /login, /auth/callback, ProtectedLayout + 5 child routes
│   └── main.tsx     # QueryClientProvider → AuthProvider → RouterProvider
└── .env.example     # VITE_API_URL, VITE_DISCORD_CLIENT_ID, VITE_DISCORD_REDIRECT_URI, VITE_DEBUG
```

## Routes

| Path | Component | Protection |
|---|---|---|
| `/login` | LoginPage | Public |
| `/auth/callback` | AuthCallbackPage | Public |
| `/` | → `/dashboard` redirect | Protected |
| `/dashboard` | DashboardPage | Protected |
| `/trades` | TradesPage | Protected |
| `/trades/new` | NewTradePage | Protected |
| `/trades/:id` | TradeDetailPage | Protected |
| `/settings` | → `/settings/broker` redirect | Protected |
| `/settings/broker` | BrokerSettingsPage | Protected |

`ProtectedLayout` checks `token` from `useAuth()` and redirects to `/login` if absent.

## Key Patterns

### Auth
- JWT stored in `localStorage('neurospect_token')`.
- `AuthProvider` lives outside `RouterProvider` — uses `window.location.href` (not `useNavigate`) for redirects.
- Debug login via `POST /auth/debug/token {discord_id}` when `VITE_DEBUG=true`.
- ky `beforeRequest` hook injects `Authorization: Bearer <token>`. `afterResponse` hook clears token and redirects to `/login` on 401.

### Trade Form
- Single `<TradeForm>` handles both create and edit modes (no separate view mode).
- Three collapsible sections: Pre-Trade, Entry, Post-Trade.
- PATCH sends only dirty fields (`dirtyFields` from React Hook Form).
- R-multiple auto-calculated from entry/stop/exit prices (user can override).
- Zod schema uses `z.string()` for ENUM fields (not `z.enum([...])`) to avoid duplicating all backend values. Backend validates ENUM correctness.

### Screenshot Upload
- Per-phase drag-and-drop upload zones are rendered based on `trade.status` (see `PHASE_SETS` map in `trade-detail.tsx`).
- Uploads use `FormData` with `file` + `phase` fields.
- `staleTime: 30 * 60 * 1000` (presigned URLs expire in 1hr).
- Uploads will 503 locally (R2 not configured in local dev) — graceful error message shown.

### Analytics Hooks — Response Shape
The backend wraps breakdown responses in containers:
- `GET /api/analytics/by-setup` → `{ rows: BreakdownRow[] }` (not flat array)
- `GET /api/analytics/by-session` → `{ rows: BreakdownRow[] }`
- `GET /api/analytics/by-instrument` → `{ rows: BreakdownRow[] }`
- `GET /api/analytics/by-day-of-week` → `{ rows: DayOfWeekRow[] }`
- `GET /api/analytics/mistakes` → `{ rows: MistakeRow[] }`
- `GET /api/analytics/r-distribution` → `{ buckets: RBucket[], bins, r_min, r_max }`
- `GET /api/analytics/summary` → flat `SummaryStats` (no wrapper)

The hooks in `use-analytics.ts` extract the inner array via `.then(r => r.rows)` / `.then(r => r.buckets)` so consumers receive the correct typed array directly.

### Dashboard
- `DashboardPage` composes all analytics components. Each component manages its own loading and empty states.
- Empty state (zero total trades) shows a full-page CTA rather than empty charts.
- ENUM label maps (`Record<EnumType, string>`) are cast to `Record<string, string>` at call sites — TypeScript limitation with index-signature assignability.

## Environment Variables

Defined in `.env.example`:

| Variable | Purpose |
|---|---|
| `VITE_API_URL` | Backend base URL (default `http://localhost:8000`) |
| `VITE_DISCORD_CLIENT_ID` | Discord application client ID (for real OAuth) |
| `VITE_DISCORD_REDIRECT_URI` | OAuth callback URL |
| `VITE_DEBUG` | If `"true"`, shows Debug Login UI |

## Development Setup

```bash
cd app
npm install
cp .env.example .env   # fill in as needed
npm run dev            # Vite dev server at localhost:5173
```

Backend must be running at `localhost:8000` with `DEBUG=true` in `.env`.

## See Also

- [[concepts/architecture/tech-stack]] — backend stack decision
- [[concepts/architecture/trade-schema]] — ICT trade data model and REST API surface
- [[concepts/architecture/phase2-project-structure]] — backend project layout
- [[processes/distributed-workflow/active/journal-analytics]] — implementation tracker with all session logs and decisions
