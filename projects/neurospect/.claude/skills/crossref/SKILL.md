---
name: crossref
description: "Search across all wikis (team wiki, personal wikis) for content relevant to current work or a specific topic."
---

# /crossref — Cross-Wiki Intelligence Search

## Usage
```
/crossref                    # Search other wikis for content relevant to current work
/crossref "order blocks"     # Search for a specific topic across all wikis
/crossref --phase 7          # Search for content relevant to Phase 7
```

## What This Skill Does

Searches across all knowledge sources (wiki/, vlad-wiki/, paul-wiki/, roadmap/) for content relevant to the current context or a specific query. Surfaces content from the other engineer's wiki that you might not know exists.

## Steps

### 1. Determine Search Context

If `$ARGUMENTS` contains a quoted string, use that as the search query.

If `$ARGUMENTS` contains `--phase N`, search for content relevant to Phase N.

If no arguments, infer context from:
- Current working directory
- Recently modified files (`git diff --name-only HEAD~3..HEAD`)
- Active phase (from `roadmap/status.md`)

Build a search query from the inferred context. For example, if recent commits touch `api/app/backtest/ict_detectors.py`, the search terms would be: "FVG detector", "order block detection", "swing classification", "ICT patterns".

### 2. Search All Wikis

Search across all markdown files in:
- `wiki/` — team knowledge base
- `vlad-wiki/` — Vlad's personal wiki
- `paul-wiki/` — Paul's personal wiki
- `roadmap/` — phase definitions and deviations

For each wiki, search:
- **Filename match** — does the file name contain the search terms?
- **Content match** — does the file body contain the search terms? (grep)
- **Tag match** — does the YAML frontmatter tags contain the search terms?
- **Heading match** — do any `##` headings contain the search terms?

### 3. Rank Results

Rank results by relevance:
1. Exact term match in heading or filename (highest)
2. Tag match in frontmatter
3. Content match (multiple occurrences ranked higher)
4. Recency (recently updated files ranked higher)

Group by wiki source:
```
=== From paul-wiki (other engineer) ===
  paul-wiki/research/fvg-edge-cases.md (updated 2026-05-08)
    Heading match: "## FVG Detection Edge Cases"
    Excerpt: "FVGs that form during low-volume periods should be treated differently..."

  paul-wiki/phases/phase-7-backtesting/tickets/NEU-045-fvg-detector/README.md
    Tag match: [fvg, detector, backtesting]
    Excerpt: "Decided to use 3-candle strict rule, not the relaxed 5-candle variant..."

=== From wiki (team knowledge) ===
  wiki/concepts/business-logic/ict-liquidity.md (updated 2026-04-22)
    Content match: "Fair Value Gaps" (12 occurrences)
    
  wiki/concepts/entry-models/consolidation-model.md
    YAML block contains FVG conditions

=== From roadmap ===
  roadmap/phases/phase-7-backtesting/deviations.md
    Deviation: "FVG detector uses strict 3-candle rule per Paul's research"
```

### 4. Surface Actionable Insights

Beyond just listing matches, identify actionable connections:

- **Decision already made:** "Paul decided X in his ticket notes — you should use the same approach"
- **Potential conflict:** "Your implementation assumes X but Paul's research notes suggest Y"
- **Missing context:** "The team wiki defines this concept but you haven't referenced it in your implementation notes"
- **Promoted content:** If a personal wiki page has `promote: true`, flag it: "This page is marked for promotion to the team wiki — it may become the canonical reference"

### 5. Output Format

```
Cross-Wiki Search Results for: "FVG detection"
═══════════════════════════════════════════════

📋 From paul-wiki (2 results):
  1. research/fvg-edge-cases.md (updated 2 days ago)
     "FVGs that form during low-volume periods..."
     → May affect your FVG detector implementation

  2. phases/phase-7/tickets/NEU-045/README.md
     Decision: strict 3-candle rule chosen
     → Use the same rule in your detector

📚 From wiki (3 results):
  1. concepts/business-logic/ict-liquidity.md
     Canonical FVG definition (BISI/SIBI, IOFED, BAG)

  2. concepts/entry-models/consolidation-model.md
     YAML strategy block with FVG conditions

  3. concepts/course/module-1-foundations/lesson-2-fvg.md
     Full FVG lesson with worked examples

🗺️ From roadmap (1 result):
  1. phases/phase-7-backtesting/deviations.md
     Deviation captured: strict 3-candle FVG rule

No conflicts detected.
```

### 6. Suggest Follow-Up

If relevant cross-wiki content was found, suggest:
- Reading specific files for context
- Updating your own implementation notes to reference the findings
- Discussing with the other engineer if a potential conflict was detected
