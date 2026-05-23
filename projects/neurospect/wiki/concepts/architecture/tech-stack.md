---
tags: [architecture, tech-stack, neurospect, backend, fastapi, postgres, render, discord-oauth, tradingview]
aliases: [Tech Stack, Backend Stack, Neurospect Backend Stack]
sources: []
created: 2026-04-22
updated: 2026-04-23
---

# Tech Stack

Canonical decision doc for the Neurospect backend. The **AI Trading Coach** and the **Trade Journal & Analytics** modules share one FastAPI app, one Postgres database, one auth layer, and one object-store bucket. This doc pins every load-bearing technology choice so both workstreams build on identical foundations.

The stack-level decisions (FastAPI, Postgres on Render, Render hosting, Discord OAuth2, TradingView Pro webhooks, multi-tenant from day one) are **pre-decided**. The job of this doc is to resolve the specifics: which libraries, which auth mechanics, what the Render topology looks like, how the TradingView webhook is secured, and where user-uploaded screenshots live.

Both module trackers — [[processes/distributed-workflow/active/ai-coach]] and [[processes/distributed-workflow/active/journal-analytics]] — boot their implementation phases from this document.

## 1. Stack Overview

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12+ | Claude SDK is Python-first; trade-schema spec is already written against SQLAlchemy. |
| Web framework | FastAPI | Async-native, Pydantic validation, OpenAPI for free, excellent DI. |
| ASGI server (dev) | `uvicorn[standard]` | Standard FastAPI dev server. |
| ASGI server (prod) | `gunicorn` + `uvicorn.workers.UvicornWorker` | Graceful restarts, worker management under Render. |
| ORM | SQLAlchemy 2.0 (async) | Pinned by [[concepts/architecture/trade-schema]] Phase 1. Mature async story with `asyncpg`. |
| DB driver | `asyncpg` | Fastest Postgres driver for async SQLAlchemy. |
| Migrations | Alembic | Standard pair with SQLAlchemy; autogenerate + env-aware revisions. |
| Database | Postgres 16 (Render managed) | Required by the trade schema: ENUMs, JSONB, `TEXT[] GIN`, `TIMESTAMPTZ`, `uuid-ossp`/`gen_random_uuid`. |
| Validation / DTOs | Pydantic v2 | Native FastAPI integration; `pydantic-settings` for env loading. |
| HTTP client | `httpx` (async) | Used for Discord token exchange and any non-SDK Claude edge cases. |
| Claude SDK | `anthropic` (official) | Supports prompt caching for the static strategy-library system prompt. |
| JWT auth | `python-jose[cryptography]` | HS256 JWT signing/verification. SPA pattern — frontend captures Discord code, backend returns JWT. |
| Object storage | Cloudflare R2 (S3-compatible) via `boto3` | Zero egress, decoupled from Render compute. See §7. |
| Webhook auth | Shared-secret-in-body + IP allowlist + idempotency | TradingView doesn't sign webhooks. See §6. |
| Background jobs | FastAPI `BackgroundTasks` | MVP only. Upgrade to Arq/RQ when we outgrow it. No Celery, no Redis until justified. |
| Logging | `structlog` (JSON) → Render log drains | **Not yet added.** Planned for prod readiness. |
| Error tracking | Sentry (optional, env-gated) | **Not yet added.** Free tier is sufficient for 5–10 beta users. |
| Testing | `pytest`, `pytest-asyncio`, `httpx` | In `pyproject.toml` dev deps. `testcontainers` planned but not yet added. |
| Lint / types | `ruff`, `mypy` | **Not yet added.** Planned for prod readiness. |

### System diagram

```
                        ┌───────────────────────────┐
                        │        Discord OAuth2     │
                        │   (identify scope only)   │
                        └─────────────┬─────────────┘
                                      │ callback (code → token → @me)
                                      ▼
  TradingView Pro ──webhook──▶  ┌─────────────────────┐  ──Claude API──▶  Anthropic
  (Pine Script alert)           │   FastAPI backend   │
                                │   (Render web svc)  │  ──presigned───▶  Cloudflare R2
                                └──────────┬──────────┘      URLs
                                           │ async SQLAlchemy
                                           ▼
                                  ┌──────────────────┐
                                  │ Postgres 16      │
                                  │ (Render managed) │
                                  └──────────────────┘
```

