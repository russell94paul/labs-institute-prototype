# NeuroSpect Monorepo

Single repository for the NeuroSpect AI trading intelligence platform. Data-foundation-first architecture: verified trading data → risk protection → ICT event detection → backtesting → AI coaching → forensics → scoring → rewards → advanced ML.

## Product Hierarchy

```
NeuroSpect (company / product brand)
├── Trader Workspace         — Journal, analytics, behavior metrics, trader profile
├── Prop Shield              — Prop firm rule tracking, tilt lockouts, Tradovate protection
├── ICT Event Engine         — Programmable ICT market event detection primitives
├── EdgeLab                  — Event-driven backtesting, feature engineering, experiments
├── NeuroSpect Mentor        — AI coaching, RAG citations, structured trade review
├── Edge Forensics           — Loss pattern mining → testable hypothesis generation
├── NeuroCore                — Knowledge/retrieval layer (hybrid 3-signal search)
├── NSLM                     — NeuroSpect Language Model (ICT-aware model family)
├── NeuroGraph               — Persistent trading intelligence graph (compounds with every interaction)
├── NeuroScore               — Risk-adjusted trader ranking and verification
├── NeuroFund Elite          — Company-sponsored rewards/eligibility (NOT pooled capital)
├── NeuroQuant               — Production model layer (promoted from EdgeLab)
└── NeuroTrader Agent        — Automated trading agent (shadow → paper → live)
```

| Component | Description |
|---|---|
| **NeuroSpect** | Company and product brand. AI trading intelligence platform for traders and educators. |
| **Trader Workspace** | Core trading data, journal, analytics, behavior metrics (tilt, discipline, consistency), trader profile. The daily-use engagement layer. |
| **Prop Shield** | Prop firm rule tracking, trailing drawdown monitoring, tilt lockouts, daily loss limits, Tradovate protection. The first paid feature wedge. |
| **ICT Event Engine** | Programmable ICT market event detection. FVGs, sweeps, order blocks, market structure, sessions as queryable events. Foundation for backtesting and forensics. |
| **EdgeLab** | Event-driven backtesting, quant feature engineering, strategy compilation from YAML, Monte Carlo, walk-forward optimization, experiment registry. |
| **NeuroSpect Mentor** | AI coaching with RAG citations, structured trade review (setup/execution/risk/psychology/rules/improvement), grounded in wiki content and user trade data. |
| **Edge Forensics** | Loss pattern mining, mistake taxonomy, hypothesis generation. Turns repeated losses into testable improvement hypotheses connected to EdgeLab backtests. |
| **NeuroCore** | Knowledge/retrieval layer. Hybrid 3-signal search (keyword + semantic + entity) across wiki, transcripts, playbooks, trade journal. Powers coaching RAG and agent reasoning. |
| **NSLM** | NeuroSpect Language Model. ICT-aware LLM/model family. Prompt-versioned, model-versioned, evaluated through EdgeLab. Produces setup classifications and features. |
| **NeuroGraph** | Persistent trading intelligence graph. Nodes = trades, events, features, setups, patterns, concepts. Edges = relationships. Seeded with wiki corpus + ICT models on build, compounds with every trade/coaching/experiment. Temporal/regime-aware with confidence decay and reinforcement. Queried by all components. The compounding moat. |
| **NeuroScore** | Risk-adjusted trader ranking. Considers performance, drawdown discipline, rule adherence, consistency, tilt control, execution quality. Broker-verified trades only. |
| **NeuroFund Elite** | Company-sponsored rewards and eligibility program funded from NeuroSpect revenue. Premium opt-in. NOT pooled user capital, NOT an investment vehicle. |
| **NeuroQuant** | Production model layer. Consumes validated features and models promoted from EdgeLab. Regime-aware scoring, model ensembles, confluence decisions. |
| **NeuroTrader Agent** | Automated trading agent. Shadow → Paper → Live progression. 5-layer safety architecture. Gated by EdgeLab null test and NeuroQuant scoring. |

## Directory Structure

### Core Product
- `wiki/` — ICT knowledge base, architecture, transcripts, course content. Source of truth for team knowledge. **Read `wiki/CLAUDE.md` first.**
- `api/` — FastAPI backend. Read `api/CLAUDE.md`.
- `app/` — React 19 + TS frontend. Read `app/CLAUDE.md`.

