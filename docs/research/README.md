# Research System

This directory contains the research intake, synthesis, and decision workflow for Conductor's platform rebuild.

## Workflow

### 1. Pick a topic
Browse `docs/research/prompts/` and pick the next priority topic from `research-status.md`.

### 2. Copy the prompt
Open the prompt file (e.g., `prompts/01-multi-tenant-saas-rls-client-portals.md`) and copy the Deep Research prompt section.

### 3. Run ChatGPT Deep Research
Paste the prompt into ChatGPT Deep Research and run it. Wait for the full report.

### 4. Save the output
Save the result as a markdown file using the expected filename listed in the prompt file:

```
local-inputs/research-inbox/01-multi-tenant-saas-rls-client-portals.report.md
```

### 5. Ingest with Claude
In Claude Code, run the ingestion prompt:

```
docs/prompts/ingest-new-research-output.md
```

Claude will:
- Read the report from `local-inputs/research-inbox/`
- Create a synthesis in `docs/research/syntheses/`
- Extract key findings, architecture implications, risks, and decisions
- Update `research-index.md` and `research-status.md`
- Update `config/research-topics.json`
- Create decision candidates in `docs/research/decisions/`

### 6. Review the synthesis
Read the synthesis file Claude created. Verify findings, flag disagreements, and approve or reject.

### 7. Synthesize into roadmap
After multiple topics are completed, run:

```
docs/prompts/synthesize-research-into-roadmap.md
```

This turns syntheses into roadmap updates, phase dependencies, and implementation recommendations.

## Directory Structure

```
docs/research/
├── README.md              ← you are here
├── research-index.md      ← index of all research topics and their outputs
├── research-status.md     ← kanban-style status board
├── synthesis-log.md       ← log of all synthesis operations
├── prompts/               ← Deep Research prompts (copy into ChatGPT)
│   ├── 01-multi-tenant-saas-rls-client-portals.md
│   ├── 02-agent-orchestration-dag-parallelization.md
│   ├── 03-ai-product-onboarding-decision-simulation.md
│   ├── 04-data-platform-modernization-factory.md
│   ├── 05-context-memory-vector-db-self-improvement.md
│   ├── 06-secure-credential-artifact-workflows.md
│   ├── 07-market-intelligence-growth-engine.md
│   └── 08-hybrid-context-fabric-wiki-memory-knowledge-graph.md
├── syntheses/             ← Claude-generated synthesis outputs
│   └── README.md
└── decisions/             ← Decision candidates extracted from research
    └── README.md
```

## Related Files

- `config/research-topics.json` — machine-readable topic registry
- `local-inputs/research-inbox/` — raw research outputs (gitignored)
- `docs/prompts/ingest-new-research-output.md` — ingestion prompt
- `docs/prompts/synthesize-research-into-roadmap.md` — roadmap synthesis prompt
- `docs/inputs/09-questions-for-deep-research.md` — source questions
