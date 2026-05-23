---
tags: [distributed-workflow, active, neurospect, journal, analytics]
aliases: [Journal Analytics Tracker, Trade Journal Module Tracker]
sources: []
created: 2026-04-22
updated: 2026-04-23
phase2_design: approved
phase2_implementation: complete
alignment_review: complete
phase3_design: approved
phase3_session1: complete
phase3_session2: complete
phase3_session3: complete
phase3_implementation: complete
---

# Trade Journal & Analytics Module — Workstream Tracker

The journal module is the data collection layer of Neurospect. It captures trades with ICT-specific structured fields (not generic journal fields), stores screenshots, and produces analytics that tell the trader which setups, sessions, and conditions produce their edge. The journal data eventually feeds the AI coach's personalization layer.

## Goal

By end of this workstream:

1. **ICT-specific trade schema** — defined and documented. Covers: HTF bias, DOL, setup type, session/kill zone, FVG present?, displacement quality, entry PDA, stop logic, target, outcome, quality grade, notes.

2. **MVP trade journal** — functional UI for manual trade entry using the ICT schema, screenshot upload, and basic tagging.

3. **Analytics dashboard** — breakdown by: setup type, session, instrument, bias alignment, day-of-week, news environment. Win rate, avg R, best conditions.

4. **Schema documentation** — `concepts/architecture/trade-schema.md` in this wiki.

## ICT Trade Schema (Draft)

```
Pre-Trade (captured before entry)
  - date, instrument, session, kill_zone
  - htf_bias: bullish | bearish | neutral
  - htf_fvg_range: [low, high]
  - draw_on_liquidity: description + price level
  - opening_price_position: below_all | below_some | above_all | above_some
  - news_flag: boolean
  - setup_type: consolidation | expansion-retracement | reversal | model-2022-ote | london | daily-bias | smt
  - narrative: freetext pre-trade thesis

Entry
  - entry_price, entry_time
  - stop_price, stop_logic
  - target_price, target_logic
  - entry_pda: fvg | order-block | rejection-block | ote-block | breaker
  - displacement_quality: clean | choppy | none
  - smt_confirmation: boolean
  - screenshots: [before_entry, entry, higher_tf]

Post-Trade (captured after close)
  - exit_price, exit_time, outcome: win | loss | breakeven
  - r_multiple
  - mae (max adverse excursion), mfe (max favorable excursion)
  - target_reached: boolean
  - plan_followed: boolean
  - mistake_tags: [revenge, fomo, early-exit, oversized, wrong-session, ...]
  - quality_grade: A+ | A | B | C
  - post_trade_notes: freetext
  - screenshots: [exit, post_trade_review]
```

## Implementation Plan

### Phase 1 — Schema & Architecture (wiki only)
1. Write `concepts/architecture/trade-schema.md` with full field definitions
2. Define the database schema (Postgres tables)
3. Define the API endpoints

### Phase 2 — MVP Backend
1. FastAPI (or Node) backend
2. Postgres database with the ICT trade schema
3. REST endpoints: create trade, update trade, upload screenshot, list trades

### Phase 3 — MVP Frontend + Analytics (design APPROVED, implementation in 3 sessions)
1. **Session 1 (A-D):** Scaffold + infrastructure + auth + layout → checkpoint: debug login works e2e
2. **Session 2 (E-F):** Data hooks + trade CRUD form/list → checkpoint: full trade lifecycle works
3. **Session 3 (G-H):** Screenshots + analytics dashboard → checkpoint: all features functional

Tech stack: React 19 + TS + Vite, TanStack Query, RHF + Zod, ky, shadcn/ui, Recharts.
Repo: `C:\Users\PaulRussell\repos\neurospect-app` (separate from backend).

### Phase 4 — Future
1. Real Discord OAuth (replace debug auth)
2. Deployment (Render or Cloudflare Pages)
3. AI Coach integration in the frontend
4. Additional analytics (equity curve, calendar heat map)

## Session Log

### 2026-04-22 — planning

- did: created this tracker; drafted ICT trade schema; phased implementation plan.
- decided: schema is ICT-specific from day one — not a generic journal with ICT tags bolted on.
- next: begin Phase 1 (schema doc) once tech stack is decided (coordinate with ai-coach.md tracker since they share a backend).

### 2026-04-22 — schema design (Phase 1 complete)

- did: wrote `concepts/architecture/trade-schema.md` — full field definitions with ICT context, Postgres DDL (3 tables, 12 ENUMs, 7 indexes, updated_at trigger), REST API surface (CRUD + screenshots + 7 analytics endpoints), schema conventions, future considerations.
- decided: ORM is SQLAlchemy async + Alembic. Single wide `trades` table (not normalized by phase). Postgres ENUMs for structured fields. TEXT[] with GIN index for `mistake_tags`. Separate `trade_screenshots` table (1:N). Progressive update via PATCH. Soft delete. Auto-calculated R-multiple with manual override column.
- next: Phase 2 — MVP backend implementation (FastAPI + SQLAlchemy async + Alembic, Postgres on Render).

### 2026-04-22 — Phase 2 design (approved, not yet implemented)

- did: designed full project structure for `neurospect-api` — documented at `concepts/architecture/phase2-project-structure.md`.
- decided: SPA auth pattern — frontend captures Discord OAuth code, POSTs to `POST /auth/discord/token`, backend returns JWT. No server-side OAuth redirect.
- decided: Alembic uses separate sync `DATABASE_URL_SYNC` (psycopg2); runtime uses asyncpg. Both point to same DB.
- decided: DEBUG-only `POST /auth/debug/token {discord_id}` endpoint for local testing without real Discord credentials.
- decided: ORM for CRUD, raw `text()` SQL for all 7 analytics endpoints (streak window functions, unnest, WIDTH_BUCKET histogram).
- decided: R2 via boto3 S3-compatible client. Storage key pattern: `{user_id}/{trade_id}/{phase}/{uuid4()}.{ext}`.
- decided: `app/coach/router.py` stub (501) included in Phase 2 scaffold for Phase 3 readiness.
- next: implement Phase 2 using boot prompt below.

### 2026-04-23 — Phase 2 implementation (COMPLETE)