## 2. Python Libraries — pinned recommendations

> **Canonical source:** `api/pyproject.toml`. This list summarises what's installed.

Runtime (in `pyproject.toml`):

- `fastapi` — web framework.
- `uvicorn[standard]` — dev server.
- `sqlalchemy[asyncio]>=2.0` — ORM. Async engine + async session.
- `asyncpg` — Postgres driver used under the async engine.
- `alembic` — migrations. Env reads `DATABASE_URL_SYNC` (psycopg2, sync) — separate from the async runtime URL.
- `psycopg2-binary` — sync Postgres driver for Alembic.
- `pydantic-settings` — env-var loading (Pydantic v2 comes transitively via FastAPI).
- `httpx` — outbound HTTP (Discord `/users/@me`, any non-SDK calls).
- `anthropic` — official Claude SDK. Used with prompt caching for the strategy-library system prompt; see [[concepts/ai-coach/system-prompt-template.md]].
- `python-jose[cryptography]` — HS256 JWT signing/verification. SPA auth pattern — see §3.
- `python-multipart` — multipart form parsing for screenshot uploads.
- `boto3` — S3-compatible SDK for Cloudflare R2.

Dev / test (in `pyproject.toml`):

- `pytest`, `pytest-asyncio` — test runner with async support.
- `httpx` — also listed as a dev dep for test client usage.

Planned but **not yet in deps**:

- `gunicorn` — prod process manager. Needed before Render deployment.
- `structlog` — structured logging.
- `sentry-sdk` — optional, env-gated error tracking.
- `testcontainers[postgresql]` — real Postgres for integration tests.
- `ruff` — linter + formatter.
- `mypy` — type checker.

Explicitly **not chosen**:

- **Tortoise ORM** — the trade schema is already written against SQLAlchemy DDL and conventions. Switching would be gratuitous rework.
- **Celery + Redis** — overkill for MVP. `BackgroundTasks` covers the single async workflow we have (Claude call after webhook).
- **Django / Flask** — wrong shape for async + typed APIs.

## 3. Discord OAuth2 — login flow

> **Canonical source:** [[concepts/architecture/phase2-project-structure]] §Auth Design. This section summarises the implemented pattern. If details conflict, phase2-project-structure.md wins.

### Principle

**Discord snowflake ID is an external identifier, not the primary key.** The `users` table in [[concepts/architecture/trade-schema]] uses `id UUID PK`. Discord's ID is stored as `discord_id VARCHAR(32) UNIQUE NOT NULL`.

This preserves the UUID-based foreign-key surface of the trade schema, lets us swap identity providers later without migrating every FK, and keeps Discord IDs out of URLs and logs.

### Users table

See [[concepts/architecture/trade-schema]] §Postgres DDL for the canonical `CREATE TABLE users` statement. Key columns: `id UUID PK`, `discord_id VARCHAR(32) UNIQUE NOT NULL`, `discord_username VARCHAR(128)`, `discord_avatar_url TEXT`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`.

### Scopes

Request **`identify` only**. That gives us snowflake ID, username, avatar hash — everything we need. Skip `email` (not verified on Discord) and `guilds` (not needed until bot integration is scoped).

### Flow — SPA pattern (implemented)

The backend is a pure API — no server-side redirects. The frontend handles the OAuth redirect flow.

```
[Frontend SPA]            [FastAPI backend]          [Discord]
    │                         │                          │
    │── redirect user to ─────────────────────────────▶  │
    │   discord.com/oauth2/authorize?                    │
    │   client_id&scope=identify&redirect_uri=<frontend> │
    │                                                    │
    │◀─ redirect to frontend?code=... ───────────────────│
    │                         │                          │
    │── POST /auth/discord/token ──▶│                    │
    │   {code, redirect_uri}  │                          │
    │                         │── POST /oauth2/token ───▶│
    │                         │◀──── access_token ───────│
    │                         │── GET /users/@me ───────▶│
    │                         │◀──── id, username, ──────│
    │                         │      avatar              │
    │                         │── UPSERT users by        │
    │                         │   discord_id             │
    │                         │── mint JWT (sub=user.id) │
    │◀── {access_token, token_type: "bearer"} ──────────│
    │                         │                          │
    │── All subsequent requests: Authorization: Bearer <jwt>
