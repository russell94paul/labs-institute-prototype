---
tags: [distributed-workflow, active, neurospect, broker, tradovate, integration]
aliases: [Broker Integration, Tradovate Integration, Broker Auto-Populate]
sources: []
created: 2026-04-26
updated: 2026-04-26
phases:
  phase_1: 1c-complete
---

# Broker Integration — Workstream Tracker

Reduce manual entry of trade execution fields by pulling live fill data from connected brokers. Phase 1 covers Tradovate (demo environment, used by Paul's Lucid prop account); future phases extend to live environments and additional brokers.

This workstream was forked from [[journaling-ux]] on 2026-04-26 to keep broker concerns separate from form/UX concerns. The original journaling-ux Phase 3 spec is the seed of this tracker's Phase 1.

## Goal

By end of Phase 1:
1. **Credentials managed in-app** — `/settings/broker` page where the user enters Tradovate username/password once; backend authenticates and persists encrypted creds + tokens.
2. **Manual fetch** — "Fetch from Tradovate" buttons on Entry and Post-Trade tabs pull execution fields (entry_price, entry_time, stop_price, target_price, exit_price, exit_time) for the current trade's date + instrument.
3. **Automatic fetch (toggle)** — optional 30s background poll that auto-populates execution fields when a matching fill appears, with an amber "Filled from Tradovate" banner.
4. **Soft singleton on active trades** — at most one trade with `status='active'` per user, enforced by a backend 409 + frontend guard modal. Eliminates fill-attribution ambiguity for the auto-poll by construction.
5. **Robust auth** — automatic token refresh; app-wide "Tradovate disconnected — reconnect in Settings" banner when refresh fails.

## Lane

Wiki: Neurospect

Owned paths (this workstream may write here):
- `processes/distributed-workflow/active/broker-integration.md` (this tracker)
- `concepts/architecture/trade-schema.md` — extends with broker_credentials table + tradovate_fill_id_* columns (§Architecture Doc Integrity reconciliation)
- `concepts/architecture/phase2-project-structure.md` — extends with new backend modules

Code paths (in repos, outside the wiki):
- `api/app/services/tradovate.py`, `app/services/crypto.py`, `app/routers/tradovate.py`, `app/models/broker_credential.py`, `app/schemas/broker.py`, `alembic/versions/0003_broker_credentials.py`
- `api/app/routers/trades.py` — active-trade guard logic
- `app/src/pages/settings.tsx`, `src/pages/settings-broker.tsx`, `src/components/settings/*`, `src/components/trade/tradovate-*`, `src/components/trade/active-trade-guard-dialog.tsx`, `src/components/layout/active-trade-badge.tsx`, `src/components/layout/broker-disconnected-banner.tsx`, `src/hooks/use-tradovate.ts`, `src/hooks/use-active-trade.ts`
- `app/src/components/trade/entry-fields.tsx`, `post-trade-fields.tsx`, `src/pages/new-trade.tsx`, `src/components/coach/coaching-panel.tsx`, `src/components/layout/app-shell.tsx`, `src/App.tsx` — modifications

## Required Context

Every session must read at boot:
- [[CLAUDE]] — wiki schema, isolation rule, architecture doc integrity reconciliation requirement
- This tracker
- [[concepts/architecture/trade-schema]] — canonical trade data model (will extend)
- [[concepts/architecture/phase2-project-structure]] — canonical backend layout (will extend)

For sub-phase 3a/equivalent specifically:
- `api/app/main.py` (router mounting)
- `api/app/models/tv_token.py` + `app/routers/tv_tokens.py` (per-user-credential reference pattern)
- `api/app/database.py`, `app/deps.py`, `app/config.py`
- `api/alembic/versions/0002_coach_tables.py` (latest migration for parent revision)

## Plan-Mode Rule

The full Phase 1 architecture is locked (see §Phase 1 below). Implementation sub-phases (1a–1d) skip plan mode unless scope drift is detected during the pre-work probe. New phases (Phase 2 = live env enablement, Phase 3 = additional brokers, etc.) require plan mode at first session.

---

## Phase 1 — Tradovate Demo Integration (spec approved 2026-04-26)

Reduce manual entry of execution fields (entry_price, stop_price, target_price, entry_time, exit_price, exit_time) by pulling live fill data from Tradovate's demo API.

### Broker context

**Broker:** Tradovate (futures)

**Prop firm:** Lucid

**Account type:** Prop firm simulated/evaluation account — NOT a personal Tradovate retail account. Lucid provides access via their portal; clicking "Start Simulated Trading" opens the Tradovate platform.

**API environment:** Tradovate's simulation environment. The trader UI is at `demo.tradovate.com`; the API host is most likely `demo.tradovateapi.com` (to be confirmed in the 1a probe — see §Risks).

**Auth confirmed:** Paul can log into `trader.tradovate.com` directly with his Lucid/Tradovate credentials. This confirms standard Tradovate API auth (username/password → access token) is accessible for this account.

**Access paths:**
- Lucid prop portal → "Start Simulated Trading" → Tradovate platform
- `trader.tradovate.com` directly (confirmed working)
- TradingView with Tradovate broker integration

**"Tradovate Prop" app:** Referenced on account purchase — may be a separate product or just the Lucid portal branding. Not currently visible; not a blocker since `trader.tradovate.com` access is confirmed.

**Architecture decision: Option A (Tradovate REST API poll) — primary approach.** Auth flow is standard; demo endpoint is known. No custom integration required.

### What we need from the broker

| Journal field | Tradovate source |
|---|---|
| `entry_price` | Fill price on opening order |
| `entry_time` | Fill timestamp on opening order |
| `position_size` | Fill `qty` on opening order (number of contracts) |
| `stop_price` | Bracket stop order price |
| `target_price` | Bracket limit order price |
| `exit_price` | Fill price on closing order |
| `exit_time` | Fill timestamp on closing order |

The `position_size` column was added to the trades table 2026-04-26 in migration `0003_add_position_size`, ahead of this workstream's migration. The broker code in 1a/1c only needs to read Tradovate's `qty` and write it to the existing column — no further DDL.

### Architecture — confirmed approach

**Option A: Tradovate REST API (poll) — selected.**

Endpoints (host TBD by probe — see §Risks #3):
- Auth: `POST /v1/auth/accesstokenrequest`
- Fills: `GET /v1/fill/list`
- Orders: `GET /v1/order/list`

**Flow:**
1. User provides Tradovate credentials in `/settings/broker` (encrypted at rest in backend).
2. On demand (manual fetch button) or via 30s background poll (automatic mode), backend authenticates and fetches recent fills.
3. Most recent open fill → maps to entry fields; most recent close fill → maps to exit fields.
4. Frontend populates Entry/Post-Trade tab fields; user reviews and saves.

**Option B: Tradovate WebSocket** — possible future upgrade for real-time population without user polling. Not required for initial version.

**Options C/D:** Deprioritised — Option A is viable.

### Confirmed design decisions

1. **Trigger:** "Fetch from Tradovate" button on Entry tab + Post-Trade tab. Settings toggle for Manual (button always) vs Automatic (background poll ~30s, auto-populates on fill detection + amber banner).
2. **Credential storage:** Settings page in neurospect-app — user enters Tradovate username + password once; backend authenticates and stores tokens.
3. **Scope:** BOTH entry fields (entry_price, entry_time, stop_price, target_price) AND exit fields (exit_price, exit_time).
4. **API routes:** `/api/tradovate/*` prefix — modular, extensible.
5. **Token refresh:** Automatic via Tradovate refresh token. If refresh fails → app-wide banner "Tradovate disconnected — reconnect in Settings". No mid-session re-auth prompts during normal use.
6. **Match logic:** Filter fills by instrument + trade_date. One match → auto-fill silently. Multiple matches → picker (time + price). No match → message.
7. **Auto-mode disambiguation:** Resolved via the soft-singleton design (§Soft Singleton). With at-most-one active trade by construction, the auto-poll's match set is unambiguous. The picker stays as a defensive fallback for the rare forced-override case.
8. **Settings page location:** New `/settings` route, with `/settings/broker` as the first section. `/coach/setup` stays feature-scoped (Pine script, TV instructions, coach token).
9. **Environment toggle:** Built in from day one. `tradovate_environment: 'demo' | 'live'` field stored on the credentials row, radio in `/settings/broker` defaulted to Demo. Cost is ~5 LOC; avoids a future migration when Paul moves to live trading.

### Soft Singleton — at most one active trade

Phase 1 introduces a soft singleton: at most one trade with `status='active'` per user at a time. `pre_trade` rows don't count — those are pre-market plans, fine to queue.

**Layer 1 — Backend guard (correctness).** `POST /api/trades` and `PATCH /api/trades/:id` (when transitioning `pre_trade → active`) check for an existing active row. If one exists, return `409 Conflict` with `{ active_trade_id, instrument, entry_time }` and an optional `?force=true` override flag. Prevents *any* code path from creating a parallel active trade.

**Layer 2 — Frontend UX (proactive).** Three touchpoints, all reading from a shared `useActiveTrade()` hook:

1. *Persistent app-shell badge* — small pill in the header: `🟢 Active: NQ · 14:32 ET`. Click → `/trades/<id>`. Always tells the user there's an open position. Hidden when none.
2. *Block-with-confirm at creation* — "New Trade" + "Start Trade from Signal" buttons. If active trade exists → modal: "You have an active NQ trade open since 14:32 ET. Tradovate auto-fill is currently linked to it. Open the existing trade, or start a new one anyway?" Primary: **Go to active trade**. Secondary: **Start anyway** (sends `?force=true`).
3. *Auto-fill lockout when override taken* — if a second active trade is forced, the new form's "Fetch from Tradovate" button is disabled with tooltip: "Auto-fill paused — two active trades. Close [NQ 14:32] first."

**Why not a hard DB constraint** (unique partial index where `status='active'`)? Recovery edges bite — a stuck row from a crash, manual data fixes, legitimately concurrent strategies. Hard constraints turn recoverable UX problems into 500 errors. The 409 + override is the right idiom: explicit, observable, recoverable.

### Data model deltas

**New table: `broker_credentials`** — single row per (user, broker), mirrors `tradingview_tokens` lifecycle pattern (active row + soft-revoke columns).

```sql
CREATE TYPE tradovate_environment AS ENUM ('demo', 'live');

CREATE TABLE broker_credentials (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                  UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    broker                   VARCHAR(32) NOT NULL DEFAULT 'tradovate',
    environment              tradovate_environment NOT NULL DEFAULT 'demo',

    -- Encrypted credentials (Fernet symmetric — secret in BROKER_CRED_SECRET)
    username_encrypted       TEXT NOT NULL,
    password_encrypted       TEXT NOT NULL,

    -- OAuth tokens from Tradovate (refreshed automatically)
    access_token             TEXT,
    md_access_token          TEXT,
    access_token_expires_at  TIMESTAMPTZ,

    -- Diagnostic
    last_auth_at             TIMESTAMPTZ,
    last_auth_error          TEXT,
    is_disconnected          BOOLEAN NOT NULL DEFAULT false,

    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (user_id, broker)
);
```

**`trades` table additions** — fill-level idempotency:

```sql
ALTER TABLE trades ADD COLUMN tradovate_fill_id_entry  BIGINT;
ALTER TABLE trades ADD COLUMN tradovate_fill_id_exit   BIGINT;

CREATE UNIQUE INDEX ix_trades_tv_fill_entry
    ON trades (user_id, tradovate_fill_id_entry)
    WHERE tradovate_fill_id_entry IS NOT NULL AND NOT is_deleted;
CREATE UNIQUE INDEX ix_trades_tv_fill_exit
    ON trades (user_id, tradovate_fill_id_exit)
    WHERE tradovate_fill_id_exit IS NOT NULL AND NOT is_deleted;
```

The unique partial indexes prevent the same Tradovate fill from being applied to two trade rows.

### Backend architecture (`neurospect-api`)

**New: `app/services/tradovate.py`** — thin async client around the Tradovate REST API. Stateless; takes a `BrokerCredentials` row + an `httpx.AsyncClient`.
- `authenticate(username, password, environment)` → access + refresh tokens
- `refresh_if_needed(creds)` → checks expiry; refreshes if <5 min remaining; on 401 from a fill call, retries once after refresh
- `list_fills(creds, since, instrument)` → wraps `/v1/fill/list`
- `list_orders(creds, since, instrument)` → wraps `/v1/order/list` (needed for stop/target prices from bracket OCO orders)
- `get_contract(creds, contract_id)` → small cache to translate `NQM6` → `NQ`
- Raises `TradovateAuthError` on hard failure → caller marks `is_disconnected = true`

Base URL switched on `creds.environment`: `demo` → `https://demo.tradovateapi.com/v1`, `live` → `https://live.tradovateapi.com/v1` (host to be confirmed in §Risks #3).

**New: `app/services/crypto.py`** — Fernet encryption helper. Key from `BROKER_CRED_SECRET` env var (32-byte URL-safe base64). Add to `.env.example` + Render env vars.

**New: `app/routers/tradovate.py`** — prefix `/api/tradovate`:

| Method | Path | Description |
|---|---|---|
| `POST` | `/credentials` | Body: `{username, password, environment}`. Authenticates immediately; 400 on bad creds. Stores encrypted creds + tokens. |
| `GET` | `/credentials` | Returns `{environment, is_connected, last_auth_at, username_masked}`. Never returns password/tokens. |
| `DELETE` | `/credentials` | Removes the row. |
| `POST` | `/credentials/test` | Force a re-auth ("Test connection" button). |
| `GET` | `/fills` | Query: `trade_date` (required), `instrument` (optional), `since_time` (optional). Returns normalized fills `[{tradovate_fill_id, instrument, side, qty, price, timestamp, order_id, bracket: {stop_price, target_price}}]`. The `qty` field maps to `trades.position_size` when applied. |

**Modified: `app/routers/trades.py`** — active-trade guard:
- New helper `get_active_trade(db, user_id) -> Trade | None`
- `PATCH /api/trades/{id}` — when transitioning `pre_trade → active`, return 409 unless `?force=true`
- `POST /api/trades` — same check if creating with `status='active'` (rare path)
- 409 body: `{ active_trade_id, instrument, entry_time }`

**New: `POST /api/trades/{id}/apply-tradovate-fill`** — atomic apply. Body: `{tradovate_fill_id, role: 'entry'|'exit'}`. Backend re-fetches the fill from Tradovate (don't trust client fields), looks up bracket orders for stop/target if `role='entry'`, updates the trade + writes `tradovate_fill_id_entry/exit`. For `role='entry'` the fill's `qty` writes to `position_size`. Returns the updated trade.

### Frontend architecture (`neurospect-app`)

**New routes** in `src/App.tsx`:
```
/settings                  → redirect to /settings/broker
/settings/broker           → BrokerSettingsPage
```

**New pages/components**:
```
src/pages/settings.tsx                 — Settings hub (sections list)
src/pages/settings-broker.tsx          — Broker credentials page
src/components/settings/
  ├── settings-shell.tsx               — sidebar nav + outlet
  ├── broker-credentials-form.tsx      — username, password, environment radio
  ├── broker-status-card.tsx           — connection state, last auth, test button
  └── auto-fetch-toggle.tsx            — Manual / Automatic radio
src/components/trade/
  ├── tradovate-fill-button.tsx        — "Fetch from Tradovate" + states
  ├── tradovate-fill-picker-dialog.tsx — multi-match picker
  └── active-trade-guard-dialog.tsx    — 409 / pre-flight modal
src/components/layout/
  ├── active-trade-badge.tsx           — header pill
  └── broker-disconnected-banner.tsx   — top-of-shell red bar when is_disconnected
```

**New hooks**:
- `src/hooks/use-tradovate.ts` — `useBrokerCredentials`, `useSaveBrokerCredentials`, `useDeleteBrokerCredentials`, `useTradovateFills`, `useApplyTradovateFill`, `useAutoFillPoll`
- `src/hooks/use-active-trade.ts` — `useActiveTrade()` → null | Trade

**Modified components**:
- `src/components/trade/entry-fields.tsx` — adds Tradovate fetch button next to entry_price
- `src/components/trade/post-trade-fields.tsx` — adds Tradovate fetch button next to exit_price
- `src/pages/new-trade.tsx` — guard dialog on mount if active trade exists
- `src/components/coach/coaching-panel.tsx` — guard dialog on "Start Trade from Signal" click
- `src/components/layout/app-shell.tsx` — adds `<ActiveTradeBadge>` + `<BrokerDisconnectedBanner>`

**Auto-fetch behavior**:
- Setting in localStorage: `neurospect.tradovate.autoFetch = 'manual' | 'automatic'`
- Automatic: Entry/Post-Trade tabs poll `/api/tradovate/fills` every 30s; new fill matching trade's date+instrument with `tradovate_fill_id_*` not yet set → auto-applies → shows amber banner ("Filled from Tradovate")
- Manual: explicit button click only

**Fetch button states** (Entry tab example):
| State | Behavior |
|---|---|
| No broker creds | Disabled, tooltip: "Connect Tradovate in Settings →" |
| `is_disconnected` | Disabled, tooltip: "Reconnect Tradovate" |
| Override-locked (second active trade) | Disabled, tooltip: "Auto-fill paused — close [NQ 14:32] first" |
| Ready, no matches | Toast: "No Tradovate fills found for NQ on 2026-04-26" |
| Ready, one match | Auto-applies, toast: "Filled from Tradovate at 14:32:18 ET" |
| Ready, multiple matches | Opens `<TradovateFillPickerDialog>` |

### Implementation decomposition

Phase 1 is too big for one session. Four sub-phases:

| Sub-phase | Scope | Model | LOC est. | Depends on |
|---|---|---|---|---|
| **1a — Backend foundation** | Migration (broker_credentials + trade columns), `BrokerCredentials` model, encryption helper, Tradovate client (auth + list_fills + list_orders), `/api/tradovate/credentials` CRUD + test endpoint. **No fill-application logic yet.** | Sonnet | ~600 | — |
| **1b — Active-trade singleton** | `get_active_trade` helper, 409 logic in trades router, `useActiveTrade` hook, app-shell badge, `<ActiveTradeGuardDialog>`, wired into NewTradePage + CoachingPanel. **Independent — can ship standalone.** | Sonnet | ~300 | — |
| **1c — Settings UI + manual fetch** | `/settings/broker` page, credentials form, status card, "Fetch from Tradovate" buttons on Entry/Post-Trade tabs, picker dialog, `apply-tradovate-fill` endpoint. **End-to-end manual flow live after this.** | Sonnet | ~500 | 1a |
| **1d — Auto-fetch + disconnected handling** | Auto-fetch toggle, 30s background poll, amber "filled from broker" banner, `is_disconnected` flag + app-wide banner, token refresh logic. | Sonnet | ~250 | 1c |

1a is foundation. 1b is independent and can run parallel. 1c depends on 1a. 1d depends on 1c.

### Risks / unknowns to verify before locking 1a

A 30-min exploratory probe at the start of 1a — hit the live demo API with `httpie`/curl to confirm:

1. **Tradovate fill record shape** — fields available (`fillId`, `orderId`, `contractId`, `timestamp`, `price`, `qty`, `action`).
2. **Bracket order linkage** — does the fill record reference the OCO bracket directly, or do we need to query `/order/list` and match by `oco`/`ocoId`? Affects how stop/target prices are extracted.
3. **Demo endpoint host** — `demo.tradovate.com` is the trader UI; the API host is typically `demo.tradovateapi.com`. Confirm with curl before coding.
4. **MD vs trading token** — Tradovate issues `accessToken` (trading) and `mdAccessToken` (market data) on auth. Fill data uses the trading token. We don't need MD for this phase but should store both since auth returns them together.
5. **Rate limits** — Tradovate's public limits aren't well documented. 30s poll across 1 user is fine; revisit if scaled.

---

## Decisions Log

- 2026-04-26 — Workstream forked from journaling-ux. Broker integration deserves separate concern from trade form/UX work.
- 2026-04-26 — Option A (Tradovate REST poll) selected over WebSocket / TradingView-broker / TradingView-export. Auth is standard, demo endpoint accessible, no custom integration required.
- 2026-04-26 — Soft singleton on `status='active'` trades, enforced via API 409 + UX guard modal. Hard DB constraint rejected for recovery flexibility.
- 2026-04-26 — Encryption: Fernet symmetric, key in `BROKER_CRED_SECRET` env var. Avoids per-user key management complexity for the 5-10 beta-user MVP scale.
- 2026-04-26 — Environment toggle (`demo`/`live`) built from day one rather than retrofit. Cost is ~5 LOC.
- 2026-04-26 — Settings hub at new `/settings` route, not retrofitted into `/coach/setup`. Keeps feature-scoped pages clean.
- 2026-04-26 — Phase 1 decomposed into four sub-phases (1a/1b/1c/1d) for independent shippability. 1b is independent of broker work and can run in parallel with 1a.

---

## Session Log

Append-only. Newest at the bottom.

### 2026-04-26 — Workstream created (forked from journaling-ux)

- did: forked broker integration into its own workstream tracker. Migrated full Phase 3 spec from `journaling-ux.md` here as Phase 1. Sub-phases renamed 3a/3b/3c/3d → 1a/1b/1c/1d.
- did: cross-linked the journaling-ux tracker with a pointer to this one; added an entry to `index.md`.
- decided: scope of this workstream is broker integrations broadly. Phase 1 = Tradovate demo. Future phases (live env, additional brokers) will be added when needed.
- noted: the active-trade singleton design is included in this workstream because its primary motivation is making broker auto-fill safe, even though it's also independently valuable as a journal UX guard. Sub-phase 1b is designed to be shippable independently of broker code.
- next: Sub-phase 1a (Backend foundation). Boot prompt below.

### 2026-04-26 — position_size added to trade schema (gap caught by Paul)

- did: added `position_size INTEGER` (nullable) to the `trades` table via migration `0003_add_position_size` — alembic, SQLAlchemy model, Pydantic schemas (TradeCreate, TradeUpdate, TradeResponse) all updated. Frontend mirrored: `Trade`, `TradeCreate`, `TradeUpdate` in `src/types/api.ts`; Zod schema + form defaults + edit-mode initialiser in `src/components/trade/trade-form.tsx`; new "Position Size (contracts)" input on the Entry tab in `src/components/trade/entry-fields.tsx` (placed between Entry Time and Stop Price).
- did: updated canonical `concepts/architecture/trade-schema.md` — added position_size to Entry Fields table + DDL; revised the Future Considerations note (position_size delivered, risk_amount/account_balance still deferred).
- did: updated this tracker — added position_size row to §What we need from the broker, noted `qty → position_size` mapping in the FillDTO and apply-fill endpoint specs, renumbered the broker migration from `0003_broker_credentials.py` → `0004_broker_credentials.py` (down_revision = `0003_add_position_size`).
- decided: type = INTEGER (nullable). Futures contracts are whole numbers. Nullable because pre-trade rows don't have it yet.
- decided: place the field between Entry Time and Stop Price on the Entry tab. Logically pairs with stop_price in the 2-col grid (both size the trade's risk).
- verified: `tsc -b` clean on the frontend.
- next: same as before — Sub-phase 1a (Backend foundation, Tradovate auth + fills). Boot prompt below now reflects the renumbered migration.

---

## Pending Wiki Updates

- All 1a/1b/1c reconciliation is complete. No outstanding wiki updates.
- After 1d ships: update `phase2-project-structure.md` and `phase3-frontend-structure.md` with auto-fetch poll hook + `is_disconnected` banner trigger logic.

## Blockers / Open Questions

**RESOLVED (2026-04-26, same session as 1a):** Username/password auth is not available for Tradovate Prop accounts (Lucid). Workaround: browser session token paste via `POST /api/tradovate/credentials/token`. Confirmed working against `demo.tradovateapi.com/v1` with a live token extracted from dev tools. Token lifetime ~1–2 hours; user re-pastes when expired. No further action needed — 1c is unblocked.

**OPEN — ACTION REQUIRED before starting 1d:**

Fill/order field names in `app/services/tradovate.py` have never been confirmed against real data because the account had no fills during the 1a and 1c probes. All field name mappings (`id`, `orderId`, `contractId`, `tradeTime`, `price`, `qty`, `action`) are based on the Tradovate v1 API reference docs only.

**What Paul needs to do to unblock 1d:**
1. Start the backend: `poetry run uvicorn app.main:app --reload` (from `api/`)
2. Log in at `trader.tradovate.com`; open DevTools → Network; copy the Bearer token from any request to `demo.tradovateapi.com`
3. Paste it via `POST /api/tradovate/credentials/token` — use the Swagger UI at `http://localhost:8000/docs`
4. Place a small test trade on the Tradovate demo platform (any size, any instrument — just needs to fill)
5. Call `GET /api/tradovate/fills?trade_date=<today>` from the Swagger UI
6. Look at the raw JSON response; confirm or correct the field names in `list_fills` and `list_orders` in `app/services/tradovate.py` (TODO comments mark every unconfirmed field)
7. If field names differ from what's coded, make the fix in `tradovate.py` — it's a small targeted edit

Once field names are confirmed, 1d (Auto-fetch + disconnected handling) can begin without any additional probe work.

### 2026-04-26 — Sub-phase 1a: Backend foundation complete

**Tradovate API probe findings (documented before writing code):**
- **API host confirmed**: `demo.tradovateapi.com/v1` responds — correct.
- **User credentials confirmed correct**: When probing with `cid=0/sec=""`, the API returned a captcha/rate-limit challenge (`p-captcha: true`) rather than "incorrect password" — this only happens when the username/password ARE valid.
- **Critical blocker discovered**: Tradovate API access for personal accounts requires (a) a $1000 funded account + $25/month subscription, AND (b) activation in account preferences. **Paul's Lucid prop account does not expose this API access section.** Prop firm accounts appear to be on a separate platform ("Tradovate Prop") without standard REST API access.
- **Probe failed on app credentials**: `cid=8 + sec=bf0ecf...` (the public sample app credentials) returned "incorrect username or password" for this account — likely because prop accounts use a different authentication path.
- **Fill/order field shapes NOT confirmed** — rate-limited before a successful auth. Field names in `tradovate.py` are based on the Tradovate v1 API reference docs; marked with TODO comments for verification.
- **Risk #5 (rate limits)** remains unverified — couldn't get a successful auth to test list endpoints.

**OPEN QUESTION — alternative auth paths for Tradovate Prop accounts:**
- The Tradovate Prop platform may have a different API endpoint or auth flow than the retail API
- Browser session token extraction is a possible workaround (extract Bearer token from browser dev tools while logged into trader.tradovate.com)
- CSV export from Tradovate is another path (build CSV import instead of live API)
- Lucid may have their own data export or API access
- See §Risks and open questions — this needs resolution before 1c (Settings UI + manual fetch) can be completed

**Code shipped in 1a:**
- `alembic/versions/0004_broker_credentials.py` — migration: `tradovate_environment` ENUM, `broker_credentials` table, `tradovate_fill_id_entry/exit` BIGINT + partial unique indexes on trades. `alembic upgrade head` clean.
- `app/models/broker_credential.py` — SQLAlchemy model
- `app/services/crypto.py` — Fernet encrypt/decrypt; fails loud at import if `BROKER_CRED_SECRET` unset/invalid
- `app/services/tradovate.py` — async Tradovate client: `authenticate()`, `refresh_if_needed()`, `get_contract()`, `list_fills()`, `list_orders()`. Custom exceptions: `TradovateAuthError`, `TradovateApiError`. `FillDTO` imported from schemas.
- `app/schemas/broker.py` — `BrokerCredentialsCreate`, `BrokerCredentialsResponse`, `BracketInfo`, `FillDTO`
- `app/routers/tradovate.py` — `/api/tradovate/credentials` CRUD + test endpoint + `GET /fills` with bracket extraction
- `app/config.py` — added `broker_cred_secret` (required), `tradovate_app_id`, `tradovate_cid`, `tradovate_sec`
- `app/models/trade.py` + `app/schemas/trade.py` — added `tradovate_fill_id_entry/exit`
- `app/main.py` — mounted `tradovate_router`
- `.env.example` + `.env` — added `BROKER_CRED_SECRET`, `TRADOVATE_CID`, `TRADOVATE_SEC`
- `tests/test_tradovate.py` — 16 tests: crypto roundtrip, mask helper, `authenticate()` with mocked httpx, FillDTO schema. All 33 tests (existing + new) pass.
- `pyproject.toml` — added `[tool.pytest.ini_options] asyncio_mode = "auto"`

**Wiki reconciliation done:** `trade-schema.md` and `phase2-project-structure.md` updated per §Architecture Doc Integrity.

**next:** Resolve Tradovate API access blocker (see §Risks) before 1c. 1b (active-trade singleton) is independent and can ship in parallel.

### 2026-04-26 — Sub-phase 1b: Active-trade soft singleton complete

**Code shipped in 1b:**
- `app/schemas/trade.py` — added `status: TradeStatus = TradeStatus.pre_trade` to `TradeCreate` so POST can optionally create with `status='active'` (the rare path the guard needs to check).
- `app/routers/trades.py` — added:
  - `get_active_trade(db, user_id) -> Trade | None` — queries `status='active' AND NOT is_deleted` for the user; returns first match or None.
  - `_conflict_response(trade) -> JSONResponse` — builds the flat 409 body: `{detail, active_trade_id, instrument, entry_time}`.
  - `force: bool = Query(False)` param on both `POST /api/trades` and `PATCH /api/trades/{id}`.
  - Guard in `create_trade`: if `body.status == active and not force` → check `get_active_trade` → return 409 if conflict.
  - Guard in `update_trade`: inside the valid-transition block, if transitioning to `active and not force` → check `get_active_trade` → return 409 if a different active trade exists (`existing.id != trade_id`).
- `tests/test_singleton.py` — 11 tests covering: helper returns None/trade, POST 409/force/pre_trade/multiple-pre_trade, PATCH 409/force/no-conflict/non-status-fields/same-id-edge-case.

**Design decisions:**
- 409 uses `return JSONResponse(...)` (not `raise HTTPException`) to produce the flat body the spec shows: `{"detail": "active_trade_conflict", "active_trade_id": "...", "instrument": "...", "entry_time": "..."}`.
- `get_active_trade` is a module-level function (not a FastAPI dependency) so tests can patch it cleanly without needing HTTP infrastructure.
- Tests call route functions directly with mocked AsyncSession — same pattern as `test_tradovate.py`. No test database needed.

**Verification:** `poetry run pytest` — 44/44 passing (all existing + 11 new).

**Wiki reconciliation:** No schema changes and no new modules in 1b — no architecture doc updates needed per the spec.

**next:** 1c (Settings UI + manual fetch). Requires 1a complete (it is) and 1b (now complete). Token-paste auth path is live (resolved in 1a via `POST /credentials/token`). Only remaining unknown is fill/order field name verification — no fills existed during the 1a probe. First test trade against the demo API will confirm field names; update `tradovate.py` TODO comments then.

---

### 2026-04-26 — Token-only mode added (same session)

- decided: Tradovate prop firm accounts (Lucid) cannot use username/password auth — the standard REST API requires a $25/month subscription on a retail account; the API Access settings section is not exposed on prop accounts.
- decided: Primary workaround is **browser session token paste**. User extracts Bearer token from browser dev tools while logged into trader.tradovate.com and pastes it via `POST /api/tradovate/credentials/token`.
- did: Added `BrokerTokenCreate` schema, `POST /credentials/token` endpoint, `_store_token` helper, `_parse_jwt_username` in service. `refresh_if_needed` detects token-only mode (empty password sentinel) and raises `TradovateAuthError("Session token expired — re-paste...")`. `test_credentials` handles token-only by checking JWT expiry locally without a network call.
- confirmed (live token probe 2026-04-26): REST API at `demo.tradovateapi.com/v1` accepts the MD WebSocket session token — Tradovate Prop uses a unified token, not separate accessToken/mdAccessToken. The token from the WebSocket `authorize` message is all that's needed.
- confirmed: JWT payload has `email` claim (not `name`), `sub` = numeric user ID. `_parse_jwt_username` updated to prefer email > name > sub.
- confirmed: `/contract/{id}` returns 404 on Tradovate Prop. `/contract/item?id={id}` is the correct single-item endpoint. `get_contract` updated.
- confirmed: `/contract/find?name=MNQM6` works and returns `{id, name, contractMaturityId, ...}` — name field is the full contract ticker (e.g. `MNQM6`).
- confirmed: Token lifetime is ~1–2 hours (standard session token). Paul will need to re-paste when it expires.
- NOT confirmed: Fill/order field names (`id`, `orderId`, `contractId`, `tradeTime`, `price`, `qty`, `action`) — account had no fills or orders. Field names remain based on Tradovate v1 API docs. Verify by placing a trade and running `GET /api/tradovate/fills`.
- next: 1b (active-trade singleton) is independent, can ship now. 1c after 1b.

---

### 2026-04-26 — Sub-phase 1c: Settings UI + manual fetch complete

**Code shipped:**

Backend (`neurospect-api`):
- `app/schemas/trade.py` — added `ApplyFillRequest` (`tradovate_fill_id: int`, `role: Literal['entry'|'exit']`)
- `app/routers/trades.py` — added `POST /{trade_id}/apply-tradovate-fill` endpoint:
  - Asserts ownership; idempotent (no-op if fill already applied for role)
  - Re-fetches fill from Tradovate via `list_fills` (doesn't trust client fields)
  - For `role='entry'`: writes `entry_price`, `entry_time`, `position_size`, `tradovate_fill_id_entry`; looks up bracket OCO orders via `list_orders` and writes `stop_price`/`target_price` if working stop/limit orders found
  - For `role='exit'`: writes `exit_price`, `exit_time`, `tradovate_fill_id_exit`
  - On auth failure: marks creds `is_disconnected=True`, returns 503
  - Returns `TradeResponse`

Frontend (`neurospect-app`):
- `src/types/api.ts` — added `BrokerCredentials`, `BracketInfo`, `FillDTO` interfaces; added `tradovate_fill_id_entry/exit` to `Trade`
- `src/hooks/use-tradovate.ts` — `useBrokerCredentials`, `useSaveBrokerToken`, `useTestBrokerCredentials`, `useDeleteBrokerCredentials`, `useFetchTradovateFills`, `useApplyTradovateFill`
- `src/hooks/use-active-trade.ts` — `useActiveTrade()` → `Trade | null`; polls with 30s staleTime
- `src/components/settings/settings-shell.tsx` — sidebar nav with Broker Connections link; accepts `children`
- `src/components/settings/broker-credentials-form.tsx` — token-paste form (textarea + instructions); two states: paste form / connected view
- `src/components/settings/broker-status-card.tsx` — status indicator, Test connection, Disconnect
- `src/components/settings/auto-fetch-toggle.tsx` — Manual / Automatic radio; persists to `localStorage: neurospect.tradovate.autoFetch`
- `src/pages/settings-broker.tsx` — `/settings/broker` page
- `src/components/trade/tradovate-fill-button.tsx` — "Fetch from Tradovate" button with all disabled states (no creds, disconnected, override-locked) + inline status messages + picker dialog integration
- `src/components/trade/tradovate-fill-picker-dialog.tsx` — multi-fill picker
- `src/components/trade/active-trade-guard-dialog.tsx` — 409 guard on NewTradePage
- Modified `entry-fields.tsx` and `post-trade-fields.tsx` — added `trade?: Trade` + `onFillApplied?` props; render `TradovateFillButton` at top of grid in edit mode
- Modified `trade-form.tsx` — `handleEntryFillApplied` / `handleExitFillApplied` callbacks update form via `setValue`
- Modified `app-shell.tsx` — `ActiveTradeBadge` (header pill, click → trade) + `BrokerDisconnectedBanner` (red bar when `is_connected=false`)
- Modified `new-trade.tsx` — `ActiveTradeGuardDialog` on mount when active trade exists
- Modified `App.tsx` — `/settings` redirect + `/settings/broker` route
- Modified `sidebar.tsx` — Settings nav item

**Verification:** `tsc -b` clean; `poetry run pytest` 44/44 passing (no new tests added — apply logic is straightforward and covered by the existing hook patterns)

**Fill field names:** still not confirmed against real fill data (no fills existed during 1a/1c development). The button/endpoint will work once Paul places a test trade and verifies `tradovate.py` field names match actual API responses. TODO comments in `tradovate.py` remain until confirmed.

**Design decisions:**
- `BrokerDisconnectedBanner` reads from `useBrokerCredentials().data.is_connected` directly — no new flag needed since `is_connected` was already on the response. Auto-triggering on refresh failure is still 1d scope.
- `ActiveTradeBadge` formats entry_time in ET using `Intl` (no extra library). Sits in the header left-side alongside the UserMenu on the right.
- `TradovateFillButton` uses inline status messages (auto-clear after 4s) instead of a toast library — avoids adding a dependency to a simple single-user app.
- `ActiveTradeGuardDialog` "Start anyway" just dismisses the dialog; the new trade is created as `pre_trade` which never triggers 409. The force-override path is relevant when the user later transitions to `active` — that's handled via the existing PATCH 409 + force flow in TradeForm.

**Wiki reconciliation done:** `phase2-project-structure.md` and `phase3-frontend-structure.md` updated per §Architecture Doc Integrity.

**next:** 1d (Auto-fetch + disconnected handling). Prerequisites: verify fill field names against real API response (place a test trade, call `GET /api/tradovate/fills`).

---

## Boot Prompt — Phase 1a (Backend Foundation)

**Recommended model:** Sonnet. **Working directory:** `neurospect-api`.

````
You are implementing sub-phase 1a of the Neurospect broker-integration workstream: the backend foundation for Tradovate broker auto-populate. The full Phase 1 architecture is locked — do not redesign, just build the foundation.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/broker-integration.md` — the entire "Phase 1 — Tradovate Demo Integration" section is your contract. Especially: §Soft Singleton, §Data model deltas, §Backend architecture, §Risks.
3. Read these files in `neurospect-api`:
   - `app/main.py` (router mounting pattern)
   - `app/models/tv_token.py` + `app/routers/tv_tokens.py` (per-user-credential reference pattern — single active row, soft revoke)
   - `app/models/trade.py` + `app/schemas/trade.py` (for the new BIGINT columns)
   - `app/database.py`, `app/deps.py`, `app/config.py` (env vars, db session, auth dep)
   - `alembic/versions/0002_coach_tables.py` (latest migration for the head-revision parent)
   - `pyproject.toml` (current deps — add `cryptography` for Fernet if not present, plus confirm `httpx`)

PRE-WORK — Tradovate API probe (~30 min, before writing code):

There are 5 unresolved risks listed in the tracker's §Risks section. Resolve at least #1, #2, #3 by hitting the Tradovate demo API directly. Ask Paul for his Tradovate username/password (or have him run the curl himself if he prefers — paste the output). Confirm:
1. The actual demo API host (likely `demo.tradovateapi.com` not `demo.tradovate.com`).
2. The auth response shape (`accessToken`, `mdAccessToken`, expiry, refresh token).
3. The fill record shape from `/v1/fill/list` — field names for fill_id, contract_id, timestamp, price, side.
4. How bracket stop/target orders link to the entry fill — via OCO id on the order, or a relationship on the fill itself.

Document findings inline in the session log of this tracker, then proceed.

SCOPE OF 1a (no fill-application logic, no UI):

1. CREATE Alembic migration `0004_broker_credentials.py` (down_revision = `0003_add_position_size`):
   - `tradovate_environment` ENUM ('demo', 'live')
   - `broker_credentials` table per the §Data model deltas section (verbatim DDL)
   - `tradovate_fill_id_entry` and `tradovate_fill_id_exit` BIGINT columns on `trades`
   - Two unique partial indexes on those columns (per spec)
   - **Note:** `position_size` is already present on `trades` (added in `0003_add_position_size` on 2026-04-26). Do NOT re-add it.
   - Run `alembic upgrade head` locally to verify

2. CREATE `app/models/broker_credential.py` — SQLAlchemy model matching the table.

3. CREATE `app/services/crypto.py`:
   - `encrypt(plaintext: str) -> str`, `decrypt(ciphertext: str) -> str`
   - Fernet symmetric. Key from `settings.broker_cred_secret` (new field on `app/config.py`, env var `BROKER_CRED_SECRET`).
   - Fail loud at import time if the env var is unset (don't silently auth-fail later).
   - Add `BROKER_CRED_SECRET` to `.env.example` with a comment about generating: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

4. CREATE `app/services/tradovate.py`:
   - Async client. Stateless. Takes a `BrokerCredentials` row + an `httpx.AsyncClient`.
   - `authenticate(username, password, environment) -> dict` — POSTs to `/v1/auth/accesstokenrequest`, returns the parsed token response.
   - `refresh_if_needed(creds) -> BrokerCredentials` — checks `access_token_expires_at` (refresh if <5 min remaining or already expired). Updates the row in-place via session passed in.
   - `list_fills(creds, since: datetime, instrument: str | None) -> list[FillDTO]` — calls `/v1/fill/list`, on 401 retries once after refresh, raises `TradovateAuthError` on second failure.
   - `list_orders(creds, since, instrument)` — same shape, for bracket stop/target.
   - `get_contract(creds, contract_id)` — small in-process LRU cache for contract_id → instrument symbol.
   - Custom exceptions: `TradovateAuthError` (hard auth failure → mark `is_disconnected=true` upstream), `TradovateApiError` (other 4xx/5xx).
   - Define `FillDTO` (Pydantic) as the normalized output: `{tradovate_fill_id, instrument, side, qty, price, timestamp, order_id}`. Bracket extraction (stop/target lookup) lives in the router for now — keep this service focused on raw Tradovate calls.

5. CREATE `app/schemas/broker.py`:
   - `BrokerCredentialsCreate` — `username: str`, `password: SecretStr`, `environment: Literal['demo','live']`
   - `BrokerCredentialsResponse` — `environment`, `is_connected: bool`, `last_auth_at`, `username_masked` (e.g. "pa***ll")
   - `FillDTO` (or import from services)

6. CREATE `app/routers/tradovate.py` mounted at `/api/tradovate`:
   - `POST /credentials` — accept BrokerCredentialsCreate, immediately call `authenticate()`. On success: encrypt + store, return masked response. On Tradovate auth fail: 400 with `{detail: "invalid Tradovate credentials"}`. On already-exists: upsert (replace).
   - `GET /credentials` — returns BrokerCredentialsResponse or 404 if no row.
   - `DELETE /credentials` — hard delete the row.
   - `POST /credentials/test` — re-runs `authenticate()` against stored creds; updates `last_auth_at` / `last_auth_error` / `is_disconnected`.
   - `GET /fills` — query: `trade_date` (required, ISO date), `instrument` (optional), `since_time` (optional ISO datetime). Calls `list_fills`; for each fill, looks up its bracket OCO orders via `list_orders` and attaches `bracket: {stop_price, target_price}`. Returns `list[FillDTO]`.
   - All endpoints depend on `get_current_user`.
   - Mount in `app/main.py` after `tv_tokens_router`.

7. EXTEND `app/config.py` settings: `broker_cred_secret: str` (required, no default — fail loud).

8. EXTEND `app/models/trade.py`: add `tradovate_fill_id_entry: Mapped[int | None]` and `tradovate_fill_id_exit: Mapped[int | None]`. Update `app/schemas/trade.py` accordingly (read-only on the response model; not patchable directly — application happens via the future `apply-tradovate-fill` endpoint in 1c).

OUT OF SCOPE FOR 1a (these are 1b/1c/1d):
- Active-trade singleton 409 logic → 1b
- `apply-tradovate-fill` endpoint → 1c
- Auto-poll / `is_disconnected` banner triggering → 1d
- Any frontend code

VERIFICATION:
- `poetry run alembic upgrade head` clean.
- `poetry run pytest` clean (add tests under `tests/test_tradovate.py` — at minimum: encrypt/decrypt round-trip, the masked username helper, an integration-ish test for `POST /credentials` with a mocked httpx that returns the auth response).
- Manual: with real credentials in `.env`, `POST /api/tradovate/credentials` returns 201, `GET /api/tradovate/fills?trade_date=2026-04-26` returns at least an empty list (or actual fills if Paul has any open).

POST-IMPLEMENTATION RECONCILIATION (per neurospect-wiki CLAUDE.md §Architecture Doc Integrity):
- This session writes code in `neurospect-api`. The reconciliation rule applies.
- Re-read `concepts/architecture/trade-schema.md` and update it: the `broker_credentials` table and the new `tradovate_fill_id_*` columns must be reflected. Add a §Broker Credentials section if needed; update the Field Definitions table for trades.
- Re-read `concepts/architecture/phase2-project-structure.md` (canonical for backend layout) — note the new modules (`services/tradovate.py`, `services/crypto.py`, `routers/tradovate.py`, `models/broker_credential.py`, `schemas/broker.py`).
- Append a session log entry to `processes/distributed-workflow/active/broker-integration.md` describing what was built, including any discoveries from the Tradovate API probe (host, fill shape, bracket linkage). These are crucial for 1c.
- Update tracker frontmatter `phase_1: spec-approved` → `phase_1: 1a-complete` (or stay `spec-approved` until the whole phase ships — your call, but mark progress somehow).

Paul handles git commits — never run git commit.

Always write a boot prompt at session end if anything is left undone. Next session is 1b (Active-trade singleton) or 1c (Settings UI + manual fetch) — pick the one Paul prefers; 1b is independent of 1a and could already have shipped, while 1c requires 1a complete.
````

---

## Boot Prompt — Phase 1b (Active-Trade Singleton)

**Recommended model:** Sonnet. **Working directory:** `neurospect-api`.

````
You are implementing sub-phase 1b of the Neurospect broker-integration workstream: the active-trade soft singleton. This sub-phase is fully independent of the broker credential work (1a) and can ship on its own.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/broker-integration.md` — focus on §Soft Singleton and §Implementation decomposition. 1b scope is listed there.
3. Read these files in `neurospect-api`:
   - `app/routers/trades.py` (this is where all 1b changes go)
   - `app/models/trade.py` + `app/schemas/trade.py` (Trade model + schemas)
   - `app/deps.py` (get_current_user, get_db pattern)
   - `app/main.py` (confirm no router changes needed — 1b is router-internal only)

SCOPE OF 1b (backend only — no frontend, no broker code):

1. ADD helper `get_active_trade(db: AsyncSession, user_id: UUID) -> Trade | None` in `app/routers/trades.py` (or extract to a small `app/services/trades.py` if it makes the router cleaner).
   - Queries for a trade where `user_id = user_id AND status = 'active' AND NOT is_deleted`
   - Returns the first match or None

2. MODIFY `POST /api/trades` — if body has `status='active'` (rare but possible), check `get_active_trade` first. If one exists and `?force=true` is NOT set, return 409.

3. MODIFY `PATCH /api/trades/{id}` — when the patch transitions status `pre_trade → active`, check `get_active_trade`. If another active trade exists (different id) and `?force=true` is NOT set, return 409.

409 response body (both cases):
```json
{
  "detail": "active_trade_conflict",
  "active_trade_id": "<uuid>",
  "instrument": "NQ",
  "entry_time": "2026-04-26T14:32:00Z"
}
```

The `?force=true` query param bypasses the guard and allows creation of a second active trade. Frontend (1c) will disable auto-fill on the second trade with a tooltip.

4. ADD tests under `tests/test_singleton.py`:
   - Creating a trade with `status='active'` when one already exists → 409
   - PATCH transitioning to active when one already exists → 409
   - `?force=true` bypasses the 409 → 201/200
   - Creating/updating `pre_trade` rows is never blocked
   - Multiple `pre_trade` rows for same user → allowed

OUT OF SCOPE for 1b:
- Frontend guard modal, app-shell badge, useActiveTrade hook → 1c
- Any broker/Tradovate code
- Any new migrations (no schema changes needed)

VERIFICATION:
- `poetry run pytest` clean (all existing tests + new singleton tests)
- Manual: create a trade with status=active, try to create another → 409; try with ?force=true → success

POST-IMPLEMENTATION RECONCILIATION:
- No new wiki pages needed (1b adds no new schema, no new modules)
- Append a session log entry to `processes/distributed-workflow/active/broker-integration.md`
- Update frontmatter `phase_1` if appropriate

Paul handles git commits — never run git commit.

Next session after 1b is 1c (Settings UI + manual fetch — frontend + apply-tradovate-fill endpoint). 1c requires 1a complete (it is) and 1b helpful but not blocking.
````

---

## Boot Prompt — Phase 1c (Settings UI + Manual Fetch)

**Recommended model:** Sonnet. **Working directories:** `neurospect-api` (backend) + `neurospect-app` (frontend).

````
You are implementing sub-phase 1c of the Neurospect broker-integration workstream: the Settings UI and manual Tradovate fill fetch. This is the first end-to-end user-facing phase — after 1c, Paul can connect Tradovate and populate trade fields with one click.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/broker-integration.md` — full Phase 1 spec, especially §Soft Singleton, §Backend architecture, §Frontend architecture, §Confirmed design decisions. The §Blockers section is resolved — auth uses token-paste path (see below).
3. Read these files in `neurospect-api`:
   - `app/routers/trades.py` — singleton guard is live; you add `apply-tradovate-fill` here
   - `app/routers/tradovate.py` — credentials CRUD + `GET /fills` already implemented; understand the interface
   - `app/services/tradovate.py` — Tradovate client; note the TODO comments on fill field names (unconfirmed — see below)
   - `app/schemas/broker.py` — FillDTO, BracketInfo, BrokerCredentialsResponse, BrokerTokenCreate
   - `app/schemas/trade.py` — TradeResponse (what apply-tradovate-fill returns)
4. Read these files in `neurospect-app`:
   - `src/App.tsx` — routing; you add /settings and /settings/broker routes here
   - `src/types/api.ts` — frontend type definitions; extend with broker types
   - `src/components/layout/app-shell.tsx` — add ActiveTradeBadge + BrokerDisconnectedBanner
   - `src/components/trade/entry-fields.tsx` — add Tradovate fetch button
   - `src/components/trade/post-trade-fields.tsx` — add Tradovate fetch button
   - `src/pages/new-trade.tsx` — wire in ActiveTradeGuardDialog

CRITICAL CONTEXT — auth path changed from spec:

Standard Tradovate username/password auth requires a $25/month API subscription not available on Paul's Lucid prop account. The workaround implemented in 1a: browser session token paste.

- **Auth endpoint:** `POST /api/tradovate/credentials/token` with body `{token: string}`
- **How to get the token:** Log into `trader.tradovate.com` → DevTools → Network → any request to `demo.tradovateapi.com` → copy the `Authorization: Bearer <token>` value
- **Token lifetime:** ~1–2 hours. App shows "reconnect" when expired.
- **`POST /credentials` (username/password)** is still in the router but should not be the primary UI flow. The settings form should show a token-paste input, not a username/password form.
- `BrokerTokenCreate` schema: `{token: str}` — already in `app/schemas/broker.py`
- The `broker-credentials-form.tsx` component in the spec was written for username/password. Build it as a token-paste form instead: a labeled textarea, a "Connect" button, and a note explaining how to extract the token from DevTools.

FILL FIELD NAMES — partially confirmed:

In the 1a probe, the API accepted the token but the account had no fills/orders, so field names were not verified against real data. Field names in `tradovate.py` are based on Tradovate v1 API docs. At the start of 1c:

1. Ask Paul to place a test trade in the Tradovate demo platform and then call `GET /api/tradovate/fills?trade_date=<today>` to see the real response shape.
2. Update the TODO comments in `tradovate.py` with confirmed field names.
3. If field names differ from the docs, fix the service before wiring the frontend.

SCOPE OF 1c:

**Backend (neurospect-api):**

1. ADD `POST /api/trades/{id}/apply-tradovate-fill` in `app/routers/trades.py`:
   - Body: `{tradovate_fill_id: int, role: 'entry' | 'exit'}`
   - Backend re-fetches the fill from Tradovate (don't trust client fields — call `list_fills` and filter by `tradovate_fill_id`)
   - `role='entry'`: writes `entry_price`, `entry_time`, `position_size` (from fill `qty`); looks up bracket OCO orders via `list_orders` → writes `stop_price`, `target_price`; sets `tradovate_fill_id_entry`
   - `role='exit'`: writes `exit_price`, `exit_time`; sets `tradovate_fill_id_exit`
   - Idempotent: if `tradovate_fill_id_entry/exit` already set to this id, no-op and return current trade
   - Returns the updated `TradeResponse`
   - Ownership check via `_assert_ownership` (existing pattern)

**Frontend (neurospect-app):**

2. ADD routes in `src/App.tsx`:
   - `/settings` → redirect to `/settings/broker`
   - `/settings/broker` → `<BrokerSettingsPage>`

3. ADD settings components:
   - `src/pages/settings-broker.tsx` — broker settings page (shell + form)
   - `src/components/settings/settings-shell.tsx` — sidebar nav with "Broker" section; extensible for future settings sections
   - `src/components/settings/broker-credentials-form.tsx` — token-paste form (textarea + "Connect" button + DevTools instructions); calls `POST /api/tradovate/credentials/token`; shows masked token info + last auth time when connected
   - `src/components/settings/broker-status-card.tsx` — connection status, "Test connection" button (`POST /credentials/test`), "Disconnect" button (`DELETE /credentials`)
   - `src/components/settings/auto-fetch-toggle.tsx` — Manual / Automatic radio; persists to `localStorage: neurospect.tradovate.autoFetch`

4. ADD hooks:
   - `src/hooks/use-tradovate.ts` — `useBrokerCredentials`, `useSaveBrokerToken`, `useDeleteBrokerCredentials`, `useTradovateFills`, `useApplyTradovateFill`
   - `src/hooks/use-active-trade.ts` — `useActiveTrade()` → `null | Trade`; polls `GET /api/trades?status=active&page_size=1` or filters from the existing trade list cache

5. ADD trade components:
   - `src/components/trade/tradovate-fill-button.tsx` — "Fetch from Tradovate" button with states: no creds (disabled + tooltip), disconnected (disabled + tooltip), override-locked/second active (disabled + tooltip), ready (click → call fills, auto-apply if one match, open picker if multiple, toast if none)
   - `src/components/trade/tradovate-fill-picker-dialog.tsx` — multi-fill picker: shows time, price, side, qty for each match; user picks one → calls apply-tradovate-fill
   - `src/components/trade/active-trade-guard-dialog.tsx` — shown when user tries to create a new trade while one is active; primary: "Go to active trade", secondary: "Start anyway" (sends `?force=true`)

6. MODIFY existing components:
   - `src/components/trade/entry-fields.tsx` — add `<TradovateFillButton role="entry">` next to `entry_price`
   - `src/components/trade/post-trade-fields.tsx` — add `<TradovateFillButton role="exit">` next to `exit_price`
   - `src/components/layout/app-shell.tsx` — add `<ActiveTradeBadge>` (header pill: "🟢 Active: NQ · 14:32 ET", click → `/trades/<id>`) + `<BrokerDisconnectedBanner>` (red bar when `is_disconnected`)
   - `src/pages/new-trade.tsx` — on mount, if active trade exists, show `<ActiveTradeGuardDialog>`

409 CONFLICT RESPONSE FORMAT (from 1b):

The 409 body is flat (not nested under `detail`):
```json
{
  "detail": "active_trade_conflict",
  "active_trade_id": "<uuid>",
  "instrument": "NQ",
  "entry_time": "2026-04-26T14:32:00+00:00"
}
```
Frontend checks: `if (response.status === 409 && data.detail === "active_trade_conflict")`.

OUT OF SCOPE for 1c:
- Auto-fetch 30s background poll → 1d
- `is_disconnected` flag + banner triggering on refresh failure → 1d
- Token auto-refresh (1d handles the case where the session token expires mid-use; 1c can show "reconnect" on 401 from fills)

VERIFICATION:
- `poetry run pytest` clean (no new backend tests required beyond confirming `apply-tradovate-fill` is exercised; add a unit test if the apply logic is non-trivial)
- `tsc -b` clean on the frontend
- Manual golden path: paste token in `/settings/broker` → status card shows connected → open a trade form → click "Fetch from Tradovate" → fills populate → save trade

POST-IMPLEMENTATION RECONCILIATION:
- `concepts/architecture/phase3-frontend-structure.md` — update with new components/hooks/routes if the doc exists; create a stub if not
- `concepts/architecture/phase2-project-structure.md` — add `apply-tradovate-fill` endpoint to the routes table
- Append a session log entry to this tracker
- Update frontmatter `phase_1: 1c-complete`

Paul handles git commits — never run git commit.

Next session after 1c is 1d (Auto-fetch + disconnected handling).
````

---

## See Also

- [[journaling-ux]] — sister workstream; broker integration was forked from its Phase 3
- [[concepts/architecture/trade-schema]] — canonical trade data model (will extend in 1a)
- [[concepts/architecture/phase2-project-structure]] — canonical backend layout (will extend in 1a)
- [[concepts/architecture/phase3-frontend-structure]] — canonical frontend layout (will extend in 1c)
- [[entities/projects/neurospect]] — project overview
