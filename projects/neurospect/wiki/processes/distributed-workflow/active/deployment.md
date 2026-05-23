---
tags: [distributed-workflow, active, neurospect, deployment, render, cloudflare]
aliases: [Deployment Tracker, Render Deployment]
sources: []
created: 2026-04-24
updated: 2026-04-24
---

# Deployment — Workstream Tracker

Get Neurospect running in production so real TradingView webhooks can reach the backend and beta users can log in with Discord.

**Why this is the gate:** TradingView can only POST to public HTTPS URLs, not localhost. Everything built so far has been tested with curl. No real coaching session is possible until the backend has a public URL.

## Goal

By end of this workstream:

1. **Backend live on Render** — FastAPI app deployed as a Render web service, connected to Render managed Postgres. Alembic migrations run automatically on deploy. Health check passing. All 6 coach endpoints + trade journal endpoints reachable over HTTPS.

2. **Real Discord OAuth** — users can log in with "Sign in with Discord" instead of the debug endpoint. Discord application created, client ID + secret in Render env vars.

3. **Frontend live on Cloudflare Pages** — React app deployed from the `neurospect-app` repo. `VITE_API_URL` points at the Render backend. `VITE_DISCORD_CLIENT_ID` set. Discord redirect URI registered.

4. **End-to-end verified** — TradingView alert → webhook → Claude call → frontend coaching panel → complete, all over HTTPS.

## Prerequisites (do before starting the session)

### 1. Discord Application (manual — 5 minutes)

1. Go to `https://discord.com/developers/applications`
2. Click **New Application** → name it "Neurospect"
3. Go to **OAuth2** → **Redirects** → Add:
   - `http://localhost:5173/auth/callback` (local dev)
   - `http://localhost:5174/auth/callback` (local dev alt)
   - `https://<your-pages-subdomain>.pages.dev/auth/callback` (Cloudflare Pages — add after deploy)
4. Copy **Client ID** → save somewhere safe
5. Click **Reset Secret** → copy **Client Secret** → save somewhere safe
6. Keep the application **Public** (so any Discord user can authorize)

### 2. Cloudflare Account + R2 Bucket (optional for MVP)

Screenshots return 503 locally without R2 configured. This is acceptable for initial deployment — the app works without it (trade journal minus screenshots). Wire up R2 after the base deployment is stable.

If you want screenshots from day one:
1. Create a Cloudflare account (free tier)
2. R2 → Create bucket named `neurospect-screenshots`
3. Manage R2 API tokens → create token with Object Read & Write on that bucket
4. Note the endpoint URL, access key ID, secret access key

### 3. GitHub repos pushed

Both `neurospect-api` and `neurospect-app` must be pushed to GitHub before Render/Pages can deploy from them. Paul handles git — commit and push both repos to GitHub before starting the session.

---

## Architecture

```
GitHub (neurospect-app)
    │  push to main
    ▼
Cloudflare Pages  ─── VITE_API_URL ──────────────────────────────────────▶  Render Web Service
(React SPA)                                                                  (FastAPI, neurospect-api)
    │                                                                                │
    │  Discord OAuth (SPA pattern)                                                   │ DATABASE_URL
    ▼                                                                                ▼
Discord                                                                   Render Managed Postgres
    │                                                                                │
    └── /auth/callback?code=... ──▶ frontend ──▶ POST /auth/discord/token ──▶ backend

TradingView  ──── HTTPS webhook ────▶  Render (POST /webhooks/tradingview/{token})
```

---

## Implementation Plan

### Phase 1 — Backend prep (code changes before deploying)

These changes must land in the repo before Render can deploy successfully.

**1a. Bundle the AI coach prompt files into the repo**

`AI_COACH_PROMPT_DIR` currently points to the local wiki path (`C:/Users/PaulRussell/repos/neurospect-wiki/concepts/ai-coach`). This path doesn't exist on Render. Fix: copy the two prompt files into the API repo and update the default.

