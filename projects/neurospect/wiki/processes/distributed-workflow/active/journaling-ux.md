---
tags: [distributed-workflow, active, neurospect, journaling, ux, frontend]
aliases: [Journaling UX Tracker, Trade Form Redesign]
sources: []
created: 2026-04-26
updated: 2026-04-26
phases:
  phase_1: complete
  phase_2: complete
---

# Journaling UX — Workstream Tracker

Reduce trade entry friction so journaling happens consistently. Phase 1: tab-based form redesign + field reduction. Phase 2: AI Coach pre-fill + Start Trade from Signal. Voice input deprioritised — nice-to-have, lower trader value.

> **Broker auto-populate moved to its own workstream.** What was originally scoped here as Phase 3 has been forked into [[broker-integration]] (2026-04-26). That workstream owns broker credentials, Tradovate REST integration, the active-trade soft singleton, and `/settings/broker`. This tracker stays focused on the journal form/UX itself.

Design detail: [[concepts/roadmap/ideas/reduce-journaling-friction]]

## Goal

By end of Phase 1:
1. **R2 screenshots wired** — uploads work in prod (currently 503 gracefully)
2. **Tab-based trade form** — Pre-Trade / Entry / Post-Trade as tabs, not collapsible sections
3. **Reduced pre-trade fields** — 6 prominent fields + Advanced accordion for optional detail
4. **Sensible defaults** — date = today, instrument = NQ
5. **`public/neurospect-coach.pine` synced** — the static mirror in `app/public/` must reflect the updated wiki Pine script (changed during Phase 4 deployment)

## Current form state (as of 2026-04-26)

The form at `src/components/trade/trade-form.tsx` uses three `<Collapsible>` sections (Pre-Trade, Entry, Post-Trade) with auto-open logic based on trade status. All sections are on one scrolling page.

Pre-Trade section has **12 fields**: trade_date, instrument, session, kill_zone, htf_bias, htf_fvg_low, htf_fvg_high, draw_on_liquidity, dol_price_level, opening_price_position, news_flag, setup_type, narrative.

The schema, backend API, and database do not change — this is a pure frontend refactor.

---

## Phase 1 — Tab redesign + R2 wiring

### Step 1 — Wire R2 screenshots (30 min)

