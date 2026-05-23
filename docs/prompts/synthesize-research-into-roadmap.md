# Prompt: Synthesize Research into Roadmap

Run this prompt in Claude Code after multiple research topics have been synthesized and reviewed. This turns research findings into actionable roadmap updates.

## Prerequisites

- At least 2-3 research topics should be in "Synthesized" status
- Syntheses should be reviewed and approved by a human

## Prompt

Copy and paste the following into Claude Code:

---

Read all completed synthesis files in `docs/research/syntheses/` and all decision files in `docs/research/decisions/`.

Cross-reference them with:
- `docs/inputs/01-product-vision.md` (product direction)
- `docs/inputs/08-demo-script.md` (demo requirements)
- `config/research-topics.json` (dependencies and priorities)

Then produce the following updates:

1. **Roadmap updates** — Update or create `docs/build/roadmap.md` with:
   - Phases derived from research recommendations
   - Phase dependencies (what must come before what)
   - Estimated complexity per phase (S/M/L/XL)
   - Which research topics inform each phase
   - Open questions that block phase start

2. **Phase dependency updates** — Update or create `docs/build/phase-dependencies.md` with a dependency graph showing which phases can run in parallel and which are sequential.

3. **Module registry recommendations** — Update or create `docs/build/module-registry.md` listing all engine modules, dashboard pages, and infrastructure components that research says we need. For each, note: status (exists, needs changes, new), which research informed it, and priority.

4. **Risk register updates** — Update or create `docs/build/risk-register.md` with all risks identified across syntheses. For each: description, likelihood, impact, mitigation, owner, status.

5. **Acceptance criteria updates** — Review `docs/build/acceptance-criteria.md` and update with any new criteria from research.

6. **Update research status** — Move synthesized topics to "Applied to Roadmap" in `docs/research/research-status.md`.

**Do NOT:**
- Modify any code in `engine/`, `dashboard/`, or `templates/`
- Make implementation changes
- Create PRs or commits
- Change anything without explaining why

**Require human review** before any synthesis conclusions override existing product decisions in `docs/inputs/`.

After processing, report:
- Summary of roadmap changes
- New phases added
- Dependencies identified
- Top 5 risks
- Decisions still pending
- Recommended next actions

---
