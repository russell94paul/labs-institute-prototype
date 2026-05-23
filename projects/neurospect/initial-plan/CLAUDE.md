# NeuroLLM Plan Versions

This directory contains versioned product and technical plans for the NeuroLLM project.

## Version History

| Version | Date | Description |
|---|---|---|
| v1 | 2026-05-09 | Initial comprehensive plan covering coaching MVP, backtesting platform, NeuroQuant, NeuroTrader Agent (Phases 0-10) |
| v2 | 2026-05-10 | EdgeLab architecture pivot: Backtesting Platform → NeuroSpect EdgeLab (research/experimentation engine), NeuroCortex → NeuroCore, NeuroSpect Coach → NeuroSpect Mentor, new NSLM component, bidirectional NSLM↔EdgeLab evaluation loop, rewritten Phases 7-8, new pricing tiers, 14 EdgeLab database tables |

## Conventions

- Plans are named `vN-neurollm-plan.md` where N is the version number
- Each new version should document what changed from the previous version at the top
- Previous versions are never modified — create a new version instead
- The latest version is the active plan; previous versions are historical record
- Supplementary docs (architecture deep-dives, research spikes) can live alongside as `vN-topic.md`

## How to Create a New Version

1. Copy the latest version to `vN+1-neurollm-plan.md`
2. Add a changelog section at the top listing what changed
3. Update this README with the new version entry
4. Keep the old version intact
