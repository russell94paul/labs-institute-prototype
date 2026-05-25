"""Conductor — HTTP server + API routing.

Serves the dashboard from dashboard/ and routes /api/* to engine modules.
Run from repo root: python engine/server.py
"""
from __future__ import annotations

import atexit
import http.server
import json
import os
import re
import signal
import socketserver
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Ensure engine package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import sessions
from engine import bootstrap
from engine import pipelines
from engine import work_guard
from engine import events
from engine import memory
from engine import validation
from engine import audit
from engine import onboarding

from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
DASHBOARD_ROOT = REPO_ROOT / "dashboard"
DATA_DIR = DASHBOARD_ROOT / "data"
SESSIONS_DIR = REPO_ROOT / ".conductor-sessions"
SESSIONS_DATA_DIR = DATA_DIR / "sessions"

PORT = int(os.environ.get("CONDUCTOR_PORT", "8888"))

DEFAULT_CONFIG: Dict[str, Any] = {
    "max_parallel": 8,
    "default_budget_usd": 5.0,
    "default_timeout_min": 60,
    "default_model": "sonnet",
}


class ConductorHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static files from dashboard/ and handles /api/* routes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_ROOT), **kwargs)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0) or 0)
        return self.rfile.read(length) if length else b""

    def _json_body(self) -> Optional[Dict[str, Any]]:
        raw = self._read_body()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return None

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, message: str) -> None:
        self._send_json({"error": message}, status)

    def _match_session_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/sessions/(ses_[a-f0-9]+)(?:/(\w+))?$", path)
        if m:
            return m.group(1), m.group(2)
        return None

    # --- Session handlers ---

    def _handle_get_sessions(self) -> None:
        payload = sessions.get_all_sessions_snapshot()
        self._send_json(payload)

    def _handle_post_sessions(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")

        prompt = body.get("prompt", "")
        if not prompt:
            return self._send_error_json(400, "prompt is required")

        project_slug = body.get("project_slug", "")
        repo_path = body.get("repo_path", str(REPO_ROOT))
        template = body.get("template", "implement")

        read_only_templates = {"analyze", "code_review", "investigate"}
        use_worktree = template not in read_only_templates

        session = sessions.create_session(
            project_slug=project_slug,
            repo_path=repo_path,
            prompt=prompt,
            template=template,
            model=body.get("model", DEFAULT_CONFIG["default_model"]),
            budget_usd=float(body.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
            timeout_min=int(body.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
            use_worktree=use_worktree,
            task_id=body.get("task_id", ""),
            task_title=body.get("task_title", ""),
        )

        print(f"[conductor] Created session {session['id']}")
        self._send_json(session, 201)

    def _handle_get_session(self, sid: str) -> None:
        session = sessions.get_session(sid)
        if not session:
            return self._send_error_json(404, f"Session {sid} not found")
        self._send_json(session)

    def _handle_get_output(self, sid: str) -> None:
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        max_lines = int(params.get("lines", "100"))

        output = sessions.get_session_output(sid, max_lines)
        if output is None:
            return self._send_error_json(404, f"Session {sid} not found")
        self._send_json(output)

    def _handle_cancel_session(self, sid: str) -> None:
        ok = sessions.cancel_session(sid)
        if not ok:
            session = sessions.get_session(sid)
            if not session:
                return self._send_error_json(404, f"Session {sid} not found")
            return self._send_error_json(409, f"Session is {session['status']}, cannot cancel")
        self._send_json({"ok": True})

    def _handle_patch_session(self, sid: str) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")

        result = sessions.update_session(sid, body)
        if result is None:
            return self._send_error_json(404, f"Session {sid} not found")
        self._send_json(result)

    def _handle_delete_session(self, sid: str) -> None:
        ok = sessions.delete_session(sid)
        if not ok:
            return self._send_error_json(404, f"Session {sid} not found")
        self._send_json({"ok": True})

    def _handle_get_session_validation(self, sid: str) -> None:
        report = validation.get_report(sid)
        if not report:
            return self._send_error_json(404, f"No validation report for {sid}")
        self._send_json(report)

    def _handle_post_session_validate(self, sid: str) -> None:
        session = sessions.get_session(sid)
        if not session:
            return self._send_error_json(404, f"Session {sid} not found")
        checks = validation.default_checks(session)
        report = validation.run_validation(session, checks)
        validation.apply_to_quality_gates(session, report)
        sessions.update_session(sid, {"quality_gates": session["quality_gates"]})
        self._send_json({"report": report.__dict__ if hasattr(report, '__dict__') else report})

    def _handle_post_continue_session(self, sid: str) -> None:
        body = self._json_body()
        if not body or not body.get("input"):
            return self._send_error_json(400, "input is required")
        new_session = sessions.continue_session(
            original_sid=sid,
            user_input=body["input"],
            budget_usd=float(body.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
            timeout_min=int(body.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
        )
        if not new_session:
            return self._send_error_json(404, "Session not found or not in terminal state")
        self._send_json(new_session, 201)

    # --- Bootstrap handlers ---

    def _handle_get_bootstrap_phases(self) -> None:
        params = self._parse_query_params()
        project = params.get("project")
        phases = bootstrap.get_all_phases(project=project or None)
        self._send_json(phases)

    def _handle_get_bootstrap_summary(self) -> None:
        params = self._parse_query_params()
        project = params.get("project")
        phases = bootstrap.get_all_phases(project=project or None) if project else None
        summary = bootstrap.get_summary(phases)
        self._send_json(summary)

    def _handle_get_bootstrap_phase(self, phase_id: str) -> None:
        phase = bootstrap.get_phase(phase_id)
        if not phase:
            return self._send_error_json(404, f"Phase {phase_id} not found")
        self._send_json(phase)

    def _handle_patch_bootstrap_phase(self, phase_id: str) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        new_status = body.get("status")
        if not new_status:
            return self._send_error_json(400, "status is required")
        result = bootstrap.update_phase_status(phase_id, new_status, **{
            k: body[k] for k in ("nextRecommendedAction", "activeSessionId", "lastUpdated")
            if k in body
        })
        if not result:
            return self._send_error_json(404, f"Phase {phase_id} not found")
        self._send_json(result)

    def _handle_post_bootstrap_blocker(self, phase_id: str) -> None:
        body = self._json_body()
        if not body or "blockerPhaseId" not in body:
            return self._send_error_json(400, "blockerPhaseId is required")
        action = body.get("action", "add")
        if action == "clear":
            result = bootstrap.clear_blocker(phase_id, body["blockerPhaseId"])
        else:
            result = bootstrap.add_blocker(phase_id, body["blockerPhaseId"])
        if not result:
            return self._send_error_json(404, f"Phase {phase_id} not found")
        self._send_json(result)

    def _match_bootstrap_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/bootstrap/phases/([a-zA-Z0-9_-]+)(?:/(\w+))?$", path)
        if m:
            return m.group(1), m.group(2)
        return None

    # --- Pipeline handlers ---

    def _match_pipeline_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/pipelines/(pipe_[a-f0-9]+)(?:/(.+))?$", path)
        if m:
            return m.group(1), m.group(2)
        return None

    def _handle_get_pipelines(self) -> None:
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        result = pipelines.list_pipelines(
            project_slug=params.get("project"),
            status=params.get("status"),
        )
        self._send_json(result)

    def _handle_post_pipelines(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")

        name = body.get("name", "")
        template = body.get("template", "")
        if not name or not template:
            return self._send_error_json(400, "name and template are required")

        pipe, err = pipelines.create_pipeline(
            name=name,
            template_slug=template,
            project_slug=body.get("project_slug", ""),
            repo_path=body.get("repo_path", str(REPO_ROOT)),
            variables=body.get("variables", {}),
            model=body.get("model", DEFAULT_CONFIG["default_model"]),
            budget_usd=float(body.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
            timeout_min=int(body.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
        )
        if err:
            return self._send_error_json(400, err)

        if body.get("auto_start"):
            pipelines.start_pipeline(pipe["id"], session_launcher=_pipeline_session_launcher)

        print(f"[conductor] Created pipeline {pipe['id']}")
        self._send_json(pipe, 201)

    def _handle_get_pipeline(self, pid: str) -> None:
        pipe = pipelines.get_pipeline(pid)
        if not pipe:
            return self._send_error_json(404, f"Pipeline {pid} not found")
        self._send_json(pipe)

    def _handle_get_pipeline_summary(self, pid: str) -> None:
        summary = pipelines.get_pipeline_summary(pid)
        if not summary:
            return self._send_error_json(404, f"Pipeline {pid} not found")
        self._send_json(summary)

    def _handle_post_pipeline_start(self, pid: str) -> None:
        ok, msg = pipelines.start_pipeline(pid, session_launcher=_pipeline_session_launcher)
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_pipeline_advance(self, pid: str) -> None:
        ok, msg = pipelines.advance_pipeline(pid, session_launcher=_pipeline_session_launcher)
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_pipeline_cancel(self, pid: str) -> None:
        ok, msg = pipelines.cancel_pipeline(pid)
        if not ok:
            return self._send_error_json(409, msg)
        audit.record_pipeline_cancelled(pid)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_stage_retry(self, pid: str, stage_name: str) -> None:
        ok, msg = pipelines.retry_stage(pid, stage_name, session_launcher=_pipeline_session_launcher)
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_stage_skip(self, pid: str, stage_name: str) -> None:
        ok, msg = pipelines.skip_stage(pid, stage_name, session_launcher=_pipeline_session_launcher)
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_gate_approve(self, pid: str, stage_name: str) -> None:
        body = self._json_body() or {}
        notes = body.get("notes", "")
        ok, msg = pipelines.approve_gate(pid, stage_name, notes=notes, session_launcher=_pipeline_session_launcher)
        if not ok:
            return self._send_error_json(409, msg)
        audit.record_gate_approved(pid, stage_name, notes)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_pipeline_rollback(self, pid: str) -> None:
        body = self._json_body() or {}
        ok, msg = pipelines.rollback_pipeline(pid, reason=body.get("reason", ""))
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_post_pipeline_merge(self, pid: str) -> None:
        ok, msg = pipelines.approve_merge(pid)
        if not ok:
            return self._send_error_json(409, msg)
        self._send_json({"ok": True, "message": msg})

    def _handle_get_pipeline_snapshot(self, pid: str) -> None:
        data = pipelines.get_snapshot(pid)
        if not data:
            return self._send_error_json(404, f"Pipeline {pid} not found")
        self._send_json(data)

    def _handle_get_templates(self) -> None:
        self._send_json(pipelines.list_templates())

    def _handle_get_pipeline_dry_run(self) -> None:
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        template = params.get("template", "")
        if not template:
            return self._send_error_json(400, "template query param required")
        result, err = pipelines.dry_run(template)
        if err:
            return self._send_error_json(400, err)
        self._send_json(result)

    # --- Work Guard handlers ---

    def _handle_get_work_guard_status(self) -> None:
        status = work_guard.get_status(str(REPO_ROOT))
        self._send_json(status)

    def _handle_get_work_guard_safe_to_run(self) -> None:
        result = work_guard.safe_to_run(str(REPO_ROOT))
        self._send_json(result)

    def _handle_post_work_guard_lock(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        ok = work_guard.acquire_lock(str(REPO_ROOT), body)
        if not ok:
            return self._send_error_json(409, "Lock already held — cannot acquire")
        self._send_json({"ok": True, "lock": work_guard.read_lock(str(REPO_ROOT))}, 201)

    def _handle_delete_work_guard_lock(self) -> None:
        body = self._json_body()
        lock_id = (body or {}).get("lockId", "")
        if not lock_id:
            return self._send_error_json(400, "lockId is required")
        ok = work_guard.release_lock(str(REPO_ROOT), lock_id)
        if not ok:
            return self._send_error_json(409, "Lock not found or lockId mismatch")
        self._send_json({"ok": True})

    def _handle_post_work_guard_heartbeat(self) -> None:
        body = self._json_body()
        lock_id = (body or {}).get("lockId", "")
        if not lock_id:
            return self._send_error_json(400, "lockId is required")
        ok = work_guard.update_heartbeat(str(REPO_ROOT), lock_id)
        if not ok:
            return self._send_error_json(409, "Lock not found or lockId mismatch")
        self._send_json({"ok": True})

    # --- Event handlers ---

    def _handle_sse_stream(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        from queue import Empty

        q = events.subscribe()
        try:
            connect_msg = json.dumps({"status": "connected"})
            self.wfile.write(f"event: connected\ndata: {connect_msg}\n\n".encode("utf-8"))
            self.wfile.flush()

            while not events.is_shutdown():
                try:
                    event = q.get(timeout=25)
                    if event.get("type") == "__shutdown__":
                        break
                    payload = json.dumps(event)
                    msg = f"id: {event['id']}\nevent: {event['type']}\ndata: {payload}\n\n"
                    self.wfile.write(msg.encode("utf-8"))
                    self.wfile.flush()
                except Empty:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            events.unsubscribe(q)

    def _handle_get_events(self) -> None:
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
        limit = int(params.get("limit", "50"))
        event_type = params.get("type", "")
        since = params.get("since", "")

        history = events.get_history(
            limit=limit,
            event_type=event_type or None,
            since=since or None,
        )
        self._send_json({"events": history, "total": len(history)})

    def _handle_get_events_stats(self) -> None:
        self._send_json(events.get_stats())

    # --- GrooveNet handlers ---

    def _groovenet_data_path(self, name: str) -> Path:
        return DATA_DIR / f"groovenet-{name}.json"

    def _groovenet_read(self, name: str) -> list:
        p = self._groovenet_data_path(name)
        if not p.exists():
            return []
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return []

    def _groovenet_write(self, name: str, data: list) -> None:
        p = self._groovenet_data_path(name)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(p)

    def _handle_get_groovenet_events(self) -> None:
        self._send_json(self._groovenet_read("events"))

    def _handle_post_groovenet_events(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        evts = self._groovenet_read("events")
        if not body.get("id"):
            body["id"] = f"evt-{len(evts) + 1:03d}"
        evts.append(body)
        self._groovenet_write("events", evts)
        self._send_json(body, 201)

    def _handle_get_groovenet_sets(self) -> None:
        self._send_json(self._groovenet_read("sets"))

    def _handle_post_groovenet_sets(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        all_sets = self._groovenet_read("sets")
        if not body.get("id"):
            body["id"] = f"set-{len(all_sets) + 1:03d}"
        all_sets.append(body)
        self._groovenet_write("sets", all_sets)
        self._send_json(body, 201)

    def _handle_patch_groovenet_set(self, set_id: str) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        all_sets = self._groovenet_read("sets")
        for i, s in enumerate(all_sets):
            if s.get("id") == set_id:
                all_sets[i] = {**s, **body, "id": set_id}
                self._groovenet_write("sets", all_sets)
                return self._send_json(all_sets[i])
        self._send_error_json(404, "Set not found")

    def _handle_get_groovenet_profile(self) -> None:
        p = self._groovenet_data_path("profile")
        if not p.exists():
            return self._send_json({})
        try:
            self._send_json(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, ValueError):
            self._send_json({})

    def _handle_put_groovenet_profile(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        p = self._groovenet_data_path("profile")
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(body, indent=2), encoding="utf-8")
        tmp.replace(p)
        self._send_json(body)

    # --- Request handlers ---

    def _requests_path(self, slug: str) -> Path:
        return REPO_ROOT / "projects" / slug / "requests.json"

    def _read_requests(self, slug: str) -> list:
        p = self._requests_path(slug)
        if not p.exists():
            return []
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            return []

    def _write_requests(self, slug: str, data: list) -> None:
        p = self._requests_path(slug)
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
        tmp.replace(p)

    def _handle_get_requests(self, slug: str) -> None:
        self._send_json(self._read_requests(slug))

    def _handle_post_request(self, slug: str) -> None:
        body = self._json_body()
        if not body or not body.get("title"):
            return self._send_error_json(400, "title is required")
        reqs = self._read_requests(slug)
        body["id"] = f"REQ-{len(reqs) + 1:03d}"
        if "created" not in body:
            from datetime import datetime, timezone
            body["created"] = datetime.now(timezone.utc).isoformat()
        if "status" not in body:
            body["status"] = "open"
        if "comments" not in body:
            body["comments"] = []
        reqs.append(body)
        self._write_requests(slug, reqs)
        self._send_json(body, 201)

    def _handle_patch_request(self, slug: str, req_id: str) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        reqs = self._read_requests(slug)
        for r in reqs:
            if r.get("id") == req_id:
                for k, v in body.items():
                    r[k] = v
                self._write_requests(slug, reqs)
                return self._send_json(r)
        return self._send_error_json(404, f"Request {req_id} not found")

    # --- Memory handlers ---

    def _match_memory_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/projects/([a-zA-Z0-9_-]+)/memory(?:/(.+))?$", path)
        if m:
            return m.group(1), m.group(2)
        return None

    def _parse_query_params(self) -> Dict[str, str]:
        query = self.path.split("?", 1)[1] if "?" in self.path else ""
        return dict(p.split("=", 1) for p in query.split("&") if "=" in p)

    def _handle_get_memories(self, slug: str) -> None:
        params = self._parse_query_params()
        result = memory.list_memories(
            project_slug=slug,
            memory_type=params.get("type"),
            status=params.get("status", "active"),
            limit=int(params.get("limit", "50")),
            offset=int(params.get("offset", "0")),
        )
        self._send_json(result)

    def _handle_post_memory_store(self, slug: str) -> None:
        body = self._json_body()
        if not body or not body.get("content"):
            return self._send_error_json(400, "content is required")
        entry = memory.store(
            project_slug=slug,
            content=body["content"],
            source=body.get("source", ""),
            memory_type=body.get("type", "fact"),
            tags=body.get("tags"),
            metadata=body.get("metadata"),
            session_id=body.get("session_id", ""),
        )
        self._send_json(entry, 201)

    def _handle_post_memory_search(self, slug: str) -> None:
        body = self._json_body()
        if not body or not body.get("query"):
            return self._send_error_json(400, "query is required")
        results = memory.search(
            project_slug=slug,
            query=body["query"],
            limit=int(body.get("limit", 10)),
            memory_type=body.get("type"),
            tags=body.get("tags"),
        )
        self._send_json({"results": results, "total": len(results)})

    def _handle_get_memory_by_id(self, slug: str, memory_id: str) -> None:
        entry = memory.recall(slug, memory_id)
        if not entry:
            return self._send_error_json(404, f"Memory {memory_id} not found")
        evidence = memory.get_evidence(slug, memory_id)
        entry["evidence"] = evidence
        self._send_json(entry)

    def _handle_patch_memory(self, slug: str, memory_id: str) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        result = memory.update_memory(slug, memory_id, body)
        if not result:
            return self._send_error_json(404, f"Memory {memory_id} not found")
        self._send_json(result)

    def _handle_post_memory_evidence(self, slug: str, memory_id: str) -> None:
        body = self._json_body()
        if not body or not body.get("reference"):
            return self._send_error_json(400, "reference is required")
        record = memory.add_evidence(
            project_slug=slug,
            memory_id=memory_id,
            evidence_type=body.get("type", "reference"),
            reference=body["reference"],
            description=body.get("description", ""),
        )
        self._send_json(record, 201)

    def _handle_get_memory_stats(self, slug: str) -> None:
        self._send_json(memory.get_stats(slug))

    # --- Project listing ---

    def _handle_get_projects(self) -> None:
        projects_dir = REPO_ROOT / "projects"
        result = []
        if projects_dir.exists():
            for p in sorted(projects_dir.iterdir()):
                pj = p / "project.json"
                if pj.exists():
                    try:
                        data = json.loads(pj.read_text(encoding="utf-8"))
                        result.append(data)
                    except (json.JSONDecodeError, OSError):
                        pass
        self._send_json(result)

    def _handle_post_projects(self) -> None:
        body = self._json_body()
        if not body or not body.get("slug"):
            return self._send_error_json(400, "slug is required")

        slug = body["slug"]
        project_dir = REPO_ROOT / "projects" / slug
        if (project_dir / "project.json").exists():
            return self._send_error_json(409, f"Project {slug} already exists")

        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "wiki").mkdir(exist_ok=True)
        (project_dir / "phases").mkdir(exist_ok=True)

        project = {
            "name": body.get("name", slug),
            "slug": slug,
            "description": body.get("description", ""),
            "status": "active",
            "created": body.get("created", _now_iso()[:10]),
            "platform": body.get("platform", "web-responsive"),
            "stack": body.get("stack", {}),
            "phases": body.get("phases", []),
        }
        if body.get("onboarding"):
            project["onboarding"] = body["onboarding"]

        pj = project_dir / "project.json"
        tmp = pj.with_suffix(".tmp")
        tmp.write_text(json.dumps(project, indent=2), encoding="utf-8")
        tmp.replace(pj)

        # Add phases to phase-status.json if provided
        if project.get("phases"):
            from engine import bootstrap
            existing = bootstrap.get_all_phases()
            new_phases = []
            for ph in project["phases"]:
                phase_id = f"{slug[:2]}-{ph['id']}" if not ph["id"].startswith(slug[:2]) else ph["id"]
                new_phases.append({
                    "phaseId": phase_id,
                    "name": ph.get("name", ""),
                    "project": slug,
                    "status": ph.get("status", "planned"),
                    "dependencies": ph.get("dependencies", []),
                    "blockedBy": [],
                    "blocks": ph.get("blocks", []),
                    "estimatedComplexity": ph.get("estimatedComplexity", "M"),
                    "riskLevel": ph.get("riskLevel", "low"),
                    "approvalRequired": ph.get("approvalRequired", False),
                    "canRunInParallel": ph.get("canRunInParallel", False),
                    "description": ph.get("description", ""),
                    "lastUpdated": _now_iso()[:10],
                })
            all_phases = existing + new_phases
            bootstrap._save_phases(all_phases)

        events.emit("project.created", {
            "slug": slug,
            "name": project["name"],
        }, source="server")

        self._send_json(project, 201)

    # --- Project phases handlers ---

    def _match_project_phases_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/projects/([a-zA-Z0-9_-]+)/phases(?:/([a-zA-Z0-9_-]+))?(?:/(\w+))?$", path)
        if m:
            return m.group(1), m.group(2), m.group(3)
        return None

    def _handle_get_project_phases(self, slug: str) -> None:
        phases = bootstrap.get_all_phases(project=slug)
        summary = bootstrap.get_summary(phases)
        self._send_json({"phases": phases, "summary": summary})

    def _handle_get_project_phase(self, slug: str, phase_id: str) -> None:
        phase = bootstrap.get_phase(phase_id)
        if not phase or phase.get("project") != slug:
            return self._send_error_json(404, f"Phase {phase_id} not found in project {slug}")
        self._send_json(phase)

    def _handle_post_phase_execute(self, slug: str, phase_id: str) -> None:
        phase = bootstrap.get_phase(phase_id)
        if not phase or phase.get("project") != slug:
            return self._send_error_json(404, f"Phase {phase_id} not found in project {slug}")

        existing = pipelines.list_pipelines(project_slug=slug, status="running")
        for p in existing:
            if phase_id in p.get("name", ""):
                return self._send_error_json(409, f"Phase {phase_id} already has a running pipeline: {p['id']}")

        body = self._json_body() or {}

        project_path = REPO_ROOT / "projects" / slug
        if not project_path.exists():
            return self._send_error_json(404, f"Project directory not found: {slug}")

        phase_name = phase.get("name", phase_id)
        command = phase.get("command", "")

        # Build rich phase context from project.json
        phase_readme = phase.get("description", "")
        pj_path = project_path / "project.json"
        if pj_path.exists():
            try:
                pj = json.loads(pj_path.read_text(encoding="utf-8"))
                project_desc = pj.get("description", "")
                stack = pj.get("stack", {})
                tiers = pj.get("tiers", {})
                # Find the full phase definition from project.json
                for pj_phase in pj.get("phases", []):
                    if pj_phase.get("id") == phase_id.split("-", 1)[-1] or pj_phase.get("name") == phase_name:
                        if pj_phase.get("description"):
                            phase_readme = pj_phase["description"]
                        break

                # If no command file, build a rich prompt from project context
                if not command:
                    parts = [f"## Project: {pj.get('name', slug)}"]
                    if project_desc:
                        parts.append(f"\n{project_desc}")
                    if stack:
                        parts.append(f"\n### Stack\n{json.dumps(stack, indent=2)}")
                    if tiers:
                        parts.append("\n### Product Tiers")
                        for k, v in tiers.items():
                            parts.append(f"- **{k}**: {v}")
                    # List all phases for context
                    parts.append("\n### Roadmap Phases")
                    for pj_ph in pj.get("phases", []):
                        marker = ">>>" if pj_ph.get("name") == phase_name else "   "
                        parts.append(f"{marker} {pj_ph.get('id', '?')}: {pj_ph.get('name', '')} [{pj_ph.get('status', 'planned')}]")
                        if pj_ph.get("name") == phase_name:
                            parts.append(f"    {pj_ph.get('description', '')}")
                    parts.append(f"\n### Current Phase: {phase_name}")
                    parts.append(phase_readme)
                    parts.append("\nYou are working on the phase marked with >>>.")
                    parts.append("First, produce a detailed phase specification with:")
                    parts.append("- Concrete deliverables (files, endpoints, models, UI components)")
                    parts.append("- Acceptance criteria (testable conditions)")
                    parts.append("- Dependencies on other phases")
                    parts.append("- Key constraints and risks")
                    parts.append("\nThen produce the implementation plan.")
                    phase_readme = "\n".join(parts)
            except (json.JSONDecodeError, OSError):
                pass

        pipe, err = pipelines.create_pipeline(
            name=f"{slug} — {phase_name}",
            template_slug=body.get("template", "standard-phase"),
            project_slug=slug,
            repo_path=str(project_path),
            variables={
                "phase_number": phase_id,
                "phase_name": phase_name,
                "phase_readme": phase_readme,
                "phase_command": command,
            },
            model=body.get("model", DEFAULT_CONFIG["default_model"]),
            budget_usd=float(body.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
            timeout_min=int(body.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
        )
        if err:
            return self._send_error_json(400, err)

        bootstrap.update_phase_status(phase_id, "running", activeSessionId=pipe["id"])

        if body.get("auto_start", True):
            pipelines.start_pipeline(pipe["id"], session_launcher=_pipeline_session_launcher)

        events.emit("phase.execution_started", {
            "phaseId": phase_id,
            "phaseName": phase_name,
            "project": slug,
            "pipelineId": pipe["id"],
        }, source="server")

        self._send_json({"phase": phase, "pipeline": pipe}, 201)

    # --- Onboarding handlers ---

    def _match_onboarding_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/onboarding(?:/([a-zA-Z0-9_]+))?(?:/(\w+))?$", path)
        if m:
            return m.group(1), m.group(2)
        return None

    def _handle_post_onboarding_chat(self) -> None:
        body = self._json_body()
        if not body:
            return self._send_error_json(400, "Request body required")
        sid = body.get("session_id", "")
        message = body.get("message", "")
        if not message:
            return self._send_error_json(400, "message is required")
        if not sid:
            session = onboarding.create_session()
            sid = session["id"]
        try:
            result = onboarding.chat(sid, message)
        except Exception as exc:
            return self._send_error_json(500, str(exc))
        if result.get("error"):
            return self._send_error_json(400, result["error"])
        result["session_id"] = sid
        self._send_json(result)

    def _handle_get_onboarding_session(self, sid: str) -> None:
        session = onboarding.get_session(sid)
        if not session:
            return self._send_error_json(404, f"Onboarding session {sid} not found")
        self._send_json(session)

    def _handle_post_onboarding_create(self, sid: str) -> None:
        result = onboarding.create_project_from_blueprint(sid)
        if result.get("error"):
            status = 409 if "already exists" in result["error"] else 400
            return self._send_error_json(status, result["error"])
        events.emit("project.created", {
            "slug": result["slug"],
            "name": result["project"]["name"],
            "method": "chat-onboarding",
        }, source="onboarding")
        self._send_json(result, 201)

    # --- Config handler ---

    def _handle_get_config(self) -> None:
        self._send_json(DEFAULT_CONFIG)

    # --- HTTP verbs ---

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/sessions":
            return self._handle_get_sessions()
        if path == "/api/config":
            return self._handle_get_config()
        if path == "/api/pipelines":
            return self._handle_get_pipelines()
        if path == "/api/templates":
            return self._handle_get_templates()
        if path == "/api/pipelines/dry-run":
            return self._handle_get_pipeline_dry_run()
        if path == "/api/events/stream":
            return self._handle_sse_stream()
        if path == "/api/events":
            return self._handle_get_events()
        if path == "/api/events/stats":
            return self._handle_get_events_stats()
        if path == "/api/work-guard/status":
            return self._handle_get_work_guard_status()
        if path == "/api/work-guard/safe-to-run":
            return self._handle_get_work_guard_safe_to_run()
        if path == "/api/bootstrap/phases":
            return self._handle_get_bootstrap_phases()
        if path == "/api/bootstrap/summary":
            return self._handle_get_bootstrap_summary()
        if path == "/api/groovenet/events":
            return self._handle_get_groovenet_events()
        if path == "/api/groovenet/sets":
            return self._handle_get_groovenet_sets()
        if path == "/api/groovenet/profile":
            return self._handle_get_groovenet_profile()
        if path == "/api/projects":
            return self._handle_get_projects()

        onb_match = self._match_onboarding_route()
        if onb_match:
            sid, action = onb_match
            if sid and action is None:
                return self._handle_get_onboarding_session(sid)
            return self._send_error_json(404, "Not found")

        ppmatch = self._match_project_phases_route()
        if ppmatch:
            slug, phase_id, action = ppmatch
            if phase_id is None:
                return self._handle_get_project_phases(slug)
            if action is None:
                return self._handle_get_project_phase(slug, phase_id)
            return self._send_error_json(404, f"Unknown action: {action}")

        rmatch = re.match(r"^/api/projects/([a-zA-Z0-9_-]+)/requests(?:/(.+))?$", path)
        if rmatch:
            slug, action = rmatch.group(1), rmatch.group(2)
            if action is None:
                return self._handle_get_requests(slug)
            return self._send_error_json(404, f"Unknown action: {action}")

        mmatch = self._match_memory_route()
        if mmatch:
            slug, action = mmatch
            if action is None:
                return self._handle_get_memories(slug)
            if action == "stats":
                return self._handle_get_memory_stats(slug)
            if action.startswith("mem_"):
                return self._handle_get_memory_by_id(slug, action)
            return self._send_error_json(404, f"Unknown memory action: {action}")

        pmatch = self._match_pipeline_route()
        if pmatch:
            pid, action = pmatch
            if action is None:
                return self._handle_get_pipeline(pid)
            if action == "summary":
                return self._handle_get_pipeline_summary(pid)
            if action == "snapshot":
                return self._handle_get_pipeline_snapshot(pid)
            if action == "audit":
                if not pipelines.get_pipeline(pid):
                    return self._send_error_json(404, f"Pipeline {pid} not found")
                return self._send_json(audit.get_audit(pid))
            return self._send_error_json(404, f"Unknown action: {action}")

        bmatch = self._match_bootstrap_route()
        if bmatch:
            phase_id, action = bmatch
            if action is None:
                return self._handle_get_bootstrap_phase(phase_id)
            return self._send_error_json(404, f"Unknown action: {action}")

        match = self._match_session_route()
        if match:
            sid, action = match
            if action is None:
                return self._handle_get_session(sid)
            if action == "output":
                return self._handle_get_output(sid)
            if action == "validation":
                return self._handle_get_session_validation(sid)
            return self._send_error_json(404, f"Unknown action: {action}")

        return super().do_GET()

    def do_POST(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/sessions":
            return self._handle_post_sessions()
        if path == "/api/pipelines":
            return self._handle_post_pipelines()
        if path == "/api/work-guard/lock":
            return self._handle_post_work_guard_lock()
        if path == "/api/work-guard/heartbeat":
            return self._handle_post_work_guard_heartbeat()
        if path == "/api/projects":
            return self._handle_post_projects()
        if path == "/api/onboarding/chat":
            return self._handle_post_onboarding_chat()
        onb_match = self._match_onboarding_route()
        if onb_match:
            sid, action = onb_match
            if sid and action == "create":
                return self._handle_post_onboarding_create(sid)
            return self._send_error_json(404, "Not found")
        if path == "/api/groovenet/events":
            return self._handle_post_groovenet_events()
        if path == "/api/groovenet/sets":
            return self._handle_post_groovenet_sets()
        ppmatch = self._match_project_phases_route()
        if ppmatch:
            slug, phase_id, action = ppmatch
            if phase_id and action == "execute":
                return self._handle_post_phase_execute(slug, phase_id)
            return self._send_error_json(404, f"Unknown phase action: {action}")

        if re.match(r"^/api/projects/[a-zA-Z0-9_-]+/requests$", path):
            slug = path.split("/")[3]
            return self._handle_post_request(slug)

        mmatch = self._match_memory_route()
        if mmatch:
            slug, action = mmatch
            if action is None or action == "store":
                return self._handle_post_memory_store(slug)
            if action == "search":
                return self._handle_post_memory_search(slug)
            if action.startswith("mem_") and action.endswith("/evidence"):
                mid = action.replace("/evidence", "")
                return self._handle_post_memory_evidence(slug, mid)
            return self._send_error_json(404, f"Unknown memory action: {action}")

        pmatch = self._match_pipeline_route()
        if pmatch:
            pid, action = pmatch
            if action == "start":
                return self._handle_post_pipeline_start(pid)
            if action == "advance":
                return self._handle_post_pipeline_advance(pid)
            if action == "cancel":
                return self._handle_post_pipeline_cancel(pid)
            if action == "rollback":
                return self._handle_post_pipeline_rollback(pid)
            if action == "merge":
                return self._handle_post_pipeline_merge(pid)
            m = re.match(r"^stages/([a-zA-Z0-9_-]+)/(retry|skip|approve)$", action or "")
            if m:
                stage_name, op = m.group(1), m.group(2)
                if op == "retry":
                    return self._handle_post_stage_retry(pid, stage_name)
                if op == "skip":
                    return self._handle_post_stage_skip(pid, stage_name)
                if op == "approve":
                    return self._handle_post_gate_approve(pid, stage_name)
            return self._send_error_json(404, f"Unknown action: {action}")

        bmatch = self._match_bootstrap_route()
        if bmatch:
            phase_id, action = bmatch
            if action == "blocker":
                return self._handle_post_bootstrap_blocker(phase_id)
            return self._send_error_json(404, f"Unknown action: {action}")

        match = self._match_session_route()
        if match:
            sid, action = match
            if action == "cancel":
                return self._handle_cancel_session(sid)
            if action == "validate":
                return self._handle_post_session_validate(sid)
            if action == "continue":
                return self._handle_post_continue_session(sid)
            return self._send_error_json(404, f"Unknown action: {action}")

        return self._send_error_json(404, "Not found")

    def do_PATCH(self) -> None:
        path = self.path.split("?")[0]
        rmatch = re.match(r"^/api/projects/([a-zA-Z0-9_-]+)/requests/(.+)$", path)
        if rmatch:
            return self._handle_patch_request(rmatch.group(1), rmatch.group(2))

        mmatch = self._match_memory_route()
        if mmatch:
            slug, action = mmatch
            if action and action.startswith("mem_"):
                return self._handle_patch_memory(slug, action)
            return self._send_error_json(404, f"Unknown memory action: {action}")

        bmatch = self._match_bootstrap_route()
        if bmatch:
            phase_id, action = bmatch
            if action is None:
                return self._handle_patch_bootstrap_phase(phase_id)
            return self._send_error_json(404, f"Unknown action: {action}")

        gn_set_match = re.match(r"^/api/groovenet/sets/(.+)$", path)
        if gn_set_match:
            return self._handle_patch_groovenet_set(gn_set_match.group(1))

        match = self._match_session_route()
        if match:
            sid, action = match
            if action is None:
                return self._handle_patch_session(sid)
            return self._send_error_json(404, f"Unknown action: {action}")
        return self._send_error_json(404, "Not found")

    def do_PUT(self) -> None:
        path = self.path.split("?")[0]
        if path == "/api/groovenet/profile":
            return self._handle_put_groovenet_profile()
        return self._send_error_json(404, "Not found")

    def do_DELETE(self) -> None:
        path = self.path.split("?")[0]
        if path == "/api/work-guard/lock":
            return self._handle_delete_work_guard_lock()
        match = self._match_session_route()
        if match:
            sid, action = match
            if action is None:
                return self._handle_delete_session(sid)
            return self._send_error_json(404, f"Unknown action: {action}")
        return self._send_error_json(404, "Not found")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args) -> None:
        if "/api/" in self.path:
            super().log_message(format, *args)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def _pipeline_session_launcher(pipeline: Dict[str, Any], stage: Dict[str, Any]) -> str:
    """Create a session for a pipeline stage.  Returns the session ID."""
    session = sessions.create_session(
        project_slug=pipeline.get("project_slug", ""),
        repo_path=pipeline.get("repo_path", str(REPO_ROOT)),
        prompt=stage.get("prompt", ""),
        template=stage.get("template", "implement"),
        model=stage.get("model", DEFAULT_CONFIG["default_model"]),
        budget_usd=float(stage.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
        timeout_min=int(stage.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
        use_worktree=True,
        task_id=f"{pipeline['id']}/{stage['name']}",
        task_title=stage.get("label", stage["name"]),
    )

    def _on_complete(sess):
        success = sess.get("status") == "succeeded"
        report_dict = None

        if success and sess.get("use_worktree"):
            checks = validation.default_checks(sess)
            if checks:
                report = validation.run_validation(sess, checks)
                validation.apply_to_quality_gates(sess, report)
                if pipeline.get("project_slug"):
                    validation.store_evidence(pipeline["project_slug"], sess["id"], report)
                report_dict = {
                    "all_passed": report.all_passed,
                    "results": [{"check_name": r.check_name, "passed": r.passed,
                                 "output": r.output, "duration_ms": r.duration_ms}
                                for r in report.results],
                }
                audit.record_validation_ran(pipeline["id"], stage["name"], report_dict)
                events.emit("session.validated", {
                    "sessionId": sess["id"],
                    "allPassed": report.all_passed,
                    "results": len(report.results),
                }, source="validation")
                if not report.all_passed:
                    success = False

        audit.record_stage_completed(pipeline["id"], stage["name"], sess, report_dict)

        pipelines.handle_stage_complete(
            pid=pipeline["id"],
            stage_name=stage["name"],
            success=success,
            error=sess.get("error"),
            cost_usd=sess.get("cost_usd", 0.0),
            session_launcher=_pipeline_session_launcher,
        )

        pipe = pipelines.get_pipeline(pipeline["id"])
        if pipe and pipe.get("status") in ("completed", "failed"):
            audit.record_pipeline_completed(pipe["id"], pipe["status"], pipe.get("cost_usd", 0.0))

    sessions.set_on_complete_for(session["id"], _on_complete)
    return session["id"]


def _shutdown() -> None:
    print("[conductor] Shutting down — cleaning up sessions...")
    events.emit("system.shutdown", {}, source="server")
    events.shutdown()
    pipelines.shutdown()
    sessions.shutdown()
    print("[conductor] Shutdown complete.")


atexit.register(_shutdown)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    gi = SESSIONS_DIR / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")

    sessions.configure(
        data_dir=DATA_DIR,
        sessions_dir=SESSIONS_DIR,
        default_config=DEFAULT_CONFIG,
    )
    sessions.load_state()

    pipelines.configure(
        data_dir=DATA_DIR,
        sessions_dir=SESSIONS_DIR,
        repo_root=REPO_ROOT,
    )
    pipelines.load_state()

    validation.configure(data_dir=DATA_DIR)
    audit.configure(data_dir=DATA_DIR)

    def _on_stage_transition(pipeline, stage, old_status, new_status):
        pid = pipeline.get("id", "")
        name = stage.get("name", "")
        if new_status == "running":
            audit.record_stage_started(pid, name, stage.get("prompt", ""))
        elif new_status == "failed":
            audit.record_stage_failed(pid, name, stage.get("error", ""))
        elif new_status == "skipped":
            audit.record_stage_skipped(pid, name)
        elif new_status == "cancelled":
            audit.record_stage_skipped(pid, name)

    pipelines.set_on_stage_transition(_on_stage_transition)

    events.configure(max_events=500)
    events.emit("system.startup", {"port": PORT}, source="server")

    print(f"[conductor] Conductor — Product Orchestrator")
    print(f"[conductor] Dashboard:  http://127.0.0.1:{PORT}/")
    print(f"[conductor] API:        http://127.0.0.1:{PORT}/api/sessions")
    print(f"[conductor] Pipelines:  http://127.0.0.1:{PORT}/api/pipelines")
    print(f"[conductor] Templates:  http://127.0.0.1:{PORT}/api/templates")
    print(f"[conductor] Events:     http://127.0.0.1:{PORT}/api/events")
    print(f"[conductor] SSE:        http://127.0.0.1:{PORT}/api/events/stream")
    print(f"[conductor] Max parallel: {DEFAULT_CONFIG['max_parallel']}")
    print()

    server = ThreadingHTTPServer(("127.0.0.1", PORT), ConductorHandler)

    def _sigint(sig, frame):
        print("\n[conductor] Caught SIGINT, shutting down...")
        server.shutdown()

    signal.signal(signal.SIGINT, _sigint)

    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
