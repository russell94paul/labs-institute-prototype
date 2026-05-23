---
tags: [distributed-workflow, active, neurospect, ai-coach, llm, tradingview]
aliases: [AI Coach Tracker, Trading Coach Module Tracker]
sources: []
created: 2026-04-22
updated: 2026-04-24
---

# AI Trading Coach — Workstream Tracker

The AI Coach is the most differentiated module of Neurospect. It connects Claude to live TradingView price data and the ICT strategy library to give the trader real-time coaching: which strategies are valid right now, which checklist items are met, and what still needs to happen before an entry is justified.

**Prerequisite:** `processes/distributed-workflow/active/course-and-kb.md` must be complete — specifically the entry models library with machine-readable YAML strategy blocks.

## Goal

By end of this workstream:

1. **Structured strategy data** — all entry models converted to a clean JSON format that an LLM can load in a system prompt and reason over efficiently.

2. **Claude system prompt template** — a well-engineered prompt that loads the strategy library, accepts live market context (price, structure, time, news), and outputs: active valid strategies, checklist status per strategy, and narrative commentary in ICT language.

3. **TradingView → backend connector** — a lightweight backend endpoint that receives price/structure data from TradingView (via webhook or Pine Script alert) and passes it to the Claude API.

4. **Live coaching response format** — a defined JSON response schema that the Neurospect frontend can render as: current valid setups, checklist cards, narrative text.

## Architecture Overview

```
TradingView (Pine Script)
    │  webhook alert (OHLCV + indicators + session + news flag)
    ▼
Neurospect Backend (REST endpoint)
    │  builds context payload
    ▼
Claude API
    │  system prompt: strategy library + ICT rules
    │  user message: current market context
    ▼
Coaching Response (JSON)
    │  valid_strategies[], checklist_status{}, narrative, bias
    ▼
Neurospect Frontend (coaching panel)
```

## Data Layers

### Layer 1 — Strategy Library (static, from entry models wiki)

JSON array of strategy objects loaded into Claude's system prompt. Each strategy object:
```json
{
  "id": "consolidation-model",
  "name": "Consolidation Model",
  "conditions": ["..."],
  "checklist": [
    {"id": "htf_fvg", "label": "HTF FVG bias confirmed", "timeframe": "1H-4H"},
    {"id": "below_open", "label": "Price below opening price (longs)"},
    ...
  ],
  "stop_logic": "Below the PDA",
  "target_logic": "Opposite side of range, then PDH/PDL",
  "kill_zones": ["london", "ny_am", "ny_pm"]
}
```

### Layer 2 — Live Market Context (dynamic, from TradingView)

What TradingView sends per alert:
```json
{
  "instrument": "NQ",
  "timestamp": "2026-04-22T09:45:00Z",
  "session": "ny_am",
  "open": 19820.50,
  "high": 19855.00,
  "low": 19810.25,
  "close": 19845.75,
  "midnight_open": 19830.00,
  "open_830": 19815.00,
  "open_930": 19822.50,
  "htf_fvg_bias": "bullish",
  "htf_fvg_range": [19800, 19850],
  "price_vs_midnight_open": "below",
  "news_flag": false,
  "structure_note": "optional free text from trader"
}
```

### Layer 3 — Claude Response Schema

```json
{
  "bias": "bullish",
  "narrative": "NQ is currently inside a 4H bullish FVG below the midnight open during NY AM. Smart money conditions favor accumulation here...",
  "valid_strategies": [
    {
      "strategy_id": "consolidation-model",
      "confidence": "high",
      "checklist": [
        {"id": "htf_fvg", "met": true, "note": "Inside 4H bullish FVG"},
        {"id": "below_open", "met": true, "note": "Below all 3 session opens"},
        {"id": "pda_at_eq", "met": false, "note": "Waiting for PDA near 50%"},
        ...
      ],
      "missing": ["Consolidation range not yet formed", "No PDA at EQ confirmed"],
      "watch_for": "Wait for intra-range SSL sweep then return to EQ"
    }
  ],
  "invalid_strategies": ["reversal-raid-on-stops", "smt-confirmation-entry"],
  "alerts": ["FOMC this week — avoid NY AM on Wednesday"]
}
```

## Implementation Plan

### Phase 1 — Strategy JSON (depends on: entry models library)
1. Write a script that parses `concepts/entry-models/*.md` YAML blocks → `data/strategies.json`
2. Review/validate the JSON output
3. Save to `concepts/ai-coach/strategies.json`

### Phase 2 — Claude System Prompt Engineering
1. Write `concepts/ai-coach/system-prompt-template.md` — the full system prompt with:
   - ICT conceptual rules (loaded from KB pages as compressed reference)
   - Strategy library (embedded JSON)
   - Instructions for reasoning over live context
   - Output format specification (JSON response schema)
2. Test prompt in Claude Workbench with mocked market context
3. Iterate until coaching responses are accurate and ICT-idiomatic

