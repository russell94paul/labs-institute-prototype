# Parallelization Status

## Current Phase: Bootstrap Console Complete — P0 Pipeline DAG Next

### Eligible Now

| Work item | Status | Branch | Notes |
|-----------|--------|--------|-------|
| P0 Pipeline DAG Engine | Eligible (approval-gated) | `conductor/p0-pipeline-engine` | Core engine — blocks all downstream |
| Deep Research Topic 01 (Multi-Tenant SaaS) | Ready to start | N/A | Manual ChatGPT |
| Deep Research Topic 02 (Agent Orchestration) | Ready to start | N/A | Manual ChatGPT |
| Deep Research Topic 08 (Hybrid Context Fabric) | Ready to start | N/A | Manual ChatGPT |

### Safe to Parallelize

| Work A | Work B | Reason |
|--------|--------|--------|
| Deep Research Topics | P0 Pipeline DAG design/planning | Research is docs-only, no code overlap |
| Service inventory fill-in | P0 Pipeline DAG design/planning | Manual input vs. code work |

### Must Serialize

| Work item | Reason |
|-----------|--------|
| P0 Pipeline DAG Engine | Core engine — touches engine/pipelines.py, engine/phases.py |
| P0 Event System | Depends on P0 Pipeline DAG completion |
| P1 Build Studio | Depends on P0 Pipeline DAG + P0 Events |
| P2 Product Onboarding | Depends on P1 Build Studio |

### Blocked and Why

| Work item | Blocked by | Missing |
|-----------|-----------|---------|
| P0-events | P0-pipeline-dag | P0 Pipeline DAG Engine not started |
| P1-build-studio | P0-pipeline-dag, P0-events | Both prerequisites not started |
| P2-onboarding | P1-build-studio | Build Studio not started |

### Autonomous / Parallel Execution Hold

**Autonomous and parallel execution should remain limited until P0.5 (Repo Work Guard, Session Lock, and Execution Queue) is implemented.** P0.5 adds the repo-level lock, dirty-tree gate, commit checkpoints, and queue model needed to safely run concurrent or autonomous tasks. Until then:

- Only one code-modifying session at a time.
- Research ingestion is safe only if it touches docs-only paths and no config files.
- Manual edits must be committed before starting any autonomous phase.

See: `docs/architecture/repo-work-guard-session-lock.md`, `docs/decisions/ADR-0009-repo-work-guard-session-lock.md`

### Recommended Max Concurrency

**2** — One code implementation track + one research/docs track (non-overlapping paths only)

### Next 3 Recommended Actions

1. **Review and approve P0.5 Work Guard ADR** — safety layer before autonomous execution
2. **Implement P0.5 minimal Work Guard** — enables safe parallel and autonomous work
3. **Run Deep Research Topics 03–07** — unblocks synthesis for downstream phases