### Roadmap & Research
- `roadmap/` — **Single source of truth for project state.** Phase definitions, boot prompts, deviations, status dashboard, and the master plan. Read `roadmap/CLAUDE.md`.
- `prompts/` — Engineering, product, and meta-prompts used to build and operate NeuroSpect. Organized by phase and ad-hoc. Graduates to a versioning module in Phase 4. Read `prompts/CLAUDE.md`.
- `research/` — Engineering research artifacts (benchmarks, evaluations, prototype findings). Organized by phase. NOT product content — that goes in `wiki/`. Read `research/README.md`.
- `initial-plan/` — Historical archive of original plan versions (read-only).

### Marketing & Demo
- `neurospect-ui/` — React 18 interactive marketing site. Primary marketing codebase (replaces `site/`). No build step — CDN-loaded React + Babel.
- `site/` — **Deprecated.** Original Astro SSG marketing site. Being replaced by `neurospect-ui/`.
- `design-handoff/` — Design specification documents for marketing site pages and components.
- `docs/` — Product documentation (product overview & user guide).
- `prompts/` — Prompt library for external LLM tools (ChatGPT design prompts, etc.).

### Personal Wikis (Obsidian Vaults)
- `vlad-wiki/` — Vlad's personal working wiki.
- `paul-wiki/` — Paul's personal working wiki.

Both personal wikis share identical structure:

```
{vlad,paul}-wiki/
├── research/            # Research notes (any domain)
├── decisions/           # Decision records (DEC-NNN-short-title.md)
├── journal/             # Daily/weekly working notes (YYYY-MM-DD.md)
├── components/          # Per-component working docs
├── phases/              # Personal view of roadmap phases
│   ├── README.md        # Phase index with synced status (who's working on what)
│   ├── phase-0-research/
│   │   ├── README.md    # Personal status + notes (references roadmap/ for canonical def)
│   │   └── tickets/     # One subfolder per Linear ticket
│   │       └── NEU-042-rag-retrieval-pipeline/
│   │           ├── README.md      # Ticket implementation notes, blockers, decisions
│   │           └── boot-prompt.md # Ticket-specific boot prompt (optional, for complex tickets)
│   ├── phase-1-rag-mvp/
│   └── ...
└── scratch/             # Temporary notes (gitignored)
```

They are **personal working memory** — drafts, research-in-progress, daily notes. Mature content gets promoted to `wiki/` via `promote: true` frontmatter tag.

## Roadmap Phases (v3)

| Phase | Name | Component | Revenue Event |
|---|---|---|---|
| 0 | Marketing + Demo | — | Waitlist |
| 1 | Trading Data Foundation | Trader Workspace | — |
| 2 | Trader Workspace | Trader Workspace | — |
| 3 | Prop Shield | Prop Shield | **FIRST REVENUE** (Mentor $29 / Trader $99) |
| 4 | ICT Event Intelligence | ICT Event Engine | — |
| 5 | EdgeLab Core (5A/5B/5C) | EdgeLab | Research $199 |
| 6 | AI Trade Review + RAG | Mentor + NeuroCore | Mentor upsell |
| 7 | Edge Forensics | Edge Forensics | Research retention |
| 8 | NeuroScore + Leaderboard | NeuroScore | Quant $349 |
| 9 | NeuroFund Elite Rewards | NeuroFund Elite | Elite retention |
| 10 | Allocation Watchlist | NeuroFund Elite | — |
| 11 | Advanced ML Research (11A/11B/11C) | NSLM + NeuroQuant + NeuroTrader | Quant/Team $499 |
| 3-NG | NeuroGraph (Plan → Build) | NeuroGraph | Retention (all tiers) |

**Build order:** `verified data → risk engine → events → backtesting → AI review → forensics → scoring → rewards → ML`

Compliance/business deliverables are embedded per-phase (no separate Track C). Each phase's `/ns-phaseN` slash command includes its compliance constraints.

### Where Phase Information Lives

| Content | Location | Maintained By |
|---|---|---|
| Phase definition (goals, scope, exit criteria) | `roadmap/phases/phase-N/README.md` | Manual + `/sync` |
| Planning boot prompt | `roadmap/phases/phase-N/boot-prompts/planning.md` | `/sync` (generated) |
| Execution boot prompt | `roadmap/phases/phase-N/boot-prompts/execution.md` | `/sync` (generated) |
| Deviations from plan | `roadmap/phases/phase-N/deviations.md` | Manual + `/sync` |
| Status dashboard | `roadmap/status.md` | `/sync` (generated) |
| Personal ticket notes | `{vlad,paul}-wiki/phases/phase-N/tickets/NEU-NNN-title/` | Manual |
| Ticket-specific boot prompt | `{vlad,paul}-wiki/phases/phase-N/tickets/NEU-NNN-title/boot-prompt.md` | Optional, manual or `/sync` |
| Personal phase status view | `{vlad,paul}-wiki/phases/phase-N/README.md` | `/sync` (synced from roadmap + Linear) |

