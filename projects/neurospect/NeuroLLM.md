# AI Coaching Platform for Trading Educators — Complete Solution Specification

## What this is

A platform that lets any trading educator deploy a personalized AI coach trained on their content and teaching style. The instructor provides their course recordings, coaching examples, and methodology — the platform turns it into an AI that teaches in their voice, corrects students the way they would, and knows their specific interpretation.

The technology is methodology-agnostic. The same pipeline serves ICT, Wyckoff, SMC, price action, Elliott Wave, or any structured trading approach. The first customer is an ICT (Inner Circle Trader) instructor — ICT is the launch vertical, not the product boundary. This document uses ICT examples throughout, but every component generalizes to other methodologies.

The platform starts as educational coaching (Phases 1-2) and can extend into chart analysis, practice trading, and eventually automated trading (Phases 3-5) — though later phases carry progressively higher risk and are methodology-dependent.

### Risk note on the first customer's methodology

The platform itself is methodology-agnostic — it doesn't depend on any particular trading approach being "correct." However, the first customer teaches ICT (Inner Circle Trader), which carries specific risks worth disclosing:

ICT concepts (order blocks, FVGs, liquidity sweeps, displacement) have **zero peer-reviewed academic validation**. No published study confirms these patterns have predictive power in financial markets. The broader academic literature on technical analysis is mixed — a 2023 meta-analysis (Springer) found: *"out-of-sample analysis shows that the performance of technical rules is not persistent"* and *"markets turn unpredictable in the last years of our sample."*

ICT's creator, Michael Huddleston, failed publicly in the 2016 $10K-to-$1M challenge and again in the 2024 Robbins Cup trading competition. He has acknowledged his income is primarily from mentorship, not trading.

**What this means:** This is a customer-level risk, not a platform-level risk. If ICT falls out of fashion, the platform serves other methodologies. Phases 1-3 (coaching) are viable regardless of whether ICT "works" — the platform builds AI coaches for any teachable methodology. Phases 4-5 (detection engine + automated trading) depend on the specific methodology having predictive power, which for ICT is unproven. Phase 5 includes a mandatory null test to address this.

---

## Instructor onboarding data (one dataset, multiple uses)

Every instructor provides the same categories of data. The items below are methodology-agnostic — an ICT instructor, a Wyckoff instructor, or a price action instructor all have course recordings, written materials, coaching examples, and common student mistakes. The same material feeds every phase of the platform.

**For the first customer (ICT instructor):** everything comes from their ICT courses, experience, and teaching practice.

### A. Course recordings

**What:** All recorded ICT courses. Video files, YouTube links, course platform exports. Any format.

**Why:** This is the primary knowledge base. The AI learns ICT by reading transcriptions of the client teaching it. TeachLM (arxiv 2510.05087, Oct 2025) processed 100,000+ hours of tutoring sessions from Polygence's proprietary archive — PhD-level tutors across 150+ STEM/social science subjects — into training data via audio transcription, cleaning, and structured knowledge base construction. Modern transcription (OpenAI Whisper at $0.006/min, or ElevenLabs API) handles this automatically with speaker diarization.

**Important caveat on source quality:** ICT course recordings are famously long (8+ hours), conversational, repetitive, and full of tangents. RAG quality is bounded by source quality. Before embedding, transcripts require significant editorial curation: de-duplication, filler removal, contradiction resolution across course versions (2016, 2019, 2021, 2022, 2024 contain redefined concepts), and restructuring into information-dense passages. Budget 4-8 weeks of human editorial work for this step — it is not automated.

**How much:** All of it. Every course, every module, every session. More content = deeper knowledge coverage. Partial coverage = the AI can't answer questions about topics it hasn't seen.

### B. Written course materials

**What:** PDFs, slides, handouts, study guides, checklists, playbooks. Whatever structured materials exist alongside the video courses.

**Why:** Course recordings are conversational — the client goes on tangents, repeats themselves, explains concepts in multiple ways across different sessions. Written materials are definitive and structured. The AI needs both: conversational explanations (from recordings) for the coaching voice, and authoritative definitions (from written materials) for factual accuracy. Without written materials, the AI may retrieve a casual tangent instead of the canonical definition when answering a direct question. Written materials are the single most important quality lever for RAG — they serve as the authoritative anchor that prevents hallucination of plausible-sounding but wrong ICT analysis.

### C. Coaching feedback examples (minimum 200, ideally 500+)

**What:** Instances where the client corrected a student's mistake, explained why an analysis was wrong, praised correct work, or walked through a chart review. Sources:
- Student Q&A sections within courses
- Discord/community interactions where they gave feedback
- Email exchanges with students
- Live session recordings where they reviewed student work
- Any written feedback they've given to students

**Why:** LoRA fine-tuning for voice and style is well-validated by practitioners at this scale. 200-500 high-quality, stylistically consistent examples are sufficient for SFT-based style transfer — confirmed by Databricks, IBM, and multiple production teams. The quality is determined primarily by dataset consistency (all examples sounding like the same "teacher" persona), not volume.

PERSA (arxiv 2605.01123, May 2026) demonstrated an SFT→reward model→PPO pipeline on code-feedback benchmarks achieving 96.2% Style Alignment Score on APPS with Llama-3.2-3B. However, PERSA tested exclusively on programming feedback (APPS, PyFiXV, CodeReviewQA) using 2-3B models, and the authors explicitly warn: *"gains may not directly transfer to new courses without additional preference data."* We use PERSA's architecture as a reference but do not assume its metrics transfer to trading coaching.

**Format per example:**
```
Student question or mistake: "I identified this bearish candle at 4250 as an order block"
Client's response: "That's not an order block — it didn't precede displacement. An OB is specifically the last opposing candle before a significant impulse move. Here you have a bearish candle followed by ranging price action, not displacement. Look for the candle at 4238 instead — that one has the 15-point displacement candle right after it."
```

### D. Common student mistakes

**What:** A list of frequent errors students make when learning ICT, and how the client corrects them.

