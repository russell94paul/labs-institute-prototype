---
tags: [index, navigation]
created: 2026-04-18
updated: 2026-05-23
last_fork: 2026-04-26-broker-integration-forked-from-journaling-ux
last_build: 2026-04-26-phase4-deployment-complete
last_design: 2026-04-24-phase4-coach-frontend-design
last_ingest: 2026-04-22
last_integration: 2026-05-23-conductor-integration-neurofusion-research
---

# Neurospect Wiki Index

Master catalog of all Neurospect wiki pages.

> **Isolation Rule:** This wiki is fully decoupled from the ALDC work wiki. The only allowed cross-wiki reference is ALDC research → Neurospect, by absolute path, from trackers. See [[CLAUDE]] § *Isolation Rule*.

---

## Entities

### Projects

- [[entities/projects/neurospect]] — core project entity (ICT trading journal + AI coach)

### People

- [[entities/people/mrwitness-axl]] — MrWitness and Axel (AXL), the two instructors delivering the mentorship curriculum

### Tools

_None yet._

---

## Roadmap

Forward-looking product roadmap (horizons: Now / Next / Later / Strategic / Research / Compliance-Sensitive). Supersedes the v1 phased plan in `entities/projects/neurospect.md` for forward decisions.

- [[concepts/roadmap/README]] — main roadmap with horizon assignments, prioritization rationale, lifecycle convention
- [[concepts/roadmap/ideas/README]] — idea-backlog index (15 stubs)

---

## Concepts

### Business Logic

- [[concepts/business-logic/ict-liquidity]] — BSL/SSL, swing highs/lows, DOL, FVG (BISI/SIBI), IOFED, BAG — the two forces that move price
- [[concepts/business-logic/ict-narratives]] — 4 stages of algorithmic price delivery (consolidation/expansion/retracement/reversal), Power of Three (AMD), session kill zones, opening prices, daily bias (Vol 1–2)
- [[concepts/business-logic/ict-entry-models]] — FVG, order blocks, rejection blocks, breaker blocks, BPR, OTE, Model 2022, CSD, three-step execution framework (Vol 1, 3)
- [[concepts/business-logic/ict-market-structure]] — MSS, BOS, STH/ITH/LTH, STL/ITL/LTL, market structure fractality, CSD, reversal types (Vol 3)
- [[concepts/business-logic/ict-smt]] — SMT divergence, The Triad (NQ/ES/YM), cracking correlation, Price SMT, PDR SMT (Vol 4 Class 2); trust-the-program framework
- [[concepts/business-logic/ict-deviations]] — Fibonacci deviation targeting for HOD/LOD, HPDL, two-set market structure deviations (Vol 2 Class 3, Vol 3 Class 4)
- [[concepts/business-logic/ict-order-flow]] — HTF/LTF order flow, closing basis, quadrant levels, LRLR/HRLR, order block respect/disrespect (Vol 4 Class 1)
- [[concepts/business-logic/ict-live-commentary]] — live pre-market framework, day-of-week protocol, HOD/LOD calling, weekly opening price, first presentation FVG, liquidity void, contract rollover (stream + YouTube ingest)

### Architecture

- [[concepts/architecture/tech-stack]] — canonical backend stack decision (FastAPI + SQLAlchemy async + Postgres on Render + Discord OAuth2 + TradingView webhooks + Cloudflare R2); shared by AI Coach and Journal modules
- [[concepts/architecture/trade-schema]] — ICT trade data model: field definitions, Postgres DDL, indexes, REST API surface (Phase 1 of Journal & Analytics)
- [[concepts/architecture/phase2-project-structure]] — APPROVED project layout for `api/` (formerly the `neurospect-api` repo): directory structure, Poetry deps, auth flow, analytics SQL approach, file creation order (Phase 2)
- [[concepts/architecture/tradingview-connector]] — AI Coach Phase 3 end-to-end design: Pine Script indicator, `/webhooks/tradingview/{user_token}` validation stack, `coaching_events` table, Claude prompt-cached call, polling endpoint
- [[concepts/architecture/transcript-pipeline]] — transcript ingestion decision doc (manual + Whisper)
- [[concepts/architecture/phase3-frontend-structure]] — **canonical frontend doc**: React 19 + TS + Vite project layout, route map, key patterns (auth, trade form, screenshot upload, analytics hooks), env vars
- [[concepts/architecture/phase4-coach-frontend]] — AI Coach frontend: routes, hooks, component tree, polling strategy, TV token UX, Pine asset sync
- [[concepts/architecture/frontend-codebases]] — Three frontend codebases: neurospect-ui/ (marketing), app/ (product), site/ (deprecated Astro SSG — deleted 2026-05-23)