### Phase 3 — TradingView Connector
1. Design the Pine Script alert payload (what data to send)
2. Write Pine Script indicator that fires alerts with the JSON payload
3. Build the backend webhook endpoint (Python/FastAPI or Node)
4. Wire endpoint → Claude API call → return response

### Phase 4 — Frontend Coaching Panel
1. Define the UI: bias badge, narrative text, strategy cards with checklist items, watch-for text
2. Wire to backend response schema
3. Real-time or on-demand refresh (alert-triggered vs. poll)

## Session Log

### 2026-04-22 — planning

- did: created this tracker; defined architecture, data layers, response schema, implementation phases.
- decided: strategy library is JSON sourced from entry models YAML blocks — single source of truth in the wiki.
- decided: TradingView sends structured JSON via webhook alert; Claude does not directly access TradingView — all market data is passed as context.
- next: complete entry models library first (see course-and-kb.md tracker), then begin Phase 1 here.

### 2026-04-22 — Phase 1 + Phase 2 complete

- did: Phase 1 — parsed all 7 entry model YAML blocks → `concepts/ai-coach/strategies.json` (v1.0). Includes `_meta` block with universal minimum confluence rules, stop/target conventions; 7 strategy objects with conditions arrays, itemized checklist arrays (with `optional: true` flags on SMT items), stop/target logic strings, kill_zones arrays, avoid_conditions, and strategy-specific fields (smt_signal, retracement_quality, trigger_conditions, entry sub-object, etc.).
- did: Phase 2 — wrote `concepts/ai-coach/system-prompt-template.md` (v1.0). Full Claude system prompt with: ICT core rules (daily bias + stand-aside conditions, kill zones, PDA position, entry TF confirmation, HRLR/LRLR distinction, calendar protocols), `{{STRATEGY_LIBRARY_JSON}}` injection placeholder, 6-step reasoning sequence, strict JSON output matching Layer 3 schema, output rules (daily-bias-model never in valid/invalid; SMT never standalone invalid), input context schema documentation, testing checklist (8 scenarios).
- decided: `daily-bias-model` is applied internally by the prompt, never surfaced in `valid_strategies` / `invalid_strategies`. Keeps the frontend schema clean.
- decided: `smt-confirmation-entry` is a confidence multiplier within other strategies, not an independent invalid/valid decision. SMT absence is an unmet optional checklist item, not an invalid strategy.
- next: Phase 3 — design the Pine Script alert payload and the FastAPI backend webhook spec. Enter plan mode for this phase per the tracker instructions.

### 2026-04-22 — Phase 3 designed + implemented

- did: wrote `concepts/architecture/tradingview-connector.md` — end-to-end design for the Pine Script → FastAPI → Claude pipeline. Sections: architecture diagram, Pine input/computed/FVG-detection/alert-firing sections, webhook validation stack (token → secret → IP → Pydantic → dedupe), per-user `tradingview_tokens` table, `coaching_events` table, Claude prompt-cached system-message call, polling endpoint contract, Phase 3.5 open items, implementation map.
- did: built `assets/pine/neurospect-coach.pine` (v1.0) — Pine v5 indicator. Hybrid 4H FVG detection (auto via `request.security` + trader override inputs), deterministic session and opens tracking in America/New_York, JSON payload assembled via string concatenation, rising-edge `Request coaching` toggle triggers `alert()`.
- did: backend — added `CoachingEventStatus` enum, `TradingViewToken` + `CoachingEvent` ORM models, Alembic migration `0002_coach_tables.py` (ENUM + 2 tables + partial index on active tokens + composite idempotency uniq + user/created-desc index), `app/schemas/coach.py` (Layer2Payload extra=forbid; Layer3Response extra=allow for prompt forward-compat; `WebhookAccepted`, `CoachingEventResponse`, `TvTokenResponse`), `app/coach/prompt_loader.py` (fenced-block extraction + `{{STRATEGY_LIBRARY_JSON}}` substitution, cached via `lru_cache`), `app/coach/validation.py` (constant-time secret + env-driven IP allowlist with X-Forwarded-For), `app/coach/claude_client.py` (prompt-cached system block; defensive code-fence stripping; no auto-retry on parse error; error details truncated to 2000 chars), `app/coach/router.py` (webhook + `/api/coach/events/{id}` + `/latest`; idempotency handled via IntegrityError on the composite unique index), `app/routers/tv_tokens.py` (create-or-rotate atomic revoke + new insert). Config + `.env.example` updated with `TRADINGVIEW_WEBHOOK_SECRET`, `TRADINGVIEW_IP_ALLOWLIST`, `PUBLIC_BASE_URL`, `ANTHROPIC_API_KEY`, `CLAUDE_MODEL`, `CLAUDE_MAX_TOKENS`, `CLAUDE_TIMEOUT_SECONDS`, `AI_COACH_PROMPT_DIR`. `pyproject.toml` adds `anthropic ^0.40`.
- did: tests — `test_coach_pine_payload.py` (4 fixtures cover bullish NY AM / bearish London / off-session news / missing opens + negative tests for secret, session, extra fields), `test_coach_prompt_loader.py` (happy path + missing-placeholder + missing-files), `test_coach_validation.py` (secret happy/mismatch/unset, IP allowlist disabled/block/allowed-via-XFF).
- decided: hybrid FVG (Pine auto-detects 4H via `request.security` three-candle detector; trader overrides via `Manual FVG override` + low/high/bias inputs). Reason: auto gives a usable baseline; manual respects the ICT workflow where traders draw FVGs by hand.
- decided: on-demand trigger (bool input + rising edge) rather than per-bar-close. Reason: live-tape-read workflow; avoids Claude-API spam; trader controls coaching cadence directly.
- decided: per-user webhook token in URL path (`/webhooks/tradingview/{user_token}`). Generated via `secrets.token_urlsafe(32)`, stored in `tradingview_tokens`, revocable by flipping `revoked_at`. Two-factor: URL scopes user; body `secret` scopes source.
- decided: polling (`GET /api/coach/events/{id}` + `/latest`) for the response channel — simplest for 5–10 beta users. SSE is a drop-in upgrade later.
- decided: no auto-retry on Claude parse failure. Trader fires another request if they want a second attempt. Avoids silent bill burn on structurally broken prompts.
- note: Phase 2 backend scaffolding (main.py, deps.py, auth router, `0001_initial` migration) still needs to land before the new routers mount. Phase 3 files are written to plug into the approved Phase 2 structure once it lands.
- next: Phase 4 — frontend coaching panel (bias badge, narrative, strategy cards with checklist items, polling loop, TV token management UI).