- Copy `neurospect-wiki/concepts/ai-coach/system-prompt-template.md` → `api/app/coach/prompts/system-prompt-template.md`
- Copy `neurospect-wiki/concepts/ai-coach/strategies.json` → `api/app/coach/prompts/strategies.json`
- Update `app/config.py` to default `AI_COACH_PROMPT_DIR` to `Path(__file__).parent / "coach" / "prompts"` so it works without setting the env var
- On local dev, override with the wiki path via `.env` (keeps the wiki as canonical for editing)
- The `app/coach/prompt_loader.py` uses `lru_cache` — no changes needed there

**Sync rule:** When the wiki prompt files change, manually re-copy them to `app/coach/prompts/` and commit. A note in `api/README.md` records this requirement.

**1b. Add `gunicorn` dependency**

`gunicorn` is the prod process manager. Add to `pyproject.toml`:
```toml
gunicorn = "^23.0"
```
Generate a `requirements.txt` from Poetry for Render's pip-based build:
```bash
poetry export -f requirements.txt --without-hashes --output requirements.txt
```
Commit `requirements.txt`. Render uses `pip install -r requirements.txt`.

**1c. Fix the health check path**

`render.yaml` specifies `/healthz` but `main.py` has the health endpoint at `/health`. Reconcile — change `main.py` to `/healthz` OR update `render.yaml` to `/health`. Either is fine; just make them match.

**1d. Add a `DATABASE_URL` → `postgresql+asyncpg://` startup shim**

Render injects `DATABASE_URL` as `postgres://...` (without the driver prefix). SQLAlchemy async needs `postgresql+asyncpg://...`. Add a shim in `app/config.py`:

```python
@property
def async_database_url(self) -> str:
    url = self.database_url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url
```

Do the same for `DATABASE_URL_SYNC` (replace `postgres://` → `postgresql+psycopg2://`). Use `async_database_url` and `sync_database_url` properties everywhere instead of the raw env vars.

**1e. Create `render.yaml`**

Add to the root of `neurospect-api`:

```yaml
services:
  - type: web
    name: neurospect-api
    runtime: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements.txt
    preDeployCommand: alembic upgrade head
    startCommand: gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:$PORT --graceful-timeout 30 --timeout 60
    healthCheckPath: /health
    autoDeploy: true
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: neurospect-db
          property: connectionString
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
      - key: CORS_ORIGINS
        sync: false
      - key: R2_ENDPOINT_URL
        sync: false
      - key: R2_ACCESS_KEY_ID
        sync: false
      - key: R2_SECRET_ACCESS_KEY
        sync: false
      - key: R2_BUCKET
        sync: false
      - key: DEBUG
        value: "false"

databases:
  - name: neurospect-db
    plan: starter
    postgresMajorVersion: 16
    region: oregon
```

**1f. Update `TRADINGVIEW_IP_ALLOWLIST` for prod**

TradingView's webhook source IPs (as of 2026): `52.89.214.238`, `34.212.75.30`, `54.218.53.128`, `52.32.178.7`. Set these in Render env vars after verifying against current TradingView docs (they occasionally change). Leave empty to disable allowlist while testing, enable before going live.

---

### Phase 2 — Render dashboard setup (manual steps)

1. **New Web Service** → connect GitHub → select `neurospect-api` repo → Render detects `render.yaml` and pre-fills most settings.
2. **New Postgres** → name `neurospect-db`, Starter plan, Postgres 16, same region. Link to the web service (this populates `DATABASE_URL` automatically).
3. **Environment variables** — set all `sync: false` vars manually in the Render dashboard:
   - `ANTHROPIC_API_KEY` — from your Anthropic console
   - `DISCORD_CLIENT_ID` — from Discord Developer Portal
   - `DISCORD_CLIENT_SECRET` — from Discord Developer Portal
   - `PUBLIC_BASE_URL` — the Render service URL (e.g. `https://neurospect-api.onrender.com`) — set after first deploy
   - `CORS_ORIGINS` — `["https://<your-pages-subdomain>.pages.dev"]` — set after Cloudflare Pages deploy; in the meantime use `["http://localhost:5173","http://localhost:5174"]`
   - `DATABASE_URL_SYNC` — manually set to the same connection string as `DATABASE_URL` but with `postgresql+psycopg2://` prefix (Render only auto-links one connection string format)
   - R2 vars — if configuring screenshots now, otherwise leave blank