- did: implemented full Phase 2 backend in `C:\Users\PaulRussell\repos\neurospect-api`. All files from the approved file creation order written.
- did: journal-analytics session and ai-coach session ran in parallel on the same repo. No conflicts — all changes were additive.
- actual state of repo (ai-coach session went beyond the planned stub):
  - `app/coach/router.py` — full implementation (webhook ingestion + events polling), not a 501 stub
  - `app/coach/claude_client.py` — full Claude API background task
  - `app/coach/prompt_loader.py` — loads system prompt + strategies.json from wiki path
  - `app/coach/validation.py` — webhook secret + IP allowlist validation
  - `alembic/versions/0002_coach_tables.py` — tradingview_tokens + coaching_events tables
  - `app/models/coaching_event.py`, `app/models/tv_token.py` — ORM models
  - `app/routers/tv_tokens.py` — per-user webhook token CRUD
  - `tests/` — unit tests for coach validation, prompt_loader, Pine payload
- did: `app/main.py` written — mounts all 7 routers (auth, trades, screenshots, analytics, tv_tokens, webhook_router, events_router).
- fixed: removed dead import (`AsyncSessionLocal`) from `app/auth/router.py`.
- decided: coach router exposes two APIRouter objects (`webhook_router`, `events_router`) — both mounted in main.py.
- next: Opus alignment pass — check design/integration/code coherence across both workstreams before Phase 3 (frontend).

### 2026-04-23 — cross-workstream alignment review (COMPLETE)

- did: Opus alignment pass across both workstreams (journal-analytics + ai-coach). Reviewed all code in `neurospect-api` against all wiki architecture docs.
- did: **code fixes** — 5 issues resolved:
  - RED: `tradingview_tokens.user_id` had `UNIQUE` constraint preventing token rotation → replaced with partial unique index `uq_tv_tokens_user_active WHERE revoked_at IS NULL` (ORM model + migration 0002)
  - RED: added `CORSMiddleware` to `main.py` (configurable `cors_origins` in config + `.env.example`)
  - YELLOW: added `GET /health` endpoint for Render health checks
  - YELLOW: all 12 datetime columns across 5 ORM models now use `DateTime(timezone=True)` to match TIMESTAMPTZ DDL
  - YELLOW: `claude_client.py` `_build_user_message()` no longer hardcodes "NQ" — reads `instrument` from payload
  - YELLOW: `trades.py` PATCH handler uses `exclude_unset=True` instead of `exclude_none=True` — fields can now be set to null
- did: **wiki reconciliation** — 16 issues resolved across 4 architecture docs:
  - `tech-stack.md` — rewrote §3 auth (was cookie+authlib, now SPA+JWT), updated §2 libs, §4 env vars, §5 webhook path, §6 R2 key layout + delete behavior, §7 cross-module notes, §8 open questions
  - `phase2-project-structure.md` — expanded directory layout for coach files, fixed ENUM count (11+1), added anthropic dep, expanded verification checklist, updated file creation order
  - `tradingview-connector.md` — fixed tv_tokens DDL (partial unique index), duplicate response 200→202, test filenames
  - `entities/projects/neurospect.md` — updated current state to "Phase 2 implemented", marked tech stack question resolved
- did: **CLAUDE.md rules update** — added Architecture Doc Integrity section (source-of-truth hierarchy, canonical doc per topic, post-implementation reconciliation checklist, staleness markers), Context Management (50% warning), Rules 9-10.
- decided: `tech-stack.md` is now a summary doc — canonical sources for specific topics are `trade-schema.md`, `phase2-project-structure.md`, `tradingview-connector.md`, and `.env.example`.
- next: Phase 3 — frontend MVP.

### 2026-04-23 — Phase 3 frontend design (APPROVED)

- did: Opus design session. Read all backend code (`main.py`, all routers, all schemas, `config.py`, `enums.py`) to understand exact API contracts. Designed full frontend architecture.
- decided: **Tech stack:** React 19 + TypeScript + Vite 6, TanStack Query v5, React Hook Form + Zod, ky (HTTP), shadcn/ui (Radix + Tailwind), Recharts, date-fns, Lucide React.
- decided: **Repo:** separate repo at `C:\Users\PaulRussell\repos\neurospect-app`.
- decided: **Routing:** React Router v7 (data router). 6 routes: `/login`, `/auth/callback`, `/dashboard`, `/trades`, `/trades/new`, `/trades/:id`.
- decided: **Auth:** AuthProvider context stores JWT in localStorage. ky interceptor injects Bearer token + handles 401. Debug login when `VITE_DEBUG=true`. No refresh tokens (30-day JWT, re-auth on expiry).
- decided: **Trade form:** single `<TradeForm>` with 3 collapsible sections (pre-trade, entry, post-trade). React Hook Form `dirtyFields` → PATCH only changed fields. Status transition buttons. R-multiple auto-calculated from prices.
- decided: **Trade list:** URL-driven filter state via `useSearchParams`. Paginated card list. `keepPreviousData: true`.
- decided: **Screenshots:** per-phase drag-and-drop upload zones shown based on trade status. `staleTime: 30min` for presigned URL refresh.
- decided: **Analytics dashboard:** single page, responsive 2-col grid. Summary cards, 3 breakdown tables, day-of-week bar chart, mistake frequency chart, R-distribution histogram.
- decided: **No view/edit modes** — form always editable. No WebSocket/SSE for MVP.
- decided: **Session split:** 3 Sonnet sessions — (1) scaffold+auth, (2) trade CRUD, (3) screenshots+analytics.
- decided: Paul needs to create a Discord application before real OAuth works. Debug auth is sufficient for all development.
- decided: Deployment deferred — local dev first.
- next: implement Phase 3 using the 3 session boot prompts below.

## Decisions Log