```

### Auth implementation: JWT via `python-jose`

- `python-jose[cryptography]` signs HS256 JWTs.
- JWT payload: `{"sub": "<user uuid>", "discord_id": "<snowflake>", "exp": <timestamp>}`.
- Default expiry: 43200 minutes (30 days), configurable via `JWT_EXPIRE_MINUTES`.
- `get_current_user()` FastAPI dependency: decodes JWT → queries `users` table → injects `User` ORM object.

### Debug endpoint

`POST /auth/debug/token {discord_id}` — mints a JWT without real Discord OAuth. Gated on `DEBUG=true`. Auto-creates a user row if none exists. Never deployed to prod.

### Required env vars

- `DISCORD_CLIENT_ID` — from Discord Developer Portal
- `DISCORD_CLIENT_SECRET` — from Discord Developer Portal
- `JWT_SECRET` — 32+ random bytes; rotating it invalidates all sessions
- `JWT_EXPIRE_MINUTES` — default 43200 (30 days)

### Developer app setup (one-time)

In the Discord Developer Portal → New Application:

1. OAuth2 → Redirects → add the frontend's callback URL (e.g. `http://localhost:5173/auth/callback` for dev).
2. Copy Client ID → `DISCORD_CLIENT_ID`; Reset Secret → `DISCORD_CLIENT_SECRET`.
3. Keep the application *public* (so beta users can authorize without being invited).
4. No bot token needed until bot integration is scoped.

## 4. Render Deployment Architecture

### Topology

**One web service + one managed Postgres.** No worker. No Redis. Add those only when load demands it.

```
  GitHub main branch ── auto-deploy ──▶  Render Web Service (FastAPI)
                                                │
                                                │ DATABASE_URL
                                                ▼
                                         Render Managed Postgres
```

### Web service config

- **Runtime:** Python 3.12.
- **Build command:** `pip install -r requirements.txt` (or `uv pip install -r ...` if we adopt uv).
- **Pre-deploy command:** `alembic upgrade head` — runs before traffic cuts over; fails the deploy if a migration fails.
- **Start command:** `gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:$PORT --graceful-timeout 30 --timeout 60`.
- **Plan:** Starter ($7/mo) for beta. 512 MB RAM handles 5–10 users comfortably.
- **Health check path:** `GET /healthz` — must return 200 OK with `{"status": "ok"}`.
- **Auto-deploy:** on push to `main`.

### Postgres config

- **Plan:** Starter. Shared CPU, enough storage for the 5–10 beta user window.
- **Version:** Postgres 16.
- **Backups:** Render-managed daily snapshots are sufficient for MVP. Retention per Render's plan defaults.
- **Connection string:** injected as `DATABASE_URL` (format: `postgres://user:pass@host:port/db`).
  - Note: SQLAlchemy async needs `postgresql+asyncpg://...`. A tiny startup shim rewrites `postgres://` → `postgresql+asyncpg://` so the app works with whatever string Render provides.
- **Extensions:** enable `pgcrypto` (for `gen_random_uuid()`) in the initial Alembic migration.

### `render.yaml` blueprint

Commit a blueprint to the API repo so infra is reproducible:

```yaml
services:
  - type: web
    name: neurospect-api
    runtime: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements.txt
    preDeployCommand: alembic upgrade head
    startCommand: gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:$PORT
    healthCheckPath: /healthz
    autoDeploy: true
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: neurospect-db
          property: connectionString
      - key: DATABASE_URL_SYNC
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: DISCORD_CLIENT_ID
        sync: false
      - key: DISCORD_CLIENT_SECRET
        sync: false
      - key: TRADINGVIEW_WEBHOOK_SECRET
        generateValue: true
      - key: PUBLIC_BASE_URL
        sync: false
      - key: R2_ENDPOINT_URL
        sync: false
      - key: R2_ACCESS_KEY_ID
        sync: false
      - key: R2_SECRET_ACCESS_KEY
        sync: false
      - key: R2_BUCKET
        sync: false
      - key: AI_COACH_PROMPT_DIR
        sync: false
      - key: DEBUG
        value: "false"

databases:
  - name: neurospect-db
    plan: starter
    postgresMajorVersion: 16
```

