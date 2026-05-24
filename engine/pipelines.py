"""Pipeline DAG engine — dependency resolution, stage lifecycle, session integration.

Manages pipelines as directed acyclic graphs of stages.  Each stage can be a
``claude-p`` session, a manual gate, or a script.  Stages execute in dependency
order with automatic advancement when ``auto_advance`` is set.

Persistence: ``dashboard/data/pipelines.json`` (atomic writes).
"""
from __future__ import annotations

import json
import os
import re
import threading
import uuid
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from engine import events

# ---------------------------------------------------------------------------
# Module-level configuration — call configure() before first use
# ---------------------------------------------------------------------------
_data_dir: Path = Path(".")
_sessions_dir: Path = Path(".conductor-sessions")
_state_file: Path = Path("pipelines.json")
_templates_dir: Path = Path("templates/pipelines")
_repo_root: Path = Path(".")

_lock = threading.Lock()
_pipelines: Dict[str, Dict[str, Any]] = {}

_on_stage_transition: Optional[Callable[[Dict[str, Any], Dict[str, Any], str, str], None]] = None

# Valid states for pipelines and stages
PIPELINE_STATES = {"pending", "running", "completed", "failed", "cancelled", "rolled_back"}
STAGE_STATES = {
    "pending", "ready", "running", "blocked",
    "waiting_for_approval", "completed", "failed", "cancelled", "skipped",
}
TERMINAL_STAGE_STATES = {"completed", "failed", "cancelled", "skipped"}
ACTIVE_STAGE_STATES = {"running", "waiting_for_approval"}


def configure(
    data_dir: Path,
    sessions_dir: Path,
    repo_root: Path,
    templates_dir: Optional[Path] = None,
) -> None:
    global _data_dir, _sessions_dir, _state_file, _templates_dir, _repo_root
    _data_dir = Path(data_dir)
    _sessions_dir = Path(sessions_dir)
    _state_file = _data_dir / "pipelines.json"
    _repo_root = Path(repo_root)
    if templates_dir:
        _templates_dir = Path(templates_dir)
    else:
        _templates_dir = _repo_root / "templates" / "pipelines"
    _data_dir.mkdir(parents=True, exist_ok=True)


def set_on_stage_transition(fn: Callable) -> None:
    """Register callback: fn(pipeline, stage, old_status, new_status)."""
    global _on_stage_transition
    _on_stage_transition = fn


# ---------------------------------------------------------------------------
# ID generation
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# State persistence — atomic writes
# ---------------------------------------------------------------------------
def _flush_state() -> None:
    """Write pipelines dict to disk.  Caller must hold _lock."""
    _data_dir.mkdir(parents=True, exist_ok=True)
    payload = list(_pipelines.values())
    tmp = _state_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(_state_file)


