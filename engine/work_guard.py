"""Work Guard — repo safety checks, session locks, and execution gating."""
from __future__ import annotations

import json
import os
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine import events

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO_ROOT / "config" / "work-guard-policy.json"
PHASE_STATUS_PATH = REPO_ROOT / "config" / "phase-status.json"


def _load_policy() -> Dict[str, Any]:
    if not POLICY_PATH.exists():
        return {}
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _lock_path(repo_path: str) -> Path:
    policy = _load_policy()
    rel = policy.get("lockFilePath", ".conductor/runtime/session-lock.json")
    return Path(repo_path) / rel


def _run_git(repo_path: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + list(args),
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=15,
    )


def check_git_status(repo_path: str) -> Dict[str, Any]:
    """Returns branch, latest commit, clean/dirty state, and dirty file list."""
    branch_result = _run_git(repo_path, "rev-parse", "--abbrev-ref", "HEAD")
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

    commit_result = _run_git(repo_path, "log", "-1", "--format=%H %s")
    if commit_result.returncode == 0 and commit_result.stdout.strip():
        parts = commit_result.stdout.strip().split(" ", 1)
        latest_commit = parts[0]
        commit_message = parts[1] if len(parts) > 1 else ""
    else:
        latest_commit = "unknown"
        commit_message = ""

    status_result = _run_git(repo_path, "status", "--porcelain")
    dirty_files: List[str] = []
    if status_result.returncode == 0 and status_result.stdout.strip():
        for line in status_result.stdout.strip().splitlines():
            if line.strip():
                dirty_files.append(line.strip())

    return {
        "branch": branch,
        "latestCommit": latest_commit[:12],
        "latestCommitFull": latest_commit,
        "commitMessage": commit_message,
        "clean": len(dirty_files) == 0,
        "dirtyFiles": dirty_files,
        "dirtyFileCount": len(dirty_files),
    }


def read_lock(repo_path: str) -> Optional[Dict[str, Any]]:
    """Reads the lock file if it exists, returns parsed JSON or None."""
    lp = _lock_path(repo_path)
    if not lp.exists():
        return None
    try:
        with open(lp, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def acquire_lock(repo_path: str, lock_data: Dict[str, Any]) -> bool:
    """Creates the lock file. Fails if a non-stale lock already exists."""
    lp = _lock_path(repo_path)
    existing = read_lock(repo_path)

    if existing is not None:
        policy = _load_policy()
        timeout = policy.get("heartbeatTimeoutMinutes", 10)
        if not is_stale(existing, timeout):
            return False

    lp.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    lock_data.setdefault("lockId", str(uuid.uuid4()))
    lock_data.setdefault("startedAt", now)
    lock_data.setdefault("lastHeartbeatAt", now)
    lock_data.setdefault("status", "active")
    lock_data.setdefault("pid", os.getpid())
    lock_data.setdefault("repoPath", repo_path)

    tmp = lp.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2, ensure_ascii=False)
    tmp.replace(lp)

    events.emit("work_guard.lock_acquired", {
        "lockId": lock_data.get("lockId"),
        "owner": lock_data.get("owner"),
        "phaseId": lock_data.get("phaseId"),
    }, source="work_guard")

    return True


def release_lock(repo_path: str, lock_id: str) -> bool:
    """Deletes the lock file if lockId matches."""
    lp = _lock_path(repo_path)
    existing = read_lock(repo_path)
    if existing is None:
        return False
    if existing.get("lockId") != lock_id:
        return False
    try:
        lp.unlink()
    except OSError:
        return False

    events.emit("work_guard.lock_released", {"lockId": lock_id}, source="work_guard")

    return True


def update_heartbeat(repo_path: str, lock_id: str) -> bool:
    """Updates lastHeartbeatAt in the lock file."""
    lp = _lock_path(repo_path)
    existing = read_lock(repo_path)
    if existing is None or existing.get("lockId") != lock_id:
        return False

    existing["lastHeartbeatAt"] = datetime.now(timezone.utc).isoformat()

    tmp = lp.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)
    tmp.replace(lp)
    return True


def is_stale(lock_data: Dict[str, Any], timeout_minutes: int) -> bool:
    """Returns True if lastHeartbeatAt is older than timeout_minutes."""
    heartbeat_str = lock_data.get("lastHeartbeatAt")
    if not heartbeat_str:
        return True
    try:
        heartbeat = datetime.fromisoformat(heartbeat_str)
        if heartbeat.tzinfo is None:
            heartbeat = heartbeat.replace(tzinfo=timezone.utc)
        age_minutes = (datetime.now(timezone.utc) - heartbeat).total_seconds() / 60
        return age_minutes > timeout_minutes
    except (ValueError, TypeError):
        return True


