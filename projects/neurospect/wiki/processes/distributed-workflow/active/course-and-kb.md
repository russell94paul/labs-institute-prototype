---
tags: [distributed-workflow, active, neurospect, course, entry-models]
aliases: [Course Construction Tracker, Entry Models Library Tracker]
sources: []
created: 2026-04-22
updated: 2026-04-22
---

# Course Construction & Entry Models Library — Workstream Tracker

Two tightly related workstreams: (1) build a structured, learner-facing ICT course from the ingested KB, and (2) build a per-strategy entry models library with machine-readable checklists. The entry models library is a prerequisite for the AI coach module (see `ai-coach.md` tracker).

## Goal

By end of this workstream:

1. **Structured ICT Course** — `concepts/course/` directory with module and lesson pages organized for progressive learning (foundations → session context → market structure → order flow). Each lesson has: concept explanation, worked examples extracted from transcripts, homework extracted from class assignments.

2. **Entry Models Library** — `concepts/entry-models/` directory with one page per strategy. Each page has: human-readable explanation, setup conditions, step-by-step checklist, timeframe requirements, stop/target logic, and a machine-readable YAML block at the bottom (used by the AI coach).

3. **Updated `index.md` and `log.md`** in this wiki reflecting the above.

## Lane

Wiki: Neurospect (`C:\Users\PaulRussell\repos\neurospect-wiki\`)

Owned paths (write here):
- `concepts/course/` (new directory + lesson pages)
- `concepts/entry-models/` (new directory + strategy pages)
- `index.md`, `log.md` (this wiki's shared files only)

## Course Structure (Proposed)

```
concepts/course/
├── README.md              # Course overview, learning path
├── module-1-foundations/
│   ├── 01-what-moves-the-market.md      # Liquidity & Inefficiency (Vol 1 Cls 1)
│   ├── 02-fair-value-gaps.md            # FVG mechanics, BISI/SIBI (Vol 1 Cls 1)
│   └── 03-homework-and-practice.md     # Extracted homework assignments
├── module-2-price-delivery/
│   ├── 01-four-stages-apd.md            # Consolidation/Expansion/Retracement/Reversal (Vol 1 Cls 2-4)
│   ├── 02-consolidation-model.md        # Entry model + examples (Vol 1 Cls 2)
│   ├── 03-expansion-retracement.md      # E&R model + examples (Vol 1 Cls 3)
│   └── 04-reversals.md                  # 3 reversal types (Vol 1 Cls 4 notes)
├── module-3-session-and-bias/
│   ├── 01-power-of-three.md             # AMD framework (Vol 2 Cls 1)
│   ├── 02-session-kill-zones.md         # Sessions, opening prices (Vol 2 Cls 2 notes)
│   ├── 03-deviations.md                 # Fibonacci targeting (Vol 2 Cls 3)
│   └── 04-daily-bias.md                 # HTF FVG + opening price bias (Vol 2 Cls 4)
├── module-4-market-structure/
│   ├── 01-swing-classification.md       # STH/ITH/LTH, STL/ITL/LTL (Vol 3 Cls 2)
│   ├── 02-fractality.md                 # Same pattern at all timeframes (Vol 3 Cls 2)
│   ├── 03-structure-deviations.md       # Two-set deviation targeting (Vol 3 Cls 4)
│   └── 04-model-2022-ote-csd.md         # Model 2022, OTE, CSD (Vol 3 Cls 5)
└── module-5-order-flow-and-smt/
    ├── 01-htf-ltf-order-flow.md         # Quadrant levels, closing basis (Vol 4 Cls 1)
    └── 02-smt-divergence.md             # Triad, cracking correlation (Vol 4 Cls 2)
```

## Entry Models Library (Proposed)

```
concepts/entry-models/
├── README.md                            # Library overview, how to use checklists
├── consolidation-model.md              # Consolidation range + EQ entry
├── expansion-retracement-model.md      # E&R with FVG at discount
├── reversal-raid-on-stops.md           # Raid on stops (80% reversal)
├── london-model.md                     # London takes Asia side, delivers to other
├── model-2022-ote.md                   # MSS + deep OTE retracement
├── daily-bias-model.md                 # HTF FVG + below/above opening price
└── smt-confirmation-entry.md           # SMT divergence + PDA entry
```

Each file ends with a YAML block:
```yaml
# --- MACHINE_READABLE_STRATEGY ---
strategy_id: consolidation-model
conditions:
  - Consolidation range identified on 1M-5M
  - Price sweeps intra-range liquidity (swing low taken)
  - Price returns to EQ (50%)
  - PDA (FVG/OB/rejection-block) present below EQ
  - Kill zone active
checklist:
  - [ ] HTF FVG bias confirmed (1H-4H-Daily)
  - [ ] Opening price position correct (below open for longs)
  - [ ] Consolidation range bodies defined (not wicks)
  - [ ] EQ (50%) identified
  - [ ] Intra-range liquidity swept
  - [ ] PDA at or below EQ
  - [ ] Kill zone active
timeframes:
  bias: [1H, 4H, Daily]
  entry: [1M, 5M]
stop_logic: Below the PDA (FVG low or OB body low)
target_logic: Opposite side of range, then previous day high/low
```

## Prerequisites

Before starting this workstream, run the **stream/YouTube ingest session** (boot prompt in `kickoff.md`). The stream transcripts contain live worked examples and real pre-market commentary that should be embedded in course lessons. Without them the course will lack applied, real-world context.

## Plan

### Phase A — Course Construction
1. Create `concepts/course/README.md` with learning path overview
2. Write one lesson page per topic (map from existing KB pages → course format)
3. Extract homework assignments from transcripts → `03-homework-and-practice.md` per module
4. Extract worked examples (trade reviews) from transcripts → embed in lesson pages

### Phase B — Entry Models Library
1. Create `concepts/entry-models/README.md`
2. Write one page per strategy (7 strategies listed above)
3. Each page: human explanation + conditions + checklist + YAML machine-readable block
4. Cross-reference with course lesson pages

## Session Log

### 2026-04-22 — planning

- did: created this tracker; defined course structure and entry models library structure; boot prompt written below.
- decided: entry models library will use YAML machine-readable blocks embedded in markdown — this is the format the AI coach will consume.
- next: open a fresh session using the boot prompt below; start with Module 1 course pages and the consolidation model entry page.

### 2026-04-22 — course-and-kb session 1

- did:
  - Created `concepts/course/README.md` — full learning path, 5-module overview, prerequisite order, volume-to-module map
  - Created `concepts/course/module-1-foundations/01-what-moves-the-market.md` — Lesson 1 covering BSL/SSL/DOL, swing high/low mechanics, FVG displacement, BISI/SIBI, worked example from AXL's Class 1 live trade walk-through, homework assignment verbatim
  - Created `concepts/course/module-1-foundations/02-fair-value-gaps.md` — Lesson 2 covering FVG precision entry (CE/50%, candle 3 entry), IOFED, BAG, inversion FVG, volume imbalance, multiple FVG rules; worked examples from MrWitness Class 2 live NQ + AXL Class 1 Part 2
  - Created `concepts/course/module-1-foundations/03-homework-and-practice.md` — both homework assignments extracted verbatim from transcripts; MrWitness's demonstration back-test example; AXL mindset quotes; Module 1 readiness checklist
  - Created `concepts/entry-models/README.md` — library index, universal minimum confluence (5 conditions), stop/target conventions
  - Created `concepts/entry-models/consolidation-model.md` — full entry model: conditions, step-by-step entry process, stop/target logic, timeframe table, Class 2 worked example (NQ + SMT), common mistakes; YAML machine-readable strategy block at bottom
  - Updated `index.md` with Course and Entry Models sections
  - Updated `log.md` with build operation entry
- decided:
  - Course lesson format: Concept → Rules → Worked Example → Common Mistakes → Homework (one lesson per class's content)
  - Homework assignments are extracted verbatim from transcripts, not paraphrased — preserves instructor intent
  - Readiness checklist added to Module 1 homework page — students check off before advancing
  - YAML strategy block uses fenced code block (``` yaml ```) inside the H1 sentinel comment, consistent with tracker schema
- next:
  - Module 2 course pages: 01-four-stages-apd.md, 02-consolidation-model.md (course-facing), 03-expansion-retracement.md, 04-reversals.md
  - Entry Models: expansion-retracement-model.md, reversal-raid-on-stops.md, london-model.md
  - Then Module 3 and remaining entry models (model-2022-ote, daily-bias, smt-confirmation)

### 2026-04-22 — course-and-kb session 2 (same conversation as session 1)

- did:
  - Created `concepts/course/module-2-price-delivery/01-four-stages-apd.md` — four stages overview: consolidation/expansion/retracement/reversal; real vs. fake retracement; healthy vs. choppy; BPR skip condition; two confirming rules ("if retracement → reversal it wasn't a retracement")
  - Created `concepts/course/module-2-price-delivery/02-consolidation-model.md` — course-facing page: range identification using bodies, the two delivery paths (clean vs. BPR), AXL sniper entry version, live NQ Class 2 worked example
  - Created `concepts/course/module-2-price-delivery/03-expansion-retracement.md` — expansion measurement, real/fake retracement, healthy/choppy retracement, algorithmic body signature, Class 3 worked examples (February gap, OB+FVG alignment), AXL's BPR+failure swing trade
  - Created `concepts/course/module-2-price-delivery/04-reversals.md` — three types: failure swing (~10%), raid on stops (~80%), accumulation (~10%); layered liquidity rule; reversal vs. retracement decision framework; manual intervention pattern
  - Created `concepts/entry-models/expansion-retracement-model.md` — full entry model + YAML strategy block
  - Created `concepts/entry-models/reversal-raid-on-stops.md` — full entry model + YAML strategy block; partial_exit_rule for type 1 false positives
  - Created `concepts/entry-models/london-model.md` — full entry model + YAML strategy block; frequency/timing notes; avoid conditions
  - Updated `index.md` — Module 2 course section + 4 new entry model entries
  - Updated `log.md`
- decided:
  - Course page for consolidation in Module 2 focuses on recognition and context (not repeating the entry model details) — cross-references the entry model for the checklist
  - Reversal entry model includes a `partial_exit_rule` field to guide handling of type 1 failure swing false positives
  - London model notes include full avoid_conditions list (Sunday, news weeks, CPI Monday) in YAML
- next:
  - Module 3 course pages: 01-power-of-three.md, 02-session-kill-zones.md, 03-deviations.md, 04-daily-bias.md
  - Entry Models: model-2022-ote.md, daily-bias-model.md, smt-confirmation-entry.md
  - Then Module 4 + Module 5 (if session continues)

### 2026-04-22 — course-and-kb session 3

- did:
  - Created `concepts/course/module-3-session-and-bias/01-power-of-three.md` — AMD framework: daily candle phases, retail vs. SM psychology, four opening prices (midnight/8:30/9:30/1:30), AMD repeating four times per day; worked Asia session trade from AXL Class 1 (external+internal liquidity, FVG, COS, 1:28 R:R); common mistakes; homework (10-day mark + observe routine)
  - Created `concepts/course/module-3-session-and-bias/02-session-kill-zones.md` — five KZ windows with anchors; the two-part NY AM structure (8:30 + 9:30 and their relationship); ORG size → LRLR/HRLR signal; highest-probability triple-open stack; pre-session quick checklist; homework (track which KZ sets HOD/LOD)
  - Created `concepts/course/module-3-session-and-bias/03-deviations.md` — Fibonacci sequence and fractality context; deviation settings table; anchoring rules (manipulation swing → swing high for bullish); HPDL; two worked examples (London bullish LOD through -7 deviation; PM short to -2.5); manual intervention exception; 10-day backtest homework
  - Created `concepts/course/module-3-session-and-bias/04-daily-bias.md` — bias = liquidity → inefficiency → liquidity; Step 1 (4H FVG identification, timeframe hierarchy); Step 2 (opening price position filter); when to stand aside (FVG violated, above all opens on bullish day); live 4H FVG walk-through from Class 4 replay; daily pre-session checklist; ignore small structures rule
  - Created `concepts/entry-models/model-2022-ote.md` — full entry model: MSS + no-50% trigger; HRLR secondary trigger; OTE block selection rules (highest down-close body, propulsion block preference, 0.705 level concert); CSD as pre-MSS entry signal; stop below OTE closing price; deviation targets; full YAML strategy block
  - Created `concepts/entry-models/daily-bias-model.md` — prerequisite filter model (not standalone entry); Step 1 HTF FVG cycle; Step 2 opening price position; stand-aside conditions; integration table linking to all other 6 entry models; full YAML block
  - Created `concepts/entry-models/smt-confirmation-entry.md` — Price SMT vs. PDR SMT; bullish/bearish signal conditions; Context Requirements (pre-existing bias required); trust-the-program framework; contract rollover caution; weakest index by day type; full YAML block with entry priority order (inversion FVG > rejection block > CSD > OTE block)
  - Updated `index.md` — Module 3 course section + 3 new entry model entries
  - Updated `log.md`
- decided:
  - Entry Models Library is now COMPLETE — all 7 models written; library is prerequisite for AI coach module ✓
  - `daily-bias-model` is framed as a `role: prerequisite_filter` (not standalone entry); this distinguishes it clearly in the YAML schema consumed by the AI coach
  - `smt-confirmation-entry` YAML lists entry signals in priority order (inversion FVG first) because that's the most precise; AI coach should prefer higher items in the list
  - Module 3 lesson format consistent with Module 1 and 2: Concept → Rules → Worked Example → Common Mistakes → Homework
- next:
  - Module 4 course pages: 01-swing-classification.md, 02-fractality.md, 03-structure-deviations.md, 04-model-2022-ote-csd.md (sources: vol3-class2, vol3-class4, vol3-class5)
  - Module 5 course pages: 01-htf-ltf-order-flow.md, 02-smt-divergence.md (sources: vol4-class1, vol4-class2)
  - Then: stream/YouTube live commentary integration into Module 5 or a Module 6

### 2026-04-22 — course-and-kb session 4

- did:
  - Created `concepts/course/module-4-market-structure/01-swing-classification.md` — STH/ITH/LTH gap-qualification rule (creates/fills FVG); why STLs are suspect; MSS trigger (break of initiating high); the "measuring swing" STL to the right; daily chart ITL walk-through (+9.41% example from Vol 3 Cls 2)
  - Created `concepts/course/module-4-market-structure/02-fractality.md` — FVG invites liquidity into itself → engineered swing forms inside FVG; turtle soup pattern from that engineered swing; multi-TF nesting table (5s through weekly); HRLR vs. LRLR effect on fractality entries; daily ITL fractal walk-through
  - Created `concepts/course/module-4-market-structure/03-structure-deviations.md` — two-set deviation method: Set 1 (ITL to initiating high) + Set 2 (STL measuring swing to high); convergence zone = precise HOD/LOD; London session worked example (+16 handles per deviation beyond target); holiday liquidity example (-5.5 convergence midpoint)
  - Created `concepts/course/module-4-market-structure/04-model-2022-ote-csd.md` — course-facing Model 2022 page: OTE zone (62-79%); OTE block selection rules (highest open body, propulsion block, 0.705 concert); CSD as pre-MSS signal (opening price of down-close candles breached); full entry sequence from bias → ITL → MSS → OTE → CSD → entry; Vol 3 Cls 5 live example
  - Created `concepts/course/module-5-order-flow-and-smt/01-htf-ltf-order-flow.md` — bodies vs. wicks; closing basis rules (bullish and bearish); quadrant levels (0/0.25/0.50/0.75/1.0) of any dealing range; LRLR vs. HRLR identification and model selection; BPR behavior at equilibrium; LTF order flow at 1M; 5-minute bearish ES session walk-through (OBs at each quadrant level)
  - Created `concepts/course/module-5-order-flow-and-smt/02-smt-divergence.md` — triad and sub-algorithm explanation; cracking correlation definition; Price SMT vs. PDR SMT; bullish and bearish cracking correlation; chart setup (3 methods: new pane, overlaid line, three templates); contract rollover caution; trust-the-program framework after SMT; Six Sisters distinction; bullish and bearish worked examples from Vol 4 Cls 2
  - Updated `index.md` with Module 4 and Module 5 course sections
  - Updated `log.md`
- decided:
  - **Course is now COMPLETE** — all 5 modules (15 lessons) written; all 7 entry models written
  - Module 4 Lesson 4 is the course-facing version of the Model 2022 entry; cross-references the entry model page rather than duplicating the YAML
  - "Six Sisters" is explicitly noted as a distinct concept from SMT in Lesson 5-2, matching the KB page
  - Boot prompt updated to reflect completion; next options are live commentary integration or AI coach workstream
- next:
  - Optional: Module 6 (live commentary integration) from stream/YouTube transcripts
  - Start AI coach workstream (entry models prerequisite now satisfied)
  - Lint pass if desired

## Decisions Log

- 2026-04-22 — Course pages are separate from the KB reference pages (concepts/business-logic/). KB = reference; Course = learning path with progression, homework, and examples. Both exist in parallel.
- 2026-04-22 — Entry models library uses embedded YAML blocks rather than separate JSON files, so human-readable and machine-readable are always in sync.
- 2026-04-22 — 7 entry models in scope for V1 library (consolidation, E&R, raid-on-stops, london, model-2022-OTE, daily-bias, SMT-confirmation). More can be added as new curriculum is ingested.

## Next Session Boot Prompt

```
The ICT Course + Entry Models Library workstream is COMPLETE as of 2026-04-22.

All 5 modules (15 lessons) and all 7 entry models have been written. See the
Session Log in this tracker for the full list of what exists.

If you are starting a new session and the user wants to extend the course, possible
next work includes:

1. **Live Commentary Integration** — a Module 6 or standalone page synthesizing
   stream/YouTube content into the course format: day-of-week protocol, HOD/LOD
   calling, economic calendar framing, speed-and-velocity filter. Source material:
   `sources/neurospect/2026-04-20-stream-*.md` and `sources/neurospect/2026-04-22-youtube-*.md`
   KB reference: `concepts/business-logic/ict-live-commentary.md`

2. **AI Coach workstream** — see `processes/distributed-workflow/active/ai-coach.md`.
   Entry Models Library prerequisite is now satisfied.

3. **Lint pass** — check for orphaned pages, stale index entries, broken wikilinks.

Boot procedure for any of these:
1. Read `C:\Users\PaulRussell\repos\neurospect-wiki\CLAUDE.md`
2. Read this tracker to confirm current state
3. Read `index.md` for full wiki catalog
4. Begin work based on user's direction
```

## See Also

- [[concepts/roadmap/README]] — strategic context (course KB feeds in-app course section + AI coaching)
- [[processes/distributed-workflow/active/ai-coach]] — consumes the entry models YAML
- [[processes/distributed-workflow/active/kickoff]] — previous workstream
- `C:\Users\PaulRussell\repos\wiki\processes\distributed-workflow\orchestration-pattern.md`