def _load_state() -> None:
    """Load pipelines from disk.  Running stages become failed on restart."""
    if not _state_file.exists():
        return
    try:
        data = json.loads(_state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    if not isinstance(data, list):
        return
    for pipe in data:
        pid = pipe.get("id")
        if not pid:
            continue
        for stage in pipe.get("stages", []):
            if stage.get("status") == "running":
                stage["status"] = "failed"
                stage["error"] = "Server restarted"
                stage["ended_at"] = _now_iso()
        if pipe.get("status") == "running":
            has_active = any(
                s["status"] in ("running", "ready", "waiting_for_approval")
                for s in pipe.get("stages", [])
            )
            if not has_active:
                pipe["status"] = "failed"
                pipe["error"] = "Server restarted — pipeline did not complete"
        _pipelines[pid] = pipe


def load_state() -> None:
    with _lock:
        _load_state()


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------
def list_templates() -> List[Dict[str, Any]]:
    """Return available pipeline templates from templates/pipelines/."""
    templates = []
    if not _templates_dir.exists():
        return templates
    for f in sorted(_templates_dir.glob("*.yaml")):
        try:
            raw = f.read_text(encoding="utf-8")
            tpl = yaml.safe_load(raw)
            templates.append({
                "slug": f.stem,
                "name": tpl.get("name", f.stem),
                "description": tpl.get("description", ""),
                "stage_count": len(tpl.get("stages", [])),
            })
        except Exception:
            continue
    return templates


def _load_template(slug: str) -> Optional[Dict[str, Any]]:
    path = _templates_dir / f"{slug}.yaml"
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# DAG core: dependency resolution
# ---------------------------------------------------------------------------
def _build_stage_map(stages: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {s["name"]: s for s in stages}


def calculate_ready_stages(pipeline: Dict[str, Any]) -> List[str]:
    """Return names of stages whose dependencies are all met and that are pending."""
    stages = pipeline.get("stages", [])
    sm = _build_stage_map(stages)
    ready = []
    for stage in stages:
        if stage["status"] != "pending":
            continue
        deps = stage.get("depends_on", [])
        all_met = all(
            sm.get(d, {}).get("status") in {"completed", "skipped"}
            for d in deps
        )
        if all_met:
            ready.append(stage["name"])
    return ready


def _has_cycle(stages: List[Dict[str, Any]]) -> bool:
    """Detect cycles in the stage dependency graph via topological sort."""
    sm = _build_stage_map(stages)
    in_degree: Dict[str, int] = {s["name"]: 0 for s in stages}
    for s in stages:
        for d in s.get("depends_on", []):
            if d in in_degree:
                in_degree[s["name"]] += 1

    queue = [n for n, deg in in_degree.items() if deg == 0]
    visited = 0
    while queue:
        node = queue.pop(0)
        visited += 1
        for s in stages:
            if node in s.get("depends_on", []):
                in_degree[s["name"]] -= 1
                if in_degree[s["name"]] == 0:
                    queue.append(s["name"])
    return visited != len(stages)


def _validate_dag(stages: List[Dict[str, Any]]) -> Optional[str]:
    """Validate stage DAG.  Returns error message or None."""
    names = {s["name"] for s in stages}
    for s in stages:
        for d in s.get("depends_on", []):
            if d not in names:
                return f"Stage '{s['name']}' depends on unknown stage '{d}'"
    if _has_cycle(stages):
        return "Stage dependency graph contains a cycle"
    return None


# ---------------------------------------------------------------------------
# Stage state transitions
# ---------------------------------------------------------------------------
def _transition_stage(
    pipeline: Dict[str, Any],
    stage_name: str,
    new_status: str,
    error: Optional[str] = None,
    session_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Transition a stage to a new status.  Returns the stage or None."""
    sm = _build_stage_map(pipeline.get("stages", []))
    stage = sm.get(stage_name)
    if not stage:
        return None

    old_status = stage["status"]
    stage["status"] = new_status

    if new_status == "running":
        stage["started_at"] = _now_iso()
        if session_id:
            stage["session_id"] = session_id
    elif new_status in TERMINAL_STAGE_STATES:
        stage["ended_at"] = _now_iso()
        if error:
            stage["error"] = error

    events.emit("pipeline.stage.status_changed", {
        "pipelineId": pipeline.get("id"),
        "pipelineName": pipeline.get("name"),
        "stageName": stage["name"],
        "stageLabel": stage.get("label", stage["name"]),
        "oldStatus": old_status,
        "newStatus": new_status,
    }, source="pipelines")

    if _on_stage_transition:
        try:
            _on_stage_transition(pipeline, stage, old_status, new_status)
        except Exception:
            pass

    return stage


# ---------------------------------------------------------------------------
# Pipeline creation
# ---------------------------------------------------------------------------
def create_pipeline(
    name: str,
    template_slug: str,
    project_slug: str = "",
    repo_path: str = "",
    variables: Optional[Dict[str, str]] = None,
    model: str = "sonnet",
    budget_usd: float = 5.0,
    timeout_min: int = 60,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Create a pipeline from a template.  Returns (pipeline, error)."""
    tpl = _load_template(template_slug)
    if not tpl:
        return None, f"Template '{template_slug}' not found"

    tpl_stages = tpl.get("stages", [])
    if not tpl_stages:
        return None, "Template has no stages"

    variables = variables or {}
    short = _short_id()
    pid = f"pipe_{short}"

    stages: List[Dict[str, Any]] = []
    for ts in tpl_stages:
        prompt_tpl = ts.get("prompt_template", "")
        for k, v in variables.items():
            prompt_tpl = prompt_tpl.replace("{" + k + "}", str(v))

        stage: Dict[str, Any] = {
            "name": ts["name"],
            "label": ts.get("label", ts["name"]),
            "type": ts.get("type", "claude-p"),
            "template": ts.get("template", "implement"),
            "model": ts.get("model", model),
            "budget_usd": float(ts.get("budget_usd", budget_usd)),
            "timeout_min": int(ts.get("timeout_min", timeout_min)),
            "auto_advance": ts.get("auto_advance", True),
            "depends_on": list(ts.get("depends_on", [])),
            "prompt": prompt_tpl,
            "gate_type": ts.get("gate_type"),
            "status": "pending",
            "session_id": None,
            "started_at": None,
            "ended_at": None,
            "error": None,
        }
        stages.append(stage)

    err = _validate_dag(stages)
    if err:
        return None, err

    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", name.lower())[:40]
    worktree_id = f"{safe_name}-{short}"

    pipeline: Dict[str, Any] = {
        "id": pid,
        "name": name,
        "template": template_slug,
        "project_slug": project_slug,
        "repo_path": repo_path or str(_repo_root),
        "model": model,
        "variables": variables,
        "status": "pending",
        "stages": stages,
        "worktree_id": worktree_id,
        "worktree_path": f".conductor-sessions/{worktree_id}",
        "branch": f"pipeline/{worktree_id}",
        "created_at": _now_iso(),
        "started_at": None,
        "ended_at": None,
        "error": None,
        "cost_usd": 0.0,
        "snapshot": None,
        "rollback_history": [],
        "merge_approved": False,
    }

    with _lock:
        _pipelines[pid] = pipeline
        _flush_state()

    events.emit("pipeline.created", {
        "pipelineId": pid,
        "name": name,
        "template": template_slug,
    }, source="pipelines")

    return pipeline, None


# ---------------------------------------------------------------------------
# Pipeline lifecycle
# ---------------------------------------------------------------------------
def start_pipeline(pid: str, session_launcher: Optional[Callable] = None) -> Tuple[bool, str]:
    """Start a pipeline: mark ready stages, launch auto-advance stages.

    session_launcher: fn(pipeline, stage) -> session_id or None.
    If not provided, stages are marked ready but not auto-launched.
    """
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        if pipeline["status"] not in ("pending",):
            return False, f"Pipeline is {pipeline['status']}, cannot start"

        pipeline["status"] = "running"
        pipeline["started_at"] = _now_iso()

        from engine.stage_scripts.git_ops import snapshot_branch
        pipeline["snapshot"] = snapshot_branch(
            pipeline.get("repo_path", str(_repo_root)),
        )

        ready = calculate_ready_stages(pipeline)
        for name in ready:
            _transition_stage(pipeline, name, "ready")

        _flush_state()

    events.emit("pipeline.started", {
        "pipelineId": pid,
        "name": pipeline.get("name"),
        "snapshot": pipeline.get("snapshot", {}),
    }, source="pipelines")

    if session_launcher:
        _auto_launch_ready(pid, session_launcher)

    return True, "started"


def _auto_launch_ready(pid: str, session_launcher: Callable) -> None:
    """Launch sessions for ready stages that have auto_advance and are claude-p type."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline or pipeline["status"] != "running":
            return
        stages_to_launch = []
        for stage in pipeline["stages"]:
            if stage["status"] != "ready":
                continue
            if stage["type"] == "gate":
                stage["status"] = "waiting_for_approval"
                continue
            if stage.get("auto_advance") and stage["type"] == "claude-p":
                stages_to_launch.append(stage["name"])
        _flush_state()

    for stage_name in stages_to_launch:
        with _lock:
            pipeline = _pipelines.get(pid)
            if not pipeline:
                return
            sm = _build_stage_map(pipeline["stages"])
            stage = sm.get(stage_name)
            if not stage or stage["status"] != "ready":
                continue

        try:
            session_id = session_launcher(pipeline, stage)
            with _lock:
                pipeline = _pipelines.get(pid)
                if pipeline:
                    _transition_stage(pipeline, stage_name, "running", session_id=session_id)
                    _flush_state()
        except Exception as exc:
            with _lock:
                pipeline = _pipelines.get(pid)
                if pipeline:
                    _transition_stage(pipeline, stage_name, "failed", error=str(exc))
                    _flush_state()


def advance_pipeline(pid: str, session_launcher: Optional[Callable] = None) -> Tuple[bool, str]:
    """Advance a pipeline: mark pending stages as ready if deps met, launch auto stages.

    Also handles gate advancement (call this after approving a gate).
    Returns (success, message).
    """
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        if pipeline["status"] != "running":
            return False, f"Pipeline is {pipeline['status']}"

        ready = calculate_ready_stages(pipeline)
        for name in ready:
            _transition_stage(pipeline, name, "ready")

        _check_pipeline_completion(pipeline)
        _flush_state()

    if pipeline["status"] == "running" and session_launcher:
        _auto_launch_ready(pid, session_launcher)

    status = pipeline["status"]
    return True, f"advanced (pipeline {status})"


def handle_stage_complete(
    pid: str,
    stage_name: str,
    success: bool,
    error: Optional[str] = None,
    cost_usd: float = 0.0,
    session_launcher: Optional[Callable] = None,
) -> Tuple[bool, str]:
    """Called when a stage's session finishes.  Updates state and advances the pipeline."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"

        new_status = "completed" if success else "failed"
        _transition_stage(pipeline, stage_name, new_status, error=error)

        pipeline["cost_usd"] = pipeline.get("cost_usd", 0.0) + cost_usd

        if not success:
            _propagate_failure(pipeline, stage_name)

        _flush_state()

    return advance_pipeline(pid, session_launcher)


def _propagate_failure(pipeline: Dict[str, Any], failed_stage: str) -> None:
    """Block downstream stages when a stage fails."""
    for stage in pipeline["stages"]:
        if stage["status"] != "pending":
            continue
        if failed_stage in stage.get("depends_on", []):
            stage["status"] = "blocked"
            stage["error"] = f"Blocked by failed stage '{failed_stage}'"


def _check_pipeline_completion(pipeline: Dict[str, Any]) -> None:
    """Mark pipeline as completed/failed if all stages are terminal."""
    stages = pipeline.get("stages", [])
    if not stages:
        return

    all_terminal = all(s["status"] in TERMINAL_STAGE_STATES for s in stages)
    if not all_terminal:
        return

    any_failed = any(s["status"] == "failed" for s in stages)
    if any_failed:
        pipeline["status"] = "failed"
        events.emit("pipeline.failed", {
            "pipelineId": pipeline.get("id"),
            "name": pipeline.get("name"),
        }, source="pipelines")
    else:
        pipeline["status"] = "completed"
        events.emit("pipeline.completed", {
            "pipelineId": pipeline.get("id"),
            "name": pipeline.get("name"),
        }, source="pipelines")
    pipeline["ended_at"] = _now_iso()


# ---------------------------------------------------------------------------
# Gate advancement
# ---------------------------------------------------------------------------
def approve_gate(pid: str, stage_name: str, session_launcher: Optional[Callable] = None) -> Tuple[bool, str]:
    """Approve a gate stage, marking it completed and advancing the pipeline."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        sm = _build_stage_map(pipeline["stages"])
        stage = sm.get(stage_name)
        if not stage:
            return False, f"Stage '{stage_name}' not found"
        if stage["status"] != "waiting_for_approval":
            return False, f"Stage is {stage['status']}, not waiting for approval"

        _transition_stage(pipeline, stage_name, "completed")
        _flush_state()

    return advance_pipeline(pid, session_launcher)


# ---------------------------------------------------------------------------
# Retry / cancel / skip
# ---------------------------------------------------------------------------
def retry_stage(pid: str, stage_name: str, session_launcher: Optional[Callable] = None) -> Tuple[bool, str]:
    """Reset a failed stage to pending and re-advance the pipeline."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        sm = _build_stage_map(pipeline["stages"])
        stage = sm.get(stage_name)
        if not stage:
            return False, f"Stage '{stage_name}' not found"
        if stage["status"] not in ("failed", "blocked"):
            return False, f"Stage is {stage['status']}, can only retry failed/blocked"

        stage["status"] = "pending"
        stage["error"] = None
        stage["session_id"] = None
        stage["started_at"] = None
        stage["ended_at"] = None

        _unblock_downstream(pipeline, stage_name)

        if pipeline["status"] in ("failed",):
            pipeline["status"] = "running"
            pipeline["ended_at"] = None
            pipeline["error"] = None

        _flush_state()

    return advance_pipeline(pid, session_launcher)


def _unblock_downstream(pipeline: Dict[str, Any], stage_name: str) -> None:
    """Reset blocked downstream stages back to pending when retrying."""
    for stage in pipeline["stages"]:
        if stage["status"] == "blocked" and stage_name in stage.get("depends_on", []):
            stage["status"] = "pending"
            stage["error"] = None


def skip_stage(pid: str, stage_name: str, session_launcher: Optional[Callable] = None) -> Tuple[bool, str]:
    """Skip a stage (mark as skipped) and advance the pipeline."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        sm = _build_stage_map(pipeline["stages"])
        stage = sm.get(stage_name)
        if not stage:
            return False, f"Stage '{stage_name}' not found"
        if stage["status"] in TERMINAL_STAGE_STATES:
            return False, f"Stage is already {stage['status']}"

        _transition_stage(pipeline, stage_name, "skipped")
        _flush_state()

    return advance_pipeline(pid, session_launcher)


def cancel_pipeline(pid: str) -> Tuple[bool, str]:
    """Cancel a pipeline and all non-terminal stages."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        if pipeline["status"] in ("completed", "cancelled"):
            return False, f"Pipeline is already {pipeline['status']}"

        pipeline["status"] = "cancelled"
        pipeline["ended_at"] = _now_iso()
        for stage in pipeline["stages"]:
            if stage["status"] not in TERMINAL_STAGE_STATES:
                _transition_stage(pipeline, stage["name"], "cancelled")

        _flush_state()

    events.emit("pipeline.cancelled", {
        "pipelineId": pid,
        "name": pipeline.get("name"),
    }, source="pipelines")

    return True, "cancelled"


# ---------------------------------------------------------------------------
# Query API
# ---------------------------------------------------------------------------
def get_pipeline(pid: str) -> Optional[Dict[str, Any]]:
    with _lock:
        p = _pipelines.get(pid)
        return dict(p) if p else None


_STATUS_ORDER = {"running": 0, "pending": 1, "completed": 2, "failed": 3, "rolled_back": 4, "cancelled": 5}


def list_pipelines(
    project_slug: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    with _lock:
        result = list(_pipelines.values())
    if project_slug:
        result = [p for p in result if p.get("project_slug") == project_slug]
    if status:
        result = [p for p in result if p.get("status") == status]
    result.sort(key=lambda p: p.get("created_at") or "", reverse=True)
    result.sort(key=lambda p: _STATUS_ORDER.get(p.get("status", ""), 9))
    return result


def get_pipeline_summary(pid: str) -> Optional[Dict[str, Any]]:
    """Return a computed summary of pipeline state."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return None
        pipeline = dict(pipeline)

    stages = pipeline.get("stages", [])
    status_counts: Dict[str, int] = {}
    for s in stages:
        st = s.get("status", "unknown")
        status_counts[st] = status_counts.get(st, 0) + 1

    ready = calculate_ready_stages(pipeline)
    total_cost = sum(s.get("budget_usd", 0) for s in stages if s["status"] == "completed")

    return {
        "id": pipeline["id"],
        "name": pipeline["name"],
        "status": pipeline["status"],
        "stage_count": len(stages),
        "status_counts": status_counts,
        "ready_stages": ready,
        "cost_usd": pipeline.get("cost_usd", 0.0),
        "created_at": pipeline.get("created_at"),
        "started_at": pipeline.get("started_at"),
        "ended_at": pipeline.get("ended_at"),
    }


# ---------------------------------------------------------------------------
# Dry-run / simulation
# ---------------------------------------------------------------------------
def dry_run(
    template_slug: str,
    variables: Optional[Dict[str, str]] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Simulate a pipeline without persisting.  Returns (result, error).

    Result includes the DAG with computed ready stages, stage order, and
    estimated total cost/time.
    """
    tpl = _load_template(template_slug)
    if not tpl:
        return None, f"Template '{template_slug}' not found"

    tpl_stages = tpl.get("stages", [])
    if not tpl_stages:
        return None, "Template has no stages"

    stages = []
    for ts in tpl_stages:
        stages.append({
            "name": ts["name"],
            "label": ts.get("label", ts["name"]),
            "type": ts.get("type", "claude-p"),
            "depends_on": list(ts.get("depends_on", [])),
            "auto_advance": ts.get("auto_advance", True),
            "budget_usd": float(ts.get("budget_usd", 5.0)),
            "timeout_min": int(ts.get("timeout_min", 60)),
            "status": "pending",
        })

    err = _validate_dag(stages)
    if err:
        return None, err

    fake_pipeline = {"stages": stages}
    ready = calculate_ready_stages(fake_pipeline)

    topo_order = _topological_sort(stages)
    total_budget = sum(s["budget_usd"] for s in stages)
    total_time = sum(s["timeout_min"] for s in stages)

    return {
        "template": template_slug,
        "template_name": tpl.get("name", template_slug),
        "stages": [
            {
                "name": s["name"],
                "label": s["label"],
                "type": s["type"],
                "depends_on": s["depends_on"],
                "auto_advance": s["auto_advance"],
                "budget_usd": s["budget_usd"],
                "timeout_min": s["timeout_min"],
            }
            for s in stages
        ],
        "ready_stages": ready,
        "execution_order": topo_order,
        "total_budget_usd": total_budget,
        "total_time_min": total_time,
        "stage_count": len(stages),
    }, None


def _topological_sort(stages: List[Dict[str, Any]]) -> List[str]:
    """Return stage names in topological order."""
    in_degree: Dict[str, int] = {s["name"]: 0 for s in stages}
    dependents: Dict[str, List[str]] = {s["name"]: [] for s in stages}
    for s in stages:
        for d in s.get("depends_on", []):
            if d in in_degree:
                in_degree[s["name"]] += 1
                dependents[d].append(s["name"])

    queue = sorted(n for n, deg in in_degree.items() if deg == 0)
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for dep in sorted(dependents.get(node, [])):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
    return order


# ---------------------------------------------------------------------------
# Rollback + Merge
# ---------------------------------------------------------------------------
def rollback_pipeline(pid: str, reason: str = "") -> Tuple[bool, str]:
    """Rollback a pipeline's worktree branch to the pre-pipeline snapshot."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        snapshot = pipeline.get("snapshot")
        if not snapshot or snapshot.get("commit") == "unknown":
            return False, "No snapshot available for rollback"

    wt_path = _sessions_dir / pipeline.get("worktree_id", "")
    if not wt_path.exists():
        return False, "Worktree no longer exists"

    from engine.stage_scripts.git_ops import rollback_to_snapshot
    result = rollback_to_snapshot(str(wt_path), snapshot["commit"])

    with _lock:
        pipeline.setdefault("rollback_history", []).append({
            "timestamp": _now_iso(),
            "reason": reason,
            "to_commit": snapshot["commit"],
            "success": result.success,
        })
        if result.success:
            pipeline["status"] = "rolled_back"
            pipeline["ended_at"] = _now_iso()
        _flush_state()

    events.emit("pipeline.rolled_back", {
        "pipelineId": pid,
        "name": pipeline.get("name"),
        "toCommit": snapshot["commit"][:12],
        "reason": reason,
        "success": result.success,
    }, source="pipelines")

    return result.success, result.summary or result.error or "Unknown error"


def approve_merge(pid: str) -> Tuple[bool, str]:
    """Approve merging a completed pipeline's branch."""
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return False, "Pipeline not found"
        if pipeline["status"] != "completed":
            return False, f"Pipeline is {pipeline['status']}, must be completed to merge"
        pipeline["merge_approved"] = True
        _flush_state()

    events.emit("pipeline.merge_approved", {
        "pipelineId": pid,
        "name": pipeline.get("name"),
    }, source="pipelines")

    return True, "Merge approved"


def get_snapshot(pid: str) -> Optional[Dict[str, Any]]:
    with _lock:
        pipeline = _pipelines.get(pid)
        if not pipeline:
            return None
        return {
            "snapshot": pipeline.get("snapshot"),
            "rollback_history": pipeline.get("rollback_history", []),
            "merge_approved": pipeline.get("merge_approved", False),
        }


# ---------------------------------------------------------------------------
# Shutdown
# ---------------------------------------------------------------------------
def shutdown() -> None:
    """Flush state on server shutdown."""
    with _lock:
        for pipeline in _pipelines.values():
            if pipeline["status"] == "running":
                for stage in pipeline["stages"]:
                    if stage["status"] in ("running", "ready"):
                        stage["status"] = "failed"
                        stage["error"] = "Server shutdown"
                        stage["ended_at"] = _now_iso()
                pipeline["status"] = "failed"
                pipeline["error"] = "Server shutdown"
                pipeline["ended_at"] = _now_iso()
        _flush_state()