### Full env var surface

> **Canonical source:** `api/.env.example`. The table below is a summary — if it conflicts with `.env.example`, the file wins.

| Var | Source | Used by |
|---|---|---|
| `DATABASE_URL` | Render-linked | SQLAlchemy async engine (`postgresql+asyncpg://...`) |
| `DATABASE_URL_SYNC` | Render-linked | Alembic migrations (`postgresql+psycopg2://...`) |
| `JWT_SECRET` | Render-generated | `python-jose` JWT signing |
| `JWT_EXPIRE_MINUTES` | manual (default 43200) | JWT expiry |
| `ANTHROPIC_API_KEY` | manual | AI Coach Claude calls |
| `DISCORD_CLIENT_ID` | manual (Discord portal) | OAuth client |
| `DISCORD_CLIENT_SECRET` | manual (Discord portal) | OAuth client |
| `TRADINGVIEW_WEBHOOK_SECRET` | Render-generated | Webhook body-secret check |
| `TRADINGVIEW_IP_ALLOWLIST` | manual | Comma-separated IPs; empty = disabled |
| `PUBLIC_BASE_URL` | manual | Generated webhook URLs |
| `R2_ENDPOINT_URL` | manual (Cloudflare) | R2 boto3 endpoint |
| `R2_ACCESS_KEY_ID` | manual (Cloudflare) | R2 client |
| `R2_SECRET_ACCESS_KEY` | manual (Cloudflare) | R2 client |
| `R2_BUCKET` | manual | R2 bucket name |
| `CLAUDE_MODEL` | manual (default `claude-sonnet-4-6`) | AI Coach model selection |
| `CLAUDE_MAX_TOKENS` | manual (default 2048) | AI Coach response limit |
| `CLAUDE_TIMEOUT_SECONDS` | manual (default 30.0) | AI Coach call timeout |
| `AI_COACH_PROMPT_DIR` | manual | Path to wiki `concepts/ai-coach/` dir |
| `DEBUG` | manual (default false) | Enables `/auth/debug/token`; never true in prod |

### Custom domain

Deferred. Use `<service>.onrender.com` for beta. Switch to `api.neurospect.app` (or chosen apex) once a domain is bought — update the Discord app's allowed redirect URIs and `PUBLIC_BASE_URL` in lock-step.

## 5. TradingView Webhook Ingestion

> **Canonical source:** [[concepts/architecture/tradingview-connector]] has the full design (Pine Script, validation stack, `coaching_events` table, Claude call, polling). This section is a summary.

### Endpoint

`POST /webhooks/tradingview/{user_token}` — unauthenticated (no JWT), secured by a per-user URL token + shared secret + IP allowlist.

### Validation stack (in order)

1. **Per-user URL token.** `{user_token}` in the path identifies the user. Looked up in `tradingview_tokens WHERE revoked_at IS NULL`. Miss → 401.
2. **Shared secret in body.** `hmac.compare_digest(body.secret, TRADINGVIEW_WEBHOOK_SECRET)`. Mismatch → 401.
3. **IP allowlist.** `TRADINGVIEW_IP_ALLOWLIST` env var (comma-separated). Empty = disabled (dev). Miss → 403.
4. **Pydantic `Layer2Payload`** validation. Malformed → 422.
5. **Idempotency.** `UNIQUE(user_id, idempotency_key)` on `coaching_events`. Duplicate → 202 `{"status":"duplicate"}`.

### Response channel

Polling — `GET /api/coach/events/{id}` and `GET /api/coach/events/latest`. Frontend polls every 2–3 s until `status != "pending"`. SSE is a drop-in upgrade later.

### Async note

The Claude API call takes 5–20 seconds. The webhook handler returns `202 Accepted` immediately and dispatches the Claude call via `BackgroundTasks`. TradingView's webhook timeout is aggressive — blocking would cause retries.