### Ticket Subfolder Convention

Each Linear ticket gets a subfolder (not a flat file) in the personal wiki:

```
tickets/NEU-042-rag-retrieval-pipeline/
├── README.md        # Implementation notes, decisions, blockers
└── boot-prompt.md   # Ticket-specific boot prompt (for complex multi-session tickets)
```

Ticket README frontmatter:

```yaml
---
linear_id: NEU-NNN
title: Short title
status: backlog | in_progress | review | done
assignee: vlad | paul
priority: P0 | P1 | P2 | P3
phase: N
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Ticket-specific boot prompts are optional — only create them for complex tickets that span multiple sessions and need persistent implementation context.

## Wiki Conventions

All three wikis (`wiki/`, `vlad-wiki/`, `paul-wiki/`) follow the same conventions:
- YAML frontmatter on every page: `tags`, `created`, `updated`
- `[[wikilinks]]` for internal cross-references within the same wiki
- Absolute paths for cross-wiki references
- One page per entity/concept — update existing rather than duplicate
- `corpus_type` frontmatter field on `wiki/` pages: `training` (for LLM/RAG), `development` (for engineers), or `both`

### Promotion Workflow (personal → team wiki)
1. When a personal wiki page is ready to become team knowledge, add `promote: true` to its frontmatter
2. A lint/skill catches promoted pages and suggests moving them to `wiki/`
3. After promotion, the personal wiki page becomes a stub linking to the canonical `wiki/` page

## NeuroCore — Knowledge Layer

NeuroCore is the hybrid retrieval/intelligence layer that indexes all knowledge sources:

| Source | Indexed For |
|---|---|
| `wiki/` (training content) | RAG coaching, fine-tuning dataset generation |
| `wiki/` (dev docs) | Engineer reference, project context |
| `paul-wiki/`, `vlad-wiki/` | Cross-engineer intelligence |
| `initial-plan/` | Project context |
| Trade journal (PostgreSQL) | Personalized coaching |
| EdgeLab experiments (PostgreSQL) | Strategy evaluation, NSLM evaluation |
| Market data context | Real-time coaching enrichment |
| Agent signals (PostgreSQL) | Agent self-improvement |

Search uses 3 signals fused via Reciprocal Rank Fusion:
1. **Keyword/BM25** (tsvector) — catches exact ICT jargon
2. **Semantic** (pgvector embeddings) — catches conceptual similarity
3. **Entity/Tag** — catches instrument, session, strategy references

Cross-wiki intelligence: when an engineer is working on a component, NeuroCore can surface relevant content from the other engineer's wiki or the team wiki.

## Architecture Patterns

Several patterns proven in production elsewhere should be replicated independently. See `initial-plan/v1-neurollm-plan.md` § *Patterns to Replicate from Zeus Memory* for the full mapping.

## Skills (Slash Commands)

### Workflow Skills

Runtime skills that generate context from live state. Located in `.claude/skills/`.

| Skill | Purpose |
|---|---|
| `/phase N [plan\|exec]` | Load Phase N boot prompt. Generated from roadmap definition + upstream deviations + Linear tickets + git state + cross-wiki content. Default mode is `exec`. Use `/phase status` to see all phases. |
| `/sync` | End-of-session sync. Updates Linear tickets, regenerates boot prompts, captures deviations, flags cross-wiki content, suggests which `/phase` to run next. **Must be offered before every session ends.** |
| `/lint` | Cross-artifact consistency check. Detects drift between CLAUDE.md files, roadmap phases, status dashboard, plan.md, skill mappings, and product naming. **Must be offered before every session ends.** |
| `/crossref [query]` | Search across all wikis for content relevant to current work or a specific topic. Surfaces notes from the other engineer, canonical wiki definitions, and roadmap deviations. |

### Phase Execution Commands

Static implementation guides for each phase. Located in `.claude/commands/`. Run these when starting implementation work on a phase.

| Command | Phase |
|---|---|
| `/ns-phase0` | Marketing + Demo (0A/0B sub-phases) |
| `/ns-phase1` | Trading Data Foundation |
| `/ns-phase2` | Trader Workspace (Journal + Analytics + Behavior Metrics) |
| `/ns-phase3` | Prop Shield (Prop Risk + Tradovate Protection) — **FIRST REVENUE** |
| `/ns-phase4` | ICT Event Intelligence |
| `/ns-phase5a` | EdgeLab Core — Engine + Data Pipeline |
| `/ns-phase5b` | EdgeLab Core — Detectors + Stats + Features |
| `/ns-phase5c` | EdgeLab Core — Dashboard + Null Test |
| `/ns-phase6` | AI Trade Review + RAG (NeuroCore + Mentor) |
| `/ns-phase7` | Edge Forensics |
| `/ns-phase8` | NeuroScore + Verified Leaderboard |
| `/ns-phase9` | NeuroFund Elite Rewards MVP (compliance-critical) |
| `/ns-phase10` | Allocation Watchlist Pipeline |
| `/ns-phase11` | Advanced ML Research (NSLM + NeuroQuant + NeuroTrader) |
| `/ns-phase3-neurograph` | NeuroGraph Planning (Data Sources + Schema Design) |

**Workflow:** Run `/phase N exec` first (for live context), then `/ns-phaseN` (for implementation guide).

### How Boot Prompts Work

Boot prompts are **generated by skills at runtime**, not hand-written. The `/phase` skill assembles context from:
- Phase definition (`roadmap/phases/phase-N/README.md`)
- All upstream deviations (`roadmap/phases/phase-{0..N-1}/deviations.md`)
- Current phase deviations
- Active Linear tickets (if connected)
- Recent git activity
- Cross-wiki content from the other engineer

When a phase's implementation deviates from the plan, `/sync` captures it in `deviations.md`. The next phase's `/phase` call automatically incorporates those deviations. No manual boot prompt maintenance needed.

Cached copies are written to `roadmap/phases/phase-N/boot-prompts/` so they're browsable in Obsidian, but the skills always regenerate from live state.

### End-of-Session Behavior

**Before ending any session that modifies code, wiki, or tickets, offer to run both `/sync` and `/lint`.** This is mandatory.

```
Before ending this session:
1. /sync  — Update tickets, boot prompts, and phase status from this session's work
2. /lint  — Check that all roadmap artifacts are consistent
```

**Why both?** As you work, you add ideas, rename components, and reorganize phases. These changes touch `CLAUDE.md`, `status.md`, phase READMEs, and skill definitions — but not always all of them at once. `/sync` captures *what you did this session*. `/lint` catches *drift between artifacts* that accumulated while you worked. Running both ensures the next session inherits clean, consistent context.

`/sync` will:
1. Sync Linear ticket status against git
2. Regenerate boot prompts for active phases
3. Update `roadmap/status.md`
4. Capture any deviations from this session
5. Check per-phase compliance gates
6. Flag cross-wiki content
7. Suggest which `/phase` to run next

`/lint` will:
1. Verify phase tables match across all CLAUDE.md files and status.md
2. Check phase directories are complete (README, deviations, boot-prompts)
3. Detect product/component naming drift across documents
4. Validate frontmatter on all phase READMEs
5. Verify per-phase compliance gates are documented
6. Check file references and wikilinks resolve
7. Flag stale artifacts that may need updating

## NeuroFusion-13 (SIHRE) — Advanced Quant Architecture

NeuroSpect's advanced tier is powered by NeuroFusion-13, a Self-Improving Heterogeneous Reasoning Ensemble (SIHRE) — a 13-signal quant architecture that fuses heterogeneous reasoning modalities (statistical, semantic, causal, adversarial, generative, self-supervised, evolutionary, meta-learned) at the reasoning level.

The AI coach (Mentor) is a **separate feature** — it does NOT use the NeuroFusion model. NeuroFusion powers systematic signal generation, strategy discovery, and automated decision-making for advanced-tier subscribers only.

### Research Reports

Deep research reports are at `research/neurofusion/data/` (7 ChatGPT Pro + 1 Gemini). Architecture overview at `research/neurofusion/README.md`. Technical spec at `research/neurofusion/architecture/signal-fusion-design.md` (when created).

### Deep Research Flagging

**When implementing any phase, proactively identify components that could benefit from deeper research.** If a technique, algorithm, or architecture decision could be significantly improved by exploring academic papers, alternative approaches, or cutting-edge methods, flag it inline:

`🔬 Deep research opportunity: <description of what could be researched and why>`

Accumulate these as you work. At session end, present them to Paul as potential ChatGPT Deep Research prompts. Focus on areas where:
- The current approach is "good enough" but a researched approach could be 10x better
- There are known academic papers or techniques that could apply but haven't been explored
- A design decision has multiple viable paths and research could identify the optimal one
- The implementation touches a NeuroFusion-13 signal and the research reports suggest specific techniques

Do NOT flag trivial optimizations or well-understood patterns. Flag only where deep research would meaningfully change the implementation approach.

### SIHRE External Wiki (Obsidian Vault)

The SIHRE framework has a dedicated Obsidian vault at `C:\Users\PaulRussell\Documents\SIHRE-Framework\` that serves as the master knowledge base for the NeuroFusion-13 architecture — separate from the Neurospect project wiki because SIHRE is a framework-level concept that may apply beyond NeuroSpect.

**Whenever working on anything related to SIHRE / NeuroFusion-13, proactively update this wiki:**

1. **New findings** — any discovery, technique, paper, insight, or implementation decision related to the 13 signals, fusion architecture, or meta-orchestrator gets written to the appropriate folder
2. **Create folders as needed** — organize by topic. If a finding doesn't fit an existing folder, create one. Keep the structure clean and navigable.
3. **Restructure when necessary** — if the wiki grows disorganized, proactively reorganize folders and files. Move content to better locations, split large files, merge related small files.

**Vault structure:**
```
SIHRE-Framework/                              # Obsidian vault root
├── INDEX.md                                  # Master navigation — update when adding content
├── SIHRE Framework/                          # Core framework definition
│   ├── Overview/                             # What is SIHRE, positioning, differentiators
│   ├── Signals/                              # Per-signal deep dives
│   │   ├── Signal-01-VectorDB/
│   │   ├── Signal-02-DSLM/
│   │   ├── ...through Signal-13-Meta-Orchestrator/
│   ├── Architecture/                         # System architecture, data flow, interfaces
│   ├── Fusion/                               # Reasoning-level fusion techniques (RRF, HMoE, attention)
│   ├── Governance/                           # Trust, audit, explainability, compliance
│   ├── Research Reports/                     # Deep research outputs (prompts 1-7 + Gemini)
│   └── Whitepapers/                          # Public whitepaper, publication memo
├── Walkthrough/                              # In-depth educational guide (10 chapters)
│   ├── 01-What-Is-SIHRE/ through 10-Advanced-Topics/
├── Implementation Guide/                     # Practical engineering guide
│   ├── Getting Started/
│   ├── Build Order/
│   ├── Domain Adaptations/                   # Per-domain: Trading, Robotics, Cyber, Healthcare
│   ├── Patterns and Recipes/
│   ├── Anti-Patterns/
│   └── Evaluation and Benchmarking/
├── Publication/                              # Authorship and public presence
│   ├── Whitepaper/ Academic/ Blog Posts/ Talks/ Brand/
├── Monetization/                             # Revenue streams and business model
│   ├── Licensing/ SDK/ Certification/ Consulting/ Education/ Paid Research/
├── Papers/                                   # Academic papers, competitive landscape, prior art
├── Legal and IP/                             # Patents, trademark, licensing templates
└── Roadmap/                                  # Framework development roadmap
```

Create new folders as needed when content doesn't fit existing structure. Update `INDEX.md` when adding new sections.

**What to write:**
- New techniques discovered during implementation that enhance a signal
- Design decisions and their rationale (why approach A over B)
- Academic papers found during implementation (title, key finding, how it applies)
- Performance benchmarks, evaluation results, comparisons
- Failure modes discovered (what didn't work and why)
- Cross-signal interactions discovered (Signal X improves when combined with Signal Y)
- Implementation gotchas specific to the trading domain

**Format:** Use Obsidian-compatible markdown with `[[wikilinks]]` for cross-references within the vault. YAML frontmatter with `tags`, `created`, `updated` fields.

## Cross-Cutting Rules

- Cross-cutting changes (touching `wiki/` + `api/` + `app/`) ride in a single PR
- See `wiki/CLAUDE.md` § *Architecture Doc Integrity* for the reconciliation rule
- When in doubt, start in `wiki/` — it's the index and source of truth
- **Always offer `/sync` + `/lint` before ending a session**

## History

This repo was created on 2026-05-02 by merging three predecessor repos via `git filter-repo --to-subdirectory-filter`:

- `neurospect-wiki` → `wiki/`
- `neurospect-api` → `api/`
- `neurospect-app` → `app/`

The predecessor repos are archived on GitHub. Their pre-merge tips are tagged `pre-monorepo-snapshot` for reference.