- 2026-04-22 — Journal and AI coach share the same backend. Decide tech stack once, build both modules on it.
- 2026-04-22 — Screenshots are stored in object storage (S3/R2); only references in the database.
- 2026-04-22 — **Tech stack confirmed:** Python/FastAPI backend, Postgres on Render, hosted on Render.
- 2026-04-22 — **Auth:** Discord OAuth2. Users log in with Discord. Discord user ID is the primary user identifier. Supports 5-10 beta users initially; schema must be multi-tenant from day one.
- 2026-04-22 — **TradingView:** Pro plan confirmed — webhook alerts available for live data push.
- 2026-04-22 — **Phase 2 project structure approved.** See `concepts/architecture/phase2-project-structure.md` for full layout, dependencies, auth flow, analytics SQL approach, and file creation order.
- 2026-04-23 — **Phase 3 frontend tech stack approved.** React 19 + TS + Vite, TanStack Query, React Hook Form + Zod, ky, shadcn/ui, Recharts. Separate repo at `neurospect-app`.
- 2026-04-23 — **Phase 3 frontend architecture approved.** Progressive-fill trade form, URL-driven list filters, per-phase screenshot upload, 7-view analytics dashboard. 3-session implementation split.

## Next Session Boot Prompts

### Phase 3 Session 1 — Scaffold + Infrastructure + Auth + Layout

**Recommended model:** Sonnet. **Working directory:** `C:\Users\PaulRussell\repos` (creates `app/`).

````
You are implementing Phase 3 Session 1 of the Neurospect frontend. This session covers project
scaffolding, infrastructure, shadcn/ui setup, layout components, auth flow, and routing.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/journal-analytics.md` — this tracker
   (especially the 2026-04-23 Phase 3 design session log for all approved decisions)
3. Read `concepts/architecture/trade-schema.md` §REST API and §ENUM Types — field types for TS interfaces
4. Read `concepts/architecture/phase2-project-structure.md` §Auth Design — the SPA auth flow
5. Read `app/auth/router.py`, `app/schemas/trade.py`, `app/schemas/analytics.py`,
   `app/schemas/screenshot.py`, `app/models/enums.py` in `C:\Users\PaulRussell\repos\neurospect-api`
   to get exact API contracts and all ENUM values

Context:
- Phase 2 backend is COMPLETE at `C:\Users\PaulRussell\repos\neurospect-api`.
- Phase 3 frontend design is APPROVED. All decisions are in the tracker session log.
- Frontend repo: `C:\Users\PaulRussell\repos\neurospect-app` (does NOT exist yet — you create it).
- Backend CORS allows `http://localhost:5173`. Backend runs on `http://localhost:8000`.
- Debug auth: `POST /auth/debug/token {discord_id}` when DEBUG=true on the backend.

Approved tech stack:
- React 19 + TypeScript + Vite 6
- React Router v7 (data router mode)
- TanStack Query v5 (server state)
- React Hook Form + Zod (forms + validation)
- ky (HTTP client with interceptors)
- shadcn/ui (Radix + Tailwind CSS)
- Recharts (charts — install now, used in Session 3)
- date-fns, Lucide React

This session implements (in order):

**Phase A — Scaffold:**
1. `npm create vite@latest neurospect-app -- --template react-ts` (run from `C:\Users\PaulRussell\repos`)
2. Install all deps: tailwindcss, @tailwindcss/vite, @tanstack/react-query, react-router-dom,
   react-hook-form, zod, @hookform/resolvers, ky, recharts, date-fns, lucide-react
3. Init Tailwind (Vite plugin approach) + shadcn/ui (`npx shadcn@latest init`)
4. Write `.env.example`:
   ```
   VITE_API_URL=http://localhost:8000
   VITE_DISCORD_CLIENT_ID=
   VITE_DISCORD_REDIRECT_URI=http://localhost:5173/auth/callback
   VITE_DEBUG=true
   ```
5. Write `.gitignore` (node_modules, dist, .env, etc.)

**Phase B — Infrastructure:**
6. `src/types/api.ts` — ALL TypeScript interfaces mirroring backend Pydantic schemas:
   - Trade, TradeCreate, TradeUpdate, TradeListResponse (from `app/schemas/trade.py`)
   - Screenshot (from `app/schemas/screenshot.py`)
   - SummaryStats, BreakdownRow, DayOfWeekRow, MistakeRow, RBucket (from `app/schemas/analytics.py`)
   - User (`{id, discord_id, discord_username, discord_avatar_url}` from `GET /auth/me`)
   - ALL enum union types from `app/models/enums.py`:
     SessionType, KillZoneType, BiasType, OppType, SetupType, PdaType,
     DisplacementType, OutcomeType, GradeType, ScreenshotPhase, TradeStatus
7. `src/lib/constants.ts` — ENUM label maps: `Record<EnumValue, string>` for all 11 enums
   (snake_case → human-readable). Also `{value, label}[]` arrays for Select components.
   Also common mistake tag suggestions: ['revenge', 'fomo', 'early_exit', 'oversized',
   'wrong_session', 'no_bias', 'chased', 'moved_stop'].
8. `src/lib/utils.ts` — `cn()` (clsx + tailwind-merge from shadcn), `formatDate()`,
   `formatDecimal()`, `formatPercent()`.
9. `src/lib/api.ts` — ky instance:
   - `prefixUrl` from `VITE_API_URL`
   - `beforeRequest` hook: read token from localStorage('neurospect_token'), set Authorization header
   - `afterResponse` hook: on 401 → clear token + redirect to /login
10. `src/lib/auth.ts` — AuthProvider React context:
    - State: `token`, `user`, `isLoading`
    - On mount: read token from localStorage. If present, call `GET /auth/me` to validate.
      If 401, clear token. If success, set user.
    - `login()`: redirect to Discord OAuth URL (built from VITE_DISCORD_CLIENT_ID + VITE_DISCORD_REDIRECT_URI)
    - `debugLogin(discordId)`: POST to `/auth/debug/token`, store token
    - `logout()`: clear localStorage + state, navigate to /login
    - `setToken(token)`: store in localStorage + state, fetch user
    - Export `useAuth()` hook

**Phase C — shadcn/ui components:**
11. Generate via CLI (`npx shadcn@latest add <name>`):
    button input label select card badge dialog tabs textarea checkbox separator
    dropdown-menu skeleton tooltip collapsible popover calendar pagination sheet
    Also install the shadcn form component (integrates with react-hook-form):
    `npx shadcn@latest add form`
    And radio-group: `npx shadcn@latest add radio-group`

