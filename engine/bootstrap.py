"""Bootstrap Orchestration Console — phase dependency engine.

Reads config/phase-status.json and computes eligible, blocked, parallelizable
phases plus critical path and next recommendations.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine import events

REPO_ROOT = Path(__file__).resolve().parent.parent
PHASE_STATUS_PATH = REPO_ROOT / "config" / "phase-status.json"

TERMINAL_STATUSES = {"completed", "skipped", "cancelled"}
BLOCKED_STATUSES = {"blocked", "failed"}
ACTIVE_STATUSES = {"running", "needs_review"}
SERIALIZED_RISK_CATEGORIES = {
    "core engine", "auth", "database", "rls", "deployment",
    "repo restructuring", "session state", "pipeline state",
}


def _load_phases() -> List[Dict[str, Any]]:
    if not PHASE_STATUS_PATH.exists():
        return []
    with open(PHASE_STATUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_phases(phases: List[Dict[str, Any]]) -> None:
    tmp = PHASE_STATUS_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(phases, f, indent=2, ensure_ascii=False)
    tmp.replace(PHASE_STATUS_PATH)


def _phase_map(phases: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {p["phaseId"]: p for p in phases}


def get_all_phases() -> List[Dict[str, Any]]:
    return _load_phases()


def get_phase(phase_id: str) -> Optional[Dict[str, Any]]:
    pm = _phase_map(_load_phases())
    return pm.get(phase_id)


def compute_eligible(phases: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    if phases is None:
        phases = _load_phases()
    pm = _phase_map(phases)
    eligible = []
    for p in phases:
        if p["status"] in TERMINAL_STATUSES | ACTIVE_STATUSES | BLOCKED_STATUSES:
            continue
        deps_met = all(
            pm.get(d, {}).get("status") in TERMINAL_STATUSES
            for d in p.get("dependencies", [])
        )
        no_blockers = not p.get("blockedBy") or all(
            pm.get(b, {}).get("status") in TERMINAL_STATUSES
            for b in p["blockedBy"]
        )
        if deps_met and no_blockers:
            eligible.append(p)
    return eligible


def compute_blocked(phases: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    if phases is None:
        phases = _load_phases()
    pm = _phase_map(phases)
    blocked = []
    for p in phases:
        if p["status"] in TERMINAL_STATUSES | ACTIVE_STATUSES:
            continue
        missing_deps = [
            d for d in p.get("dependencies", [])
            if pm.get(d, {}).get("status") not in TERMINAL_STATUSES
        ]
        blocking = [
            b for b in p.get("blockedBy", [])
            if pm.get(b, {}).get("status") not in TERMINAL_STATUSES
        ]
        if missing_deps or blocking:
            blocked.append({
                **p,
                "_missingDeps": missing_deps,
                "_blockedByActive": blocking,
            })
    return blocked


def compute_parallelizable(phases: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    eligible = compute_eligible(phases)
    return [p for p in eligible if p.get("canRunInParallel") or p.get("allowedParallelism")]


def compute_critical_path(phases: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    if phases is None:
        phases = _load_phases()
    pm = _phase_map(phases)
    complexity_weight = {"S": 1, "M": 2, "L": 4, "XL": 8}

    def _longest_path(pid: str, visited: set) -> tuple:
        if pid in visited or pid not in pm:
            return (0, [])
        visited.add(pid)
        p = pm[pid]
        if p["status"] in TERMINAL_STATUSES:
            return (0, [])
        w = complexity_weight.get(p.get("estimatedComplexity", "M"), 2)
        best_cost, best_path = 0, []
        for dep_id in p.get("blocks", []):
            cost, path = _longest_path(dep_id, visited.copy())
            if cost > best_cost:
                best_cost, best_path = cost, path
        return (w + best_cost, [pid] + best_path)

    roots = [p["phaseId"] for p in phases if not p.get("dependencies")]
    longest_cost, longest_path = 0, []
    for r in roots:
        cost, path = _longest_path(r, set())
        if cost > longest_cost:
            longest_cost, longest_path = cost, path

    if not longest_path:
        incomplete = [p for p in phases if p["status"] not in TERMINAL_STATUSES]
        if incomplete:
            return [incomplete[0]["phaseId"]]
    return longest_path


def compute_next_recommended(phases: Optional[List[Dict[str, Any]]] = None) -> Optional[Dict[str, Any]]:
    eligible = compute_eligible(phases)
    if not eligible:
        return None
    critical = compute_critical_path(phases)
    for p in eligible:
        if p["phaseId"] in critical:
            return p
    return eligible[0]


def get_summary(phases: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    if phases is None:
        phases = _load_phases()
    eligible = compute_eligible(phases)
    blocked = compute_blocked(phases)
    parallelizable = compute_parallelizable(phases)
    critical_path = compute_critical_path(phases)
    next_rec = compute_next_recommended(phases)

    status_counts = {}
    for p in phases:
        s = p.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    return {
        "totalPhases": len(phases),
        "statusCounts": status_counts,
        "eligiblePhases": [p["phaseId"] for p in eligible],
        "blockedPhases": [
            {"phaseId": p["phaseId"], "missingDeps": p.get("_missingDeps", []),
             "blockedBy": p.get("_blockedByActive", [])}
            for p in blocked
        ],
        "parallelizablePhases": [p["phaseId"] for p in parallelizable],
        "criticalPath": critical_path,
        "nextRecommended": next_rec["phaseId"] if next_rec else None,
        "approvalGated": [p["phaseId"] for p in phases if p.get("approvalRequired")],
    }


def update_phase_status(phase_id: str, new_status: str, **kwargs) -> Optional[Dict[str, Any]]:
    phases = _load_phases()
    for p in phases:
        if p["phaseId"] == phase_id:
            old_status = p.get("status", "not_started")
            p["status"] = new_status
            if "nextRecommendedAction" in kwargs:
                p["nextRecommendedAction"] = kwargs["nextRecommendedAction"]
            if "activeSessionId" in kwargs:
                p["activeSessionId"] = kwargs["activeSessionId"]
            p["lastUpdated"] = kwargs.get("lastUpdated", p.get("lastUpdated"))
            _save_phases(phases)
            events.emit("phase.status_changed", {
                "phaseId": phase_id,
                "name": p.get("name", ""),
                "oldStatus": old_status,
                "newStatus": new_status,
            }, source="bootstrap")
            return p
    return None


def add_blocker(phase_id: str, blocker_phase_id: str) -> Optional[Dict[str, Any]]:
    phases = _load_phases()
    for p in phases:
        if p["phaseId"] == phase_id:
            if blocker_phase_id not in p.get("blockedBy", []):
                p.setdefault("blockedBy", []).append(blocker_phase_id)
            if p["status"] == "not_started":
                p["status"] = "blocked"
            _save_phases(phases)
            return p
    return None


def clear_blocker(phase_id: str, blocker_phase_id: str) -> Optional[Dict[str, Any]]:
    phases = _load_phases()
    for p in phases:
        if p["phaseId"] == phase_id:
            bl = p.get("blockedBy", [])
            if blocker_phase_id in bl:
                bl.remove(blocker_phase_id)
            if p["status"] == "blocked" and not bl:
                p["status"] = "not_started"
            _save_phases(phases)
            return p
    return None
