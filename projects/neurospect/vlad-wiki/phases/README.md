---
tags: [phases, roadmap, index]
created: 2026-05-09
updated: 2026-05-09
---

# Roadmap Phases — Vlad's View

_Phase status synced from `roadmap/status.md` by `/sync`._

| Phase | Name | Status | Vlad | Paul |
|---|---|---|---|---|
| 0 | Research & Validation | in_progress | — | marketing site + NEU-27 |
| 1 | Knowledge Base & RAG MVP | not_started | — | — |
| 2 | Market Context & Trade Integration | not_started | — | — |
| 3 | Product MVP | not_started | — | — |
| 4 | Evaluation, Reliability & Prompt Infrastructure | not_started | — | — |
| 5 | Private Beta | not_started | — | — |
| 6 | V1 Launch | not_started | — | — |
| 7 | NeuroSpect EdgeLab Foundation | not_started | — | — |
| 8 | Hybrid Model Research + NeuroQuant Promotion | not_started | — | — |
| 9 | NeuroTrader Agent | not_started | — | — |
| 10 | Advanced Features | not_started | — | — |

### Track C: Business & Operations

| Phase | Name | Status | Vlad | Paul |
|---|---|---|---|---|
| 11 | Content Licensing & IP Strategy | not_started | — | — |
| 12 | Regulatory & Compliance Framework | not_started | — | — |
| 13 | Go-to-Market & User Acquisition | not_started | — | — |
| 14 | Retention, Analytics & Coaching Quality | not_started | — | — |
| 15 | Competitive Intelligence & Moat Strategy | not_started | — | — |
| 16 | Team Scaling & Org Design | not_started | — | — |

## Ticket Convention

Each ticket lives in `phases/phase-N-name/tickets/NEU-NNN-short-title/`:

```
tickets/
└── NEU-042-rag-retrieval-pipeline/
    ├── README.md        # Ticket details, implementation notes, blockers
    └── boot-prompt.md   # Ticket-specific boot prompt (optional, for complex tickets)
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

_Ticket status synced from Linear by `/sync`._
