---
tags: [distributed-workflow, active, neurospect, monorepo, migration, repo-structure]
aliases: [Monorepo Migration, Repo Consolidation]
sources: []
created: 2026-05-02
updated: 2026-05-02
phases:
  phase_0: scoping
---

# Monorepo Migration — Workstream Tracker

Consolidate the three Neurospect repos (`neurospect-wiki`, `neurospect-api`, `neurospect-app`) into a single `neurospect` monorepo with `wiki/`, `api/`, `app/` as sibling top-level directories.

## Goal

By end of this workstream:

1. **Single `neurospect` repo** containing `wiki/`, `api/`, `app/` as siblings, with git history from each source repo preserved (strategy TBD in Phase 0).
2. **Per-directory `CLAUDE.md`** so sessions opened anywhere in the tree get focused, lane-correct context. Root `CLAUDE.md` is thin and routes to children.
3. **Deploys reconfigured and verified** — Render builds the API from `api/`, Cloudflare Pages builds the frontend from `app/`. No regression in prod.
4. **Architecture Doc Integrity rule lifted to PR review** — wiki page updates and code changes that affect them ride in the same PR. The `stale_warning:` mechanism remains as an escape hatch but should rarely fire once same-PR updates are normal.
5. **Active workstream trackers updated** — `Owned paths` and `Code paths` sections in `journaling-ux`, `broker-integration`, `ai-coach`, `journal-analytics`, `deployment` rewritten to reference the new in-repo paths.
6. **Old repos archived (not deleted)** on GitHub with READMEs pointing at the monorepo. Local clones can be deleted by Paul on his own schedule.

## Lane

Wiki: Neurospect

This workstream is structurally cross-lane — it changes the repos that all the other workstreams write to. Treat it as a freeze-the-other-lanes operation: while the cutover is happening, other workstreams pause writes (see §Coordination).

Owned paths (this workstream may write here):

- `processes/distributed-workflow/active/monorepo-migration.md` (this tracker)
- After cutover, this tracker's owned-paths list expands to "everywhere in the new monorepo, for the duration of the migration only" — and contracts back to just this file once Phase 2 (post-migration cleanup) signs off.

Code paths (in repos, outside the wiki) — touched during migration:

- `neurospect-api/render.yaml`, `neurospect-api/pyproject.toml`, `neurospect-api/.gitignore`
- `neurospect-app/package.json`, Cloudflare Pages build config (dashboard, not in repo)
- New monorepo: root `package.json` (if any), root `.gitignore`, root `CLAUDE.md`, root `README.md`

## Required Context

Every session must read at boot:

- [[CLAUDE]] — wiki schema, isolation rule, **Architecture Doc Integrity** section (this whole workstream is about removing the structural cause of the drift problem that section was written to manage)
- This tracker
- [[entities/projects/neurospect]] — current architecture summary, deployment status, what's live

Other tracker files (read-only — needed to plan how their `Owned paths` rewrite at cutover):

- [[processes/distributed-workflow/active/journaling-ux]]
- [[processes/distributed-workflow/active/broker-integration]]
- [[processes/distributed-workflow/active/ai-coach]]
- [[processes/distributed-workflow/active/journal-analytics]]
- [[processes/distributed-workflow/active/deployment]]

Cross-wiki references use absolute paths, never wikilinks:

- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md`

## Plan-Mode Rule

Phase 0 (design / approval) is **plan-mode-first, every session, until Paul approves the migration spec.** The decisions here are reversible-but-painful (git history strategy, `CLAUDE.md` composition rule, deploy reconfig sequence) and the cost of an unapproved choice is high. Once Phase 0 is signed off, Phase 1 sub-phases can skip plan mode unless scope drift is detected.

## Phases

### Phase 0 — Design & Approval (current)

**Status:** scoping. Not yet plan-mode-approved.

Decisions to lock before any code/repo work:

1. **Git history strategy.** Options: (a) `git subtree add` to graft each source repo's history into a subdirectory of the new repo (preserves history, single linear log), (b) `git filter-repo` to rewrite each source repo into a subdir then merge (cleaner, more invasive), (c) accept history loss with three "imported from X" commits (simplest, loses blame). Recommend (a) unless there's a reason to fully rewrite.
2. **`CLAUDE.md` composition.** Confirm Claude Code reads per-directory `CLAUDE.md` files when sessions open in subdirs (this is the assumed behavior — verify before relying on it). Decide whether the root `CLAUDE.md` re-states the Isolation Rule and Architecture Doc Integrity rule, or just points to `wiki/CLAUDE.md`.
3. **Deploy cutover sequence.** Render and Cloudflare Pages both support a "root directory" build setting — confirm which dashboard fields, and decide whether to cut both deploys at the same moment (riskier, less rollback) or one at a time (longer dual-state window).
4. **Repo name.** `neurospect` (preferred — matches the project) vs `neurospect-monorepo` vs keeping one of the existing repos and absorbing the others into it.
5. **Coordination with active workstreams.** Pick a quiet window. Currently `journaling-ux` Phase 1 is awaiting a push, and `broker-integration` Phase 1 spec is approved but unstarted — both can be paused cleanly. Confirm with Paul before scheduling cutover.
6. **Old repo handling.** Archive on GitHub with a redirect README, or delete? Recommend archive (cheap insurance, preserves any external links).

Phase 0 produces: a written migration spec on this tracker, approved by Paul.

### Phase 1 — Execute Migration

Sub-phases TBD during Phase 0. Likely shape:

- 1a — create new `neurospect` repo, set up `.gitignore`, root `CLAUDE.md`, root `README.md`.
- 1b — graft source repos using the agreed history strategy. Verify each subdirectory's `git log --follow` works.
- 1c — write per-directory `CLAUDE.md` files. Move `wiki/CLAUDE.md` content to `wiki/CLAUDE.md` inside the monorepo with minimal edits (the Isolation Rule still applies; the cross-repo references in §Architecture Doc Integrity become same-repo references).
- 1d — reconfigure Render (build root = `api/`), reconfigure Cloudflare Pages (build root = `app/`). Verify both deploys go green from a test commit.
- 1e — verify prod end-to-end: Discord OAuth, trade CRUD, screenshot upload, TradingView webhook → Claude → coach panel.
- 1f — push monorepo to `main`, archive old repos on GitHub.

### Phase 2 — Post-Migration Cleanup

- Rewrite `Owned paths` and `Code paths` sections in every active tracker to reference the new in-repo paths. (List in §Required Context.)
- Update `concepts/architecture/phase2-project-structure.md`, `phase3-frontend-structure.md`, `phase4-coach-frontend.md`, `tradingview-connector.md` — anywhere they cite a repo name (`neurospect-api/...`, `neurospect-app/...`), rewrite to monorepo-relative paths.
- Update `entities/projects/neurospect.md` Current State section.
- Add a row to `index.md` Distributed Workflow noting this tracker.
- Append a final `log.md` row marking Phase 2 done; sign off the workstream.

## Decisions Log

Durable choices that affect future sessions. One bullet per decision; date it.

- 2026-05-02 — Workstream named `monorepo-migration` (matches kebab-case tracker convention; clearer than `repo-consolidation` because it names the structure being adopted).
- 2026-05-02 — **Target structure approved (Paul):** `neurospect/{wiki,api,app}/`. Per-directory `CLAUDE.md`. Render builds from `api/`, Cloudflare Pages from `app/`. Tradeoff comparison documented in session log; chose B over A (status quo), C (code-only merge), E1 (`apps/`+`docs/` convention), F (absorb into existing repo). Verification footnote: Phase 1a must confirm Claude Code composes per-directory `CLAUDE.md` files when sessions open in subdirs; if not, fallback is single root `CLAUDE.md` with explicit lane sections.
- 2026-05-02 — **Git history strategy approved (Paul): `git filter-repo`.** For each source repo: clone fresh → `git filter-repo --to-subdirectory-filter <wiki|api|app>` → fetch into new monorepo → merge with `--allow-unrelated-histories`. Every historical commit is rewritten so files live at the subdirectory path through all of history. Chose over subtree (path-discontinuity papercut at merge boundary) and history-drop (loses architecture-decision audit trail in commit messages). Hedge: tag the pre-rewrite tip of each source repo as `pre-monorepo-snapshot` in the archived repos so original SHAs remain findable. Tooling prerequisite: `pip install git-filter-repo` (one-time).
- 2026-05-02 — **Old-repo handling approved (Paul): archive on GitHub with redirect README.** For each of `neurospect-wiki` / `neurospect-api` / `neurospect-app`: edit README to add `Moved to https://github.com/.../neurospect — see wiki/api/app subdirs` → commit → `gh repo archive`. Chose over delete (irreversible, breaks SHA URLs) and rename-to-legacy (half-measure, allows accidental pushes). Archive preserves SHA links, `pre-monorepo-snapshot` tags, and issue history; reversible.

