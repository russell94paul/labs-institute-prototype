# F. Context Manager Improvements + G. Memory/Self-Improvement Improvements + H. Conductor Board/Orchestration Improvements

## F. Context Manager Improvements

Conductor's `engine/context.py` is planned but not yet implemented. These recommendations define what it should become.

### Context Sources (prioritized)

| Priority | Source | Content | When to Query |
|----------|--------|---------|---------------|
| 1 | **Local project files** | Project README, phase definitions, prior stage outputs | Every session start |
| 2 | **Session history** | Prior sessions in same pipeline (JSONL outputs) | Every session in a multi-stage pipeline |
| 3 | **Zeus Memory** | Build learnings, failure patterns, architectural decisions | Phase planning, bug fixing, deployment |
| 4 | **Wiki** | Client rules, architecture docs, deployment runbooks | Project initialization, deployment stages |
| 5 | **Git history** | Recent commits, branch state, diff context | Code review, implementation stages |

### Context Assembly Pattern (from ccx + zeus-memory)

```
┌─────────────────────────────────────────────┐
│ Context Assembly Pipeline                    │
│                                              │
│  1. Resolve project → load project.json      │
│  2. Resolve phase → load phase markdown      │
│  3. Query prior stages → extract key outputs │
│  4. Query Zeus Memory (if available):        │
│     - "failures for {tech_stack}"            │
│     - "learnings from {similar_project}"     │
│     - "deployment patterns for {target}"     │
│  5. Query Wiki (if available):               │
│     - Pages matching project tags            │
│     - Deployment runbooks for target env     │
│  6. Assemble context pack (token-budgeted)   │
│  7. Inject into agent prompt template        │
└─────────────────────────────────────────────┘
```

### Token Budget Management

Adopt from ccx/cce pattern: each context source gets a token budget. If the total exceeds the agent's context window minus prompt + output reserve, lower-priority sources are truncated or omitted.

| Source | Max Tokens | Truncation Strategy |
|--------|-----------|---------------------|
| Phase definition | 2,000 | Never truncate |
| Prior stage outputs | 4,000 | Most recent stage first; summarize older |
| Zeus Memory results | 3,000 | Top-K by relevance score |
| Wiki pages | 2,000 | First 2 sections + See Also links |
| Git context | 1,000 | Recent commits only |
| **Total budget** | **12,000** | Adjustable per agent model |

### Stale Context Detection

From wiki's lint operation: flag context that may be outdated.

| Signal | Detection | Action |
|--------|-----------|--------|
| Wiki page `updated:` > 30 days ago | Frontmatter date check | Surface warning: "context may be stale" |
| Zeus Memory item > 90 days old | Timestamp filter | Lower ranking score by 50% |
| Prior stage output from a failed pipeline | Pipeline status check | Exclude unless explicitly requested |
| Git branch behind main by > 20 commits | git rev-list count | Warn: "branch significantly behind main" |

### Conflict Detection

When context from multiple sources disagrees:

1. **Zeus Memory says X; Wiki says Y** — Surface both with source attribution. Let agent/operator decide.
2. **Prior stage output contradicts current code** — Flag as "potential drift" in context pack.
3. **Two Zeus Memory items contradict** — Use content_origin dimension: authoritative > ai_generated > user_contributed.

---

## G. Memory/Self-Improvement Improvements

### Build Memory Lifecycle

Adopt the auto-learn virtuous cycle from ccx/cce, adapted for Conductor's pipeline model:

```
Pipeline Run N
    │
    ├─ Each session produces JSONL output
    │
    ├─ Pipeline completes (success or failure)
    │
    ├─ Post-Pipeline Learning Hook:
    │   ├─ Parse all session JSONLs
    │   ├─ Extract: failures, successes, decisions, timing
    │   ├─ Call Sonnet to synthesize:
    │   │   "What worked, what failed, what to do differently"
    │   ├─ Store in Zeus Memory with tags:
    │   │   project:{slug}, phase:{N}, outcome:{pass|fail}
    │   └─ Store locally in project/learnings.json (offline fallback)
    │
Pipeline Run N+1
    │
    ├─ Context assembly queries Zeus Memory:
    │   "learnings for project:{slug}" → top 5 by relevance
    │
    └─ Agents start with institutional knowledge
```

### Learning Categories (structured extraction)

