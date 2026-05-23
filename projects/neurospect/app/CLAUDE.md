# app — Claude Instructions

React 19 + TypeScript + Vite frontend for Neurospect. Formerly the `neurospect-app` repo.

## Required Reading

Before non-trivial changes:

- `../wiki/concepts/architecture/phase3-frontend-structure.md` — canonical frontend doc.
- `../wiki/concepts/architecture/phase4-coach-frontend.md` — AI Coach UI.
- The active workstream tracker for the area: `../wiki/processes/distributed-workflow/active/<tracker>.md`.

## Architecture Doc Integrity

Same rule as `api/`: when shipped code diverges from the canonical doc, update the doc in the same PR. See `../wiki/CLAUDE.md` § *Architecture Doc Integrity*.

## Conventions

- TanStack Query for server state. React Hook Form + Zod for forms.
- shadcn/ui + Tailwind v4. `cn()` from `lib/utils`.
- Type-only imports use `import type`.
- API base URL: `VITE_API_BASE_URL`. JWT in localStorage; auth state via React Context.

## Static Assets

`public/neurospect-coach.pine` mirrors `../wiki/assets/pine/neurospect-coach.pine`. Currently re-synced manually when the wiki version bumps. Open question for the migration: replace with a build-step copy now that they're in the same repo.

## Deployment

Cloudflare Pages builds from this directory. Build command: `npm run build`. Output: `dist/`.
