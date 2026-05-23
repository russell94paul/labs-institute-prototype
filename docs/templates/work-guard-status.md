# Work Guard Status Report

**Generated:** {{timestamp}}
**Repo:** {{repoPath}}

## Active Lock

| Field | Value |
|-------|-------|
| Lock ID | {{lockId}} |
| Status | {{lockStatus}} |
| Owner | {{owner}} |
| Session Type | {{sessionType}} |
| Phase | {{phaseId}} |
| Branch | {{branch}} |
| Started | {{startedAt}} |
| Last Heartbeat | {{lastHeartbeatAt}} |
| Stale? | {{isStale}} |

## Git State

| Check | Result |
|-------|--------|
| Current Branch | {{branch}} |
| Working Tree | {{cleanOrDirty}} |
| Dirty Files | {{dirtyFileCount}} |
| Latest Commit | {{latestCommitHash}} — {{latestCommitMessage}} |
| Commit Since Phase Start | {{commitAdvanced}} |

## Current Phase

| Field | Value |
|-------|-------|
| Phase ID | {{currentPhaseId}} |
| Phase Name | {{currentPhaseName}} |
| Phase Status | {{currentPhaseStatus}} |
| Commit Required Before Next | {{commitRequired}} |

## Queued Jobs

| # | Job ID | Type | Requested By | Priority | Status | Reason |
|---|--------|------|-------------|----------|--------|--------|
| {{index}} | {{jobId}} | {{sessionType}} | {{requestedBy}} | {{priority}} | {{status}} | {{reason}} |

## Stale Lock Check

| Check | Result |
|-------|--------|
| Last Heartbeat Age | {{heartbeatAgeMinutes}} minutes |
| Timeout Threshold | {{heartbeatTimeoutMinutes}} minutes |
| PID ({{pid}}) Alive? | {{pidAlive}} |
| Stale Lock Detected | {{staleLockDetected}} |
| Recovery Action | {{recoveryAction}} |

## Safe to Run?

| Check | Pass? | Detail |
|-------|-------|--------|
| No active lock | {{noActiveLock}} | {{lockDetail}} |
| Clean working tree | {{cleanTree}} | {{treeDetail}} |
| Previous phase committed | {{prevCommitted}} | {{commitDetail}} |
| No path overlap | {{noPathOverlap}} | {{overlapDetail}} |
| No stale lock | {{noStaleLock}} | {{staleDetail}} |
| **Overall: safeToRun** | **{{safeToRun}}** | |

## Recommended Action

{{recommendedAction}}