Manual setup required before code:
1. Cloudflare dashboard → R2 → Create bucket named `neurospect-screenshots`
2. R2 → Manage R2 API tokens → create token with **Object Read & Write** on that bucket
3. Note: endpoint URL, access key ID, secret access key
4. In Render env vars, set:
   - `R2_ENDPOINT_URL` — e.g. `https://<account_id>.r2.cloudflarestorage.com`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`
   - `R2_BUCKET` = `neurospect-screenshots`
5. Render will redeploy. Test by uploading a screenshot in the trade detail page — should return a URL instead of 503.

### Step 2 — Sync `neurospect-coach.pine` static mirror

File: `app/public/neurospect-coach.pine`

This is a static mirror of the wiki canonical Pine script. It was updated significantly during the Phase 4 deployment session. Sync it:
- Copy `neurospect-wiki/assets/pine/neurospect-coach.pine` → `app/public/neurospect-coach.pine`
- The `PineScriptCard` component in `coach-setup` serves this file as a download.

### Step 3 — Tab-based trade form refactor

**Files to change:**
- `src/components/trade/trade-form.tsx` — replace `<Collapsible>` sections with `<Tabs>` from shadcn/ui
- `src/components/trade/pre-trade-fields.tsx` — add Advanced collapsible for optional fields; add defaults

**Tab UX design:**
- Use shadcn `<Tabs>` / `<TabsList>` / `<TabsTrigger>` / `<TabsContent>`
- Tab order: Pre-Trade → Entry → Post-Trade
- Active tab driven by trade status on edit (`pre_trade` → Pre-Trade tab, `active` → Entry tab, `closed` → Post-Trade tab)
- On create: always open to Pre-Trade tab
- Tab switching is always allowed (no gating) — user may need to jump between tabs

**Pre-Trade tab — prominent fields (no accordion):**
```
Trade Date (default: today)     Instrument (default: NQ)
Session                         Kill Zone
HTF Bias [Bullish | Bearish | Neutral]  (full width radio)
Setup Type                      (full width select)
Narrative                       (full width textarea, 3 rows)
```

**Pre-Trade tab — Advanced collapsible (collapsed by default):**
```
HTF FVG Low    HTF FVG High
Draw on Liquidity    DOL Price Level
Opening Price Position    News Flag
```

**Entry tab — fields (unchanged from current `entry-fields.tsx`):**
entry_time, entry_price, stop_price, stop_logic, target_price, target_logic, entry_pda, displacement_quality, smt_confirmation

**Post-Trade tab — fields (unchanged from current `post-trade-fields.tsx`):**
exit_time, exit_price, outcome, r_multiple (auto-calc), mae, mfe, target_reached, plan_followed, quality_grade, mistake_tags, post_trade_notes

**Status transition buttons** stay at the bottom of the form (outside tabs):
- Create: "Save Trade" (saves pre_trade status)
- Edit pre_trade: "Mark as Active" 
- Edit active: "Close Trade"

**Default values for new trades:**
```typescript
trade_date: format(new Date(), 'yyyy-MM-dd'),  // today
instrument: 'NQ',
```

### Step 4 — Deploy frontend

Push `neurospect-app` to GitHub → Cloudflare Pages auto-deploys. Verify:
- New trade form opens on Pre-Trade tab with today's date + NQ pre-filled
- Tabs switch correctly
- Advanced section collapses correctly
- Status transitions still work
- Screenshot upload works (after R2 wiring)

---

## Phase 2 — AI Coach Pre-fill (spec approved 2026-04-26)

Pre-fill the Pre-Trade tab on **new trade creation** from the most recent completed coaching event, when the event's session matches the *current* ET session. Pure frontend — no backend or schema changes.

### Data source

`coaching_event.request_payload` (Layer 2 — TradingView's posted payload). Layer 3 (`response_payload`) is **not** used: Claude's `bias` can be `stand_aside`, which doesn't map to the form's bias enum, and the user's pre-trade thesis should reflect raw chart context, not Claude's verdict.

### Field mapping

| Form field | Coach source | Notes |
|---|---|---|
| `instrument` | `request_payload.instrument` | Overrides the `NQ` default — a recent coach signal wins |
| `session` | `request_payload.session` | `off` → `null`; otherwise pass through |
| `htf_bias` | `request_payload.htf_fvg_bias` | direct enum match |
| `htf_fvg_low` | `request_payload.htf_fvg_range[0]` | skip if `htf_fvg_range` is null |
| `htf_fvg_high` | `request_payload.htf_fvg_range[1]` | skip if `htf_fvg_range` is null |
| `news_flag` | `request_payload.news_flag` | pre-filled even though it lives in Advanced |

**Not pre-filled:** `kill_zone`, `setup_type`, `narrative`, `draw_on_liquidity`, `dol_price_level`, `opening_price_position`. (No L2 source, or the mapping is lossy — e.g. L2 `price_vs_midnight_open` doesn't distinguish `*_all` vs `*_some`.)

### Eligibility (session-aware staleness)

Pre-fill happens only when ALL of these hold:
1. Latest coaching event exists (`/api/coach/events/latest` returns non-null).
2. Event `status === 'complete'`.
3. `request_payload.session` equals the **current ET session** computed at form-mount time.
4. Form is in create mode (no `trade` prop).

**No time-based cutoff** — session match is the staleness rule. If the session changes, the next mount will not pre-fill.

#### Current-session helper

Mirror the Pine script logic exactly (`public/neurospect-coach.pine` lines 51-54):

| Session | ET window (minutes since 00:00 ET) |
|---|---|
| `london` | 120 ≤ tod < 300 (02:00-05:00) |
| `ny_am`  | 510 ≤ tod < 690 (08:30-11:30) |
| `ny_pm`  | 810 ≤ tod < 960 (13:30-16:00) |
| `off`    | everything else |

Note: the L2 schema allows `asia`, but the Pine script never emits it — so a coach event with session `asia` would never match. Acceptable: live alerts only ever produce `london`/`ny_am`/`ny_pm`/`off`, and `off` will never match (frontend treats `off` as "no current session" → no pre-fill, ever).

ET conversion: `Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit', hour12: false })`.

### UX treatment

Banner above the Pre-Trade tab content, only when pre-fill actually happened:

```
┌──────────────────────────────────────────────────┐
│ ✨ Pre-filled from coach              [Clear]    │
└──────────────────────────────────────────────────┘
```