### 2026-04-23 — cross-workstream alignment review (COMPLETE)

- did: Opus alignment pass reviewed all coach code against wiki docs. See `journal-analytics.md` 2026-04-23 session log for the full list of fixes.
- fixed (code): `tradingview_tokens.user_id` UNIQUE → partial unique index `WHERE revoked_at IS NULL`. Token rotation now works.
- fixed (code): `claude_client.py` `_build_user_message()` reads instrument from payload instead of hardcoding "NQ".
- fixed (code): `DateTime(timezone=True)` on all ORM timestamp columns (tv_token.py, coaching_event.py).
- fixed (wiki): `tradingview-connector.md` §3 DDL matches the partial unique index fix. Duplicate response corrected to 202. Test filenames corrected.
- fixed (wiki): `tech-stack.md` fully reconciled — auth, libs, env vars, webhook path, R2 layout all updated.
- next: Phase 4 — frontend coaching panel.

### 2026-04-24 — Phase 4 implementation (COMPLETE)

- did: implemented all Phase 4 frontend components in `C:\Users\PaulRussell\repos\neurospect-app`.
- **Types & constants (`src/types/api.ts`, `src/lib/constants.ts`):**
  - Added `CoachBias`, `Confidence`, `CoachingEventStatus` union types; `ChecklistItem`, `ValidStrategy`, `Layer3Response`, `CoachingEvent`, `TvTokenResponse` interfaces.
  - Added `COACH_BIAS_LABELS`, `COACH_BIAS_STYLES`, `CONFIDENCE_LABELS`, `CONFIDENCE_STYLES`, `STRATEGY_LABELS` to constants.
  - Deviation: used `CoachBias` (not `Bias`) to avoid naming collision with existing `BiasType` trade type. Constants named `COACH_BIAS_LABELS`/`COACH_BIAS_STYLES` accordingly.
- **Hooks:**
  - `src/hooks/use-coaching.ts` — `useLatestCoachingEvent()` (GET /api/coach/events/latest, 404→null, dynamic refetchInterval 2s pending / 10s otherwise) + `useCoachingEvent(id)`.
  - `src/hooks/use-tv-token.ts` — `useTvToken()` (404→null), `useRotateTvToken()` (POST /api/coach/tv-token), `useRevokeTvToken()` (DELETE /api/coach/tv-token). Both mutations invalidate `['coach', 'tv-token']`.
- **Coach panel components (`src/components/coach/`):**
  - `bias-badge.tsx` — Badge styled from `COACH_BIAS_STYLES`.
  - `confidence-pill.tsx` — small Badge from `CONFIDENCE_STYLES`.
  - `freshness-pill.tsx` — date-fns `differenceInSeconds`: <5m green / 5–30m amber / ≥30m gray.
  - `event-meta.tsx` — instrument · `formatDistanceToNow` · FreshnessPill · Claude latency.
  - `checklist-row.tsx` — `CheckCircle2` (green if met) / `Circle` (muted if not) + title-cased id + note.
  - `strategy-card.tsx` — Card with header (name + ConfidencePill), checklist rows, missing bullets, watch_for callout.
  - `invalid-strategies.tsx` — shadcn Collapsible, default closed, renders `STRATEGY_LABELS[id]`.
  - `alerts-banner.tsx` — amber Card per alert string with `AlertTriangle` icon; null if empty.
  - `coaching-panel.tsx` — composes all above; handles loading skeleton / null (404 empty state) / pending (pulse + skeletons) / error (red card) / complete states.