### NeuroFusion-13 (SIHRE)

- `research/neurofusion/README.md` — NeuroFusion-13 architecture overview: 13-signal Self-Improving Heterogeneous Reasoning Ensemble (SIHRE) for quant trading
- `research/neurofusion/deep-research-prompts.md` — 7 deep research prompts (all completed via ChatGPT Pro + Gemini)
- `research/neurofusion/data/` — 8 research reports (prompts 1-7 + Gemini second opinion on prompt 1)
- `paul-wiki/decisions/DEC-001-conductor-integration.md` — Conductor integration audit, mapping decisions, gap analysis

### AI Coach

- [[concepts/ai-coach/strategies.json]] — machine-readable strategy library (generated from entry-models YAML blocks; loaded into Claude system prompt)
- [[concepts/ai-coach/system-prompt-template.md]] — full Claude system prompt template (ICT rules + strategy library + JSON output schema); v1.0
- [[concepts/ai-coach/chart-analysis-boot-prompt]] — standalone boot prompt for manual chart analysis sessions (copy-paste into any Claude session with vision)

### Course (Module 1 — Foundations)

- [[concepts/course/README]] — course overview and learning path (5 modules, prerequisite order)
- [[concepts/course/module-1-foundations/01-what-moves-the-market]] — Liquidity (BSL/SSL/DOL), Inefficiency (FVG), the daily price cycle (Vol 1 Cls 1)
- [[concepts/course/module-1-foundations/02-fair-value-gaps]] — FVG precision, BISI/SIBI, IOFED, BAG, inversion FVG, AXL sniper entries (Vol 1 Cls 1–2)
- [[concepts/course/module-1-foundations/03-homework-and-practice]] — Class 1 and Class 2 homework assignments + readiness checklist

### Course (Module 2 — Price Delivery)

- [[concepts/course/module-2-price-delivery/01-four-stages-apd]] — Consolidation/Expansion/Retracement/Reversal overview; real vs. fake retracement; BPR skipping (Vol 1 Cls 2–4)
- [[concepts/course/module-2-price-delivery/02-consolidation-model]] — Stage 1 in depth: range definition, EQ, two delivery paths, SMT at sweep, live NQ example (Vol 1 Cls 2)
- [[concepts/course/module-2-price-delivery/03-expansion-retracement]] — Stages 2 & 3: measuring expansion, real/fake retracement, healthy/choppy, algorithmic body signature, worked examples (Vol 1 Cls 3)
- [[concepts/course/module-2-price-delivery/04-reversals]] — Stage 4: three reversal types (failure swing ~10%, raid on stops ~80%, accumulation ~10%), layered liquidity rule (Vol 1 Cls 4)

### Course (Module 3 — Session Context & Bias)

- [[concepts/course/module-3-session-and-bias/01-power-of-three]] — AMD framework; four opening prices; daily candle anatomy; worked Asia trade example (Vol 2 Cls 1)
- [[concepts/course/module-3-session-and-bias/02-session-kill-zones]] — five KZ windows; opening price anchors; NY AM two-part structure; ORG size; highest-probability stack (Vol 2 Cls 2)
- [[concepts/course/module-3-session-and-bias/03-deviations]] — Fibonacci deviation targeting; HOD/LOD anchoring; HPDL; two worked London examples (Vol 2 Cls 3)
- [[concepts/course/module-3-session-and-bias/04-daily-bias]] — HTF FVG cycle; opening price position; 80% bias framework; live 4H FVG walk-through (Vol 2 Cls 4)

### Course (Module 4 — Market Structure)

