---
name: lint
description: "Cross-artifact consistency check. Detects drift between CLAUDE.md files, roadmap phases, status dashboard, plan.md, skill mappings, and product naming. Run at end of every session."
---

# /lint — Cross-Artifact Consistency Check

## Usage
```
/lint              # Full lint: all checks
/lint phases       # Only check phase consistency
/lint naming       # Only check product/component naming
/lint refs         # Only check file references and wikilinks
/lint frontmatter  # Only check YAML frontmatter validity
```

## Why This Skill Exists

The NeuroSpect roadmap is a living system — phases get added, renamed, and reorganized as ideas evolve. Multiple files reference the same phases, components, and structure:

- Root `CLAUDE.md` has a phase table and product hierarchy
- `roadmap/CLAUDE.md` has a track/gate table
- `roadmap/status.md` has a status dashboard
- `roadmap/plan.md` has the master plan
- `.claude/skills/phase/SKILL.md` has slug mappings
- `.claude/skills/sync/SKILL.md` has gate definitions
- 17 phase directories each have README.md with frontmatter
- Personal wikis reference phases

When one file changes, the others can silently drift. This skill catches that drift before it becomes confusion.

**This is not the same as `/sync`.** `/sync` is session-scoped — it updates tickets, boot prompts, and deviations based on what changed *this session*. `/lint` is repo-scoped — it checks whether all artifacts agree with each other *right now*, regardless of what changed.

## Steps

### 1. Phase Table Consistency

Check that these three sources list identical phases:

**Source files:**
- Root `CLAUDE.md` → the `## Roadmap Phases` table
- `roadmap/status.md` → the status dashboard table(s)
- `roadmap/CLAUDE.md` → the `## Tracks` table

**For each source, extract:**
- Phase number
- Phase name
- Track assignment

**Check:**
- All three sources list the same phase numbers
- Phase names match exactly across all sources
- Track assignments match
- No phase exists in one source but not the others

**Report:**
```
✓ Phase tables consistent (17 phases across 3 sources)
```
or
```
✗ Phase 4: root CLAUDE.md says "Evaluation & Reliability" but status.md says "Evaluation, Reliability & Prompt Infrastructure"
✗ Phase 14 missing from roadmap/CLAUDE.md tracks table
```

### 2. Phase Directory Completeness

**Check that every phase in the tables has a matching directory:**
- `roadmap/phases/phase-{N}-{slug}/` exists
- Contains `README.md`
- Contains `deviations.md`
- Contains `boot-prompts/planning.md`
- Contains `boot-prompts/execution.md`

**Check for orphan directories:**
- Every directory under `roadmap/phases/` corresponds to a phase in the tables

**Check that `/phase` skill slug mapping covers all directories:**
- Read `.claude/skills/phase/SKILL.md`
- Extract the slug mapping lines
- Verify every phase directory has a mapping entry

**Report:**
```
✓ All 17 phases have complete directories
✓ Skill slug mapping covers all phases
```
or
```
✗ phase-14-retention/ missing boot-prompts/execution.md
✗ Phase 16 has directory but no entry in /phase skill slug mapping
⚠ Orphan directory: roadmap/phases/phase-99-experimental/ has no table entry
```

### 3. Product Hierarchy & Naming Consistency

The product hierarchy (component names, descriptions) appears in multiple places. Check for naming drift.

**Source of truth:** Root `CLAUDE.md` → `## Product Hierarchy`

**Check these files for conflicting names:**
- `roadmap/plan.md`
- `initial-plan/v2-neurollm-plan.md`
- `NeuroLLM.md`
- `wiki/` pages that reference components
- Phase READMEs that reference components

**Known component names to check (from root CLAUDE.md):**

| Canonical Name | Common Variants to Flag |
|---|---|
| NeuroSpect Mentor | NeuroSpect Coach, Coach, Mentor |
| NeuroCore | NeuroCortex, Knowledge Layer |
| NSLM | NeuroLLM (when referring to the model, not the plan doc) |
| NeuroSpect EdgeLab | EdgeLab, Backtesting Platform |
| NeuroQuant | Quant, Hybrid Model Layer |
| NeuroTrader Agent | NeuroTrader, Trading Agent |

**Scan method:** For each canonical name and its variants, grep across all `.md` files. If a variant appears in a file that should use the canonical name, flag it.

**Exception:** `initial-plan/` and `NeuroLLM.md` are historical documents — flag naming differences as informational (⚠), not errors (✗).

