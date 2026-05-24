# Deployment Guide — Phase P2: Trader Workspace

**Phase:** ns-P2 — Trader Workspace  
**Status:** Build passing. No staging environment configured as of 2026-05-24.

## What was shipped in P2

- `app/src/pages/analytics.tsx` — Analytics dashboard (behavior metrics, tilt scoring, consistency charts)
- `app/src/pages/dashboard.tsx` — Enhanced daily trader workspace
- `app/src/components/trade/journal-fields.tsx` — Pre-trade checklist + emotion tagging UI
- `app/src/components/trade/trade-form.tsx` — Extended trade form schema (journal fields)

## Build

```bash
cd projects/neurospect/app
npm run build
# Output: dist/
```

Build artifact: `projects/neurospect/app/dist/`  
Bundle size: ~1.2 MB JS / 48 KB CSS (gzip: ~360 KB / 9 KB)

## Manual deployment steps (staging not yet configured)

Until a staging environment is provisioned, these are the manual steps to run the P2 build:

### 1. Local staging verification

```bash
# Start all services
cd projects/neurospect
./start.sh all

# Or individual services:
./start.sh api        # FastAPI on :8000
./start.sh app        # React dev server on :5173
./start.sh marketing  # Marketing site on :3000
```

Verify:
- Dashboard loads at http://localhost:5173
- Analytics page renders with behavior metrics
- Journal fields appear on new trade form
- Pre-trade checklist saves/loads correctly

### 2. Production build preview

```bash
cd projects/neurospect/app
npm run build
npm run preview  # Serves dist/ locally
```

### 3. When a staging environment is provisioned

Deploy steps will depend on host (Vercel/Netlify/Fly.io/VPS). Add a `deploy.sh` to `projects/neurospect/` with:
- `npm run build` → upload `dist/` to CDN or static host
- `poetry run alembic upgrade head` for any DB migrations
- Restart the FastAPI process (uvicorn / gunicorn)

## Known issues / notes

- Bundle is ~1.2 MB — code splitting should be added before public launch
- No environment variables documented yet for API URL / auth provider
- `pre_trade_checklist` uses `z.record(z.string(), z.boolean())` (Zod v4 requires both key and value types)