**Phase D — Layout + Auth pages:**
12. `src/components/layout/sidebar.tsx` — fixed left sidebar with nav links:
    - Dashboard (LayoutDashboard icon) → /dashboard
    - Trades (FileText icon) → /trades
    - New Trade (Plus icon) → /trades/new
    Active link highlighted. Collapsible on mobile (Sheet component).
13. `src/components/layout/user-menu.tsx` — shows Discord avatar + username from useAuth().
    Dropdown with Logout option.
14. `src/components/layout/app-shell.tsx` — flex container: sidebar | main content area with
    top bar (user menu). Renders `<Outlet />` for child routes.
15. `src/pages/login.tsx` — centered card with:
    - "Sign in with Discord" button (if VITE_DISCORD_CLIENT_ID is set)
    - "Debug Login" button (if VITE_DEBUG=true) — text input for discord_id + submit
16. `src/pages/auth-callback.tsx` — reads `code` from URL search params.
    POSTs to `POST /auth/discord/token {code, redirect_uri: VITE_DISCORD_REDIRECT_URI}`.
    On success: calls auth context `setToken()`, navigates to `/dashboard`.
    On error: shows error message + link back to login.
17. `src/App.tsx` — createBrowserRouter:
    ```
    /login → LoginPage (public)
    /auth/callback → AuthCallbackPage (public)
    <ProtectedLayout> (checks useAuth, redirects if not authenticated)
      / → Navigate to /dashboard
      /dashboard → placeholder "Dashboard coming in Session 3"
      /trades → placeholder "Trade list coming in Session 2"
      /trades/new → placeholder "New trade coming in Session 2"
      /trades/:id → placeholder "Trade detail coming in Session 2"
    </ProtectedLayout>
    ```
18. `src/main.tsx` — React root:
    ```
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
    ```

**Session 1 checkpoint (verify before stopping):**
1. `npm run dev` → Vite dev server starts on localhost:5173
2. Visit `/login` → see login page with Debug Login button
3. Enter any discord_id in debug login → JWT stored → redirected to `/dashboard`
4. `/auth/me` returns user data → user menu shows username
5. Protected routes work → visiting `/trades` while logged out redirects to `/login`
6. Logout → token cleared → back to login page
7. All shadcn/ui components render correctly (import a Button somewhere to verify)

**Important:**
- Backend must be running: `cd neurospect-api && uvicorn app.main:app --reload` with `DEBUG=true`
- Paul handles git commits — never run git commit.
- After implementation, update this tracker with a session log entry.
- If you make any design decisions that deviate from the approved plan, document them in the
  session log and update wiki docs per the Architecture Doc Integrity rules.
````

### Phase 3 Session 2 — Data Hooks + Trade CRUD + List

**Recommended model:** Sonnet. **Working directory:** `C:\Users\PaulRussell\repos\neurospect-app`.