- **Setup components (`src/components/coach-setup/`):**
  - `token-card.tsx` — no-token state / generate; masked token display, readonly webhook URL + copy-to-clipboard; Rotate (Dialog) + Revoke (Dialog) confirmation patterns mirroring `trade-form.tsx`.
  - `pine-script-card.tsx` — Download button (link to `/neurospect-coach.pine`) + Collapsible `<pre>` with copy-to-clipboard (fetches from public URL at mount).
  - `tv-setup-instructions.tsx` — numbered steps Card: download → paste → set secret (must match `TRADINGVIEW_WEBHOOK_SECRET` env) → create alert with `neurospect-coach` condition → paste webhook URL in Notifications tab → flip `Request coaching` OFF→ON to fire.
- **Pages & routing:**
  - `src/pages/coach.tsx` — "AI Coach" title + Setup link-button; renders `<CoachingPanel />`.
  - `src/pages/coach-setup.tsx` — "Coach Setup" + Back to Coach; stacks TokenCard / PineScriptCard / TvSetupInstructions.
  - `src/App.tsx` — added `/coach` and `/coach/setup` routes under `ProtectedLayout`.
  - `src/components/layout/sidebar.tsx` — appended `{ to: '/coach', label: 'AI Coach', icon: Sparkles }`.
- **Static asset:** copied `neurospect-wiki/assets/pine/neurospect-coach.pine` → `app/public/neurospect-coach.pine`. Added Static Assets note to `app/README.md`.
- **Checkpoint:** `tsc -b` clean. Vite dev server starts on localhost:5173 with no errors.
- **Wiki docs:** created `concepts/architecture/phase4-coach-frontend.md` (canonical frontend-coach architecture doc). Updated `entities/projects/neurospect.md` (Phase 4 implemented). Updated `index.md` and `log.md`.

### 2026-04-24 — Phase 4 design (APPROVED)

- did: Opus plan-mode design session. Read backend contracts (`app/schemas/coach.py`, `app/coach/router.py`, `app/routers/tv_tokens.py`, `app/models/coaching_event.py`, `app/models/enums.py`) and existing frontend patterns in `app/src/` (routing in `App.tsx`, auth in `lib/auth.ts`, ky client in `lib/api.ts`, hook conventions in `hooks/use-trades.ts` + `hooks/use-analytics.ts`, Card/Dialog/Chart patterns in journal components). Verified no coach code exists in the frontend yet.
- decided: **Scope** — Phase 4 v1 is coaching panel + TV token setup page. **History deferred.** A history page would require a new backend list endpoint (`GET /api/coach/events?page=…` with user filter + pagination); revisit post-MVP if traders ask.
- decided: **Routes** — `/coach` (live coaching panel) and `/coach/setup` (TV token management + Pine script). Both under `ProtectedLayout`.
- decided: **Sidebar nav** — single new item `AI Coach` → `/coach` (Sparkles icon). Setup reached via a button in the coach page header, not a separate sidebar entry. Keeps the nav lean.
- decided: **Polling strategy** — one `useLatestCoachingEvent()` hook with dynamic `refetchInterval`: 2000ms when `status === 'pending'`, 10000ms when `complete` / `error` / 404. `refetchIntervalInBackground: false` (TanStack default) so polling pauses on hidden tabs. Matches the tracker's original "2–3s polling, 10s ceiling" guidance.
- decided: **Staleness model** — visual-only freshness pill on the panel: `<5m` green "Fresh", `5–30m` amber "Stale (Xm)", `≥30m` gray "Stale (Xh)" + muted panel. The event is always shown; staleness never suppresses it. If the trader wants fresh coaching, they fire another TV alert.
- decided: **Status rendering** — `pending` → skeleton + "Claude is thinking…"; `complete` → full panel; `error` → red card with `error_message` + hint to fire another alert; 404 → empty state CTA pointing at `/coach/setup`.
- decided: **Layer 3 component breakdown** — `BiasBadge`, `ConfidencePill`, `ChecklistRow` (CheckCircle2 / Circle icons), `StrategyCard` (one per `valid_strategy`), `InvalidStrategies` (shadcn Collapsible), `AlertsBanner` (amber Card), `EventMeta` (instrument · relative time · freshness · Claude latency), `FreshnessPill`, `CoachingPanel` (composer).
- decided: **Strategy ID labels** — hardcoded `STRATEGY_LABELS` map in `lib/constants.ts` covering all 7 entry models from `concepts/ai-coach/strategies.json` (`consolidation-model` → "Consolidation Model" etc.). Handles both `valid_strategies[].strategy_id` and `invalid_strategies[]` strings.
- decided: **Pine script distribution** — copy `assets/pine/neurospect-coach.pine` from this wiki into `app/public/neurospect-coach.pine`. Setup page shows a Download button + collapsible `<pre>` with copy-to-clipboard. Deliberate minor duplication; wiki file remains canonical. A README note in the frontend repo records the sync requirement.
- decided: **Backend unchanged** — existing 6 coach endpoints cover all Phase 4 v1 UI.
- decided: **Session split** — one Sonnet session (~4–5h). Scope is smaller than journal Session 2 or 3 and lives entirely in a self-contained `coach/` feature slice.
- decided: **Canonical frontend-coach architecture doc** — not pre-written. Per wiki Architecture Doc Integrity rules, the implementation session creates `concepts/architecture/phase4-coach-frontend.md` reconciled against actual code.
- plan file: `C:\Users\PaulRussell\.claude\plans\playful-juggling-galaxy.md` — full component list and file tree.
- next: execute Phase 4 using the boot prompt below (Boot Prompt D).

