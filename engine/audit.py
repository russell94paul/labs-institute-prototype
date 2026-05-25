"""Pipeline audit trail — append-only evidence log per pipeline."""
from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_data_dir: Optional[Path] = None
_lock = threading.Lock()


def configure(data_dir: Path) -> None:
    global _data_dir
    _data_dir = data_dir
    (data_dir / "audits").mkdir(parents=True, exist_ok=True)


def _audit_path(pid: str) -> Path:
    return _data_dir / "audits" / f"{pid}.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_event(pid: str, event_type: str, stage_name: Optional[str], details: Dict[str, Any]) -> None:
    if not _data_dir:
        return
    with _lock:
        try:
            path = _audit_path(pid)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
            else:
                data = {"pipeline_id": pid, "events": []}

            data["events"].append({
                "timestamp": _now_iso(),
                "event_type": event_type,
                "stage_name": stage_name,
                "details": details,
            })

            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(path)
        except OSError:
            pass


def _extract_output_summary(sid: str) -> Dict[str, Any]:
    if not _data_dir:
        return {}
    jsonl_path = _data_dir / "sessions" / f"{sid}.jsonl"
    if not jsonl_path.exists():
        return {"output_lines": 0}

    try:
        lines = jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines()
        total = len(lines)
        texts: List[str] = []
        result_text = ""

        for line in lines:
            try:
                ev = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if ev.get("type") == "assistant":
                for block in ev.get("message", {}).get("content", []):
                    if block.get("type") == "text" and block.get("text", "").strip():
                        texts.append(block["text"].strip()[:300])
            if ev.get("type") == "result":
                result_text = str(ev.get("result", ""))[:500]

        return {
            "result_text": result_text,
            "last_texts": texts[-3:] if texts else [],
            "output_lines": total,
        }
    except OSError:
        return {"output_lines": 0}


def record_stage_started(pid: str, stage_name: str, prompt: str) -> None:
    _append_event(pid, "stage_started", stage_name, {
        "prompt_preview": prompt[:500] if prompt else "",
    })


def record_stage_completed(
    pid: str,
    stage_name: str,
    sess: Dict[str, Any],
    validation_report: Optional[Dict[str, Any]] = None,
) -> None:
    sid = sess.get("id", "")
    started = sess.get("started_at", "")
    ended = sess.get("ended_at", "")
    duration_s = None
    if started and ended:
        try:
            t0 = datetime.fromisoformat(started)
            t1 = datetime.fromisoformat(ended)
            duration_s = round((t1 - t0).total_seconds())
        except (ValueError, TypeError):
            pass

    _append_event(pid, "stage_completed", stage_name, {
        "session_id": sid,
        "cost_usd": sess.get("cost_usd", 0.0),
        "tokens_in": sess.get("tokens_in", 0),
        "tokens_out": sess.get("tokens_out", 0),
        "started_at": started,
        "ended_at": ended,
        "duration_s": duration_s,
        "files_changed": sess.get("files_changed", [])[:30],
        "quality_gates": sess.get("quality_gates"),
        "output_summary": _extract_output_summary(sid),
        "validation": validation_report,
    })


def record_stage_failed(pid: str, stage_name: str, error: str) -> None:
    _append_event(pid, "stage_failed", stage_name, {"error": error or ""})


def record_stage_skipped(pid: str, stage_name: str) -> None:
    _append_event(pid, "stage_skipped", stage_name, {})


def record_validation_ran(pid: str, stage_name: str, report: Dict[str, Any]) -> None:
    _append_event(pid, "validation_ran", stage_name, {
        "all_passed": report.get("all_passed", True),
        "results": report.get("results", []),
    })


def record_gate_approved(pid: str, stage_name: str, notes: str = "") -> None:
    _append_event(pid, "gate_approved", stage_name, {"notes": notes})


def record_gate_rejected(pid: str, stage_name: str, notes: str = "") -> None:
    _append_event(pid, "gate_rejected", stage_name, {"notes": notes})


def record_pipeline_completed(pid: str, final_status: str, cost_usd: float = 0.0) -> None:
    _append_event(pid, "pipeline_completed", None, {
        "final_status": final_status,
        "cost_usd": cost_usd,
    })


def record_pipeline_cancelled(pid: str) -> None:
    _append_event(pid, "pipeline_cancelled", None, {})


def get_audit(pid: str) -> Dict[str, Any]:
    if not _data_dir:
        return {"pipeline_id": pid, "events": []}
    path = _audit_path(pid)
    if not path.exists():
        return {"pipeline_id": pid, "events": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"pipeline_id": pid, "events": []}
