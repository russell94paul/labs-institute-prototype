# ADR: Bootstrap Orchestration Console

**Status**: Accepted
**Date**: 2026-05-18
**Phase**: 00-bootstrap

## Context

Conductor needs a way to track its own build progress before the full Build Studio (P1) exists. Without visibility into phase status, dependencies, and eligible work, build coordination relies entirely on reading markdown files and manual tracking.

## Decision

Build a lightweight Bootstrap Orchestration Console as a temporary internal tool that:

1. Reads phase data from `config/phase-status.json`
2. Computes dependencies, eligibility, and critical path via `engine/bootstrap.py`
3. Exposes phase data through REST API endpoints
4. Renders a tabbed dashboard page at `#bootstrap` with 10 views

## Architecture Choices

- **Backend dependency engine** (`engine/bootstrap.py`) rather than frontend-only JS — enables API consumers and future automation
- **Vanilla HTML/CSS/JS** matching the existing SPA pattern — no new framework dependencies
- **JSON file persistence** via atomic writes — consistent with existing data layer pattern
- **REST API** following existing handler pattern in `server.py` — no new routing library
- **Assisted mode only** — console recommends but does not auto-execute

## Alternatives Considered

1. **Frontend-only (no API)**: Simpler but prevents future automation/integration
2. **Full Build Studio now**: Too early — dependencies (P0 Pipeline DAG, P0 Events) not built yet
3. **CLI-only tool**: Useful but misses the visual DAG/status overview value
4. **Separate micro-service**: Overkill for internal build tracking

## Consequences

- Build progress is visible and trackable through the dashboard
- Future Build Studio can reuse or replace the bootstrap engine
- Phase status changes are API-driven, enabling automation later
- Console is intentionally limited — does not auto-merge, auto-deploy, or auto-rollback
