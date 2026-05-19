# Local Inputs

This directory contains local-only files that are not committed to git.

## Contents

- `research-inbox/` — Drop zone for raw Deep Research outputs. Files here are gitignored.

## Workflow

1. Run a Deep Research prompt from `docs/research/prompts/`
2. Save the output to `local-inputs/research-inbox/` using the expected filename
3. Run the ingestion prompt from `docs/prompts/ingest-new-research-output.md` in Claude Code
4. Claude will process the raw output and create committed synthesis files

## Security

- Do NOT place credentials, API keys, or secrets in any file here
- Raw research outputs may contain sensitive architectural details — review before sharing
- The inbox is gitignored to prevent accidental commits of large raw files
