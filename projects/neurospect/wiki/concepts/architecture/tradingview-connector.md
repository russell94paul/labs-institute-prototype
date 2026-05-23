---
tags: [architecture, ai-coach, tradingview, webhook, claude, neurospect, backend]
aliases: [TradingView Connector, AI Coach Phase 3, Coach Pipeline]
sources: [processes/distributed-workflow/active/ai-coach.md, concepts/ai-coach/system-prompt-template.md, concepts/ai-coach/strategies.json, concepts/architecture/tech-stack.md, concepts/architecture/phase2-project-structure.md]
created: 2026-04-22
updated: 2026-04-23
---

# TradingView Connector (AI Coach Phase 3)

End-to-end design for the live coaching pipeline: TradingView Pine Script alert → FastAPI webhook → Claude API → Layer 3 JSON response → frontend polling endpoint. Phase 3 of the AI Coach workstream.

## Overview

The trader runs a custom Pine Script indicator on their NQ chart. When they flip the indicator's `Request coaching` toggle, Pine's `alert()` fires a webhook carrying the [[processes/distributed-workflow/active/ai-coach|Layer 2]] market-context payload. The backend validates the payload, persists it, dispatches the Claude call in a background task, and stores the [[processes/distributed-workflow/active/ai-coach|Layer 3]] coaching response. The frontend polls a GET endpoint until the coaching response is ready.

```
TradingView Pine Script (NQ chart)
  │ trader flips "Request coaching" toggle (rising edge)
  │ alert() fires JSON body
  ▼
POST /webhooks/tradingview/{user_token}   →  202 Accepted + {coaching_event_id}
  │ 1. user_token → user_id             (401 if unknown / revoked)
  │ 2. hmac.compare_digest(body.secret)  (401 if mismatch)
  │ 3. IP allowlist                      (403 if not in list)
  │ 4. Pydantic Layer2Payload            (422 if malformed)
  │ 5. dedupe on idempotency_key         (200 duplicate if seen)
  │ 6. INSERT coaching_events (pending)
  │ 7. BackgroundTasks → run_claude_call
  ▼
Background: run_claude_call(event_id)
  │ 1. load system prompt (template + strategies.json, cached once at boot)
  │ 2. anthropic.messages.create(system=[...prompt-cached...], user=layer2)
  │ 3. parse + validate Layer 3 JSON
  │ 4. UPDATE coaching_events → complete | error
  ▼
Frontend polls
  GET /api/coach/events/{id}           → {status, response_payload, ...}
  GET /api/coach/events/latest         → most recent event for user
```

## Design decisions (resolved 2026-04-22)

| Decision | Choice | Rationale |
|---|---|---|
| HTF FVG source in Pine | **Hybrid** — auto-detect with manual override | Auto-detection is a starting point; the trader retains final say via an override that fits the manual ICT drawing workflow. |
| Alert trigger | **On-demand toggle** (bool input, rising edge) | Matches live-tape-read workflow. Avoids Claude-API spam. Cheap at scale. |
| Multi-tenant routing | **Per-user token in URL path** | Revocable scoping layer on top of the global shared secret. Two independent factors (URL token = user; body secret = source). |
| Response channel | **Polling** (2–3 s cadence) | Simplest for 5–10 beta users. Stateless. SSE/WS can replace it without changing the webhook side. |

## 1. Pine Script indicator

Source: `assets/pine/neurospect-coach.pine`. Pine v5. Installs as a custom study on the trader's chart.

### Inputs

| Group | Name | Type | Notes |
|---|---|---|---|
| Credentials | `Webhook shared secret` | string (confirm) | Must match `TRADINGVIEW_WEBHOOK_SECRET` on the backend. |
| Trigger | `Request coaching` | bool | Rising edge (OFF→ON) fires one alert. |
| HTF FVG | `Manual FVG override` | bool | When true, uses the three inputs below. |
| HTF FVG | `Manual FVG bias` | `bullish` / `bearish` / `neutral` | Used only when override is on. |
| HTF FVG | `Manual FVG low` / `high` | float | Used only when override is on. |
| Context | `News flag` | bool | FOMC/CPI/NFP toggle. Phase 3 is manual; Phase 3.5 replaces with calendar API. |
| Context | `Structure note` | string | Optional free-text trader observation. |

### Computed (deterministic, each bar)

