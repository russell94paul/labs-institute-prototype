---
phase: 6
name: "AI Trade Review + RAG"
status: in_progress
assigned: [paul]
started: 2026-05-10
completed: null
tickets_total: 0
tickets_done: 0
goal: "Ground AI coaching in methodology docs and trade data. Build NeuroCore (hybrid 3-signal retrieval) and upgrade Mentor to multi-turn chat with citations and structured reviews."
deliverables:
  - "6A: pgvector extension + WikiChunk model"
  - "6A: Embedding pipeline (OpenAI text-embedding-3-small)"
  - "6A: Wiki content ingestion pipeline (idempotent)"
  - "6A: Hybrid retrieval (BM25 + semantic + entity, Reciprocal Rank Fusion)"
  - "6A: ICT terminology normalization"
  - "6B: ChatSession and ChatMessage models"
  - "6B: Chat API (SSE streaming)"
  - "6B: Trade review context injection (trades, events, behavior, backtests)"
  - "6B: Structured review output (setup, execution, risk, psychology, rules, improvement)"
  - "6B: Chat UI with citations and confidence indicators"
  - "6B: Evaluation dataset (100-200 Q&A pairs)"
constraints:
  - "AI output must be educational/analytical — NOT financial advice"
  - "Citations must link to actual wiki source sections"
  - "Content licensing gate: public wiki content usable; private instructor content requires licensing"
  - "Extend existing Claude client — do not replace"
  - "Keep prompt caching"
  - "Free tier: 5 questions/day. Mentor: unlimited."
acceptance_criteria:
  - "Wiki content ingested into pgvector with correct chunking"
  - "Hybrid search returns relevant chunks for ICT queries"
  - "Multi-turn chat persists conversation history"
  - "Chat API streams via SSE"
  - "Trade review includes structured sections"
  - "Citations link to wiki sources"
  - "Hallucination rate < 15% on evaluation dataset"
  - "Response latency < 5s (p95)"
compliance_gate: "Content licensing for private instructor content. ToS + Privacy Policy. 'Not financial advice'"
created: 2026-05-15
updated: 2026-05-23
---

# Phase 6: AI Trade Review + RAG

NeuroCore hybrid retrieval + Mentor upgrade to multi-turn coaching with citations. Two sub-phases: 6A (NeuroCore) and 6B (Mentor upgrade).

Partially implemented: coach backend with Claude integration, prompt loading, trade-to-coach pipeline exist. Full RAG retrieval (NeuroCore) not yet started.

See `/ns-phase6` for full implementation guide.

## Deviations

_None yet._
