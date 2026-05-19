# Prompt: P0 Pipeline DAG Engine

You are an autonomous engineering/product agent working in the Conductor repo. Preserve existing functionality. Do not perform destructive git operations. Do not expose secrets. Do not ingest raw client data. Prefer local-first, testable changes. Write build reports under docs/build/. Stop at the requested phase.


## Mission
Implement pipeline DAG engine, stage lifecycle, pipeline templates, session integration, failure/retry/cancellation, and pipeline reports.

## Inspect
server.py, sessions.py, git_ops.py, agent definitions, pipeline templates, UI board/dashboard files.

## States
Pipeline and stage states: pending, ready, running, blocked, waiting_for_approval, completed, failed, cancelled. Stages may also be skipped.

## API
create_pipeline, start_pipeline, cancel_pipeline, retry_stage, get_pipeline, list_pipelines, advance_pipeline, handle_stage_complete, calculate_ready_stages.

## Acceptance
Standard pipeline can run through existing sessions; failures block downstream; retry/cancel work; standalone sessions still work.