## 6. File / Screenshot Storage — Cloudflare R2

### Recommendation: **Cloudflare R2** (S3-compatible object storage). Not Render Disk.

### Why R2 over Render Disk

- **Egress cost.** R2 has **zero egress fees**. The journal UI will repeatedly load screenshots (list views, detail views, review flows); once the AI coach ingests screenshots as context (Phase 3+), per-trade fetches multiply. Render Disk served through the app routes all reads through Render's bandwidth meter. Over a few thousand screenshots, egress dominates.
- **Durability + scaling.** R2 is object storage: effectively unbounded capacity, 11 9s durability, independent of any compute instance. Render Disk is a volume mounted to a single instance — it does not survive service recreation, does not scale horizontally, and is not backed up on the same cadence as Postgres.
- **Portability.** R2 speaks the S3 API. `boto3` works unchanged. If we ever need to leave Cloudflare, AWS S3 is a drop-in replacement — just rotate endpoint + credentials. A Render Disk abstraction would be thrown away the day we grew out of it.

Tradeoff accepted: one extra provider account, one extra set of credentials. Worth it on egress alone.

### Implementation (as built)

- **Upload:** browser → FastAPI `POST /api/trades/{trade_id}/screenshots` (multipart form: file + phase). Backend uploads to R2, then persists `(trade_id, user_id, phase, storage_key, original_filename, content_type, uploaded_at)` into `trade_screenshots`.
- **Read:** backend issues a **presigned GET URL** (1-hour expiry) when the frontend asks for a screenshot. Bucket stays private.
- **Delete (hard):** deletes both the R2 object and the `trade_screenshots` row. No soft-delete for screenshots (unlike trades).
- **Bucket policy:** private by default. No public read.

### Key layout

> **Canonical source:** `api/app/services/r2.py`.

```
<bucket>/
  {user_id}/
    {trade_id}/
      {phase}/
        {uuid4}.{ext}
```

`{phase}` is the `screenshot_phase` ENUM value (`before_entry`, `entry`, `higher_tf`, `exit`, `post_trade_review`). User UUID in the path makes multi-tenant bucket auditing trivial.

### Fallback

If Cloudflare R2 becomes friction, the escape hatch is **AWS S3**, not Render Disk. Render Disk is simply the wrong tool for user-uploaded media at any scale.

## 7. Cross-module Notes

- **Journal Phase 2** (see [[processes/distributed-workflow/active/journal-analytics]]) — implemented. CRUD, screenshots, analytics all live in `api/`.
- **AI Coach Phase 3** (see [[processes/distributed-workflow/active/ai-coach]]) — implemented. TradingView webhook, Claude call, polling endpoints all live in `api/`.
- **Repo:** both modules share one FastAPI project at `api/` (formerly the `neurospect-api` repo; merged into the `neurospect` monorepo on 2026-05-02).

## 8. Open Questions (not blocking)

- ~~**Coaching push channel**~~ — **resolved:** polling (`GET /api/coach/events/{id}` + `/latest`). SSE upgrade deferred.
- ~~**Prompt-caching strategy**~~ — **resolved:** ephemeral `cache_control` on the system message block. See [[concepts/architecture/tradingview-connector]] §5.
- **Discord bot integration** (bot token, slash commands, coaching-to-DM) — not MVP. Add `bot` scope, app token, and a worker later.
- **Multi-region / read-replica Postgres** — N/A at 5–10 users.
- **Screenshot CDN / Cloudflare Worker in front of R2** — optional. Presigned URLs are enough until the product has a frontend domain.

## 9. See Also

- [[concepts/architecture/trade-schema]] — the journal data model that this stack implements
- [[processes/distributed-workflow/active/ai-coach]] — AI Coach tracker (shared backend)
- [[processes/distributed-workflow/active/journal-analytics]] — Journal tracker (shared backend)
- [[concepts/ai-coach/system-prompt-template.md]] — Claude system prompt loaded by the AI Coach
- [[concepts/ai-coach/strategies.json]] — strategy library injected into the Claude system prompt
- [[entities/projects/neurospect]] — project overview and roadmap