## Decisions Log

- 2026-04-22 — Claude does not call TradingView directly. TradingView pushes data to Neurospect backend; backend passes it to Claude as context. Keeps architecture simple and avoids real-time latency issues.
- 2026-04-22 — Strategy library is loaded in Claude's system prompt (not retrieved per-call). With 7-10 strategies and compact JSON, this fits comfortably within context limits.
- 2026-04-22 — Response is JSON not freetext, so the frontend can render checklist cards, strategy badges, and narrative separately.

## Resolved Decisions

- **Backend:** Python / FastAPI
- **Database:** Postgres (Render managed)
- **Hosting:** Render
- **TradingView:** Pro plan confirmed — webhooks available
- **Auth:** Discord OAuth2 ("Login with Discord") — user accounts linked to Discord identity
- **Scale:** Multi-user MVP for 5-10 beta users; build auth and schema with multi-tenancy from day one

## Open Questions

- Should coaching be triggered by TradingView alerts (reactive) or on a timer (proactive)?
- Discord bot integration for in-Discord coaching notifications — desired or out of scope for MVP?

## Boot Prompts

### A — Tech Stack Decision (run before any backend code is written)

**Recommended model:** Opus 4.7 + plan mode. This is an architecture decision session.

````
You are making the tech stack decision for the Neurospect backend — a decision
that affects both the AI Coach module and the Trade Journal module (they share a backend).

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`.
2. Read `processes/distributed-workflow/active/ai-coach.md` (this tracker).
3. Read `processes/distributed-workflow/active/journal-analytics.md`.
4. Read `entities/projects/neurospect.md` for the full architecture context.

Tech stack decisions are ALREADY MADE — do not re-litigate them:
- Backend: Python / FastAPI
- Database: Postgres (Render managed Postgres)
- Hosting: Render
- Auth: Discord OAuth2 ("Login with Discord") — Discord user ID as primary identifier
- TradingView: Pro plan confirmed, webhooks available
- Scale: multi-tenant from day one, 5-10 beta users initially

Your job: produce a decision doc at `concepts/architecture/tech-stack.md` that covers:
1. Full stack overview (FastAPI + Postgres + Render + Discord OAuth + TradingView webhooks)
2. Recommended Python libraries (FastAPI, SQLAlchemy or Tortoise ORM, Alembic, httpx, anthropic SDK)
3. Discord OAuth2 flow design (how login works, how Discord user ID maps to app user)
4. Render deployment architecture (web service + managed Postgres + env vars)
5. TradingView webhook ingestion pattern (endpoint design, security/secret validation)
6. File/screenshot storage recommendation (Cloudflare R2 or Render Disk)

Enter plan mode and walk Paul through the document before writing it.
````

### B — AI Coach Phase 1-2 (COMPLETE)

Phases 1 and 2 are done. Outputs: `concepts/ai-coach/strategies.json` (v1.0) and `concepts/ai-coach/system-prompt-template.md` (v1.0).

### C — AI Coach Phase 3 (COMPLETE)

Backend + Pine Script implemented. Design doc: `concepts/architecture/tradingview-connector.md`. Code: `app/coach/`, `app/routers/tv_tokens.py`, `app/schemas/coach.py`, `alembic/versions/0002_coach_tables.py`. Pine: `assets/pine/neurospect-coach.pine`.

### D — Phase 4 Implementation: Frontend Coaching Panel + TV Token Setup

**Recommended model:** Sonnet 4.6. Design is complete (see the 2026-04-24 session log); this is execution. **No plan mode needed.**

**Working directory:** `C:\Users\PaulRussell\repos\neurospect-app`.

**Scope (v1):** `/coach` live panel + `/coach/setup` TV token & Pine script page. History deferred.

````
You are implementing Phase 4 of the Neurospect AI Coach — the frontend coaching panel and TV token
setup page. Design is APPROVED (2026-04-24 in the tracker). Scope is a single session.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md` — pay attention to the Architecture
   Doc Integrity rules (§Source-of-truth hierarchy, §Post-implementation reconciliation).