- **`instrument`** ← `syminfo.ticker`
- **`timestamp`** ← UTC ISO-8601 of current bar
- **`session`** ← minute-of-day (ET) → `london` (02:00–05:00), `ny_am` (08:30–11:30), `ny_pm` (13:30–16:00), else `off`
- **`open` / `high` / `low` / `close`** ← current bar
- **`midnight_open`, `open_830`, `open_930`** ← `var float` snapshots on the bar that opens 00:00 / 08:30 / 09:30 ET; survive subsequent bars via Pine's `var` persistence
- **`price_vs_midnight_open`** ← `below` / `above` / `at` / `na`
- **`idempotency_key`** ← `ticker + ":" + time + ":" + bar_index` — stable per (symbol, bar) so Pine retries collapse

### Auto-detected 4H FVG

`request.security(symbol, "240", detect4hFvg(), lookahead=off)` calls a three-candle detector on the 4H timeframe. At confirmed 4H bar close:

- **Bullish FVG:** `low[1] > high[3]` → range = `[high[3], low[1]]`, bias = `bullish`
- **Bearish FVG:** `high[1] < low[3]` → range = `[high[1], low[3]]`, bias = `bearish`
- Stored in `var` so the most-recent FVG persists until a new one forms.

`fvg_source` is emitted in the payload as `"auto"` or `"manual"` so the coach (and any downstream analysis) knows which path produced the numbers.

### Alert firing

```pine
var bool prevRequest = false
fire = requestCoaching and not prevRequest
prevRequest := requestCoaching
if fire
    alert(body, alert.freq_once_per_bar)
```

The body is assembled as a JSON string via concatenation (str.format is avoided because JSON braces collide with its placeholder syntax). The alert fires exactly once per OFF→ON transition; the trader flips the toggle back to arm the next request.

### Payload (Layer 2 — matches `system-prompt-template.md` Input Context Schema)

```json
{
  "secret": "<TRADINGVIEW_WEBHOOK_SECRET>",
  "idempotency_key": "NQ1!:1714046700000:12345",
  "instrument": "NQ1!",
  "timestamp": "2026-04-22T13:45:00Z",
  "session": "ny_am",
  "open": 19820.50, "high": 19855.00, "low": 19810.25, "close": 19845.75,
  "midnight_open": 19830.00, "open_830": 19815.00, "open_930": 19822.50,
  "htf_fvg_bias": "bullish",
  "htf_fvg_range": [19800.00, 19850.00],
  "price_vs_midnight_open": "below",
  "news_flag": false,
  "structure_note": "",
  "fvg_source": "auto"
}
```

## 2. Webhook endpoint

`POST /webhooks/tradingview/{user_token}` — unauthenticated (no session cookie/JWT); secured by the validation stack.

### Validation stack (in order)

