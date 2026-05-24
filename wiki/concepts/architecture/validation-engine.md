---
tags: [architecture, validation, quality-gates, evidence]
created: 2026-05-23
updated: 2026-05-23
---

# Validation Engine

`engine/validation.py` — auto-checks session output against acceptance criteria after completion.

## How It Works

1. Session completes (status = succeeded)
2. `default_checks(session)` auto-detects project type:
   - Python (`pyproject.toml`/`setup.py`) → runs `python -m pytest`
   - Node (`package.json`) → runs `npm test`
   - File existence → verifies `files_changed` still exist
3. `run_validation(session, checks)` executes each check in the worktree
4. `apply_to_quality_gates(session, report)` auto-populates `tests_pass`, `compiles`, `requirements_met`
5. Results stored as `{data_dir}/validations/{sid}.json`

## Pipeline Integration

For pipeline sessions, validation runs BEFORE `handle_stage_complete()`. If validation fails, `success=False` propagates — downstream stages get blocked. This replaces manual quality gate checking.

Gate type `validation` auto-approves if upstream session validation passed; otherwise requires manual override.

## Evidence Linking

Validation results are stored as evidence records via `memory.add_evidence()` with type `validation_record`, linking to the project's memory store.

## API

- `GET /api/sessions/{sid}/validation` — retrieve validation report
- `POST /api/sessions/{sid}/validate` — re-run validation manually

## Related

- [[session-lifecycle]] — completion callback flow
- [[DEC-001-per-session-callbacks]] — per-session callbacks enable validation hooking