2. Read `processes/distributed-workflow/active/ai-coach.md` — full tracker. Focus on the 2026-04-24
   Phase 4 design session log — every decision there is load-bearing.
3. Read `processes/distributed-workflow/active/journal-analytics.md` 2026-04-23 Session 1/2/3 log
   entries — the frontend patterns you must follow are documented there (hooks, forms, Cards, Dialogs).
4. Read backend API contracts in `C:\Users\PaulRussell\repos\neurospect-api`:
   - `app/schemas/coach.py` — `Layer2Payload`, `Layer3Response` (with `ValidStrategy`,
     `ChecklistItem`), `WebhookAccepted`, `CoachingEventResponse`, `TvTokenResponse`
   - `app/coach/router.py` — webhook + events endpoints (paths, auth, error codes)
   - `app/routers/tv_tokens.py` — TV token CRUD (paths, auth, atomic rotation behavior)
   - `app/models/enums.py` — `CoachingEventStatus` enum values (pending / complete / error)
5. Read existing frontend patterns in `C:\Users\PaulRussell\repos\neurospect-app\src\`:
   - `App.tsx` — routing + `ProtectedLayout`
   - `lib/api.ts`, `lib/auth.ts` — ky instance, `useAuth`, `TOKEN_KEY`
   - `hooks/use-trades.ts`, `hooks/use-analytics.ts` — query-key convention, mutation pattern,
     `refetchInterval` and `staleTime` usage
   - `components/layout/sidebar.tsx` — `navItems` array shape
   - `lib/constants.ts`, `types/api.ts` — label-map + interface conventions
   - `components/analytics/summary-cards.tsx`, `components/trade/trade-form.tsx` — Card, Dialog,
     skeleton, and empty-state patterns (reuse the delete-confirmation Dialog pattern)
6. Read `C:\Users\PaulRussell\repos\neurospect-wiki\assets\pine\neurospect-coach.pine` — this file
   gets copied into `app/public/` as a static asset. Read the alert-firing section so
   the setup instructions describe the Pine `Request coaching` toggle accurately.
7. Read `C:\Users\PaulRussell\repos\neurospect-wiki\concepts\ai-coach\strategies.json` — confirm
   the 7 strategy IDs for the `STRATEGY_LABELS` map.

Context from the design:
- Backend is COMPLETE and alignment-reviewed. 6 coach endpoints live. Claude call runs as async
  `BackgroundTask` (sync within the task). Polling channel at `GET /api/coach/events/latest`.
- Frontend has no coach code — confirmed. All patterns (hooks, routing, forms, Cards, shadcn) are
  established by Sessions 1–3 of the journal module. Follow them; do not invent new conventions.
- No new shadcn components needed — Collapsible, Dialog, Card, Button, Badge are all installed.

Implementation (in order):

**Phase A — Types & constants:**
1. Extend `src/types/api.ts`:
   - Union types: `Bias = 'bullish' | 'bearish' | 'neutral' | 'stand_aside'`;
     `Confidence = 'high' | 'medium' | 'low'`;
     `CoachingEventStatus = 'pending' | 'complete' | 'error'`.
   - Interfaces: `ChecklistItem {id: string; met: boolean; note: string}`;
     `ValidStrategy {strategy_id: string; confidence: Confidence; checklist: ChecklistItem[];
       missing: string[]; watch_for: string}`;
     `Layer3Response {bias: Bias; narrative: string; valid_strategies: ValidStrategy[];
       invalid_strategies: string[]; alerts: string[]}` (allow extra fields — backend uses
       `extra="allow"` for forward-compat);
     `CoachingEvent {id: string; status: CoachingEventStatus; instrument: string;
       alert_timestamp: string; request_payload: Record<string, unknown>;
       response_payload: Record<string, unknown> | null; error_message: string | null;
       claude_latency_ms: number | null; created_at: string; completed_at: string | null}`;
     `TvTokenResponse {token: string; webhook_url: string; created_at: string}`.
2. Extend `src/lib/constants.ts`:
   - `BIAS_LABELS: Record<Bias, string>` (e.g. `bullish` → "Bullish", `stand_aside` → "Stand Aside").
   - `BIAS_STYLES: Record<Bias, string>` — Tailwind class strings. Bullish=green, bearish=red,
     neutral=slate, stand_aside=amber. Match the color vocabulary used by `status-badge.tsx`.
   - `CONFIDENCE_LABELS` + `CONFIDENCE_STYLES` (high=green, medium=amber, low=slate).
   - `STRATEGY_LABELS: Record<string, string>` — all 7 strategy IDs from strategies.json:
     `consolidation-model` → "Consolidation Model",
     `expansion-retracement-model` → "Expansion & Retracement Model",
     `reversal-raid-on-stops` → "Reversal — Raid on Stops",
     `london-model` → "London Model",
     `model-2022-ote` → "Model 2022 (OTE)",
     `daily-bias-model` → "Daily Bias Model",
     `smt-confirmation-entry` → "SMT Confirmation Entry".

**Phase B — Hooks:**
3. `src/hooks/use-coaching.ts`:
   - `useLatestCoachingEvent()` — `GET /api/coach/events/latest`. Query key `['coach', 'latest']`.
     On 404, return `null` rather than throwing (wrap the ky call in a try/catch on `HTTPError` with
     `error.response.status === 404`). Dynamic `refetchInterval`:
     `(query) => query.state.data?.status === 'pending' ? 2000 : 10000`.
     Do NOT set `refetchIntervalInBackground` (default false is what we want).
   - `useCoachingEvent(id: string | undefined)` — `GET /api/coach/events/{id}`, `enabled: !!id`.
     Kept for future deep-linking; not used by Phase 4 UI.
4. `src/hooks/use-tv-token.ts`:
   - `useTvToken()` — `GET /api/coach/tv-token`. Query key `['coach', 'tv-token']`. Treat 404 as
     `data: null` using same pattern as `useLatestCoachingEvent`. Default `staleTime` is fine.
   - `useRotateTvToken()` — mutation `POST /api/coach/tv-token` → `TvTokenResponse`. On success
     invalidate `['coach', 'tv-token']`.
   - `useRevokeTvToken()` — mutation `DELETE /api/coach/tv-token`. On success invalidate
     `['coach', 'tv-token']`.

**Phase C — Coaching panel components (`src/components/coach/`):**
5. `bias-badge.tsx` — colored pill driven by `BIAS_LABELS` + `BIAS_STYLES`.
6. `confidence-pill.tsx` — small colored pill driven by `CONFIDENCE_LABELS` + `CONFIDENCE_STYLES`.
7. `freshness-pill.tsx` — computes tier from `created_at`: <5m green "Fresh"; 5–30m amber
   "Stale (Xm)"; ≥30m gray "Stale (Xh)". Use `date-fns` `differenceInSeconds`.
8. `event-meta.tsx` — inline row `{instrument} · {relativeTime (formatDistanceToNow)} · <FreshnessPill> · Claude {latency}ms`.
   Muted text except the pill.
9. `checklist-row.tsx` — icon (CheckCircle2 green if `met`, else Circle muted) + Title-Cased `id` +
   `note` in muted text after an em-dash.
10. `strategy-card.tsx` — shadcn Card. Header: `STRATEGY_LABELS[strategy_id] ?? strategy_id` +
    `<ConfidencePill>`. Body: Checklist list (map to `<ChecklistRow>`); Missing section (bulleted,
    skip if empty); "Watch for" callout (skip if empty string).
11. `invalid-strategies.tsx` — shadcn Collapsible, default closed. Header `"Invalid Strategies (N)"`.
    Contents: list of `STRATEGY_LABELS[id] ?? id`. Return null if empty.
12. `alerts-banner.tsx` — amber Card with `AlertTriangle` icon per alert string. Return null if empty.
13. `coaching-panel.tsx` — composer:
    - Calls `useLatestCoachingEvent()`.
    - `isLoading && !data` → Skeleton card.
    - `data === null` (404) → empty-state Card: "No coaching yet. Configure TradingView in
      [Setup](→ /coach/setup) to receive coaching."
    - `data.status === 'pending'` → `<EventMeta>` + pulsing "Claude is thinking…" + skeletons
      for strategy cards.
    - `data.status === 'error'` → red Card with `data.error_message` (monospaced, wrapped) +
      hint "Fire another alert from TradingView to try again."
    - `data.status === 'complete'` → `<EventMeta>` + narrative paragraph + `<AlertsBanner>` +
      stacked `<StrategyCard>`s from `(data.response_payload as Layer3Response).valid_strategies` +
      `<InvalidStrategies>`. Defensively check `response_payload` is truthy.

**Phase D — Setup page components (`src/components/coach-setup/`):**
14. `token-card.tsx` — uses `useTvToken()`, `useRotateTvToken()`, `useRevokeTvToken()`:
    - `data === null` → "No active token" + "Generate Token" button (calls rotate mutation).
    - Otherwise: masked token display (`token.slice(0,6) + '…' + token.slice(-6)`),
      `webhook_url` input (readonly) with copy-to-clipboard button (use `navigator.clipboard`),
      `created_at` formatted, "Rotate Token" button (Dialog confirmation), "Revoke Token" button
      (Dialog confirmation).
    - Mirror the delete-confirmation Dialog pattern from `trade-form.tsx`.
15. `pine-script-card.tsx` — shadcn Card:
    - "Download Pine Script" button linking to `/neurospect-coach.pine`.
    - Collapsible `<pre>` showing the script (fetch from `/neurospect-coach.pine` at mount; no
      caching concerns — static file). Copy-to-clipboard button.
16. `tv-setup-instructions.tsx` — shadcn Card with numbered steps covering: download Pine script,
    paste into TradingView Pine Editor, add to chart, create alert with `Request coaching`
    condition, paste webhook URL from Token Card into the Webhook URL field, save. Include a
    callout noting that the `secret` field in the Pine payload must match the backend's
    `TRADINGVIEW_WEBHOOK_SECRET` env var. Read the Pine script at Boot step 6 so the wording
    matches the actual alert mechanics.

**Phase E — Pages & routing:**
17. `src/pages/coach.tsx` — title "AI Coach" with a right-aligned "Setup" link-button to
    `/coach/setup`. Body: `<CoachingPanel />`.
18. `src/pages/coach-setup.tsx` — title "Coach Setup" with a "Back to Coach" link. Body: vertical
    `space-y-6` stack of `<TokenCard>`, `<PineScriptCard>`, `<TvSetupInstructions>`.
19. Update `src/App.tsx`:
    - Add `{ path: '/coach', element: <CoachPage /> }` under `ProtectedLayout` children.
    - Add `{ path: '/coach/setup', element: <CoachSetupPage /> }` under same.
20. Update `src/components/layout/sidebar.tsx`:
    - Append `{ to: '/coach', label: 'AI Coach', icon: Sparkles }` to `navItems`. Import
      `Sparkles` from `lucide-react`.

**Phase F — Static asset & repo hygiene:**
21. Copy `C:\Users\PaulRussell\repos\neurospect-wiki\assets\pine\neurospect-coach.pine` to
    `C:\Users\PaulRussell\repos\neurospect-app\public\neurospect-coach.pine`.
22. Add a note to `app/README.md` (create if missing) under a "Static Assets" heading:
    `public/neurospect-coach.pine` is a mirror of the wiki's canonical file at
    `C:\Users\PaulRussell\repos\neurospect-wiki\assets\pine\neurospect-coach.pine`. Re-sync
    manually when the wiki version bumps.

**Session checkpoint (verify before stopping):**
1. `tsc -b` clean, `npm run dev` starts on localhost:5173 with no console errors.
2. Sidebar shows "AI Coach" nav item with Sparkles icon; clicking navigates to `/coach`.
3. `/coach/setup`:
   - No token state → "Generate Token" works; token + webhook URL appear.
   - Rotate → confirmation Dialog → new token replaces old; webhook URL updates.
   - Revoke → confirmation Dialog → returns to "No active token" state.
   - Pine script download returns the file with correct content.
   - Script content renders in collapsible; copy-to-clipboard works.
4. `/coach`:
   - No events in DB → empty state with CTA linking to `/coach/setup`.
   - Fire a test webhook via `curl` using the token from Setup and `TRADINGVIEW_WEBHOOK_SECRET`
     from backend `.env` — panel flips to `pending` skeleton then to `complete` with bias,
     narrative, strategy cards, checklist, alerts after Claude responds.
   - If `ANTHROPIC_API_KEY` is unset, event flips to `error` status — panel shows red error card.
   - Freshness pill transitions as the event ages (wait a few minutes or manipulate
     `created_at` via DB to test).
5. Navigating away from `/coach` and back stops/restarts polling cleanly (check Network tab).

**Post-session (MANDATORY per wiki Architecture Doc Integrity rules):**
- Append a Phase 4 COMPLETE entry to the ai-coach tracker's §Session Log. Include every file
  created, any deviations, and decisions made mid-flight.
- Create `concepts/architecture/phase4-coach-frontend.md` in the wiki as the canonical
  frontend-coach architecture doc (routes, hooks, components, polling, Pine asset sync). Reconcile
  against actual shipped code, not this boot prompt.
- Update `entities/projects/neurospect.md` — move Phase 4 from "designed" to "implemented".
- Update `index.md` — add the new architecture doc under Concepts → Architecture; bump
  `last_build` frontmatter.
- Append a row to `log.md` (`YYYY-MM-DD | build | Phase 4 (AI Coach frontend) implemented. …`).

Backend must be running with `DEBUG=true` during development (`cd neurospect-api && uvicorn app.main:app --reload`).
Paul handles git commits — never run `git commit`.
````


## See Also

- [[concepts/roadmap/README]] — strategic context (AI Coach surface underpins multiple Later/Strategic ideas)
- [[processes/distributed-workflow/active/course-and-kb]] — prerequisite (entry models library)
- [[processes/distributed-workflow/active/journal-analytics]] — sister module
- [[entities/projects/neurospect]] — full project overview and roadmap
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