- "Clear" resets the pre-filled fields back to base defaults (today + NQ + nulls) and dismisses the banner.
- Banner auto-dismisses if the user manually edits any pre-filled field (it stops being accurate at that point).
- **Advanced section auto-expands** on mount when FVG levels were pre-filled, so the user sees the populated values. Otherwise it stays collapsed by default.

### Edge cases

| Case | Behavior |
|---|---|
| No event ever | Existing defaults. No banner. |
| Latest event session ≠ current ET session | Existing defaults. No banner. |
| Current ET session is `off` | Existing defaults (no session can match `off`). No banner. |
| Latest event still `pending` | Existing defaults. No banner. (Don't pre-fill from L2 alone — wait for full event.) |
| Event arrives while form is open and user has typed | Don't stomp. Use `form.reset(merged, { keepDirtyValues: true })`. |
| `htf_fvg_range` is null | Pre-fill bias/session/instrument/news_flag; leave FVG levels at null; do NOT auto-expand Advanced. |
| Edit mode (existing trade) | Hook is not called; no pre-fill. |

### Implementation plan

**Backend:** no changes. ✓

**Frontend:** ~120 LOC across three files.

1. **`src/lib/coach-prefill.ts`** *(new)* — pure helpers, easy to unit-test:
   - `getCurrentEtSession(now: Date): 'london' | 'ny_am' | 'ny_pm' | 'off'`
   - `extractPrefill(event: CoachingEvent | null, now: Date): { values: Partial<TradeFormValues>; expandAdvanced: boolean } | null`
     - returns `null` if event missing, not `complete`, or session mismatch
     - narrows `request_payload` (typed `Record<string, unknown>` today) safely inside the helper
     - sets `expandAdvanced = true` iff `htf_fvg_low` or `htf_fvg_high` was pre-filled

2. **`src/components/trade/trade-form.tsx`** — modify create-mode init:
   - Call `useLatestCoachingEvent()` (gate with `enabled: !isEdit` would require a small hook tweak — alternative: just call it and ignore in edit mode).
   - On data arrival (`useEffect`), call `extractPrefill`. If non-null:
     - `form.reset({ ...currentValues, ...prefill.values }, { keepDirtyValues: true })`
     - Track `prefilledFieldNames` in a `ref` for the banner's "user dirtied a pre-filled field" detection.
     - Pass `expandAdvanced` and `prefilledFieldNames` down to `<PreTradeFields>`.
   - Render `<CoachPrefillBanner>` above the Tabs (or inside the Pre-Trade tab content) when prefill is active and user hasn't dirtied any pre-filled field.

3. **`src/components/trade/coach-prefill-banner.tsx`** *(new, ~30 LOC)* — presentational:
   - Props: `onClear: () => void`
   - Static copy: "Pre-filled from coach" + Clear button.

4. **`src/components/trade/pre-trade-fields.tsx`** — accept `defaultAdvancedOpen?: boolean` prop and use it to seed `useState`. (One-line change.)

**Tests:** `coach-prefill.ts` is pure → unit-testable.
- `getCurrentEtSession` across DST boundary, all four windows, edges (e.g. exactly 11:30 ET = `off`).
- `extractPrefill` with: stale session, pending status, missing range, missing payload, `off` current session, happy path.

### Decisions log

| Decision | Reasoning |
|---|---|
| Source = L2 `request_payload`, not L3 `response_payload` | L3 `bias` allows `stand_aside`, doesn't fit the form enum; pre-trade thesis = raw context |
| Session-aware match, not time-based cutoff | Matches the user's mental model (alerts are session-bounded); robust on slow days |
| Coach instrument overrides `NQ` default | A recent signal is stronger evidence than the static default |
| News flag pre-fills even though it's in Advanced | Free signal; auto-expand surfaces it when set |
| Advanced auto-expands only when FVG levels pre-filled | Hiding pre-filled values defeats the indicator |
| Banner copy = "Pre-filled from coach" (no relative time) | Time-since adds little when match is session-bounded; simpler |

---

## Session Log

### 2026-04-26 — tracker created

- did: created this tracker. Phase 4 (TradingView webhook) now complete. Paul's feedback on trade form: too many fields, wants tab-based pre-trade/entry/post-trade flow.
- decided: Phase 1 is a pure frontend refactor — no backend changes, no schema changes. Backend API already has PATCH semantics so partial saves work correctly.
- decided: Chrome extension (one-click screenshot) is a separate session — too large to combine with form redesign. It requires its own browser extension project.
- next: wire R2 → sync Pine script mirror → tab form refactor → deploy

### 2026-04-26 — Phase 2 implementation complete

- did: created `src/lib/coach-prefill.ts` — `getCurrentEtSession` mirrors Pine script windows exactly (london 120-300, ny_am 510-690, ny_pm 810-960, half-open); `extractPrefill` returns null for null/pending/session-mismatch/off-session, maps instrument, session, htf_bias (from htf_fvg_bias), htf_fvg_low/high (from htf_fvg_range tuple, skipped if null), news_flag; `fieldNames` list enables dirty-based banner auto-dismiss; `expandAdvanced` true iff FVG levels were pre-filled.
- did: created `src/components/trade/coach-prefill-banner.tsx` — sparkles icon + "Pre-filled from coach" + Clear button; styled div with `bg-muted` (no Alert component present in this project).
- did: modified `src/components/trade/pre-trade-fields.tsx` — added `defaultAdvancedOpen?: boolean` prop, seeds `useState(defaultAdvancedOpen)`.
- did: modified `src/components/trade/trade-form.tsx` — `useLatestCoachingEvent()` called unconditionally; `useEffect` on `coachQuery.data` runs only in create mode, calls `extractPrefill`, calls `form.reset({...getValues(), ...prefill.values}, { keepDirtyValues: true })`; `form.watch` on 6 prefillable fields drives dirty detection; `showBanner` derived from `prefilledFieldNames.length > 0 && !anyPrefilledDirty`; `<CoachPrefillBanner>` rendered above `<PreTradeFields>` in Pre-Trade tab; Clear handler resets only pre-filled fields to base defaults and collapses Advanced; `<PreTradeFields key={String(expandAdvanced)}>` forces remount when advanced auto-expand state changes.
- verified: `tsc -b` — zero errors.
- no test runner present (no vitest/jest in package.json) — skipped test file.
- next: Paul runs `npm run dev`, opens `/trades/new`, verifies banner and pre-fill with a complete coach event in the matching session. Then push to main for Cloudflare auto-deploy.

### 2026-04-26 — Phase 2 spec approved

- did: read `use-coaching.ts`, `trade-form.tsx`, `pre-trade-fields.tsx`, `coach.py`, and the Pine script's session logic. Drafted Phase 2 spec.
- decided: source = L2 `request_payload` (not L3); session-aware match (not time cutoff); coach instrument wins over NQ default; news_flag pre-filled; Advanced auto-expands when FVG levels pre-filled; banner copy = "Pre-filled from coach" (no relative time).
- decided: pure frontend — no backend or schema changes. ~120 LOC across `src/lib/coach-prefill.ts` (new), `src/components/trade/trade-form.tsx` (modify), `src/components/trade/coach-prefill-banner.tsx` (new), `src/components/trade/pre-trade-fields.tsx` (one-prop change).
- noted: Pine script never emits session `asia` (only `london`/`ny_am`/`ny_pm`/`off`), so the `asia` enum value in the L2 schema is unreachable in practice; `off` cannot match (frontend doesn't pre-fill in `off`).
- next: implementation session — Sonnet, in `neurospect-app` only. Boot prompt below.

### 2026-04-26 — implementation session (Phase 1 code complete)

- did: synced `public/neurospect-coach.pine` from wiki canonical — bumped v5→v6, dropped `confirm=true` on secret input, simplified FVG auto-detection comments, replaced rising-edge `prevRequest` pattern with `requestCoaching and not na(body)`, added null-guard for `autoFvgBias`.
- did: rewrote `src/components/trade/trade-form.tsx` — replaced 3 `<Collapsible>` sections + `<Separator>` with shadcn `<Tabs>`. Removed `preTradeSectionOpen/entrySectionOpen/postTradeSectionOpen` state. Added `defaultTabForStatus()` (pre_trade→pre-trade, active→entry, closed→post-trade). Default values updated: `trade_date = format(new Date(), 'yyyy-MM-dd')`, `instrument = 'NQ'`. Button label: "Save Trade" for create, "Save" for edit.
- did: rewrote `src/components/trade/pre-trade-fields.tsx` — split into 6 prominent fields (trade_date, instrument, session, kill_zone, htf_bias, setup_type, narrative) + Advanced collapsible (htf_fvg_low, htf_fvg_high, draw_on_liquidity, dol_price_level, opening_price_position, news_flag). Advanced collapsed by default via `useState(false)`.
- did: `tsc -b` — zero TypeScript errors.
- blocker (resolved 2026-04-26): R2 env vars set on Render — Cloudflare bucket created, screenshot upload confirmed live.
- next: Paul runs `npm run dev` to verify the form locally, then pushes to main for Cloudflare auto-deploy. Once R2 env vars are set on Render and redeployed, screenshot upload is live.

### 2026-04-26 — Phase 2 extended: UX iteration + live debugging

- did: fixed banner visibility — `showBanner` was broken because RHF reset + React state batch ordering caused the dirty-field detection (`prefilledFieldNames.length > 0 && !anyPrefilledDirty`) to always evaluate false. Replaced with explicit `bannerActive` boolean state set directly in the effect.
- did: upgraded banner — changed from invisible `bg-muted` gray to amber (`border-amber-300 bg-amber-50`); now lists the specific pre-filled field names inline.
- did: added per-field amber ring highlights (`ring-1 ring-amber-400`) to each pre-filled field in `pre-trade-fields.tsx` via a `prefilledFields?: Set<keyof TradeFormValues>` prop. Applies to instrument, session, htf_bias, htf_fvg_low, htf_fvg_high, news_flag.
- did: added "Start Trade from Signal" button to `CoachingPanel` (complete state). Uses `buildTradeCreateFromEvent()` helper in `coach-prefill.ts`; `useCreateTrade` navigates to `/trades/<id>` on success.
- did: threaded coach field names through React Router navigation state so the banner and highlights show in edit mode on arrival from "Start Trade from Signal". Modified `useCreateTrade` to accept optional `navState` parameter (ref-based to avoid stale closure).
- did: split banner buttons into "Got it" (confirm — dismiss banner/highlights, keep values) and "Reset fields" (clear — reset pre-filled fields to base defaults, dismiss). Safer default (Got it), explicit destructive action (Reset fields).
- did: Pine script trigger debugging — fixed `requestCoaching and not requestCoaching[1]` (broke because inputs are compile-time constants in Pine v6, making `[1]` identical to the constant; rising-edge detection is impossible on inputs). Restored `requestCoaching and not na(body)` with confirmed-working TradingView alert setup.
- confirmed: TradingView idempotency key (`ticker:bar_time:bar_index`) correctly deduplicates same-bar alerts — tested with 3 rapid-fire alerts, third rejected as duplicate.
- confirmed: R2 screenshot upload live. Cloudflare bucket created, Render env vars set.
- decided: broker auto-populate takes precedence over voice input for Phase 3. Voice input is a nice-to-have with lower trader value — deprioritised.

### 2026-04-26 — Broker auto-populate forked to its own workstream

- did: planned what was originally Phase 3 (broker auto-populate), then forked it into a dedicated workstream tracker at `processes/distributed-workflow/active/broker-integration.md` for clarity and separation of concerns. All Phase 3 design content — soft singleton, data model deltas, Tradovate REST architecture, settings UI, sub-phase decomposition — moved there as Phase 1 of the new workstream.
- decided: this tracker stays focused on the journal form/UX (tabs, field reduction, defaults, AI Coach pre-fill). Broker work, active-trade singleton, `/settings/broker`, Tradovate REST integration all belong to the broker-integration workstream.
- next: nothing immediate on this tracker — Phases 1 and 2 are complete. Future journaling-UX work (e.g. voice input if revived, additional pre-fill sources, mobile UX) would be Phase 3+.

---

## See Also

- [[broker-integration]] — sister workstream; broker auto-populate (forked from this tracker's original Phase 3)
- [[concepts/roadmap/ideas/reduce-journaling-friction]] — design detail
- [[concepts/roadmap/ideas/chrome-screenshot-extension]] — next session (separate scope)
- [[processes/distributed-workflow/active/deployment]] — R2 setup steps in §Phase 1 §2
- [[concepts/architecture/trade-schema]] — field definitions
- [[concepts/architecture/phase3-frontend-structure]] — frontend layout
- [[entities/projects/neurospect]] — project overview