- [[concepts/course/module-4-market-structure/01-swing-classification]] — STH/ITH/LTH; gap-qualification rule; why STLs are suspect; MSS trigger; daily chart ITL example (Vol 3 Cls 2)
- [[concepts/course/module-4-market-structure/02-fractality]] — FVG liquidity engineering; engineered swing inside a FVG; turtle soup pattern; multi-TF nesting; daily fractal walk-through (Vol 3 Cls 2)
- [[concepts/course/module-4-market-structure/03-structure-deviations]] — two-set deviation anchoring (ITL price leg + STL measuring swing); convergence zone = HOD/LOD; London and holiday worked examples (Vol 3 Cls 4)
- [[concepts/course/module-4-market-structure/04-model-2022-ote-csd]] — 62–79% OTE zone; OTE block selection (highest open, propulsion block, 0.705 concert); CSD pre-MSS signal; full entry sequence (Vol 3 Cls 5)

### Course (Module 5 — Order Flow & SMT)

- [[concepts/course/module-5-order-flow-and-smt/01-htf-ltf-order-flow]] — bodies vs. wicks; closing basis; quadrant levels (0/0.25/0.5/0.75/1.0); LRLR vs. HRLR; BPR behavior; 5M bearish ES session walk-through (Vol 4 Cls 1)
- [[concepts/course/module-5-order-flow-and-smt/02-smt-divergence]] — triad (NQ/ES/YM); cracking correlation; Price SMT vs. PDR SMT; chart setup (3 methods); distribution and accumulation examples; trust-the-program; Six Sisters distinction (Vol 4 Cls 2)

### Entry Models Library

- [[concepts/entry-models/README]] — library overview, universal minimum confluence, stop/target conventions
- [[concepts/entry-models/consolidation-model]] — consolidation range + EQ + PDA entry; YAML machine-readable strategy block (Vol 1 Cls 2)
- [[concepts/entry-models/expansion-retracement-model]] — FVG/OB in discount after expansion; real retracement checklist; YAML block (Vol 1 Cls 3)
- [[concepts/entry-models/reversal-raid-on-stops]] — liquidity sweep + immediate rejection; layered liquidity rule; YAML block (Vol 1 Cls 4)
- [[concepts/entry-models/london-model]] — London takes Asia side, delivers to other; SMT at sweep; 1–3x/week; YAML block (Vol 1 Cls 2, Vol 2 Cls 2)
- [[concepts/entry-models/model-2022-ote]] — MSS + deep OTE retracement (62–79%); CSD pre-MSS signal; propulsion block selection; YAML block (Vol 3 Cls 5)
- [[concepts/entry-models/daily-bias-model]] — HTF FVG + opening price prerequisite filter; integrates with all other models; YAML block (Vol 2 Cls 4)
- [[concepts/entry-models/smt-confirmation-entry]] — NQ/ES/YM divergence at manipulation leg; Price SMT + PDR SMT; trust-the-program; YAML block (Vol 4 Cls 2)

### Patterns

_None yet._

---

## Processes

### Distributed Workflow

- [[processes/distributed-workflow/active/kickoff]] — kickoff workstream tracker (complete — wiki bootstrapped, transcripts ingested, KB populated).
- [[processes/distributed-workflow/active/course-and-kb]] — ICT course construction + entry models library with machine-readable YAML strategy blocks (do first).
- [[processes/distributed-workflow/active/ai-coach]] — AI trading coach module: Claude + TradingView integration, live strategy evaluation (depends on course-and-kb).
- [[processes/distributed-workflow/active/journal-analytics]] — trade journal + analytics module: ICT-specific trade schema, dashboard (parallel to ai-coach).
- [[processes/distributed-workflow/active/deployment]] — Render (backend) + Cloudflare Pages (frontend) + Discord OAuth + TradingView webhook deployment. Phase 4 complete 2026-04-26. R2 screenshots remaining.
- [[processes/distributed-workflow/active/journaling-ux]] — Trade form tab redesign + field reduction + R2 wiring. Phases 1 & 2 complete.
- [[processes/distributed-workflow/active/broker-integration]] — Tradovate REST integration, broker credentials, active-trade soft singleton, `/settings/broker`. Phase 1 spec approved 2026-04-26.
- [[processes/distributed-workflow/active/monorepo-migration]] — consolidated `neurospect-wiki` + `neurospect-api` + `neurospect-app` into one `neurospect` monorepo (2026-05-02). Phases 0 + 1a-1c complete; Phase 2 cleanup ongoing; pending: Render + Cloudflare dashboard reconfig, prod E2E verify, archive old repos.