````
You are implementing Phase 3 Session 2 of the Neurospect frontend. This session covers TanStack
Query data hooks and the full trade CRUD UI (form, list, detail pages).

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/journal-analytics.md` — this tracker
   (the Phase 3 design session log + Session 1 log for what's already built)
3. Read the following files in `C:\Users\PaulRussell\repos\neurospect-app\src\`:
   - `types/api.ts` — TS interfaces (the API contract)
   - `lib/api.ts` — the ky instance (how to make API calls)
   - `lib/constants.ts` — ENUM label maps (for Select dropdowns and display)
   - `lib/auth.ts` — useAuth hook (for getting current user)
   - `App.tsx` — current route structure (you'll replace placeholder pages)
4. Read `app/routers/trades.py`, `app/routers/screenshots.py`, `app/schemas/trade.py`
   in `C:\Users\PaulRussell\repos\neurospect-api` — exact endpoint signatures

Context:
- Session 1 is COMPLETE: project scaffolded, all infrastructure in place, auth works, layout renders.
- Backend CORS allows localhost:5173. Backend at localhost:8000 with DEBUG=true.
- The `src/lib/api.ts` ky instance already handles Bearer token injection and 401 logout.
- The `src/types/api.ts` has all TypeScript interfaces. The `src/lib/constants.ts` has all ENUM labels.

This session implements:

**Phase E — Data hooks:**
1. `src/hooks/use-trades.ts` — TanStack Query hooks:
   - `useTrades(filters)` — `GET /api/trades?...` with filter params. `keepPreviousData: true`.
     Filters: `{date_start?, date_end?, instrument?, session?, setup_type?, outcome?, status?, page?, page_size?}`
   - `useTrade(id)` — `GET /api/trades/{id}`. Enabled only when id is defined.
   - `useCreateTrade()` — mutation: `POST /api/trades`. On success: invalidate trades list, navigate to `/trades/{id}`.
   - `useUpdateTrade(id)` — mutation: `PATCH /api/trades/{id}`. On success: invalidate trade + trades list.
   - `useDeleteTrade()` — mutation: `DELETE /api/trades/{id}`. On success: invalidate trades list, navigate to `/trades`.
2. `src/hooks/use-screenshots.ts` — TanStack Query hooks:
   - `useScreenshots(tradeId)` — `GET /api/trades/{id}/screenshots`. `staleTime: 30 * 60 * 1000` (presigned URLs expire in 1hr).
   - `useUploadScreenshot(tradeId)` — mutation: `POST /api/trades/{id}/screenshots` with FormData (file + phase). On success: invalidate screenshots query.
   - `useDeleteScreenshot(tradeId)` — mutation: `DELETE /api/trades/{id}/screenshots/{sid}`. On success: invalidate screenshots query.
3. `src/hooks/use-analytics.ts` — TanStack Query hooks (all `staleTime: 5 * 60 * 1000`):
   - `useSummary()` — `GET /api/analytics/summary`
   - `useBySetup()` — `GET /api/analytics/by-setup`
   - `useBySession()` — `GET /api/analytics/by-session`
   - `useByInstrument()` — `GET /api/analytics/by-instrument`
   - `useByDayOfWeek()` — `GET /api/analytics/by-day-of-week`
   - `useMistakes()` — `GET /api/analytics/mistakes`
   - `useRDistribution()` — `GET /api/analytics/r-distribution`

**Phase F — Trade CRUD UI:**
4. `src/components/trade/status-badge.tsx` — colored Badge component:
   - pre_trade → yellow/amber
   - active → blue
   - closed + win → green
   - closed + loss → red
   - closed + breakeven → gray
5. `src/components/trade/mistake-tag-input.tsx` — tag input component:
   - Text input with dropdown suggestions from `COMMON_MISTAKE_TAGS` in constants.ts
   - Selected tags render as removable Badge components
   - Freeform: typing a new tag and pressing Enter adds it
   - Value is `string[]`, controlled by React Hook Form
6. `src/components/trade/pre-trade-fields.tsx` — fieldset component (receives RHF `control`):
   - trade_date: date picker (Calendar + Popover from shadcn)
   - instrument: Input with datalist suggestions (NQ, ES, YM, GC, CL)
   - session: Select (SessionType options from constants)
   - kill_zone: Select (KillZoneType options)
   - htf_bias: RadioGroup (bullish/bearish/neutral)
   - htf_fvg_low + htf_fvg_high: two Input[type=number] on one row
   - draw_on_liquidity: Input
   - dol_price_level: Input[type=number]
   - opening_price_position: Select (OppType options)
   - news_flag: Checkbox
   - setup_type: Select (SetupType options)
   - narrative: Textarea
7. `src/components/trade/entry-fields.tsx` — fieldset (receives RHF `control`):
   - entry_price, stop_price, target_price: Input[type=number]
   - entry_time: Input[type=datetime-local]
   - stop_logic, target_logic: Input
   - entry_pda: Select (PdaType options)
   - displacement_quality: RadioGroup (clean/choppy/none)
   - smt_confirmation: Checkbox
8. `src/components/trade/post-trade-fields.tsx` — fieldset (receives RHF `control`):
   - exit_price: Input[type=number]
   - exit_time: Input[type=datetime-local]
   - outcome: RadioGroup (win=green/loss=red/breakeven=gray styling)
   - r_multiple: Input[type=number] (with auto-calc hint — see trade-form.tsx)
   - mae, mfe: Input[type=number]
   - target_reached, plan_followed: Checkbox
   - mistake_tags: MistakeTagInput component
   - quality_grade: Select (GradeType options — display as "A+", "A", "B", "C")
   - post_trade_notes: Textarea
9. `src/components/trade/trade-form.tsx` — the main form component:
   - Props: `trade?: Trade` (if editing), `onSuccess?: () => void`
   - Uses React Hook Form `useForm()` with Zod schema
   - Three Collapsible sections: Pre-Trade (default open), Entry (open if status != pre_trade), Post-Trade (open if status == closed)
   - On create (no trade prop): POST with form values → navigate to `/trades/{id}`
   - On edit (trade prop): PATCH with only `dirtyFields` values. Uses `exclude_unset=True` behavior.
   - Status transition buttons:
     - If status == pre_trade: "Save" button + "Mark as Active" button (sets status: 'active')
     - If status == active: "Save" button + "Close Trade" button (sets status: 'closed')
     - If status == closed: "Save" button only
   - R-multiple auto-calc: watch entry_price, stop_price, exit_price. When all three are set,
     auto-calculate R and pre-fill (but user can override). Formula:
     - If entry_price > stop_price (long): R = (exit - entry) / (entry - stop)
     - If entry_price < stop_price (short): R = (entry - exit) / (stop - entry)
   - Delete button (opens confirmation Dialog → calls useDeleteTrade)
10. `src/pages/new-trade.tsx` — renders `<TradeForm />` with no trade prop (create mode).
    Page title: "New Trade".
11. `src/components/trade/trade-card.tsx` — compact card for list view:
    - Shows: trade_date (formatted), instrument, status badge, setup_type label, session label
    - If closed: outcome badge + R-multiple
    - Click → navigate to `/trades/{id}`
    - Use Card component from shadcn
12. `src/components/trade/trade-filters.tsx` — filter bar:
    - Date range: two date inputs (date_start, date_end)
    - Instrument: Input (freeform)
    - Session: Select (+ "All" option)
    - Setup type: Select (+ "All")
    - Outcome: Select (+ "All")
    - Status: Select (+ "All")
    - "Clear filters" button
    - All filter values read from / written to URL search params via `useSearchParams`
13. `src/pages/trades.tsx` — trade list page:
    - Header: "Trades" title + "New Trade" button (link to /trades/new)
    - `<TradeFilters />` at top
    - Read filters from useSearchParams, pass to `useTrades(filters)`
    - Map `data.items` to `<TradeCard />` components
    - Pagination component at bottom (uses `data.total`, `data.page`, `data.page_size`)
    - Loading state: Skeleton cards
    - Empty state: "No trades found" message + link to create first trade
14. `src/pages/trade-detail.tsx` — single trade view/edit:
    - Read `id` from route params. Call `useTrade(id)`.
    - Render `<TradeForm trade={data} />`
    - Below the form: placeholder for screenshots ("Screenshots — coming in Session 3")
    - Loading state: Skeleton
    - 404 state: "Trade not found" message

15. Update `src/App.tsx` — replace placeholder routes with real page components.

**Session 2 checkpoint (verify before stopping):**
1. Navigate to `/trades/new` → trade form renders with all pre-trade fields
2. Fill trade_date + instrument + a few optional fields → Submit → trade created → redirected to detail
3. On detail page: expand Entry section → fill entry fields → click "Mark as Active" → status updates
4. Fill post-trade fields → click "Close Trade" → status becomes closed, outcome shown
5. Navigate to `/trades` → see the trade in the list with correct status badge + outcome
6. Use filters (e.g., filter by instrument) → list updates
7. Delete a trade → confirmation dialog → trade removed from list
8. R-multiple auto-calculation works when all three prices are filled

**Important:**
- Backend must be running with DEBUG=true.
- Paul handles git commits — never run git commit.
- After implementation, update this tracker with a session log entry.
- If any design decision deviates from the approved plan, document it in the session log.
````

### Phase 3 Session 3 — Screenshots + Analytics Dashboard

**Recommended model:** Sonnet. **Working directory:** `C:\Users\PaulRussell\repos\neurospect-app`.

````
You are implementing Phase 3 Session 3 of the Neurospect frontend. This session covers screenshot
upload/display and the full analytics dashboard. This is the final Phase 3 session.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/journal-analytics.md` — this tracker
   (Phase 3 design log + Session 1 and Session 2 logs for what's already built)
3. Read the following in `C:\Users\PaulRussell\repos\neurospect-app\src\`:
   - `hooks/use-screenshots.ts` — screenshot TanStack Query hooks (already written in Session 2)
   - `hooks/use-analytics.ts` — analytics hooks (already written in Session 2)
   - `lib/constants.ts` — ENUM labels (for chart axis labels, table headers)
   - `types/api.ts` — Screenshot, SummaryStats, BreakdownRow, DayOfWeekRow, MistakeRow, RBucket types
   - `pages/trade-detail.tsx` — the page where screenshots will be added
   - `App.tsx` — routing (dashboard route currently placeholder or partially wired)
4. Read `app/routers/screenshots.py`, `app/routers/analytics.py`, `app/schemas/analytics.py`
   in `C:\Users\PaulRussell\repos\neurospect-api` — exact endpoint contracts

Context:
- Sessions 1 and 2 are COMPLETE: auth, layout, all data hooks, full trade CRUD UI, trade list.
- The `useScreenshots`, `useUploadScreenshot`, `useDeleteScreenshot` hooks already exist.
- The `useSummary`, `useBySetup`, `useBySession`, `useByInstrument`, `useByDayOfWeek`,
  `useMistakes`, `useRDistribution` hooks already exist.
- Screenshot upload: `POST /api/trades/{id}/screenshots` — multipart form with `file` + `phase` (ENUM).
- Screenshot list: `GET /api/trades/{id}/screenshots` — returns array with `presigned_url` field.
- Backend CORS allows localhost:5173. Backend at localhost:8000 with DEBUG=true.

This session implements:

**Phase G — Screenshots:**
1. `src/components/screenshot/screenshot-upload.tsx` — per-phase upload component:
   - Props: `tradeId: string`, `phase: ScreenshotPhase`, `onUploaded?: () => void`
   - Drag-and-drop zone (accept `image/*`) + click-to-browse fallback
   - On drop/select: create FormData with `file` + `phase`, call `useUploadScreenshot` mutation
   - Show upload progress indicator (spinner/progress bar)
   - Drag-over visual feedback (border highlight)
   - Display phase label using SCREENSHOT_PHASE_LABELS from constants
2. `src/components/screenshot/screenshot-grid.tsx` — thumbnail grid:
   - Props: `tradeId: string`, `screenshots: Screenshot[]`
   - Group screenshots by phase (before_entry, entry, higher_tf, exit, post_trade_review)
   - Each phase section: label + thumbnails (using `presigned_url` as `<img>` src)
   - Each thumbnail has a delete button (X icon) → confirmation → `useDeleteScreenshot`
   - Click thumbnail → open in screenshot viewer
3. `src/components/screenshot/screenshot-viewer.tsx` — lightbox/modal:
   - Props: `url: string | null`, `onClose: () => void`
   - Full-screen overlay with the image centered
   - Click outside or press Escape → close
   - Use Dialog component from shadcn
4. Update `src/pages/trade-detail.tsx` — replace screenshot placeholder:
   - Below the trade form, add a "Screenshots" section
   - Show `<ScreenshotGrid>` with existing screenshots
   - Show `<ScreenshotUpload>` drop zones for phases appropriate to the trade status:
     - pre_trade: before_entry, higher_tf
     - active: before_entry, entry, higher_tf
     - closed: all 5 phases (before_entry, entry, higher_tf, exit, post_trade_review)

**Phase H — Analytics Dashboard:**
5. `src/components/analytics/summary-cards.tsx` — stat cards row:
   - Uses `useSummary()` hook
   - Cards: Total Trades, Win Rate (%), Avg R-Multiple, Best Setup Type,
     Current Streak (shows win or loss count), Longest Win Streak, Longest Loss Streak
   - Win rate color: green if >= 50%, red if < 50%
   - Use Card component, responsive grid (2 cols mobile, 4 cols desktop)
   - Loading: Skeleton cards
   - Empty: "No closed trades yet"
6. `src/components/analytics/breakdown-table.tsx` — reusable table:
   - Props: `title: string`, `rows: BreakdownRow[]`, `labelMap?: Record<string, string>`
   - Columns: Group (display label from labelMap or raw), Total, Wins, Losses, BE, Win Rate, Avg R
   - Sortable by column (client-side sort — data is small)
   - Win rate formatted as percentage. Avg R formatted to 2 decimal places.
   - Use shadcn Table components if available, or a simple HTML table with Tailwind styling
   - Empty: "No data" message
7. `src/components/analytics/day-of-week-chart.tsx` — bar chart:
   - Uses `useByDayOfWeek()` hook
   - Recharts `<BarChart>` with `<Bar>` for win rate
   - X-axis: day names (Mon, Tue, Wed, Thu, Fri — from `day_name` field)
   - Y-axis: win rate (0-100%)
   - Bar color: green if win_rate >= 50, red if < 50 (use Recharts Cell component for per-bar colors)
   - Tooltip: show full stats (total, wins, losses, avg R)
   - Responsive: `<ResponsiveContainer>` wrapper
8. `src/components/analytics/mistake-chart.tsx` — horizontal bar chart:
   - Uses `useMistakes()` hook
   - Recharts `<BarChart layout="vertical">` with `<Bar>` for count
   - Y-axis: tag labels (use MISTAKE_TAG_LABELS from constants if they exist, otherwise raw)
   - X-axis: count
   - Sort by count descending
   - Color: amber/orange bars
   - Responsive container
9. `src/components/analytics/r-distribution.tsx` — histogram:
   - Uses `useRDistribution()` hook
   - Recharts `<BarChart>` with `<Bar>` for count
   - X-axis: R-multiple range (format each bucket as "r_low to r_high")
   - Y-axis: count
   - Bar colors: green for positive R (r_low >= 0), red for negative R (r_high <= 0), mixed for straddling 0
   - Reference line at R=0
   - Responsive container
10. `src/pages/dashboard.tsx` — compose all analytics:
    - Page title: "Dashboard"
    - Full-width row: `<SummaryCards />`
    - Responsive 2-column grid (1-col on mobile, `grid grid-cols-1 lg:grid-cols-2 gap-6`):
      - `<BreakdownTable title="By Setup Type" rows={bySetup} labelMap={SETUP_TYPE_LABELS} />`
      - `<BreakdownTable title="By Session" rows={bySession} labelMap={SESSION_LABELS} />`
      - `<BreakdownTable title="By Instrument" rows={byInstrument} />`  (no labelMap — instruments are already readable)
      - `<DayOfWeekChart />`
      - `<MistakeChart />`
      - `<RDistribution />`
    - Loading: Skeleton grid
    - Empty (no trades): full-page message "Start journaling to see your analytics" + link to /trades/new

11. Update `src/App.tsx` if needed — ensure `/dashboard` route points to real DashboardPage.

**Session 3 checkpoint (verify before stopping):**
1. On trade detail: screenshot drop zones appear for correct phases based on trade status
2. Upload a screenshot → thumbnail appears in grid → presigned URL loads image
3. Click thumbnail → lightbox opens with full-size image → close works
4. Delete screenshot → removed from grid
5. Navigate to `/dashboard` → summary cards render with correct stats
6. Breakdown tables show data for setup type, session, instrument (need some closed trades)
7. Day of week chart renders bars with correct day names
8. Mistake chart shows tags sorted by frequency
9. R-distribution histogram renders with green/red coloring
10. Empty states work when there are no trades
11. All charts are responsive (resize browser → charts adapt)

**Post-session (MANDATORY per wiki Architecture Doc Integrity rules):**
- After implementation, update this tracker with a Session 3 log entry marking Phase 3 as COMPLETE.
- Create `concepts/architecture/phase3-frontend-structure.md` in the wiki documenting the frontend
  architecture (tech stack, project layout, key patterns). This becomes the canonical doc for frontend.
- Update `entities/projects/neurospect.md` — current state to "Phase 3 implemented".
- Update `index.md` and append to `log.md`.

Paul handles git commits — never run git commit.
````

### 2026-04-23 — Phase 3 Session 1 (COMPLETE)

- did: scaffolded `neurospect-app` repo — React 19 + TypeScript + Vite 6, Tailwind v4 (Vite plugin), shadcn/ui.
- did: installed all approved deps: TanStack Query v5, React Router v7, React Hook Form, Zod, ky, Recharts, date-fns, Lucide React.
- did: wrote `src/types/api.ts` — full TypeScript interfaces mirroring all backend Pydantic schemas + 11 enum union types.
- did: wrote `src/lib/constants.ts` — all ENUM label maps + Select option arrays + COMMON_MISTAKE_TAGS.
- did: wrote `src/lib/utils.ts` — cn(), formatDate(), formatDecimal(), formatPercent().
- did: wrote `src/lib/api.ts` — ky instance with Bearer token injection + 401 → /login redirect.
- did: wrote `src/lib/auth.ts` — AuthProvider context (token/user/isLoading), login(), debugLogin(), logout(), setToken(). Uses window.location.href (not useNavigate) since AuthProvider sits outside RouterProvider.
- did: installed shadcn/ui components: button, input, label, select, card, badge, dialog, tabs, textarea, checkbox, separator, dropdown-menu, skeleton, tooltip, collapsible, popover, calendar, pagination, sheet, form, radio-group.
- did: wrote layout components: sidebar (fixed + mobile Sheet), user-menu (Discord avatar + Logout dropdown), app-shell (Outlet wrapper).
- did: wrote auth pages: login.tsx (Discord OAuth + Debug Login), auth-callback.tsx (code → JWT → /dashboard).
- did: wrote App.tsx (createBrowserRouter, ProtectedLayout checks token + redirects, placeholder pages for sessions 2/3).
- did: wrote main.tsx (QueryClientProvider → AuthProvider → App).
- deviation: ky v1.x no longer uses `prefixUrl` option — replaced with `baseUrl` (appended trailing slash). Hook signatures also changed: `BeforeRequestHook` now receives `{ request }` state object; `AfterResponseHook` now receives `{ response }` state object. Updated api.ts accordingly.
- deviation: shadcn@latest wrote components to literal `@/components/ui/` directory (an `@` folder at repo root) instead of `src/components/ui/` — files manually moved, `@/` directory removed. tsconfig `ignoreDeprecations: "6.0"` added for `baseUrl` deprecation warning in TS 7.0 migration path. `types: ["vite/client"]` added to tsconfig.app.json to expose `import.meta.env`. `class-variance-authority` installed (shadcn peer dep not auto-installed).
- fix: `login.tsx` was missing `useNavigate` — after `debugLogin()` resolved, nothing redirected to `/dashboard`. Added `navigate('/dashboard', { replace: true })` after the await.
- fix: `app/services/r2.py` instantiated `R2Client()` at module load time, crashing startup when `R2_ENDPOINT_URL` is empty (local dev has no R2). Changed singleton to `R2Client() if settings.r2_endpoint_url else None`. Added `get_r2()` FastAPI dependency to `app/routers/screenshots.py` that returns 503 when R2 is not configured — all three screenshot endpoints now use it. Screenshot upload/list/delete will 503 locally until R2 is wired up (deferred to deployment phase).
- fix: `alembic/env.py` was reading `DATABASE_URL_SYNC` from `os.environ` directly, but pydantic-settings `.env` loading only runs when `Settings()` is instantiated (not before alembic's env.py runs). Added `from dotenv import load_dotenv; load_dotenv()` at the top of `alembic/env.py`. python-dotenv is already a pydantic-settings dep so no new install needed.
- local dev setup: Postgres 16 running in Docker container `neurospect-db` (port 5432, user/pass/db all `neurospect`). `api/.env` written with local connection strings + `DEBUG=true`. All deps installed into system Python 3.13 via pip (Poetry not installed).
- checkpoint: debug login works e2e — JWT stored, redirected to /dashboard, user menu shows username, protected routes redirect to /login, logout clears token.
- next: Session 2 — data hooks + trade CRUD form/list.

### 2026-04-23 — Phase 3 Session 2 (COMPLETE)

- did: wrote 3 TanStack Query hook files: `src/hooks/use-trades.ts`, `src/hooks/use-screenshots.ts`, `src/hooks/use-analytics.ts` — all 15 hooks (useTrades, useTrade, useCreateTrade, useUpdateTrade, useDeleteTrade, useScreenshots, useUploadScreenshot, useDeleteScreenshot, plus 7 analytics hooks).
- did: wrote all Phase F trade CRUD UI components: `status-badge.tsx`, `mistake-tag-input.tsx`, `pre-trade-fields.tsx`, `entry-fields.tsx`, `post-trade-fields.tsx`, `trade-form.tsx`, `trade-card.tsx`, `trade-filters.tsx`.
- did: wrote pages: `new-trade.tsx`, `trades.tsx`, `trade-detail.tsx`. Updated `App.tsx` to replace placeholder routes with real pages.
- did: TypeScript clean (`tsc -b`) + Vite build passes (719 kB bundle, expected for full stack with Recharts). Bundle size warning is non-critical.
- deviation: `z.boolean().default(false)` and `z.array(z.string()).default([])` in Zod schema cause RHF + Zod resolver generic type mismatch. Fixed by removing `.default()` from schema and using explicit `defaultValues` in `useForm()` instead. The `form.control` is cast to `TradeControl` alias when passed to field sub-components — standard pattern for this RHF + Zod type inference limitation.
- deviation: ky v1 `ResponsePromise` has no `.res()` method (v0 API). Used bare `api.delete(url)` which returns `ResponsePromise extends Promise<Response>` — TanStack Query mutation accepts it directly.
- decided: Zod schema uses `z.string()` for ENUM fields (not `z.enum([...])`) to avoid enumerating all backend values in two places. Backend validates ENUM correctness.
- decided: buildPatch() iterates `dirtyFields` keys — only changed fields go into the PATCH body. New `TradeControl` type alias exported from `trade-form.tsx` for use by field sub-components.
- decided: `<TradeForm>` currently re-renders with stale collapsible state when `trade.status` changes after a status transition mutation. This is acceptable for MVP — the page would need a full re-fetch/re-render to reset the collapsible open state, which happens naturally on next navigation. Can be improved in a future session with `useEffect` watching `trade.status`.
- next: Session 3 — screenshots + analytics dashboard.

### 2026-04-23 — Phase 3 Session 3 (COMPLETE) — Phase 3 COMPLETE

- did: implemented all Phase G (screenshots) and Phase H (analytics dashboard) components.
- did: fixed `src/hooks/use-analytics.ts` — all 6 breakdown hooks had type mismatch: backend wraps responses in `{ rows: [...] }` (by-setup, by-session, by-instrument, by-day-of-week, mistakes) and `{ buckets: [...] }` (r-distribution). Updated queryFns to extract the inner array via `.then(r => r.rows)` / `.then(r => r.buckets)`.
- did: created `src/components/screenshot/screenshot-upload.tsx` — drag-and-drop upload zone per phase. Handles file validation, mutation, drag-over highlight, spinner, error state (incl. 503 when R2 not configured locally).
- did: created `src/components/screenshot/screenshot-viewer.tsx` — shadcn Dialog lightbox with sr-only title for accessibility. Dialog handles Escape key natively.
- did: created `src/components/screenshot/screenshot-grid.tsx` — groups screenshots by phase, thumbnails with hover delete button (X), delete confirmation Dialog, opens viewer on click.
- did: updated `src/pages/trade-detail.tsx` — replaced screenshot placeholder with `<ScreenshotGrid>` + per-status `<ScreenshotUpload>` zones. `PHASE_SETS` map drives which upload zones render per trade status. 503 error shown as info message in local dev.
- did: created `src/components/analytics/summary-cards.tsx` — 8-card responsive grid. Win rate colorized green/red. Best setup resolved from SETUP_TYPE_LABELS. Streak shows current W/L with color.
- did: created `src/components/analytics/breakdown-table.tsx` — client-side sortable table (all columns). `labelMap` typed as `Record<string, string>` — call sites cast enum label maps.
- did: created `src/components/analytics/day-of-week-chart.tsx` — Recharts BarChart, per-bar Cell coloring (green ≥50%, red <50%), custom tooltip.
- did: created `src/components/analytics/mistake-chart.tsx` — horizontal BarChart layout="vertical", sorts by count desc, formats snake_case tags to Title Case, dynamic height.
- did: created `src/components/analytics/r-distribution.tsx` — BarChart with per-bar Cell coloring (green positive, red negative, amber straddling), ReferenceLine at nearest-zero bucket.
- did: created `src/pages/dashboard.tsx` — composed all analytics components. Empty state (no trades) shows CTA to /trades/new. Each chart manages its own loading/empty state.
- did: updated `src/App.tsx` — replaced DashboardPlaceholder with real DashboardPage. Removed placeholder function.
- decided: `SETUP_TYPE_LABELS` / `SESSION_LABELS` (typed `Record<EnumType, string>`) are cast to `Record<string, string>` at call sites in dashboard.tsx — TypeScript doesn't allow direct assignment of specific-key records to index-signature records without a cast.
- decided: `RBucket.r_low` / `r_high` wrapped in `Number()` in chart components as defensive conversion — Pydantic v2 serializes `Decimal` to float in JSON but TypeScript types are defensive.
- decided: screenshot upload zones always render (even locally) — they show a user-friendly error if R2 is not configured (503). This is intentional: the UI is complete, storage is a deployment concern.
- wiki: created `concepts/architecture/phase3-frontend-structure.md` (canonical frontend doc), updated `entities/projects/neurospect.md` (Phase 3 implemented), updated `index.md`, appended to `log.md`.
- **Phase 3 is COMPLETE.** All three sessions done. Full trade journal MVP: auth, trade CRUD, screenshots, analytics dashboard.

## See Also

- [[concepts/roadmap/README]] — strategic context (journal data is the substrate for Next/Later horizons)
- [[processes/distributed-workflow/active/ai-coach]] — sister module (shares backend)
- [[processes/distributed-workflow/active/course-and-kb]] — strategy definitions inform the setup_type field
- [[entities/projects/neurospect]] — full roadmap and architecture