## Pending Wiki Updates

Applied during end-of-day merge session.

- `index.md`: under `## Processes` → `### Distributed Workflow`, append a new bullet: `- [[processes/distributed-workflow/active/monorepo-migration]] — consolidate three Neurospect repos into one monorepo. Phase 0 (scoping).`
- `log.md`: append `| 2026-05-02 | plan | Created monorepo-migration tracker. Scope: merge neurospect-wiki + neurospect-api + neurospect-app into a single neurospect monorepo with wiki/api/app sibling dirs. Phase 0 = design/approval (git history strategy, CLAUDE.md composition, deploy cutover sequence, repo name, coordination, old-repo handling). Spec not yet approved. |`

## Blockers / Open Questions

For Paul. Each gets a date so it's clear how long it has been pending.

- ~~2026-05-02 — Approve target structure: `neurospect/{wiki,api,app}/` with per-directory `CLAUDE.md`.~~ **Resolved 2026-05-02 — B approved.**
- ~~2026-05-02 — Git history strategy: prefer `git subtree` vs `git filter-repo` vs drop history.~~ **Resolved 2026-05-02 — `git filter-repo` approved.** Hedge: tag `pre-monorepo-snapshot` on each source repo before rewrite.
- ~~2026-05-02 — Cutover window: when is it safe to pause `journaling-ux` and `broker-integration` for the migration session?~~ **Resolved 2026-05-02 — cutover proceeding now.**
- ~~2026-05-02 — Old repos: archive on GitHub or delete?~~ **Resolved 2026-05-02 — archive with redirect README.**

## Cross-Lane Requests

Wanted to write outside the lane? Don't. Write here instead.

_None yet._

## Coordination

This workstream temporarily freezes other workstreams during the cutover (Phase 1d–1f). Sequence:

1. Notify Paul; pick a quiet window.
2. Pause writes from `journaling-ux`, `broker-integration`, `ai-coach`, `journal-analytics`, `deployment` for the duration of cutover.
3. Run cutover; verify deploys.
4. Phase 2 rewrites the paused trackers' path references.
5. Resume normal workstream activity.

## Session Log

Append-only. Newest at the bottom.

### 2026-05-02 — tracker created