**Why:** Without explicit training on common errors, the AI may validate incorrect analysis — a student says "this is an OB" about a random bearish candle, and the AI agrees because it doesn't know that's a common mistake. The correction patterns teach the AI the boundary between correct and incorrect ICT analysis per the client's interpretation.

**Examples:**
- "Students identify any bearish candle as an OB — the correct rule is it must precede displacement"
- "Students confuse BOS with CHoCH — BOS continues the trend, CHoCH reverses it"
- "Students enter FVGs without checking HTF bias — the filter is 4H structure must agree with entry direction"
- "Students trade every session — only NY open and London kill zones produce reliable setups"

### E. Chart annotations (if available)

**What:** Charts showing correct and incorrect ICT analysis, marked up by the client. "This is the OB," "this FVG is valid because...," "this is NOT a real sweep because..."

**Why:** Required for Phase 3 (chart analysis feature). The AI needs to learn what correct vs incorrect markup looks like. Without visual examples, the chart analysis feature cannot distinguish good analysis from bad.

**Format:** Screenshots with markups, or structured descriptions. Example:
```
Chart: ES 15m, 2025-03-12 09:42 ET
Correct: Bullish OB at 4242-4244 (valid — displacement candle 15 points, formed during NY open kill zone)
Incorrect: Student marked 4250-4252 as OB (invalid — no displacement followed, just ranging)
FVG: 4248-4252 (valid, unfilled, bullish)
Liquidity: Equal lows swept at 4240
HTF: 4H bullish BOS at 4230
```

### F. Trade history (for later phases)

**What:** Broker export of trades with ICT annotations — entry, stop, target, outcome, ICT zones, confluences.

**Why:** Needed only for Phase 4 (practice trading) and Phase 5 (automated trading). Not needed for the coaching app. The fields and rationale are identical to the trading model specification — each trade teaches the practice environment what a real trade looks like. See the detailed field table below under Phase 4.

---

## Platform architecture

### Base model selection

| Phase | Model | Why |
|-------|-------|-----|
| Phase 1 (RAG) | Claude Sonnet 4.6 or GPT-4o via API | Best available reasoning for Q&A. No fine-tuning needed. RAG provides the ICT knowledge. |
| Phase 2 (style fine-tuning) | Llama-3.2-3B-Instruct or Gemma-2-2B-IT | Open-weight model required for LoRA fine-tuning. PERSA validated the SFT→RLHF pipeline on these exact model families at 2-3B scale. 3B gives sufficient capacity for coaching style while remaining trainable on a single consumer GPU. Larger models (7-8B) are an option but PERSA's results are validated at 2-3B — extrapolation to 7-8B is unvalidated. |
| Phase 3 (chart analysis) | Claude Sonnet 4.6 or GPT-4o (vision) | Multimodal model that can read chart screenshots. RAG provides the correct ICT interpretation to compare against. **Warning:** vision model chart analysis is the riskiest feature — see Phase 3 section. |
| Phase 4 (practice trading) | Same as Phase 2 + rule-based ICT detection engine | The coaching model evaluates student trades. The detection engine identifies ICT patterns on historical charts for practice scenarios. |
| Phase 5 (automated trading) | MLP policy network [512, 512, 256] or Llama-3.2-3B with LoRA | RL policy network for trading. Standard MLP is the pragmatic default (used in the Forex RL paper). LLM-as-policy is experimental — FLAG-TRADER proved the concept at daily resolution with SmolLM2-135M but this does not validate intraday use. |

### Knowledge layer (shared across all phases)

**Vector database** containing the client's course content, chunked and embedded:
- Course transcripts (from recordings, Item A) — **after editorial curation**
- Written materials (Item B) — highest-priority source, used as authoritative anchor
- Common mistakes and corrections (Item D)
- Chart annotations as text descriptions (Item E)

**Technology:** Any vector DB — Pinecone, Weaviate, Chroma, pgvector. Embedding model: OpenAI text-embedding-3-large or open-source alternative (e.g., BGE-M3).

**Hallucination risk:** RAG reduces but does not eliminate hallucinations. In specialized domains, residual hallucination rates of 6-20% are documented (legal: 6.4% average, up to 33% in RAG tools; medical: 10-20%). ICT's niche terminology (CISD, PD Arrays, Consequent Encroachment, Optimal Trade Entry) did not exist in LLM pre-training data in meaningful quantity. Mitigation: system prompt instructs the model to cite specific course/module for every claim, refuse to answer when retrieval confidence is low, and never generate ICT analysis that isn't grounded in retrieved passages.

**Update cycle:** When the client records new courses or updates materials, re-index. Takes minutes. No retraining required.

### Data flow & modality pipelines

Each phase processes different data types (modalities) through different transformation chains. Understanding exactly where each modality enters, how it's converted, and where errors compound is critical for scoping risk.

