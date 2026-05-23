---
name: ns-phase6
description: NeuroSpect Phase 6 — AI Trade Review + RAG (NeuroCore + Mentor)
---

You are working on **NeuroSpect Phase 6** (AI Trade Review + RAG). This builds NeuroCore (knowledge/retrieval layer) and upgrades NeuroSpect Mentor from one-shot coaching to grounded, multi-turn trade review with citations.

## Boot Procedure

1. Read `C:\Users\PaulRussell\repos\neurospect\CLAUDE.md`
2. Read `C:\Users\PaulRussell\repos\neurospect\api\CLAUDE.md`
3. Read `C:\Users\PaulRussell\repos\neurospect\wiki\CLAUDE.md`
4. Read `C:\Users\PaulRussell\repos\neurospect\api\app\coach\claude_client.py` — existing Claude integration
5. Read `C:\Users\PaulRussell\repos\neurospect\api\app\coach\prompt_loader.py` — system prompt assembly
6. Read `C:\Users\PaulRussell\repos\neurospect\api\app\coach\prompts\system-prompt-template.md` — current system prompt
7. Read `C:\Users\PaulRussell\repos\neurospect\api\app\models\coaching_event.py` — existing coaching model
8. Read Phase 2 behavior metrics service (for trade review context)
9. Read Phase 4 event models (for event context in reviews)

## Goal

Ground AI coaching in methodology docs and actual trade data. Build NeuroCore (hybrid 3-signal retrieval over the wiki corpus) and upgrade Mentor to multi-turn chat with citations, confidence indicators, and structured trade reviews. By now, Phases 1-5 have built a rich data foundation — verified trades, behavior metrics, ICT events, backtest results — making the AI reviews far more useful than a simple RAG-over-docs approach.

## Sub-phases

| Sub-Phase | Scope | Effort |
|---|---|---|
| **6A — NeuroCore** | pgvector, embedding pipeline, hybrid search (BM25 + semantic + entity), chunk ingestion | 3 weeks |
| **6B — Mentor Upgrade** | Multi-turn chat, trade review context injection, Chat API/UI, citations | 3 weeks |

## Deliverables

### 6A — NeuroCore (Knowledge/Retrieval Layer)

1. **pgvector extension** on existing PostgreSQL (Render)
2. **WikiChunk model** — source_file, section, content, embedding (vector 1536), tags, chunk_type, priority, metadata JSONB
3. **Embedding pipeline** (`api/app/coach/rag/embedder.py`):
   - OpenAI text-embedding-3-small (1536 dims)
   - Chunk at `##` headers for KB docs (~300-600 tokens)
   - Keep YAML strategy blocks as single chunks
   - Paragraph splits for transcripts (500 tokens, 100 overlap)
4. **Ingestion pipeline** (`api/app/coach/rag/ingestor.py`):
   - Process `wiki/concepts/business-logic/`, `wiki/concepts/entry-models/`, `wiki/concepts/course/`
   - Tag each chunk with metadata (source_file, section, tags, chunk_type, priority)
   - Idempotent: re-ingest doesn't create duplicates
5. **Hybrid retrieval** (`api/app/coach/rag/retriever.py`):
   - Signal 1: Keyword/BM25 via PostgreSQL tsvector
   - Signal 2: Semantic similarity via pgvector cosine distance
   - Signal 3: Entity/tag matching (ICT concepts, instruments, sessions)
   - Reciprocal Rank Fusion to merge results
   - Top-K retrieval with configurable K (default 5)
6. **ICT terminology normalization** — dictionary of 50+ term mappings (CHoCH/CISD, FVG/imbalance, etc.)

### 6B — Mentor Upgrade

7. **ChatSession model** — user_id, title, created_at, last_message_at, message_count
8. **ChatMessage model** — session_id, role (user/assistant/system), content, citations JSONB, metadata JSONB
9. **Chat API** (`api/app/routers/chat.py`):
   - `POST /api/coach/chat` — SSE streaming endpoint
   - `GET /api/coach/sessions` — list user's sessions
   - `GET /api/coach/sessions/{id}` — get session with messages
   - `DELETE /api/coach/sessions/{id}` — delete session
10. **Trade review context injection**:
    - User's recent trades + behavior metrics (Phase 2)
    - Relevant ICT events near trade entry/exit (Phase 4)
    - Backtest results for the strategy used (Phase 5, if available)
    - Retrieved wiki chunks with citations
11. **Structured review output**:
    - Setup quality (was the ICT setup valid?)
    - Execution quality (entry timing, stop placement)
    - Risk management (position sizing, R-multiple)
    - Psychology (tilt indicators, emotion context from journal)
    - Rule adherence (prop rules if configured)
    - Improvement plan (specific, actionable next steps)
12. **Chat UI** (`app/src/pages/chat.tsx`):
    - Message bubbles with markdown rendering
    - Citation links (click to view source wiki section)
    - Confidence indicators on AI responses
    - Session history sidebar
    - "Review this trade" quick-action from journal
13. **Evaluation dataset** — 100-200 Q&A pairs covering all ICT concepts
14. **Tests** for retrieval quality, chat API, and review output structure

## Key Constraints

- AI output must be educational and analytical — NOT financial advice
- No profit promises, no trading recommendations
- Citations must link to actual wiki source sections
- **Content licensing gate:** Public wiki corpus and user's own trade data are usable without licensing. Private instructor content (transcripts, private mentorship notes) requires a content licensing agreement. Flag this as a compliance gate but do not block Phase 6 on it — there's enough public content to launch.
- Extend existing Claude client — do not replace it
- Keep prompt caching (already implemented)
- Route simple deterministic lookups (kill zones, session times) to code, not LLM
- Free tier: 5 questions/day. Mentor tier: unlimited.

## Acceptance Criteria

- [ ] Wiki content ingested into pgvector with correct chunking and metadata
- [ ] Hybrid search returns relevant chunks for ICT queries (test with 20 diverse questions)
- [ ] Multi-turn chat persists conversation history
- [ ] Chat API streams responses via SSE
- [ ] Trade review includes structured sections (setup, execution, risk, psychology, rules, improvement)
- [ ] Citations link to actual wiki source sections
- [ ] Trade context injection includes user's trades, events, and behavior metrics
- [ ] Chat UI renders markdown, citations, and confidence indicators
- [ ] Hallucination rate < 15% on evaluation dataset
- [ ] Response latency < 5s (p95)
- [ ] Tests cover retrieval quality, chat lifecycle, and review output structure

## When done

Say: "Phase 6 complete — NeuroCore retrieval and Mentor coaching are live with citations and trade context. Run `/ns-phase7` in a new session for Edge Forensics."