def check_pid_alive(pid: int) -> bool:
    """Cross-platform PID liveness check."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def safe_to_run(repo_path: str) -> Dict[str, Any]:
    """Main safety gate. Returns whether it is safe to start a new task."""
    policy = _load_policy()
    git = check_git_status(repo_path)
    lock = read_lock(repo_path)
    timeout = policy.get("heartbeatTimeoutMinutes", 10)

    checks: Dict[str, Any] = {}
    reasons: List[str] = []
    safe = True

    # Check 1: dirty working tree
    block_on_dirty = policy.get("blockOnDirtyWorkingTree", True)
    checks["cleanWorkingTree"] = git["clean"]
    if not git["clean"] and block_on_dirty:
        safe = False
        reasons.append(f"Working tree is dirty ({git['dirtyFileCount']} files)")

    # Check 2: active lock
    if lock is not None:
        stale = is_stale(lock, timeout)
        pid_alive = check_pid_alive(lock.get("pid", 0))
        checks["noActiveLock"] = False
        checks["lockStale"] = stale
        checks["lockPidAlive"] = pid_alive

        if stale and not pid_alive:
            checks["staleLockRecoverable"] = git["clean"]
            if policy.get("staleLockBehavior") == "auto-recover" and git["clean"]:
                reasons.append("Stale lock found (auto-recoverable)")
            else:
                safe = False
                reasons.append("Stale lock found — requires approval to clear")
        elif not stale:
            safe = False
            reasons.append(f"Active lock held by {lock.get('owner', 'unknown')} on {lock.get('phaseId', 'unknown')}")
    else:
        checks["noActiveLock"] = True

    # Check 3: commit before next phase
    if policy.get("requireCommitBeforeNextPhase", True):
        phases = _load_phase_status()
        last_completed = _find_last_completed_phase(phases)
        if last_completed:
            checks["previousPhaseCommitted"] = True
        else:
            checks["previousPhaseCommitted"] = True

    if safe:
        recommended = "Safe to proceed — start new work"
    elif reasons:
        recommended = "Resolve: " + "; ".join(reasons)
    else:
        recommended = "Unknown issue — inspect manually"

    return {
        "safe": safe,
        "checks": checks,
        "reasons": reasons,
        "recommendedAction": recommended,
    }


def _load_phase_status() -> List[Dict[str, Any]]:
    if not PHASE_STATUS_PATH.exists():
        return []
    try:
        with open(PHASE_STATUS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _find_last_completed_phase(phases: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    last = None
    for p in phases:
        if p.get("status") == "completed":
            last = p
    return last


def get_status(repo_path: str) -> Dict[str, Any]:
    """Full Work Guard status for dashboard display."""
    policy = _load_policy()
    git = check_git_status(repo_path)
    lock = read_lock(repo_path)
    safety = safe_to_run(repo_path)
    timeout = policy.get("heartbeatTimeoutMinutes", 10)

    lock_status = "unlocked"
    lock_detail: Optional[Dict[str, Any]] = None

    if lock is not None:
        stale = is_stale(lock, timeout)
        pid_alive = check_pid_alive(lock.get("pid", 0))
        if stale:
            lock_status = "stale"
        else:
            lock_status = "locked"
        lock_detail = {
            "lockId": lock.get("lockId"),
            "owner": lock.get("owner"),
            "sessionType": lock.get("sessionType"),
            "phaseId": lock.get("phaseId"),
            "branch": lock.get("branch"),
            "startedAt": lock.get("startedAt"),
            "lastHeartbeatAt": lock.get("lastHeartbeatAt"),
            "stale": stale,
            "pidAlive": pid_alive,
            "pid": lock.get("pid"),
            "touchedPaths": lock.get("touchedPaths", []),
            "queuedJobs": lock.get("queuedJobs", []),
        }

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repoPath": repo_path,
        "lockStatus": lock_status,
        "lock": lock_detail,
        "git": git,
        "safeToRun": safety["safe"],
        "checks": safety["checks"],
        "reasons": safety["reasons"],
        "recommendedAction": safety["recommendedAction"],
        "policy": {
            "heartbeatTimeoutMinutes": timeout,
            "blockOnDirtyWorkingTree": policy.get("blockOnDirtyWorkingTree", True),
            "requireCommitBeforeNextPhase": policy.get("requireCommitBeforeNextPhase", True),
            "staleLockBehavior": policy.get("staleLockBehavior", "require-approval"),
        },
    }
