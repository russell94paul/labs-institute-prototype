---
tags: [decision, architecture, ai]
status: accepted
created: 2026-05-23
updated: 2026-05-23
---

# DEC-002: Labs Intelligence + Wiki — AI-Driven Self-Improvement Layer

## Context

Labs Institute needs more than static management tools. After every gig, event, and campaign, the system should learn — what worked, what didn't, where the gaps are — and feed that back as actionable suggestions for both the founder and individual DJs.

## Decision

Add two interconnected systems on top of the three-tier architecture ([[DEC-001-three-tier-architecture]]):

### Lab-Intelligence (Vector DB)
- Per-project vector memory store (built on zeus-memory patterns)
- Ingests: gig outcomes, event data, social media metrics, campaign results, DJ progress snapshots
- AI-powered analysis: identifies patterns, gaps, and growth opportunities
- Generates: personalised growth roadmaps per DJ, event post-mortems, pricing recommendations
- Improvement suggestions surfaced proactively via the chat interface
- Learns from corrections — when founder/DJ disagrees with a suggestion, that feedback improves future recommendations

### Lab-Wiki (Knowledge Base)
- Structured knowledge base per project (decisions, learnings, patterns, incidents)
- Captures institutional knowledge: what works at which venues, optimal pricing by location, best promotion strategies by genre
- Cross-references with Lab-Intelligence — wiki entries become retrievable context for AI suggestions
- Searchable by founder and DJs — "what worked last time we played The Warehouse?"

### Chat Interface
- Real-time chat between founder and DJs (not replacing WhatsApp — augmenting it with context)
- AI assistant in the chat that can:
  - Answer questions using Lab-Wiki + Lab-Intelligence context
  - Generate growth roadmaps for a specific DJ
  - Suggest improvements after an event
  - Surface relevant past learnings when planning a new event
  - Flag gaps: "DJ X hasn't posted in 3 weeks" or "No recording from last Friday's set"
- Chat history itself feeds into Lab-Intelligence (decisions made in chat become searchable context)

## Data Flow

```
Events/Gigs → Outcomes logged → Lab-Intelligence ingests
                                      ↓
Social metrics → Periodic snapshots → Pattern detection
                                      ↓
                              AI generates suggestions
                                      ↓
                        Chat surfaces to founder/DJ
                                      ↓
                    Feedback loop (accept/reject/modify)
                                      ↓
                          Lab-Intelligence improves
                                      ↓
                      Lab-Wiki captures proven patterns
```

## Consequences

- Lab-Intelligence is the zeus-memory lite store we already built (engine/memory.py), extended with embedding + retrieval
- Lab-Wiki is the per-project wiki system already scaffolded at projects/labs-institute/wiki/
- Chat requires a new dashboard page + API routes for messaging
- AI suggestions need a prompt template system that assembles context from both stores
- Self-improvement loop means every interaction generates data — need to be intentional about what gets stored vs discarded
- Upgrade path: JSON files → postgres/pgvector → full zeus-memory when scale demands it
