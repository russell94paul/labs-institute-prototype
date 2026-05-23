# Deep Research Prompt: Agent Orchestration, DAGs & Parallelization

## Purpose

Research modern approaches for building an agent orchestration platform with DAG-based pipeline execution, informing Conductor's pipeline engine, phase manager, and build orchestration architecture.

## When to Run

Run this first (Priority 1, tied with Topic 1). The orchestration engine is Conductor's core differentiator.

## Deep Research Prompt

Copy the following into ChatGPT Deep Research:

---

**Research modern approaches for building an agent orchestration platform with phase DAGs, task DAGs, dependency resolution, parallel execution, branch/worktree isolation, approval gates, rollback, event streams, and progress dashboards.**

Context: I'm building a product orchestration platform (called "Conductor") that manages the full lifecycle of software products. The platform uses AI agents (Claude Code sessions) and human developers to execute work organized into phases and tasks.

Current architecture:
- Phases are defined in markdown files with frontmatter (goal, deliverables, constraints, acceptance criteria)
- Pipelines are defined in YAML with stage sequences and dependencies
- Each pipeline stage runs a Claude Code session with a specific prompt
- All stages in a pipeline share one git worktree
- Sessions have quality gates: compiles, tests_pass, requirements_met, no_security_issues
- State is persisted as JSON files
- Backend is Python, frontend is vanilla HTML/CSS/JS SPA

I need to understand:

1. **Phase DAG design** — how to model product development phases as a DAG where some phases can run in parallel and others have strict dependencies. How to handle phases that produce artifacts consumed by downstream phases. How to model phase completion criteria that go beyond simple pass/fail.

2. **Task DAG within phases** — how to break phases into granular tasks with their own dependency graph. How tasks map to agent sessions, PRs, and deployments. How to handle tasks that require human approval before downstream tasks can proceed.

3. **Dependency resolution** — algorithms and data structures for resolving dependencies in a DAG. How to detect cycles, handle optional dependencies, and support dynamic dependencies that emerge during execution. How to handle partial failures (some dependencies succeed, others fail).

4. **Parallel execution** — how to determine which tasks can run in parallel safely. Concurrency limits. Resource contention (multiple agents editing the same codebase). How git branch/worktree isolation enables safe parallelism. Merge strategies for parallel work.

5. **Branch/worktree isolation** — how to use git worktrees to isolate parallel agent work. Worktree lifecycle (create, work, merge, cleanup). How to handle merge conflicts between parallel worktrees. Shared vs. isolated worktrees for dependent tasks.

6. **Approval gates** — patterns for inserting human approval checkpoints into automated pipelines. How to pause execution, notify the approver, handle timeouts, and resume after approval. Multi-approver patterns. Conditional approvals.

7. **Rollback** — strategies for rolling back failed phases or tasks. How to determine rollback scope (just the failed task? the entire phase? dependent phases?). Automated vs. manual rollback. Rollback testing.

8. **Event streams** — how to emit real-time events from pipeline execution for dashboards, logging, and external integrations. Event schemas. Ordering guarantees. How to reconstruct pipeline state from events.

9. **Progress dashboards** — how to visualize DAG execution in real time. UI patterns for showing running, completed, failed, and blocked tasks. How to show parallel execution. How to surface blockers and required actions.

Provide your output as a structured report with:
- Architecture options (at least 3, with trade-offs)
- Dependency model (data structures, resolution algorithm)
- Parallelization rules (when it's safe, when it's not)
- Event model (schema, delivery, ordering)
- Branch/worktree strategy
- Approval/rollback strategy
- Recommended MVP implementation plan (what to build first)

Reference existing orchestration systems: Temporal, Prefect, Airflow, GitHub Actions, Argo Workflows, Tekton. Compare approaches and identify what to borrow vs. build.

---

## Expected Output Filename

`02-agent-orchestration-dag-parallelization.report.md`

## Required Save Location

`local-inputs/research-inbox/`

## How Claude Should Ingest It

Run the prompt in `docs/prompts/ingest-new-research-output.md` after saving the file to the inbox.

## Decision Areas This Affects

- Pipeline engine architecture (`engine/pipelines.py`)
- Phase manager design (`engine/phases.py`)
- Agent dispatch model (`engine/agents.py`)
- Git worktree strategy
- Dashboard DAG visualization
- Quality gate design
- Event/notification system
