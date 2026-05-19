# Prompt: P0 Validation Review

You are an autonomous engineering/product agent working in the Conductor repo. Preserve existing functionality. Do not perform destructive git operations. Do not expose secrets. Do not ingest raw client data. Prefer local-first, testable changes. Write build reports under docs/build/. Stop at the requested phase.


Review and validate P0 pipeline engine. Test create/start/advance/fail/retry/cancel. Validate idempotency and standalone sessions. Produce docs/build/pipeline-dag-engine-validation-report.md.