4. **Deploy** → watch build logs → Alembic migration runs → service starts → health check passes.
5. Note the assigned `*.onrender.com` URL. Set `PUBLIC_BASE_URL` to that URL and redeploy.

---

### Phase 3 — Cloudflare Pages (frontend)

1. **New Pages project** → connect GitHub → select `neurospect-app` repo.
2. **Build settings:**
   - Framework preset: Vite
   - Build command: `npm run build`
   - Build output directory: `dist`
3. **Environment variables (Production):**
   - `VITE_API_URL` — `https://neurospect-api.onrender.com` (the Render URL)
   - `VITE_DISCORD_CLIENT_ID` — from Discord Developer Portal
   - `VITE_DISCORD_REDIRECT_URI` — `https://<your-pages-subdomain>.pages.dev/auth/callback`
   - `VITE_DEBUG` — `false`
4. Deploy → note the `*.pages.dev` URL.
5. Go back to Discord Developer Portal → add the `*.pages.dev/auth/callback` URL to Redirects.
6. Update `CORS_ORIGINS` in Render to `["https://<your-pages-subdomain>.pages.dev"]` → trigger redeploy.

---

### Phase 4 — End-to-end verification

1. Visit the Pages URL → "Sign in with Discord" button visible
2. Click it → Discord OAuth flow → redirected back → logged in
3. Navigate to `/coach/setup` → Generate Token → Webhook URL shows the `*.onrender.com` host
4. Create a TradingView alert using the Pine script + the real webhook URL
5. Fire alert → panel cycles pending → complete on the live site
6. Trade journal: create a trade → save → detail page loads

---

## Open Questions

- **Custom domain:** Deferred. Use `.onrender.com` / `.pages.dev` for beta. When a domain is bought, update Discord redirect URIs, `PUBLIC_BASE_URL`, and `CORS_ORIGINS` in lock-step.
- **Cloudflare R2 screenshots:** Optional for initial deploy. The 503 fallback is user-friendly. Wire up after base deployment is stable.
- **TradingView IP allowlist:** Enable after confirming the webhook is working end-to-end. Double-check IPs against current TradingView docs before enabling.
- **`DATABASE_URL_SYNC`:** Render only injects one connection string format automatically. The sync URL for Alembic must be set manually in Render env vars.

## Session Log

### 2026-04-26 — Security cleanup complete

- did: rotated `TRADINGVIEW_WEBHOOK_SECRET` (new value set in Render env vars). Rotated per-user webhook token via `/coach/setup` → Revoke → Generate. Updated TradingView alert with new webhook URL and new secret value.
- did: enabled `TRADINGVIEW_IP_ALLOWLIST` in Render env vars (`52.89.214.238,34.212.75.30,54.218.53.128,52.32.178.7`). Verified webhook still returns 202 after redeploy.
- next: AI Coach pre-fill feature (Phase 2 of journaling UX) — planning session

### 2026-04-26 — Phase 4 complete — TradingView webhook verified end-to-end

- did: wired up TradingView Pine Script → webhook → Claude → coach panel end-to-end. All confirmed working in prod.
- pitfalls encountered:
  - `AI_COACH_PROMPT_DIR` was set in Render env vars to the local Windows wiki path — deleted it so the bundled `app/coach/prompts/` default kicks in
  - `CLAUDE_MAX_TOKENS` default of 2048 too small — set to 8192 in Render env vars
  - `CLAUDE_TIMEOUT_SECONDS` needed to be set to 60 in Render env vars
  - Pine Script `barstate.isrealtime` used in a plot variable (`bgcolor`) triggers TradingView's "repaint" warning which **silently blocks all alert() delivery** — removing it from `fire`/`bgcolor` fixed the issue. The `alert()` function itself already only fires on real-time bars; the guard was redundant and harmful.
  - Pine Script `alert()` with `alert.freq_once_per_bar` can have its per-bar quota consumed during input-change recalculation — use `alert.freq_all` for debugging, revert to `alert.freq_once_per_bar` for production
  - `confirm=true` on Pine inputs removed (was suspected blocker, ultimately not the cause, but simpler without it)
  - `request.security()` does NOT block `alert()` when `barstate.isrealtime` is absent from plots — confirmed working together
  - Pine Script v5 → v6 upgrade required (TradingView flags v5 as outdated; `trigger` is a reserved word in v6)
  - Test payload for curl had inconsistent `price_vs_midnight_open` flag vs actual OHLC values — Claude wrote very long reasoning responses that hit token/timeout limits. Real chart data is self-consistent and responses are shorter.