1. **`user_token` lookup** → `tradingview_tokens` table where `revoked_at IS NULL`. Miss → `401 invalid token`.
2. **Body `secret` check** → `hmac.compare_digest(body.secret, settings.tradingview_webhook_secret)`. Mismatch → `401 invalid secret`.
3. **IP allowlist** → client IP (`X-Forwarded-For` first hop on Render) must be in `TRADINGVIEW_IP_ALLOWLIST` (comma-separated env var). Miss → `403 ip not allowed`. The list is env-sourced because [TradingView's published IPs drift](https://www.tradingview.com/support/solutions/43000529348/); rotating them is a config change, not a redeploy.
4. **Pydantic `Layer2Payload.model_validate`** → malformed → `422`.
5. **Idempotency dedupe** → `UNIQUE(user_id, idempotency_key)` constraint on `coaching_events`. `IntegrityError` on insert → rollback, select existing row → `202 {"status":"duplicate","coaching_event_id":"..."}`.

Responses:

| Status | Body |
|---|---|
| 202 | `{"status":"accepted","coaching_event_id":"<uuid>"}` |
| 202 | `{"status":"duplicate","coaching_event_id":"<uuid>"}` |
| 401 | `{"detail":"invalid token"}` / `{"detail":"invalid secret"}` |
| 403 | `{"detail":"ip not allowed"}` |
| 422 | Pydantic error array |

### Background dispatch

After persisting the pending row, the handler schedules `run_claude_call(event_id)` via FastAPI `BackgroundTasks` and returns `202`. The Claude call (5–20 s) must not block the HTTP response — TradingView's webhook timeout is aggressive and retries aggressively.

## 3. Per-user TradingView token

A revocable secret embedded in the webhook URL that identifies the user.

### Schema

```sql
CREATE TABLE tradingview_tokens (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token       TEXT NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revoked_at  TIMESTAMPTZ
);
CREATE INDEX ix_tv_tokens_token ON tradingview_tokens(token) WHERE revoked_at IS NULL;
CREATE UNIQUE INDEX uq_tv_tokens_user_active ON tradingview_tokens(user_id) WHERE revoked_at IS NULL;
```

The partial unique index `uq_tv_tokens_user_active` enforces one **active** (unrevoked) token per user while allowing old revoked rows to remain for audit. Rotating a token = `UPDATE ... SET revoked_at = NOW()` on the old row + insert a new one. Lookup on the webhook path filters `revoked_at IS NULL`.

Token generation: `secrets.token_urlsafe(32)` → ~43-char URL-safe string.

### REST surface

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/api/coach/tv-token` | Discord JWT | Create or rotate the user's token. Returns `{token, webhook_url}`. |
| `GET` | `/api/coach/tv-token` | Discord JWT | Current (unrevoked) token + webhook URL. 404 if none issued. |
| `DELETE` | `/api/coach/tv-token` | Discord JWT | Revoke current token. No body. |

The UI reads `webhook_url` and shows the trader the exact URL to paste into TradingView's Alert → Notifications → Webhook URL field.

## 4. `coaching_events` table

One row per coach invocation. JSONB holds both the request and the response verbatim for replay and audit. The row is progressively updated from `pending` → `complete` / `error`.

```sql
CREATE TYPE coaching_event_status AS ENUM ('pending', 'complete', 'error');

CREATE TABLE coaching_events (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id),
    idempotency_key     TEXT NOT NULL,
    instrument          VARCHAR(20) NOT NULL,
    alert_timestamp     TIMESTAMPTZ NOT NULL,
    request_payload     JSONB NOT NULL,
    response_payload    JSONB,
    status              coaching_event_status NOT NULL DEFAULT 'pending',
    error_message       TEXT,
    claude_latency_ms   INTEGER,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ,
    UNIQUE (user_id, idempotency_key)
);
CREATE INDEX ix_coach_events_user_created ON coaching_events(user_id, created_at DESC);
```

`UNIQUE (user_id, idempotency_key)` enforces dedupe at the DB layer — a race between two webhook calls can't both insert.

## 5. Claude call orchestration

### System prompt assembly (once, at app startup)

- Read [[concepts/ai-coach/system-prompt-template.md]] (the fenced prompt block between the first and second `---` after `## The Prompt`).
- Read [[concepts/ai-coach/strategies.json]].
- Substitute `{{STRATEGY_LIBRARY_JSON}}` with the serialized strategies file.
- Cache the assembled string in process memory (it is identical for every call).

### Claude request