Pattern docs are in the ALDC wiki and consumed by absolute path:

- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\README.md`
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\session-lifecycle.md`
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\tracker-template.md`

### Operations

_None yet._

---

## Tickets

_None yet._

---

## Sources

### Transcripts (Vol 1)
- `sources/neurospect/2026-04-18-vol1-class1-pt1-liquidity-and-inefficiency.md` — video transcript
- `sources/neurospect/2026-04-18-vol1-class1-pt2-liquidity-and-inefficiency.md` — video transcript
- `sources/neurospect/2026-04-18-vol1-class1-notes.md` — PDF notes
- `sources/neurospect/2026-04-18-vol1-class2-consolidation-model.md` — video transcript
- `sources/neurospect/2026-04-18-vol1-class2-notes.md` — PDF notes
- `sources/neurospect/2026-04-18-vol1-class3-expansion-and-retracement-model.md` — video transcript
- `sources/neurospect/2026-04-18-vol1-class3-notes.md` — PDF notes
- `sources/neurospect/2026-04-18-vol1-class4-notes.md` — PDF notes (no video)

### Transcripts (Vol 2)
- `sources/neurospect/2026-04-18-vol2-class1-power-of-three.md` — video transcript
- `sources/neurospect/2026-04-18-vol2-class1-notes.md` — PDF notes
- `sources/neurospect/2026-04-18-vol2-class2-notes.md` — PDF notes (no video)
- `sources/neurospect/2026-04-18-vol2-class3-measuring-manipulation-deviations.md` — video transcript
- `sources/neurospect/2026-04-18-vol2-class3-notes.md` — PDF notes
- `sources/neurospect/2026-04-18-vol2-class4-daily-bias-practice.md` — video transcript
- `sources/neurospect/2026-04-18-vol2-class4-notes.md` — PDF notes

### Transcripts (Vol 3)
- `sources/neurospect/2026-04-18-vol3-class2-market-structure-fractality.md` — video transcript
- `sources/neurospect/2026-04-18-vol3-class4-market-structure-deviations.md` — video transcript
- `sources/neurospect/2026-04-18-vol3-class5-model-2022-ote-csd.md` — video transcript

### Transcripts (Vol 4)
- `sources/neurospect/2026-04-18-vol4-class1-htf-ltf-orderflow.md` — video transcript
- `sources/neurospect/2026-04-18-vol4-class2-smt-divergence.md` — video transcript

### Stream Transcripts (2026-04-20)
- `sources/neurospect/2026-04-20-stream-0830-mid-mon-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-0830-nfp-fri-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-0830-uc-fomc-wed-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-0830-uc-thu-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-1000-ism-pmi-1300-fed-speaks.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-1000-jolts-tue-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-fri-10-mid-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-no-news-mon-tape-reading.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-tapx-tape-reading-live-nq.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-thu-tape-reading-live-nq.md` — stream transcript
- `sources/neurospect/2026-04-20-stream-tue-10-fed-chair-testifies.md` — stream transcript

### YouTube Transcripts (2026-04-22)
- `sources/neurospect/2026-04-22-youtube-1000-points-nq-2026-03-04.md` — YouTube weekly review (+1000 pts NQ, March 4 2026)
- `sources/neurospect/2026-04-22-youtube-first-week-march-2026-03-07.md` — YouTube weekly review (first week of March, March 7 2026)

---

## Vault

Credentials live in `vault/credentials.md` (gitignored — see `.gitignore:vault/`). Never commit values here in `index.md` or any other tracked file. See [[CLAUDE]] § *Rules* #2.

---

## Daily

Handwritten notes inbox. Copy `daily/_template.md` as `daily/YYYY-MM-DD.md`.

- [[daily/_template]] — note format reference.
- [[daily/2026-04-18]] — bootstrap day.
- [[daily/2026-04-20]] — transcript ingest session checkpoint.
- [[daily/2026-04-22]] — stream + YouTube ingest session checkpoint.
- [[daily/2026-04-24]] — Phase 4 (AI Coach frontend) implemented + verified. Deployment tracker created.
