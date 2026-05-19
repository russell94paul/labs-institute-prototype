# Prompt: Ingest New Research Output

Run this prompt in Claude Code after adding one or more Deep Research output files to `local-inputs/research-inbox/`.

## Prompt

Copy and paste the following into Claude Code:

---

Scan `local-inputs/research-inbox/` for new `.md` research output files that have not yet been synthesized.

For each new file found:

1. **Read the full report.** Do not skim — read every section.

2. **Security check.** If the file contains any raw credentials, API keys, connection strings, passwords, tokens, or secrets: stop processing that file immediately, warn me, and move on to the next file.

3. **Create a synthesis** in `docs/research/syntheses/` with the naming convention `{topic-number}-{topic-slug}-synthesis.md`. Extract:
   - **Key findings** — the 5-10 most important insights
   - **Architecture implications** — how this affects Conductor's architecture
   - **Roadmap implications** — what phases, timelines, or priorities change
   - **New risks** — risks we didn't know about before
   - **New decisions required** — decisions that must be made before implementation
   - **Implementation recommendations** — specific, actionable next steps
   - **Phase changes** — any changes to the build phase structure
   - **Open questions** — what we still don't know

4. **Update `docs/research/research-index.md`** — add the output file link and synthesis link to the topic's row.

5. **Update `docs/research/research-status.md`** — move the topic from "Pending" or "Running" to "Completed — Not Synthesized" (if just saving) or "Synthesized" (after synthesis is written).

6. **Update `config/research-topics.json`** — set status to "synthesized", update lastUpdated.

7. **Update `docs/research/synthesis-log.md`** — add a row with the date, topic, synthesis file, key findings summary, and number of decisions created.

8. **Create decision candidates** in `docs/research/decisions/` for each major decision identified. Use the format in `docs/research/decisions/README.md`. Number decisions sequentially (DEC-001, DEC-002, etc.).

**Do NOT:**
- Modify any code in `engine/`, `dashboard/`, or `templates/`
- Install dependencies
- Run any deployment commands
- Store or echo any secrets found in research files
- Delete the raw research file from `local-inputs/research-inbox/`

**After processing all files, report:**
- Which files were processed
- Which syntheses were created
- Which decisions were extracted
- What the recommended next research topic is (based on `config/research-topics.json` dependencies and priorities)

---