| Category | Example | Storage |
|----------|---------|---------|
| **Failure** | "Test suite failed because X dependency wasn't mocked" | Zeus: tag=failure, project, phase |
| **Success** | "Worktree isolation prevented merge conflicts in parallel stages" | Zeus: tag=success, project, phase |
| **Decision** | "Chose React over Vue because project had existing React dependencies" | Zeus: tag=decision, project |
| **Timing** | "Review stage took 45 min; budget was 30 min" | Local: session metadata |
| **Cost** | "Pipeline total: $4.20 across 5 stages" | Local: pipeline metadata |

### Self-Improvement Loops

1. **Agent Prompt Refinement:** If a session fails and the failure is attributable to a poor prompt, store the failure + the improved prompt. Next time that agent type runs, the context pack includes "avoid: {failure pattern}; prefer: {improved approach}".

2. **Template Evolution:** Track which pipeline templates produce the best outcomes (pass rate, cost, time). Surface this as a recommendation when creating new pipelines.

3. **Budget Calibration:** Track actual vs budgeted cost/time per stage. After 10 runs, adjust default budgets to match reality.

4. **Gate Learning:** When a quality gate fails and the operator overrides it, store the override reason. If the same gate fails for the same reason repeatedly, suggest a gate rule update.

---

## H. Conductor Board/Orchestration Improvements

### Pipeline View (Priority: P0)

**Reference:** eclipse_exp TaskBoard (Kanban columns), cce Agent TUI (live status cards)

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  PLAN    │ │IMPLEMENT │ │  TEST    │ │ REVIEW   │ │ DEPLOY   │
│          │ │          │ │          │ │          │ │          │
│ ┌──────┐ │ │ ┌──────┐ │ │          │ │          │ │          │
│ │ ses_1│ │ │ │ ses_2│ │ │          │ │          │ │          │
│ │ ✓    │ │ │ │ ◉ 4m │ │ │          │ │          │ │          │
│ │ $0.80│ │ │ │ $2.1 │ │ │          │ │          │ │          │
│ └──────┘ │ │ └──────┘ │ │          │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

Each card shows: session ID, status icon (✓/◉/✗/⏸), runtime, cost. Click → slide-in detail panel.

### Agent Status Dashboard (Priority: P1)

**Reference:** cce agent-tui.py (634 lines)

Show all active sessions in a grid:
- Agent name + model (e.g., "implementer / sonnet")
- Status: running / waiting / complete / failed
- Token usage (input/output)
- Cost accumulation
- Runtime
- Current file being modified (from JSONL output)

### DAG Visualization (Priority: P2)

**Reference:** zeus-memory task_dag_service.py

Render pipeline template as directed graph:
- Nodes = stages (color-coded by status)
- Edges = dependencies
- Critical path highlighted
- Blocked stages show which dependency is pending

### Quality Gate Panel (Priority: P2)

For each session, show the 4 quality gates as a checklist:
- [ ] compiles
- [ ] tests_pass
- [ ] requirements_met
- [ ] no_security_issues

With evidence: test output snippet, review verdict, security scan results. Manual override button for operator.

### Build Timeline (Priority: P3)

Horizontal timeline showing:
- Pipeline stages as segments
- Sessions as blocks within stages
- Color = outcome (green/red/yellow)
- Hover = cost, duration, key outputs

### Context Inspector (Priority: P3)

Debug panel showing what context was assembled for a session:
- Which sources were queried
- What was returned (with token counts)
- What was truncated
- Zeus Memory query + results
- Wiki pages matched

### Orchestration Improvements

1. **Pipeline Resume:** If a pipeline fails at stage 3 of 5, allow resuming from stage 3 without re-running stages 1-2.

2. **Stage Retry with Different Agent:** If an implementer session fails, retry with a different model (Sonnet → Opus) or different budget.

3. **Parallel Stage Dispatch:** When the DAG engine identifies independent stages, dispatch them simultaneously (up to max_parallel limit).

4. **Gate Auto-Advance:** For stages that pass all quality gates, auto-advance to next stage without operator approval (configurable per pipeline template).

5. **Cost Circuit Breaker:** If a pipeline's cumulative cost exceeds 2x the template budget, pause execution and alert operator.

6. **Worktree Health Check:** Before starting a new stage, verify the shared worktree is clean (no uncommitted changes from prior stage, no merge conflicts).