```python
client.messages.create(
    model=settings.claude_model,               # default: claude-sonnet-4-6
    max_tokens=2048,
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}, # 5-min TTL
    }],
    messages=[{
        "role": "user",
        "content": "Live market context for NQ:\n\n```json\n"
                   + json.dumps(layer2_payload) + "\n```",
    }],
    timeout=30.0,
)
```

Prompt caching is load-bearing for cost: the system block is large, identical across calls, and a trading session naturally fires coaching calls inside the 5-minute cache window. Without it, the strategy library + rules re-bill on every call.

### Response handling

- Strip code fences if present (defensive — the prompt instructs raw JSON).
- `json.loads` → `Layer3Response.model_validate` (Pydantic, structure mirrors [[processes/distributed-workflow/active/ai-coach|Layer 3]]).
- On success: `UPDATE coaching_events SET response_payload = :resp, status = 'complete', completed_at = NOW(), claude_latency_ms = :ms`.
- On parse failure or SDK error: `status = 'error'`, `error_message = <first 2000 chars>`. **No automatic retry.** The trader fires another request if they want a second attempt — avoids silent Claude bill burn on structurally broken prompts.

### Model selection

`CLAUDE_MODEL` env var, default `claude-sonnet-4-6`. Opus escalation (`claude-opus-4-7`) is a config flip for multi-strategy or noisy-market sessions — matches the guidance in [[concepts/ai-coach/system-prompt-template.md]] v1.0.

## 6. Polling endpoint

```
GET /api/coach/events/{id}      — auth: Discord JWT
GET /api/coach/events/latest    — auth: Discord JWT
```

Both return:

```json
{
  "id": "uuid",
  "status": "pending | complete | error",
  "instrument": "NQ1!",
  "alert_timestamp": "2026-04-22T13:45:00Z",
  "request_payload":  { ...Layer 2... },
  "response_payload": { ...Layer 3... } | null,
  "error_message": null | "...",
  "claude_latency_ms": 8432 | null,
  "created_at": "...",
  "completed_at": null | "..."
}
```

The frontend fires the webhook (via the Pine alert → TradingView), then begins polling every 2–3 s until `status != "pending"`. Ten-second ceiling on pending before showing a spinner timeout message; the row stays in the DB either way.

### Why polling over SSE / WS

- 5–10 beta users, one coaching call every few minutes at most → polling is free.
- No long-lived connections to manage on Render's free/starter plan.
- SSE is a drop-in upgrade later: replace the poll loop with an `EventSource` that reads completion events from a pg `LISTEN/NOTIFY` fanout. The webhook/storage side does not change.

## 7. Multi-user routing flow

1. User signs in via Discord OAuth → `users` row upserted.
2. User visits the coach settings page → frontend hits `POST /api/coach/tv-token` → receives `{token, webhook_url}`.
3. User installs `neurospect-coach.pine` on their chart, enters the shared secret, then creates a TradingView alert with `webhook_url` in the Notifications panel.
4. Pine `alert()` fires → webhook → backend routes to the user via `user_token`.

Because the token is in the URL path, it appears in Render logs — treat it as a bearer credential. Rotation is one API call; compromised tokens are revoked by flipping `revoked_at`.

## 8. Open items for Phase 3.5+

- **News-calendar enrichment.** Replace the manual `news_flag` toggle with a backend lookup against an economic calendar provider (e.g. TradingEconomics, Finnhub). Augment the Layer 2 payload before handing it to Claude.
- **SSE upgrade** for the polling endpoint. Low priority until live-commentary Phase 4 lands.
- **Retry policy on transient Claude errors.** Current design: no retry. Add bounded exponential retry on 5xx / timeout, with `retry_count` column.
- **Opus escalation heuristic.** Today: manual `CLAUDE_MODEL` flip. Potential: auto-escalate when `valid_strategies.length >= 3` OR `alerts` contains a news protocol flag.
- **Coaching → journal pre-fill.** Coaching Layer 3 response → pre-populate a `POST /api/trades` draft with `htf_bias`, `setup_type`, `narrative` (see [[concepts/architecture/trade-schema|AI Coach ↔ Journal Mapping]]).
- **Rate limiting** per-user (e.g. 1 req / 10 s) once multiple beta users are hitting the endpoint concurrently.

## 9. Implementation map

| Artefact | Location |
|---|---|
| Pine Script indicator | `neurospect-wiki/assets/pine/neurospect-coach.pine` |
| Alembic migration | `api/alembic/versions/0002_coach_tables.py` |
| ORM — TradingView token | `api/app/models/tv_token.py` |
| ORM — coaching event | `api/app/models/coaching_event.py` |
| Coach internals | `api/app/coach/prompt_loader.py`, `validation.py`, `claude_client.py` |
| Coach router | `api/app/coach/router.py` (replaces the Phase 2 501 stub) |
| TV-token router | `api/app/routers/tv_tokens.py` |
| Schemas | `api/app/schemas/coach.py` |
| Config additions | `api/app/config.py` (env vars), `pyproject.toml` (`anthropic`) |
| Tests | `api/tests/test_coach_pine_payload.py`, `test_coach_prompt_loader.py`, `test_coach_validation.py` |

## See Also

- [[processes/distributed-workflow/active/ai-coach]] — AI Coach workstream tracker
- [[concepts/ai-coach/system-prompt-template]] — the Claude system prompt
- [[concepts/ai-coach/strategies.json]] — strategy library (injected into the prompt)
- [[concepts/architecture/trade-schema]] — journal schema (AI Coach ↔ Journal mapping section)
- [[concepts/architecture/tech-stack]] — shared backend stack (webhook validation doctrine is §5)
- [[concepts/architecture/phase2-project-structure]] — backend scaffold Phase 3 drops into
- [[entities/projects/neurospect]] — project overview
