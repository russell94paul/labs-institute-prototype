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

REPO_ROOT = Path(__file__).resolve().parent.parent
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

        match = self._match_session_route()
        if match:
            sid, action = match
            if action is None:
                return self._handle_get_session(sid)
            if action == "output":
                return self._handle_get_output(sid)
            return self._send_error_json(404, f"Unknown action: {action}")

        return super().do_GET()

    def do_POST(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/sessions":
            return self._handle_post_sessions()

        match = self._match_session_route()
        if match:
            sid, action = match
            if action == "cancel":
                return self._handle_cancel_session(sid)
            return self._send_error_json(404, f"Unknown action: {action}")

        return self._send_error_json(404, "Not found")

    def do_PATCH(self) -> None:
        match = self._match_session_route()
        if match:
            sid, action = match
            if action is None:
                return self._handle_patch_session(sid)
            return self._send_error_json(404, f"Unknown action: {action}")
        return self._send_error_json(404, "Not found")

    def do_DELETE(self) -> None:
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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args) -> None:
        if "/api/" in self.path:
            super().log_message(format, *args)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def _shutdown() -> None:
    print("[conductor] Shutting down — cleaning up sessions...")
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

    print(f"[conductor] Conductor — Product Orchestrator")
    print(f"[conductor] Dashboard:  http://127.0.0.1:{PORT}/")
    print(f"[conductor] API:        http://127.0.0.1:{PORT}/api/sessions")
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