#### Phase 1 — Text only (audio/PDF → text → text)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ INGESTION (one-time)                                                    │
│                                                                         │
│  Video/Audio ──→ Whisper API ──→ Raw transcript                         │
│                   (audio→text)     │                                     │
│                                    ▼                                     │
│                              Human editorial ──→ Clean passages          │
│                              (4-8 weeks)          │                      │
│  PDFs/Slides ──→ Text extraction ─────────────────┤                     │
│                   (document→text)                  │                     │
│                                                    ▼                     │
│                                              Embedding model             │
│                                              (text→vectors)              │
│                                                    │                     │
│                                                    ▼                     │
│                                              Vector DB                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ QUERY (every user interaction)                                          │
│                                                                         │
│  User question ──→ Embedding ──→ Similarity search ──→ Top-K passages   │
│  (text)            (text→vector)  (vector→text)          │              │
│                                                          ▼              │
│                                                    LLM prompt            │
│                                                    (text→text)           │
│                                                          │              │
│                                                          ▼              │
│                                                    Answer + citations    │
└─────────────────────────────────────────────────────────────────────────┘
```

**Modality transitions:** 2 (audio→text, text→vectors). Both are mature, off-the-shelf. No modality mixing at inference time — pure text in, text out.

**Where errors enter:** Whisper transcription errors on ICT jargon (e.g., "CHoCH" may transcribe as "choch" or "chalk"). Mitigation: post-transcription terminology normalization pass. Retrieval errors when query doesn't match chunk vocabulary. Mitigation: query expansion, hybrid search (keyword + semantic).

#### Phase 2 — Text only (text pairs → model weights)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TRAINING (one-time per model version)                                   │
│                                                                         │
│  200-500 coaching examples ──→ LoRA SFT ──→ Fine-tuned 3B model         │
│  (instruction, response pairs)   (text→weights)                         │
│       (text)                                                            │
│                                                                         │
│  Optional: pairwise preferences ──→ DPO ──→ Better-aligned model        │
│  ("Response A is more like the       (text→weights)                     │
│   client than Response B")                                              │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ INFERENCE (every user interaction)                                       │
│                                                                         │
│  Same as Phase 1, but the LLM is now the fine-tuned model               │
│  RAG provides knowledge; fine-tuned model provides voice                 │
│  (text→text, no modality change)                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

**Modality transitions:** 0 at inference time. Training is text→weights (standard ML). No multimodal complexity.

**Where errors enter:** Style overfitting (model memorizes phrasing instead of generalizing tone). Mitigation: short SFT (1-2 epochs), validation loss monitoring, held-out test set. LoRA intruder dimensions degrading base model capabilities. Mitigation: full-layer LoRA, small rank, DPO instead of PPO.

#### Phase 3 — Multimodal (image + text → text) — THE HARD ONE

```
┌─────────────────────────────────────────────────────────────────────────┐
│ OPTION A: Pure vision (risky)                                           │
│                                                                         │
│  Chart screenshot ──→ Vision model ──→ Description of markups           │
│  (image)               (image→text)     (text)                          │
│                                            │                            │
│  RAG: ICT rules for ──────────────────────┐│                            │
│  OBs, FVGs, etc.                          ▼▼                            │
│  (text)                             Evaluation prompt                   │
│                                     (text→text)                         │
│                                            │                            │
│                                            ▼                            │
│                                     Feedback to student                 │
│                                                                         │
│  ERROR COMPOUNDS: vision misreads chart → wrong description →           │
│  wrong evaluation → confident but incorrect feedback                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ OPTION B: Hybrid approach (recommended)                                 │
│                                                                         │
│  Student enters structured analysis:                                    │
│  "OB at 4242-4244, FVG at 4248-4252,                                   │
│   bullish bias, NY kill zone"           ──→ Rule validation             │
│  (structured text)                          (text→text)                 │
│                                                  │                      │
│  Chart screenshot ──→ Vision model ──→ Visual    │                      │
│  (image)               (image→text)    cross-check│                     │
│                                            │      │                     │
│                                            ▼      ▼                     │
│  RAG: ICT rules ──────────────────→ Combined evaluation                 │
│  (text)                              (text→text)                        │
│                                            │                            │
│                                            ▼                            │
│                                     Feedback to student                 │
│                                                                         │
│  PRIMARY PATH: text→text (reliable)                                     │
│  SECONDARY CHECK: image→text (supplementary, not authoritative)         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why Option B is better:** The primary evaluation path is text→text (student's structured input validated against ICT rules from RAG). This path is reliable — same modality as Phase 1. Vision is used only as a supplementary cross-check: "Does the chart actually show what the student claims it shows?" If vision disagrees with the student's text input, flag it for the student to resolve rather than trusting the vision model. This inverts the error profile: instead of the AI being confidently wrong, it asks clarifying questions when uncertain.

**Modality transitions (Option B):** 1 critical (structured text→text rule validation, reliable) + 1 supplementary (image→text cross-check, error-prone but non-authoritative).

**Where errors enter:** Vision model hallucinating chart features (documented: models confidently describe support/resistance levels that don't exist). Mitigation: vision is advisory, never authoritative. If vision and structured input disagree, surface the disagreement to the user.

#### Phase 4 — Numerical only (no LLM in the detection engine)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ DETECTION ENGINE (pure code, no ML, no modalities)                      │
│                                                                         │
│  OHLCV data ──→ Pattern detection algorithms ──→ Detected patterns      │
│  (float arrays)  (numerical computation)          (structured data)     │
│                                                                         │
│  Rules: "OB = last opposing candle before displacement > N points,      │
│          formed during kill zone, with HTF alignment"                   │
│                                                                         │
│  Strict causality: bar[t] can only reference bar[0..t-1]               │
│  No future data. Anti-lookahead validation on every function.           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ COACHING LAYER (same as Phase 2, text→text)                             │
│                                                                         │
│  Student's trade + detected patterns ──→ Coaching model ──→ Feedback    │
│  (structured text)                        (text→text)                   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Modality transitions:** 0 for the detection engine (pure numerical). 0 for coaching (text→text). The detection engine and coaching model are separate systems connected by structured data — no modality mixing.

**Where errors enter:** Not modality errors — algorithmic errors. The detection engine may define "displacement" differently than the client intends. The subjectivity of ICT patterns means the rules must be validated against the client's labeled trades, iteratively refined, and accepted as ONE interpretation, not ground truth.

#### Phase 5 — Numerical only (MLP default) or Text-encoded (LLM experimental)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ OPTION A: MLP policy (recommended default)                              │
│                                                                         │
│  OHLCV + ICT features + portfolio state ──→ MLP [512,512,256] ──→ Action│
│  (float vector, ~50-100 features)           (numbers→numbers)           │
│                                                                         │
│  No modality conversion. No text. No tokenization.                      │
│  Inference: microseconds. Training: standard RL.                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ OPTION B: LLM policy (experimental, not recommended)                    │
│                                                                         │
│  OHLCV + ICT features ──→ Text template ──→ LLM ──→ Action             │
│  (float vector)           "Price: $4248.50,  (text→   (discrete)       │
│                            Vol: 12.3K,        action)                   │
│                            RSI: 67.2..."                                │
│                           (numbers→text)                                │
│                                                                         │
│  PROBLEM: number→text conversion loses precision.                       │
│  "$4248.50" tokenizes as ["$", "42", "48", ".", "50"] — the LLM has    │
│  no native understanding that 4248.50 > 4241.00.                        │
│  Adds 100-1000x inference latency per timestep.                         │
│  Documented to ADD NOISE under distribution shifts (arxiv 2604.10996).  │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why MLP is the default:** RL trading is a numerical control problem. The agent observes numbers (prices, indicators, portfolio state) and outputs a discrete action. An MLP handles this natively — numbers in, action out, microseconds per step. Wrapping numbers in text and feeding them through an LLM tokenizer introduces noise, latency, and a modality conversion that has no demonstrated benefit for this task class. FLAG-TRADER showed LLM-as-policy works on daily bars (where latency doesn't matter and the text description adds market context) — but intraday ICT trading has neither of those properties.

**Modality transitions (Option A):** 0. Pure numerical. This is why it's the default.

---

## Phase 1: RAG coaching MVP

### What it does
User asks any ICT question → system retrieves relevant passages from the client's course content → LLM generates answer grounded in those passages.

### Technical pipeline
1. **Ingest:** Transcribe all course recordings (Whisper API, ~$0.006/min). Clean transcripts (remove filler words, normalize terminology). **Human editorial pass: de-duplicate, resolve contradictions across course versions, restructure into information-dense passages (budget 4-8 weeks).** Chunk into passages (~500-1000 tokens each). Embed and store in vector DB.
2. **Query:** User asks a question → embed the question → retrieve top-K relevant passages → construct prompt with passages as context → LLM generates answer → cite which course/module the answer came from.
3. **System prompt:** Instructs the LLM to act as an ICT trading coach, only answer from the provided context, admit when it doesn't know, cite the source passage for every claim, and never give financial advice or trade signals.

### Input data required
- Client Items A + B (course recordings + written materials)

### Output to user
- Text answers to ICT questions
- Citations showing which course/module the answer came from
- "I don't have information about that" when the question is outside course content

### Evidence this works
- RAG for domain-specific Q&A is the standard, well-proven approach (used in production by Khan Academy's Khanmigo, though Khanmigo uses structured authored exercises as source material — qualitatively different from video transcripts)
- TeachLM (arxiv 2510.05087) processed 100K+ hours of tutoring content into a knowledge base — but tested on STEM/social sciences with PhD-level structured tutoring data, not trading video transcripts
- The ICLR 2026 paper (arxiv 2510.01375) demonstrates RAG-augmented training for agent tasks (ALFWorld, WebShop) — its contribution is using RAG at training time to generate better demonstrations, not a "RAG for knowledge, fine-tuning for behavior" deployment architecture

### What it doesn't do
- Doesn't sound like the client — sounds like a generic chatbot that happens to know ICT
- Doesn't evaluate student work — just answers questions
- Doesn't improve from user interactions

### Known risks
- ICT course content is unstructured and repetitive — RAG retrieval may return multiple contradictory versions of the same concept from different course years. Mitigation: editorial curation (step 1) and version-aware chunking
- Domain-specific hallucination: the model may generate plausible-sounding but wrong ICT analysis by blending retrieved ICT content with general finance knowledge from pre-training. Mitigation: strict grounding instructions, confidence thresholds, citation requirements

---

## Phase 2: Instructor voice (LoRA fine-tuning)

### What it does
Same knowledge as Phase 1, but delivered in the client's specific teaching style — their analogies, their emphasis, their way of correcting mistakes, their personality.

### Technical pipeline
1. **Collect:** Extract 200-500+ coaching feedback examples from the client (Item C). Structure as instruction-response pairs.
2. **SFT:** LoRA fine-tune the base model (Llama-3.2-3B-Instruct or Gemma-2-2B-IT) on these examples. Supervised fine-tuning minimizing negative log-likelihood. Keep it short — arxiv 2508.16546 showed OOD performance peaks early during SFT (~17-20% of training steps on Qwen-2.5-7B) and degrades after. **Note:** this finding was on full fine-tuning with standard-sized datasets (thousands of examples), not 200-example regimes. For 200 examples, train 1-2 epochs and monitor validation loss — stop when validation loss starts rising.
3. **Evaluate:** Test the SFT model on held-out coaching scenarios. If style quality is sufficient, ship it. If not, proceed to step 4.
4. **DPO (if needed):** If SFT alone doesn't capture enough style nuance, collect pairwise preferences — "which response sounds more like the client?" Use Direct Preference Optimization (DPO) rather than the full reward model + PPO pipeline. DPO eliminates the reward model entirely, uses the same preference data format, costs 10x less compute, and is dramatically more stable. **Why not PPO:** standard RLHF reward models require 2,000-5,000+ pairwise comparisons minimum (InstructGPT used ~33K, Anthropic HH-RLHF: ~161K). Building a meaningful reward model from a few hundred pairs produces an underfit model that PPO will immediately reward-hack. DPO avoids this entirely.
5. **Deploy:** Replace the base LLM in Phase 1's pipeline with the fine-tuned model. RAG still provides knowledge; the fine-tuned model provides the voice.

### Input data required
- Client Item C (200-500+ coaching feedback examples)
- Client Item D (common mistakes — used to generate training scenarios)
- If DPO is needed: additional 200-500 pairwise preference comparisons (can be collected iteratively by having the client compare AI-generated responses)

### Output to user
- Same ICT answers as Phase 1, but in the client's teaching voice
- Corrections that sound like the client correcting you, not like ChatGPT

### Evidence this works
- LoRA SFT for voice/style transfer on 200-500 examples is well-validated by practitioners (Databricks, IBM production teams). Style and tone are what LoRA excels at — the quality driver is dataset consistency, not volume.
- PERSA (arxiv 2605.01123): demonstrated the full SFT→RM→PPO pipeline achieves 96.2% Style Alignment on code feedback with Llama-3.2-3B. **Caveats:** tested exclusively on programming feedback, not coaching; 2-3B models, not 7-8B; authors explicitly disclaim domain transfer; BLEU-4 of 95.8% on 200 examples suggests possible overfitting given that SOTA machine translation scores 40-60 on a 100-point scale.
- SFT then RL recovery (arxiv 2508.16546): RL recovers up to 99% of OOD generalization on Qwen-2.5-7B (full fine-tuning). **Caveats:** tested with full fine-tuning, not LoRA. LoRA introduces "intruder dimensions" (Shuttleworth et al. 2024, NeurIPS 2025) that degrade pre-training distribution modeling. Mitigated by keeping SFT short and using full-layer LoRA (attention + MLP projections), not top-layers-only.

### What it doesn't do
- Doesn't evaluate charts
- Doesn't improve from user feedback yet (but DPO preference collection creates the data loop for continuous improvement)

---

## Phase 3: Chart analysis

### What it does
User uploads a chart screenshot with their ICT markup. The AI evaluates whether they correctly identified OBs, FVGs, market structure, liquidity levels. Gives specific feedback: what's correct, what's wrong, why.

### Technical pipeline
1. **Vision input:** User uploads chart screenshot → vision model (Claude Sonnet 4.6 or GPT-4o) reads the image.
2. **RAG context:** Retrieve relevant ICT rules from the knowledge base — "what makes a valid OB," "FVG formation rules," "HTF alignment requirements."
3. **Evaluation prompt:** "The student has marked the following on this chart: [vision model describes the markups]. Based on the ICT rules in the context, evaluate each markup. Identify what is correct, what is incorrect, and explain why using the instructor's teaching approach."
4. **Fine-tuned model generates:** Specific feedback in the client's voice, referencing their rules.

### Input data required
- Client Item E (chart annotations showing correct and incorrect analysis)
- All previous phase data for knowledge and style

### Output to user
- Per-markup evaluation: correct/incorrect + explanation
- "You correctly identified the OB at 4242-4244 — that's the last bearish candle before the 15-point displacement. But the FVG you marked at 4315-4318 formed outside the NY kill zone. [Client's name] teaches that FVGs are only tradeable during the 9:30-10:00 ET window."

### Evidence — THIS IS THE RISKIEST COACHING PHASE
- Vision models (Claude, GPT-4o) can read and describe chart screenshots at a basic level.
- **However, chart analysis accuracy is poor in independent testing:**
  - ChartSnipe 2026 test (50 real charts): *"Support and resistance hallucinations alone are disqualifying for real money."* Models confidently hallucinate levels that do not exist on the chart.
  - Meta + Stanford adversarial chart test: **0% full pass rate** across all 9 models tested (GPT, Claude, Gemini families). Not one model passed all tests.
  - MMMU benchmark: GPT-4V achieves only 56% on multi-discipline charts/diagrams — and those are clean academic charts, not live candlestick charts with ICT markup.
- **No study tests ICT markup evaluation via vision models.** This is genuinely unproven and is the highest-risk coaching feature.

### Mitigation strategy
- Launch as "beta" / "experimental" with explicit disclaimers
- Always show confidence levels — "I'm X% confident in this assessment"
- Require the model to describe what it sees before evaluating — this creates an auditable intermediate step the user can verify
- Pair vision assessment with text-based rule checking where possible (user enters zones numerically, AI validates against rules without relying on vision)
- Collect user corrections to iteratively improve

### What it doesn't do
- Doesn't detect patterns automatically — evaluates the student's markups
- Doesn't provide real-time chart scanning

---

## Phase 4: Practice trading environment

### What it does
Students practice trading on historical data. They see a chart replay, identify setups, place entries with stops and targets. The AI evaluates their decisions: "Good entry — you identified the OB+FVG confluence during kill zone. But your stop should be below the OB at 4241, not at 4238 — [client's name] teaches stops go 1 tick below the OB low, not 3 points."

### Technical pipeline
1. **ICT detection engine:** Rule-based code built from scratch using the client's rulebook (Item D and the full course content). **Must NOT use the `smart-money-concepts` Python package** — it has documented look-ahead bias (GitHub Issues #34, #61, #82, #101: all detection methods use a centered window that looks into the future; profit factor drops from 7.32 to 1.82 when bias is removed; Freqtrade's detection tool found 100% of signals biased; fix PR #103 remains unmerged). Custom engine must enforce strict causality: detect patterns using only past data, with anti-lookahead validation at every step.
2. **The subjectivity problem:** ICT patterns are inherently subjective. The maintainer of the leading SMC library acknowledges: *"order blocks are very subjective — there is no one answer."* Different ICT practitioners identify different structures on the same chart. The detection engine encodes ONE specific interpretation (the client's), validated against the client's labeled trades. It does not claim to implement "ICT" universally — it implements the client's operationalization of ICT.
3. **Chart replay:** Historical OHLCV data played candle-by-candle. Student sees the chart form in real time and makes decisions. **Build vs buy:** Dedicated replay products exist (FX Replay, TradingView replay, Soft4FX). Building from scratch is a 3-6 month engineering effort. Recommend integrating with existing replay infrastructure or licensing a charting library (e.g., TradingView Lightweight Charts) rather than building from zero.
4. **Evaluation:** Student marks entry/stop/target → detection engine identifies what ICT features were present at that moment → coaching model evaluates whether the student's analysis matches the client's rules → generates feedback.
5. **Scoring:** Win rate per setup type, per session, per confluence count. Track student progress over time.

### Input data required
- Client Item F (trade history with ICT annotations) — used to build and validate the detection engine
- OHLCV data (we acquire: 3+ years, 1-minute resolution for the client's instruments. Source: Polygon.io ~$200/month)
- All previous phase data

### Output to user
- Practice trading environment with historical chart replay
- Per-trade feedback from the coaching AI
- Performance dashboard: win rate, R:R, best/worst sessions, improvement over time

### Evidence for detection engine
- smc_quant (github.com/starckyang/smc_quant): a single-contributor hobbyist project (7 commits, 10 stars) implementing rule-based SMC on ETH. Reports Sharpe 1.26 on 2024 test data. **Severe caveats:** likely uses the biased `smart-money-concepts` library; 2024 was a strong ETH bull year (buy-and-hold returned ~77%); no slippage modeling; no independent replication. This demonstrates that rule-based ICT detection can be coded — not that it's profitable.
- The `smart-money-concepts` package has documented look-ahead bias (see above). CANNOT be used. Must build custom with end-to-end causality guarantees.

### Evidence for practice environment
- Standard approach in trading education (FX Replay, TradingView replay). Not novel.

### Validation requirements
- **Minimum 300-500 annotated trades per major pattern type** (OB, FVG, BOS/CHoCH, liquidity sweeps). 200 total trades across all pattern types (as originally proposed) gives only ~30-40 per pattern class — insufficient for per-pattern precision/recall validation. With 6 pattern types, need 1,800-3,000 total labeled instances.
- **Additionally needed:** 200+ skipped setups (timestamps where ICT pattern appeared but client didn't trade, with reason). These define the filter rules in the detection engine.
- **Cross-regime validation:** trades must span trending, ranging, and volatile market conditions. A validation set drawn entirely from one regime proves nothing about other regimes.

### Trade history fields needed (from client Item F)

| Field | Example | Why |
|-------|---------|-----|
| Timestamp (entry, with TZ) | 2025-03-12 09:42:00 ET | Align with OHLCV data, validate detection engine |
| Timestamp (exit) | 2025-03-12 10:15:00 ET | Ground truth for practice scenarios |
| Instrument | ES | Must match purchased OHLCV data |
| Timeframe | 15m | Must match detection engine timeframe |
| Direction | Long | Core label |
| Entry price | 4248.50 | Validate detection engine's entry zone identification |
| Stop price | 4241.00 | Teach stop placement rules |
| Target price | 4265.00 | Teach target placement rules |
| Actual exit price | 4264.75 | Ground truth outcome |
| Outcome | Win | Label |
| Setup type | Silver Bullet | Different detection logic per setup type |
| OB zone | 4242-4244 | Ground truth for detection engine validation |
| FVG zone | 4248-4252 | Ground truth for detection engine validation |
| Liquidity swept | 4240 | Trigger condition |
| HTF bias | Bullish | Filter rule |
| Session | NY open | Timing filter |
| Confluences | OB, FVG, sweep, displacement, kill zone | Feature importance validation |

---

## Phase 5: Automated trading (optional, highest risk)

### What it does
An AI model that actually executes trades based on ICT patterns. This is the trading bot.

### Critical prerequisite: Null test

**Before any development on Phase 5, run a null test:** train an RL model with ICT features from the Phase 4 detection engine vs. an identical model without ICT features (standard technical indicators only). If ICT features don't add statistically significant signal above standard indicators across multiple market regimes, **stop here.** Phase 5 is not viable and should not be built. The probability of ICT features adding signal is unknown and academically unsupported — this null test is the single most important experiment in the entire platform.

### Technical pipeline
1. **Base model (pragmatic default):** MLP policy network [512, 512, 256] with DQN/Double DQN — this is what the Forex RL paper (arxiv 2604.00031) used and it's the well-understood default for discrete-action RL trading. **LLM-as-policy (experimental alternative):** Llama-3.2-3B with LoRA, following FLAG-TRADER's architecture. Trade-off: LLMs add pre-trained reasoning but have 100-1000x inference overhead vs MLP, tokenize numbers poorly (introducing noise), and have near-zero mathematical reasoning at small scales (SmolLM2-135M scores 1.4 on GSM8K grade-school math).
2. **State encoding:** ICT features from the custom detection engine (Phase 4) + OHLCV + session/timing + portfolio state. For MLP: numerical feature vectors. For LLM: text prompt (FLAG-TRADER's `lang(s)` format) — but note that text encoding of numerical data is documented to add noise vs. numerical encoding, and one paper (arxiv 2604.10996) found LLM features actively degrade RL trading performance under distribution shifts.
3. **Action space:** 10-action discrete (from arxiv 2604.00031): HOLD, OPEN_LONG, OPEN_SHORT, PYRAMID_LONG, PYRAMID_SHORT, MARTINGALE_LONG, MARTINGALE_SHORT, REDUCE, CLOSE, REVERSE. Legal masking for margin/directional constraints. **Note:** the Forex RL paper found its 3-action simple baseline achieved Sharpe 2.433 vs. the 10-action system's 0.765 in-sample — more complexity was worse even on training data. Start with 3 actions, add complexity only if justified by empirical results.
4. **Reward:** 11-component decomposable reward (from arxiv 2604.00031) including profit, transaction costs, drawdown penalty, overtrading penalty, liquidation penalty. Well-designed architecture, but the paper found *"strongly non-monotonic reward interactions where additional penalties do not reliably improve outcomes."* Use ablation studies to determine which components actually help.
5. **Training:** PPO (for LLM policy) or DQN/DDQN (for MLP policy) on trainable parameters. 1,000,000+ timesteps. 3+ years of OHLCV data. **Multiple seeds required** — the Forex RL paper used a single seed, which provides no statistical significance.
6. **Null test first:** Train with ICT features vs without. If ICT doesn't add signal, stop.
7. **Walk-forward validation:** Mandatory out-of-sample testing across multiple market regimes (trending, ranging, volatile, bear markets). The Forex RL paper explicitly reports only in-sample results. FLAG-TRADER tested only in a post-COVID bull market. Neither provides evidence of out-of-sample generalization.

### Input data required
- Everything from all previous phases
- 3+ years OHLCV at 1-minute resolution (we acquire)
- Client's trade history for supervised pre-training (Phase 4 Item F)

### Evidence — HONEST ASSESSMENT
- **FLAG-TRADER (ACL Findings 2025, arxiv 2502.11433):** SmolLM2-135M beat GPT-4 on **3 of 6 assets** (not 4/6 as commonly cited) on Sharpe ratio. **Critical caveats:** daily bars only (not intraday), 3-action all-in/all-out space (not 10-action), test period Oct 2020–May 2021 (post-COVID bull market, S&P 3300→4200), no walk-forward validation, paper admits *"optimizes for returns without risk-sensitive constraints"* and *"non-stationarity challenges for long-term generalization."*
- **Forex RL paper (arxiv 2604.00031):** 10-action space with 11-component reward on EURUSD hourly bars using DQN/DDQN MLP. **ALL results are in-sample** — paper explicitly states *"no held-out or test data is used at any point"* and *"all reported results reflect only the training distribution, with no claims regarding generalization."* Best in-sample Sharpe: 0.765 (full config) vs 2.433 (3-action baseline). Uses standard MLP, NOT an LLM.
- **Darmanin & Vella 2025 (arxiv 2508.02366):** LLM-guided RL outperformed RL-only baseline. Sharpe 1.10 vs 0.64 mean across **6 equities** (AAPL, AMZN, GOOGL, META, MSFT, TSLA — not 30). Out-of-sample period 2018-2020 (pre-COVID). MDD not consistently reduced. Preprint, not peer-reviewed.
- **RL trading broadly:** *"The current body of literature lacks substantial evidence supporting the practical efficacy of RL agents"* (arxiv 2512.10913 survey). Policy instability and non-stationarity are fundamental unsolved problems.
- **No paper tests ICT features in an RL model.** This is genuinely unproven territory.

### Risks — ALL SEVERE
- ICT features may not add signal over standard technical indicators (unproven — null test is mandatory)
- FLAG-TRADER architecture proven only on daily bars, not intraday (ICT is intraday)
- The only ICT detection package has 75% profit inflation from look-ahead bias — custom engine from Phase 4 is required
- All published RL trading results are either in-sample or tested in bull markets only
- SmolLM2-135M has GSM8K of 1.4 (near-zero math reasoning) — questionable as a trading policy network
- Text-encoded OHLCV degrades RL performance under distribution shifts (arxiv 2604.10996)
- Even if backtests look good, live trading introduces slippage, latency, and regime changes that backtests cannot capture

---

## Legal and regulatory considerations

### Phase 1-3 (coaching)
- System prompt must include clear disclaimers: "This is educational content, not financial advice"
- The AI must never answer "should I take this trade?" or provide specific trade signals — this crosses into individualized investment advice under the Investment Advisers Act
- Collect user acknowledgements of educational-only nature before platform access
- Monitor and log all interactions for compliance review

### Phase 4-5 (practice trading + automated trading)
- **Phase 5 triggers SEC/FINRA registration requirements** as a Registered Investment Adviser (RIA) if it manages client assets or provides automated trading signals for compensation
- The SEC has active "AI washing" enforcement — targeting platforms that misrepresent how AI works in financial decision-making (FINRA Regulatory Notice 24-09)
- Multi-jurisdiction compliance required: SEC (US), FCA (UK), MiFID II (EU), ASIC (Australia)
- **Budget for legal review before launching Phase 4.** Budget for securities counsel before Phase 5.
- Liability risk: if users lose money following AI coaching, class action exposure is real. No disclaimer language adequately protects against this if compensation is received.

---

## Competitive landscape

Existing competitors are single products built for one methodology. We are building infrastructure that any instructor plugs into. They are individual stores — we are Shopify.

| Competitor | What it does | Why it's not a threat |
|-----------|-------------|----------------------|
| **Price Action Lover** | AI trading desk for ICT traders (uses Claude), FVG/OB/killzone analysis. Integrated with Binance/OANDA. | One product, one methodology, no instructor personalization. If the ICT instructor on our platform has a stronger brand, their students want *their* coach, not a generic one. |
| **ICT GPT** (ChatGPT store) | Free GPT variants with ICT content | Anyone can build this in an afternoon. No fine-tuning, no proprietary voice, no moat. |
| **LuxAlgo** | 800K+ TradingView followers, "Pure Price Action ICT Tools" indicator | Pattern detection tool, not coaching. Different product category. |
| **n8n ICT bot** | Open-source workflow: ICT + GPT-4o + Coinbase | DIY automation, no coaching layer, no product. |
| **FX Replay / TradeZella** | Chart replay + journaling for practice trading | Practice tools without AI coaching. Potential integration partner, not competitor. |

**Our moat is not technology — it's the exclusive relationship with each instructor + the fine-tuned model trained on their proprietary coaching data.** No competitor can replicate an instructor's voice without their data. Every instructor onboarded adds a new market segment the competitors can't access. The platform scales with the number of instructors, not the number of features.

---

## Revenue model sketch

### Model: B2B2C — instructors bring the audience, we bring the technology

**Instructor-facing (B2B):**
- Platform fee: $199-499/month per instructor (covers fine-tuning, hosting, vector DB, support)
- Revenue share: 15-25% of student subscription revenue
- Onboarding fee: $2,000-5,000 one-time (covers editorial curation of course content, initial fine-tuning)

**Student-facing (B2C, set by each instructor):**
- Free tier: Limited RAG Q&A (10 questions/day), basic glossary
- Pro tier ($29-49/month): Unlimited Q&A with instructor voice, common mistake feedback
- Premium tier ($79-149/month): Chart analysis (Phase 3), practice trading (Phase 4)

### Unit economics (rough)
- LLM API cost per student per month (assuming 100 queries): $1-5
- Infrastructure per student per month: $0.50-2
- Gross margin target: 70-80%
- Per-instructor break-even: 50-100 paying students (at blended $50 ARPU, 20% rev share = $10/student → $500-1000/month covers platform fee + costs)

### Market sizing

**Single-instructor view (first customer, ICT):**
- ICT YouTube subscribers: ~2M (verified)
- Realistic addressable: 1-3% = 20,000-60,000
- Free-to-paid: 1-3% → 200-1,800 paying students
- Revenue at $50 ARPU: $10,000-$90,000/month
- **As a single product, this is a lifestyle business.**

**Platform view (multiple instructors):**
- Trading education creators with 10K+ followers across forex, crypto, equities, options: hundreds exist
- Each instructor is an independent market segment with their own audience
- 10 instructors × 500 avg paying students × $50 ARPU × 20% rev share = $50,000/month platform revenue + $1,990-4,990/month platform fees
- 50 instructors = $250,000+/month
- **The platform scales with instructors onboarded, not with any single methodology's popularity. This is what makes it venture-viable — if the unit economics work with the first customer.**

---

## Summary: what each instructor provides, what we build in phases

### Each instructor provides (once, same template for every methodology):

| Item | Description | Used in phases | Minimum |
|------|-------------|---------------|---------|
| A. Course recordings | All video/audio courses | 1, 2, 3, 4, 5 | All available |
| B. Written materials | PDFs, slides, handouts | 1, 2, 3, 4, 5 | All available |
| C. Coaching examples | Corrections, explanations, feedback to students | 2, 3 | 200+ (500+ ideal) |
| D. Common mistakes | Student errors + client's corrections | 1, 2, 3, 4 | 20+ error patterns |
| E. Chart annotations | Correct/incorrect analysis on charts | 3, 4 | 50+ charts |
| F. Trade history | Broker export with methodology zones, outcomes | 4, 5 | 300-500 per pattern type |
| G. Skipped setups | Setups seen but not traded, with reason | 4, 5 | 200+ |
| H. Instrument specification | What they trade, which timeframes, which sessions | 4, 5 | 1 page |

Items A-D are needed to launch the coaching app (Phases 1-2). Items E-H are only needed for chart analysis and trading features (Phases 3-5). Each instructor can start with A-D and provide the rest later. The onboarding template is identical regardless of methodology.

### We build (once, shared across all instructors):

| Phase | What | Depends on | Evidence | Risk |
|-------|------|-----------|----------|------|
| 1. RAG coaching MVP | Q&A from course content | Items A, B | RAG for domain Q&A is well-proven. TeachLM shows large-scale tutoring data processing works. | Low — requires significant editorial curation of source material |
| 2. Instructor voice | LoRA SFT (+ DPO if needed) for teaching style | Items C, D | LoRA SFT for style transfer validated by practitioners at 200-500 examples. PERSA architecture reference (code domain only). | Medium — domain transfer from code to coaching is unvalidated |
| 3. Chart analysis | Vision model evaluates student markups | Item E | Vision models can read charts at basic level. **ICT-specific chart evaluation is unproven. Independent tests show 0% adversarial pass rate for chart reasoning.** | High |
| 4. Practice trading | Historical replay with AI feedback | Items F, G, H + OHLCV data | Chart replay is standard. Custom detection engine required (no off-the-shelf tool is bias-free). ICT subjectivity is a fundamental challenge. | High |
| 5. Automated trading | RL trading model | All items + OHLCV data | FLAG-TRADER (daily bars/bull market/3 actions). Forex RL (in-sample only). No ICT-specific RL exists. **Null test mandatory before development.** | Very High — likely to fail |

### What's proven vs unproven per phase

| Phase | Proven | Unproven | Honestly unknown |
|-------|--------|----------|-----------------|
| 1 | RAG for domain Q&A | Whether ICT video transcripts are structured enough for good retrieval | Hallucination rate on ICT-specific terminology |
| 2 | LoRA SFT for style at 200-500 examples | Whether style transfers from code (PERSA's domain) to trading coaching | DPO effectiveness at <500 preference pairs for this domain |
| 3 | Vision models read charts at basic level | Whether AI can evaluate ICT-specific markup accuracy | Nothing — this is genuinely novel territory |
| 4 | Chart replay is standard tooling | Whether ICT patterns can be reduced to unambiguous rules for one practitioner | Whether 300-500 labeled trades per pattern suffices |
| 5 | LLM+RL can outperform baselines on daily bars in bull markets | Whether intraday RL works, whether ICT features add signal, whether it's profitable out-of-sample | Almost everything — this phase is research, not engineering |

---

## Market context

- **The trading education creator economy:** Trading educators are personality-driven businesses. Students follow instructors, not methodologies. The top 100 trading educators on YouTube collectively have 50M+ subscribers. Each educator who wants to scale their coaching beyond their personal time is a potential platform customer.
- **First customer (ICT community):** ~2M YouTube subscribers. Free content, no paid mentorship. Gap: no AI-powered interactive coaching personalized to a specific instructor. Sources: writofinance.com, inthetalks.com
- **AI education market:** $10.6B in 2026 (ResearchAndMarkets, April 2026). 36% CAGR. **Caveat:** this is all AI education including K-12, higher ed, corporate training. The directly addressable segment for AI trading education is a fraction — but with the platform model, each instructor opens a new segment.
- **Coaching platform market:** $4.22B in 2026, 11% CAGR (futuremarketinsights.com). **Caveat:** dominated by enterprise HR/leadership coaching (BetterUp, CoachHub). No platform currently serves trading education creators specifically — this is the gap.
- **EdTech sector challenges:** Investment collapsed from $16.7B (2021) to under $3B (2025). Byju's ($5.5B raised → insolvency), Korea AI Textbook ($850M → cancelled). High churn (9.6% monthly in 2025), weak monetization of free content. **Counter-argument:** these failures were horizontal platforms trying to be everything for everyone. A vertical platform for trading educators with a B2B2C model (instructors bring the audience) has fundamentally different unit economics — the instructor bears the CAC, the platform provides the technology.
- **Known ICT-specific competitors:** Price Action Lover (direct ICT AI competitor using Claude), ICT GPT (free ChatGPT variants), LuxAlgo (800K+ TradingView users, ICT-specific indicators), n8n ICT bot (open-source). All are single products for one methodology — none is a platform that serves multiple instructors.
