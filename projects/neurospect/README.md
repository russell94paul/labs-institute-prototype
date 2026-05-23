# Neurospect

ICT trading journal and AI coach. Monorepo containing:

- `wiki/` — knowledge base (ICT strategy, architecture decisions, mentor video transcripts, course content, workstream trackers).
- `api/` — FastAPI backend. Postgres + SQLAlchemy async, Discord OAuth2, TradingView webhook → Claude AI coach pipeline, Cloudflare R2 screenshot storage. Deployed on Render.
- `app/` — React 19 + TypeScript + Vite frontend. Trade journal CRUD, analytics dashboard, AI Coach live panel. Deployed on Cloudflare Pages.

## Getting Started

Each subdirectory has its own `CLAUDE.md` with conventions and required reading. The wiki is the canonical source for design decisions; start there.

- Backend: `cd api && poetry install && poetry run uvicorn app.main:app --reload`
- Frontend: `cd app && npm install && npm run dev`
- Docs: open `wiki/index.md`

## History

This monorepo was created on 2026-05-02 by merging three predecessor repos via `git filter-repo --to-subdirectory-filter`. Predecessors are archived; their pre-merge tips are tagged `pre-monorepo-snapshot`. Migration record: `wiki/processes/distributed-workflow/active/monorepo-migration.md`.