- env vars added to Render this session: `AI_COACH_PROMPT_DIR` (deleted), `CLAUDE_MAX_TOKENS=8192`, `CLAUDE_TIMEOUT_SECONDS=60`
- verified: TradingView alert fires → webhook accepted (202) → Claude call completes → coach panel updates with bias badge, narrative, strategy cards ✓
- next: rotate `TRADINGVIEW_WEBHOOK_SECRET` and webhook token (both exposed during debugging session), wire R2 screenshots, enable IP allowlist

### 2026-04-25 — Phases 2 + 3 complete, Phase 4 partially verified

- did: completed full deployment — Render web service live, Cloudflare Pages live, Discord OAuth working end-to-end, trade journal saving trades.
- pitfalls encountered (document for future deploys):
  - `DATABASE_URL` on Render uses `postgresql://` prefix not `postgres://` — async shim needed to handle both
  - FastAPI 0.115 on Python 3.14 raises AssertionError for 204 routes — added `response_class=Response` + explicit `return Response(status_code=204)`. Also pinned `.python-version` to 3.13.
  - `pythonVersion` field in render.yaml is NOT picked up for manually-created services — must use `.python-version` file
  - `preDeployCommand` in render.yaml is NOT run for manually-created services (Blueprint-only feature) — moved `alembic upgrade head` into `startCommand` as `alembic upgrade head && gunicorn ...`
  - `DISCORD_CLIENT_ID` and `DISCORD_CLIENT_SECRET` were not imported from .env (missed during setup) — must be added manually in Render dashboard
  - Render free tier cold-starts after inactivity — visit `/health` to warm before testing auth
- verified: Discord OAuth login ✓, trade saves and appears in trades list ✓, screenshots 503 gracefully (R2 not configured — expected) ✓
- deferred: TradingView Pine script → webhook → coach panel end-to-end test (requires TradingView alert setup), R2 screenshot wiring
- next: Phase 4 TradingView wiring session

### 2026-04-24 — Phase 1 backend prep complete

- did: implemented all Phase 1 code changes required before Render can deploy.
  - Copied wiki prompt files into `api/app/coach/prompts/` (system-prompt-template.md + strategies.json)
  - Updated `app/config.py`: `ai_coach_prompt_dir` default now points to bundled `app/coach/prompts/`; added `async_database_url` and `sync_database_url` properties with `postgres://` → `postgresql+asyncpg://` / `postgresql+psycopg2://` shims; made `database_url_sync` optional with empty-string default (derives from `DATABASE_URL` on Render if not set explicitly)
  - Updated `app/database.py`: uses `settings.async_database_url` instead of raw `settings.database_url`
  - Updated `alembic/env.py`: uses `settings.sync_database_url` instead of raw `os.environ.get("DATABASE_URL_SYNC")`; removed now-unused `import os`
  - Added `gunicorn = "^23.0"` to `pyproject.toml`; ran `poetry add` to generate `poetry.lock`; ran `poetry export --without-hashes` to generate `requirements.txt` (51 lines, fully pinned)
  - Created `render.yaml` at repo root (exact spec from tracker; healthCheckPath `/health` matching `main.py`)
  - Created `README.md` with Prompt Files sync rule documented
  - `tsc -b` in `neurospect-app` passes cleanly — no frontend regressions