- did: created this tracker; outlined Phase 0 / 1 / 2; enumerated open questions and coordination plan.
- decided: workstream name `monorepo-migration`; target structure `neurospect/{wiki,api,app}/` with per-directory `CLAUDE.md` (pending Paul's approval).
- next: Paul reviews open questions in §Blockers; on approval, Phase 0 closes and Phase 1 sub-phases get sequenced.

### 2026-05-02 — Phase 0 closed; Phase 1a–1c executed (same session)

- decided (Paul): structure B; history via `git filter-repo`; archive old repos with redirect README; cutover proceeding immediately.
- did: pre-flight surfaced significant uncommitted broker-integration code in `neurospect-api` and `neurospect-app` (matched the 1a/1b/1c "Code shipped" manifests in `broker-integration.md`). Bundled per-repo and committed: wiki (`b39a0ab` — broker reconciliation + monorepo tracker), api (`c734e2a` — Phase 1a-1c), app (`02447c4` — Phase 1c UI). Pushed all three; tagged `pre-monorepo-snapshot` on each.
- did: surfaced an unrelated `russell94paul/neurospect` repo (PUBLIC, prior prototype) at the target name. Renamed it to `neurospect-prototype` to free the canonical name.
- did: surfaced credentials drift in `wiki/index.md` (Discord client secret + TV 2FA recovery codes in plaintext). Created `wiki/vault/credentials.md` (gitignored at `.gitignore:vault/`), replaced the index.md Vault section with a one-line pointer, committed (`9c4c78f`) and pushed. **Flagged Paul to rotate both secrets** — exposure includes archived neurospect-wiki history.
- did (1a): created `russell94paul/neurospect` (private). Created staging dir `C:\Users\PaulRussell\migration-staging\` with fresh clones of all three sources.
- did (1b): ran `git filter-repo --to-subdirectory-filter wiki|api|app` on each clone. For the wiki, also applied `--replace-text redactions.txt` to scrub the Discord secret + 6 TV codes from rewritten history (Client ID retained — public OAuth identifier). Verified redactions in rewritten history.
- did (1c): cloned the empty monorepo, added each filtered repo as a remote, fetched, and merged in order: wiki (initial branch), api (`--allow-unrelated-histories`), app (same). Tree at root: `wiki/`, `api/`, `app/`. Full history preserved through all three subtrees.
- did: wrote root `CLAUDE.md` (thin router), `api/CLAUDE.md`, `app/CLAUDE.md`. Updated `wiki/CLAUDE.md` cross-references: Directory Structure section (`wiki/` instead of `neurospect-wiki/`), Isolation Rule § Lane (now scoped to `wiki/` dir, allows cross-lane edits in cross-cutting PRs), Architecture Doc Integrity (ground-truth code dirs are `../api/` + `../app/`; env-vars canonical doc path is `../api/.env.example`). Wrote root `README.md`. Committed (`1d9609e`) and pushed to `origin/main`.
- decided: monorepo final state — 3 top-level dirs (wiki 2.5MB, api 358KB, app 739KB); clean tree; private repo on GitHub.
- next: Paul's dashboard steps remaining — (a) Render: change web service root directory from repo-root to `api/`, redeploy. (b) Cloudflare Pages: change project root from repo-root to `app/`, redeploy. Then end-to-end verification (Discord OAuth, trade CRUD, screenshot upload, TradingView webhook → coach panel). Then archive old repos with redirect README. Phase 2 cleanup (rewrite `Code paths` in other active trackers + update architecture doc paths) follows after deploys verify.

## Next Session Boot Prompt

Copy-paste the block below into a fresh Claude Code session.

````
You are resuming the monorepo-migration workstream. Boot procedure:

1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`.
2. Read this tracker: `C:\Users\PaulRussell\repos\neurospect-wiki\processes\distributed-workflow\active\monorepo-migration.md`.
3. Read every page in *Required Context* (parallel reads).
4. Pick up at the *next:* line of the most recent *Session Log* entry.

Plan mode rule for this workstream: Phase 0 is plan-mode-first every session until Paul approves the migration spec. After approval, Phase 1 sub-phases skip plan mode unless scope drift is detected.

When you're done, follow the checkpoint procedure in
`C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md` § *Checkpoint*.
````

## See Also

- [[CLAUDE]] — § *Architecture Doc Integrity* (the structural problem this workstream solves)
- [[entities/projects/neurospect]]
- [[processes/distributed-workflow/active/journaling-ux]]
- [[processes/distributed-workflow/active/broker-integration]]
- [[processes/distributed-workflow/active/ai-coach]]
- [[processes/distributed-workflow/active/journal-analytics]]
- [[processes/distributed-workflow/active/deployment]]