**Report:**
```
✓ Product naming consistent across active documents
⚠ NeuroLLM.md uses "NeuroSpect Coach" (historical — canonical is "NeuroSpect Mentor")
```
or
```
✗ roadmap/plan.md line 42: uses "NeuroCortex" but canonical name is "NeuroCore"
✗ wiki/architecture/knowledge-layer.md: uses "NeuroSpect Coach" — should be "NeuroSpect Mentor"
⚠ initial-plan/v2-neurollm-plan.md uses "NeuroSpect Coach" (historical, informational only)
```

### 4. Frontmatter Validation

Check YAML frontmatter on all phase READMEs.

**Required fields for phase READMEs:**
```yaml
phase: <number>
name: <string>
status: <not_started | planning | in_progress | review | complete>
track: <string>
assigned: <array>
started: <date or null>
completed: <date or null>
tickets_total: <number>
tickets_done: <number>
created: <date>
updated: <date>
```

**Track C phases additionally have:**
```yaml
parallel_with: <array of phase numbers>
gates: <array of phase numbers>
```

**Check:**
- All required fields present
- `status` is a valid enum value
- `phase` number matches directory name
- `tickets_done` <= `tickets_total`
- `started` is set if status is `in_progress` or later
- `completed` is set if status is `complete`
- Dates are valid ISO format (YYYY-MM-DD)
- `updated` is not more than 30 days old for `in_progress` phases (flag as potentially stale)

**Report:**
```
✓ All 17 phase READMEs have valid frontmatter
```
or
```
✗ Phase 11 README: missing required field "tickets_total"
⚠ Phase 2 README: status is "in_progress" but "started" is null
⚠ Phase 0 README: updated 2026-05-10, last modified 35 days ago — may be stale
```

### 5. Cross-Track Gate Integrity

Verify that gate declarations are consistent across all sources.

**Sources that declare gates:**
- Track C phase READMEs (in `gates:` frontmatter and `## Dependencies` section)
- `roadmap/CLAUDE.md` gate table
- `roadmap/status.md` cross-track dependencies table
- `.claude/skills/sync/SKILL.md` Step 8 gate table

**Check:**
- All four sources agree on which business phases gate which engineering phases
- No gate is declared in one source but missing from another
- Gate conditions described in the sync skill match the deliverables in the phase README

**Report:**
```
✓ Cross-track gates consistent across 4 sources
```
or
```
✗ Phase 12 gates Phase 9 (per README) but sync skill only lists Phase 3 as gated
✗ roadmap/CLAUDE.md says Phase 13 gates Phase 6, but status.md cross-track table is missing this entry
```

### 6. File Reference & Wikilink Validation

Check that file paths and cross-references in markdown files point to real files.

**Scan these files for references:**
- Root `CLAUDE.md`
- `roadmap/CLAUDE.md`
- `roadmap/plan.md`
- All phase READMEs
- Skill files (`.claude/skills/*/SKILL.md`)

**Check:**
- Backtick-quoted file paths (e.g., `api/app/coach/rag/`) → verify directory/file exists
- Markdown links `[text](path)` → verify target exists
- `[[wikilinks]]` within personal wikis → verify target exists in same wiki

**Exceptions:**
- Future file paths in phase READMEs for phases not yet started are expected to not exist — flag as informational (ℹ), not errors
- External URLs are skipped (no HTTP checks)

**Report:**
```
✓ All file references in active documents resolve
ℹ Phase 7 README references api/app/backtest/ — does not exist yet (phase not started, expected)
```
or
```
✗ roadmap/CLAUDE.md references roadmap/phases/phase-7-backtesting/ but directory is phase-7-edgelab/
✗ Root CLAUDE.md references wiki/CLAUDE.md but file does not exist
```

### 7. Staleness Detection

Flag artifacts that may be outdated based on file modification times and cross-references.

**Check:**
- Phase READMEs for `in_progress` phases: warn if not modified in 14+ days
- `roadmap/status.md`: warn if not modified in 7+ days (should be updated by `/sync`)
- Boot prompts for active phases: warn if older than the phase README they were generated from
- Track C phase READMEs: warn if the parallel engineering phase has progressed but the business phase hasn't been updated

**Report:**
```
⚠ roadmap/status.md last modified 12 days ago — run /sync to update
⚠ Phase 0 boot-prompts/execution.md is older than Phase 0 README.md — regenerate with /sync
⚠ Phase 11 (Content Licensing) hasn't been updated since creation, but Phase 0 (parallel) is in_progress
```

