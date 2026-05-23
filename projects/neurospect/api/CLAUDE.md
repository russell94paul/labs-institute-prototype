# api — Claude Instructions

FastAPI backend for Neurospect (the trade journal + AI coach). Formerly the `neurospect-api` repo.

## Required Reading

Before non-trivial changes, read the relevant wiki canonical doc:

- Backend layout / deps / auth flow → `../wiki/concepts/architecture/phase2-project-structure.md`
- Trade data model → `../wiki/concepts/architecture/trade-schema.md`
- AI Coach pipeline → `../wiki/concepts/architecture/tradingview-connector.md`

And the active workstream tracker for the area you're touching: `../wiki/processes/distributed-workflow/active/<tracker>.md`.

## Architecture Doc Integrity

The wiki documents the architecture **as implemented**. When you ship code that diverges from the wiki, update the wiki page in the same PR. Full rule: `../wiki/CLAUDE.md` § *Architecture Doc Integrity*.

## Conventions

- Poetry for deps. `alembic upgrade head` for migrations (sync mode; async DB session for app code).
- SQLAlchemy 2.x async (`AsyncSession`, `await db.execute(...)`).
- Pydantic v2; `extra="forbid"` on Layer-2 (Claude-output) schemas.
- Tests: pytest-asyncio (`asyncio_mode = "auto"`). Route tests call route functions directly with mocked `AsyncSession` — see `tests/test_singleton.py` for the pattern. No test database.

## Env

Copy `.env.example` → `.env`. `BROKER_CRED_SECRET` must be set or `app/services/crypto.py` fails at import (intentional).

## Deployment

Render service builds from this directory. `render.yaml` and `requirements.txt` (exported from poetry) drive the build.