- decided: `database_url_sync` made optional (default `""`) so Alembic can derive sync URL from `DATABASE_URL` on Render without a second manual env var. Local dev can still override with `DATABASE_URL_SYNC` in `.env`.
- decided: poetry was not previously installed in this environment; installed via pip 26.0.1 + added `poetry-plugin-export` for `poetry export` support.
- next: Paul commits both repos → Render dashboard setup (Phase 2) → Cloudflare Pages (Phase 3) → end-to-end verification (Phase 4)

### 2026-04-24 — tracker created

- did: created this tracker. Phase 4 frontend complete and verified locally. Deployment is the next gate.
- decided: backend on Render Starter + managed Postgres; frontend on Cloudflare Pages (consistent with existing R2 Cloudflare footprint and zero egress costs).
- decided: R2 (screenshots) is optional for initial deploy — the 503 fallback means the app launches without it. Wire up after base deployment is stable.
- decided: Discord OAuth app must be created by Paul before the implementation session starts (manual step, requires browser login to Discord Developer Portal). Instructions above.
- next: create Discord app (Paul, before next session) → push both repos to GitHub → execute boot prompt below.

## Boot Prompt — Phase 5 (R2 Screenshots + IP Allowlist)

**Recommended model:** Sonnet. **Working directories:** `neurospect-api`.

````
Neurospect is fully deployed and Phase 4 (TradingView webhook end-to-end) is complete and verified.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/deployment.md`

What remains:
1. Wire Cloudflare R2 for screenshot uploads (currently 503 gracefully). Setup steps in tracker Phase 1 §2.
2. Enable `TRADINGVIEW_IP_ALLOWLIST` in Render env vars (IPs in tracker Phase 1 §1f) — do after confirming webhook still works.
3. Tokens were rotated after Phase 4 session — verify Pine script and TradingView alert webhook URL are updated to new values.

The app is live and usable without R2. R2 is the only remaining wiring task.
````

## Boot Prompt — Phase 4 TradingView Wiring

**Recommended model:** Sonnet. **Working directories:** `neurospect-api` and `neurospect-app`.

````
You are completing Phase 4 of the Neurospect deployment: wiring up the TradingView webhook end-to-end so a live alert fires the AI coach pipeline.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/deployment.md` — all deployment decisions and pitfalls are documented there.
3. Read `concepts/architecture/tradingview-connector.md` — the canonical doc for the webhook pipeline architecture.

Context (what is already done):
- Backend live at `https://neurospect-api.onrender.com` (Render Starter, Python 3.13, gunicorn + UvicornWorker)
- Frontend live at `https://neurospect-app.pages.dev` (Cloudflare Pages)
- Discord OAuth login working end-to-end
- Trade journal (create/read/close) verified working in prod
- Alembic migrations running via `startCommand`: `alembic upgrade head && gunicorn ...`
- R2 screenshots NOT wired — uploads 503 gracefully (intentionally deferred)

What remains (Phase 4):
1. Go to `https://neurospect-app.pages.dev/coach/setup` → Generate Token → copy the webhook URL (should show `neurospect-api.onrender.com/webhooks/tradingview/<token>`)
2. Open TradingView → load the Pine script from `neurospect-wiki/assets/pine/neurospect-coach.pine` → add it as an indicator
3. Create a TradingView alert using that indicator → paste the webhook URL → set the alert message to the Pine script JSON payload format
4. Fire the alert (manually trigger or wait for condition) → watch the `/coach` panel on the Pages frontend cycle from pending → complete
5. Verify the coaching response renders correctly (bias badge, strategy cards, narrative)

If the coach panel shows an error or the webhook returns 4xx/5xx, check:
- `ANTHROPIC_API_KEY` is set in Render env vars (it was marked `sync: false` — must be set manually)
- `TRADINGVIEW_WEBHOOK_SECRET` is set and matches the secret in TradingView alert payload
- `PUBLIC_BASE_URL` is set to `https://neurospect-api.onrender.com`

Optional in this session:
- Wire up R2 screenshots (Cloudflare R2 bucket + API token — see tracker Phase 1 §2 for setup steps)
- Enable `TRADINGVIEW_IP_ALLOWLIST` once webhook is confirmed working (IPs in tracker §1f)