### 8. Completed Phase Re-Sync Check

Completed phases have boot prompts that were generated at completion time. Later changes — new phases, expanded scope, renamed components, new deviations — can make those boot prompts stale in a way that matters for integration.

**Why this matters:** A completed phase's boot prompt is the context future sessions use to understand what was built and how. If Phase 4 adds a prompt versioning module after Phase 1 was completed, Phase 1's boot prompt won't mention that the RAG pipeline should have been designed with prompt versioning in mind — or that the retrieval layer interfaces need to support versioned prompts. The next engineer loading `/phase 1` context gets an incomplete picture.

**For each completed phase:**

1. **Read its boot prompt** (`boot-prompts/execution.md`) — note the `_Generated YYYY-MM-DD` date
2. **Read all downstream phase deviations** that were created *after* the boot prompt was generated
3. **Read all phase READMEs that were modified** after the boot prompt date
4. **Check for new phases** that didn't exist when the boot prompt was generated

**Flag for re-sync if any of these are true:**
- A downstream phase added scope that depends on or extends what this phase built (e.g., Phase 4 adds prompt versioning that touches Phase 1's retrieval layer)
- A component was renamed after the phase completed (boot prompt uses old name)
- A new deviation in a *peer or downstream* phase changes assumptions about what this phase delivered
- A new Track C gate was added that retroactively applies to this phase

**Report format:**
```
⚠ Re-sync recommended for completed phases:

  Phase 1 (RAG MVP) — boot prompt generated 2026-06-15
    → Phase 4 expanded (2026-05-10): prompt versioning module added. Phase 1's 
      RAG pipeline may need versioned prompt support documented in its boot prompt.
    → Phase 7 (EdgeLab) references NeuroCore retrieval interfaces that Phase 1 built.
      Boot prompt should note what EdgeLab will consume.
    Action: run `/sync boot` to regenerate Phase 1 boot prompts with current context.

  Phase 3 (Product MVP) — boot prompt generated 2026-07-20
    → Component renamed: "NeuroSpect Coach" → "NeuroSpect Mentor" (2026-05-10).
      Boot prompt uses old name.
    Action: run `/sync boot` to update naming.
```

**Not flagged:**
- Phases that are `not_started` (no boot prompt to check)
- Phases that are `in_progress` (`/sync` already regenerates these)
- Downstream changes that are purely additive and don't affect what the completed phase built

### 9. Assemble Report

Combine all check results into a single report. Group by severity:

```
/lint Report — 2026-05-10

ERRORS (must fix):
  ✗ [list]

WARNINGS (should review):
  ⚠ [list]

INFO (awareness only):
  ℹ [list]

PASSED:
  ✓ Phase tables consistent (17 phases)
  ✓ All directories complete
  ✓ Frontmatter valid
  ✓ Gates consistent
  ✓ References resolve

Summary: 0 errors, 2 warnings, 1 info, 5 passed
```

If errors are found, offer to fix them:
```
Found 2 errors. Would you like me to fix them? [y/n]
  1. Update status.md Phase 4 name to match CLAUDE.md
  2. Add missing slug mapping for Phase 16 to /phase skill
```

### 10. Auto-Fix (Optional)

If the user accepts fixes, apply them:
- Phase name mismatches → update the non-canonical source to match the canonical source (root `CLAUDE.md` is canonical for product names; phase README is canonical for phase names)
- Missing frontmatter fields → add with sensible defaults
- Missing skill mappings → add to the mapping list
- Stale boot prompts → suggest running `/sync boot`

Never auto-fix:
- Gate declarations (requires human judgment)
- Product naming in historical docs (`initial-plan/`, `NeuroLLM.md`)
- Phase READMEs content (goals, deliverables, exit criteria)

## End-of-Session Reminder

**This skill must be mentioned in the end-of-session reminder alongside `/sync`.**

The reminder should explain *why*:
> As you work, you add ideas, rename components, and reorganize phases. These changes touch `CLAUDE.md`, `status.md`, phase READMEs, and skill definitions — but not always all of them at once. `/lint` catches that drift before the next session inherits stale or conflicting context.

Format:
```
Before ending this session:
1. /sync  — Update tickets, boot prompts, and phase status from this session's work
2. /lint  — Check that all roadmap artifacts are consistent (phases added/renamed 
   this session may have created drift between CLAUDE.md, status.md, and skill files)
```