Post-session (MANDATORY per wiki Architecture Doc Integrity rules):
- Append session log to `processes/distributed-workflow/active/deployment.md`
- Update `entities/projects/neurospect.md` deployment status
- Append to `log.md`
- Write boot prompt for next session if work remains
````

---

## Boot Prompt — Phase 1 (original, archived)

**Recommended model:** Sonnet. **Working directories:** `neurospect-api` and `neurospect-app`.

````
You are deploying the Neurospect app to production: backend on Render, frontend on Cloudflare Pages.
Design is APPROVED — see the deployment tracker for every decision. This is an execution session.

Boot procedure:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read `processes/distributed-workflow/active/deployment.md` (this tracker) — all decisions are there.
3. Read the following in `neurospect-api`:
   - `app/config.py` — how settings are loaded (you need to add the DB URL shim + update the prompt dir default)
   - `app/coach/prompt_loader.py` — how AI_COACH_PROMPT_DIR is used (you need the default to work without the env var)
   - `app/main.py` — verify the health check path
   - `pyproject.toml` — you need to add gunicorn and export requirements.txt
4. Read the following in `neurospect-app`:
   - `src/lib/auth.ts` — confirm the Discord OAuth redirect_uri env var usage
   - `src/pages/login.tsx` — confirm the "Sign in with Discord" button logic (it's currently gated on VITE_DISCORD_CLIENT_ID being set)

Context:
- All code is working locally. The ONLY changes needed are the backend prep steps in Phase 1 of the tracker:
  (a) Bundle prompt files into the repo with a sensible default path
  (b) Add gunicorn + export requirements.txt
  (c) Fix health check path consistency
  (d) Add DATABASE_URL → postgresql+asyncpg:// startup shim in config.py
  (e) Create render.yaml
- DO NOT change any API logic, auth patterns, or frontend behaviour. Pure deployment plumbing only.
- Paul has already: created a Discord app (client ID and secret available), pushed both repos to GitHub.
- Paul handles git commits — never run git commit.

Implementation order:
1. Read app/config.py and app/coach/prompt_loader.py to understand the current prompt dir handling, then:
   - Copy neurospect-wiki/concepts/ai-coach/system-prompt-template.md → api/app/coach/prompts/system-prompt-template.md
   - Copy neurospect-wiki/concepts/ai-coach/strategies.json → api/app/coach/prompts/strategies.json
   - Update app/config.py: set AI_COACH_PROMPT_DIR default to Path(__file__).parent / "coach" / "prompts"
   - Add a note to api/README.md under "Prompt Files" explaining the sync requirement
2. Add gunicorn to pyproject.toml. Run: poetry export -f requirements.txt --without-hashes --output requirements.txt
3. Reconcile health check path: verify main.py and set render.yaml to match (use /health)
4. Add the DATABASE_URL shim properties to app/config.py (async_database_url + sync_database_url). Update app/database.py and alembic/env.py to use the new properties.
5. Create render.yaml at the root of neurospect-api (exact spec is in the tracker)
6. Run tsc -b in neurospect-app to confirm no regressions

Then walk Paul through the manual steps (Render dashboard + Cloudflare Pages + Discord redirect URI update) as numbered instructions with exact values to paste.

Post-session (MANDATORY per wiki Architecture Doc Integrity rules):
- Append a session log entry to processes/distributed-workflow/active/deployment.md
- Update entities/projects/neurospect.md with deployment status
- Append to log.md
- Paul handles git commits and actual dashboard clicks — you only prepare the code and write the instructions.
````

## See Also

- [[concepts/roadmap/README]] — strategic context (Now horizon: production stabilization)
- [[concepts/architecture/tech-stack]] — Render topology, env var surface, render.yaml spec
- [[concepts/architecture/phase2-project-structure]] — backend layout, Alembic config
- [[concepts/architecture/phase4-coach-frontend]] — frontend architecture (what's being deployed)
- [[processes/distributed-workflow/active/ai-coach]] — AI Coach tracker
- [[processes/distributed-workflow/active/journal-analytics]] — Journal tracker
- [[entities/projects/neurospect]] — project overview
