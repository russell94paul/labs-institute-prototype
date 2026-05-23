"""NeuroSpect Orchestrator — static file server + Claude Code session manager.

Serves platform/orchestrator/ over HTTP and adds /api/* routes for creating,
monitoring, and managing parallel Claude Code sessions. Each session launches
``claude -p`` as a subprocess, captures stream-json output, and tracks state.

Run from repo root:
    python platform/orchestrator/server.py
"""
from __future__ import annotations

import atexit
import http.server
import json
import os
import re
import signal
import socketserver
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATIC_ROOT = Path(__file__).resolve().parent
SESSIONS_DIR = REPO_ROOT / ".sessions"
DATA_DIR = STATIC_ROOT / "data"
SESSIONS_DATA_DIR = DATA_DIR / "sessions"
STATE_FILE = DATA_DIR / "sessions.json"

PORT = 8766

DEFAULT_CONFIG: Dict[str, Any] = {
    "max_parallel": 4,
    "default_budget_usd": 5.0,
    "default_timeout_min": 60,
    "default_model": "sonnet",
}

_lock = threading.Lock()
_sessions: Dict[str, Dict[str, Any]] = {}
_procs: Dict[str, subprocess.Popen] = {}
_timers: Dict[str, threading.Timer] = {}
_pool = ThreadPoolExecutor(max_workers=DEFAULT_CONFIG["max_parallel"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def _short_id() -> str:
    return uuid.uuid4().hex[:8]

def _flush_state() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"sessions": list(_sessions.values()), "config": DEFAULT_CONFIG}
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)

def _load_state() -> None:
    if not STATE_FILE.exists():
        return
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    for sess in data.get("sessions", []):
        sid = sess.get("id")
        if not sid:
            continue
        if sess.get("status") in ("running", "queued"):
            sess["status"] = "failed"
            sess["error"] = "Server restarted"
            sess["ended_at"] = _now_iso()
        _sessions[sid] = sess

# Phase-aware prompt templates
TEMPLATES: Dict[str, str] = {
    "plan": (
        "You are an autonomous Claude Code agent. Enter plan mode. "
        "Read the slash command context, explore existing code, and produce "
        "a detailed implementation plan. Do NOT implement — plan only."
    ),
    "implement": (
        "You are an autonomous Claude Code agent. Read the slash command "
        "and implement the deliverables. Follow the boot procedure, "
        "acceptance criteria, and constraints. Commit when done."
    ),
    "review": (
        "You are an autonomous Claude Code agent reviewing code. "
        "Check correctness, security, tests, and acceptance criteria."
    ),
    "fix_bug": (
        "You are an autonomous Claude Code agent. Investigate and fix "
        "the bug. Read relevant code, reproduce, fix, verify, commit."
    ),
    "analyze": (
        "You are an autonomous Claude Code agent. Read-only analysis. "
        "Do NOT make changes. Report findings and recommendations."
    ),
}

COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"


def _read_file_safe(path: Path, max_chars: int = 12000) -> Optional[str]:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n\n... (truncated at {max_chars} chars)"
        return text
    except OSError:
        return None


def _build_prompt(session: Dict[str, Any]) -> str:
    """Build a rich autonomous prompt by injecting the full slash command + boot files."""
    template_key = session.get("template", "implement")
    template_text = TEMPLATES.get(template_key, TEMPLATES["implement"])
    user_prompt = session.get("prompt", "").strip()
    command = session.get("command", "")
    phase_id = session.get("phase_id", "")

    parts = [template_text]

    # 1. Load the slash command file (the full phase spec)
    cmd_file = _find_command_file(command, phase_id)
    if cmd_file:
        cmd_content = _read_file_safe(cmd_file, max_chars=15000)
        if cmd_content:
            parts.append(f"# Phase Specification\n\n{cmd_content}")

            # 2. Read boot procedure files referenced in the command
            boot_files = _extract_boot_files(cmd_content)
            boot_context = []
            for bf in boot_files[:8]:
                content = _read_file_safe(Path(bf), max_chars=8000)
                if content:
                    boot_context.append(f"## File: {bf}\n\n{content}")
            if boot_context:
                parts.append("# Boot Procedure Context\n\n" + "\n\n---\n\n".join(boot_context))

    # 3. Always include root CLAUDE.md for project context
    claude_md = _read_file_safe(REPO_ROOT / "CLAUDE.md", max_chars=10000)
    if claude_md:
        parts.append(f"# Project Context (CLAUDE.md)\n\n{claude_md}")

    # 4. Include user prompt if provided
    if user_prompt:
        ctx_marker = "\n--- CONTEXT ---\n"
        if ctx_marker in user_prompt:
            user_prompt = user_prompt[:user_prompt.index(ctx_marker)].strip()
        if user_prompt:
            parts.append(f"# Additional Instructions\n\n{user_prompt}")

    # 5. Autonomous execution instructions
    parts.append("""# Execution Mode: Autonomous

You are running autonomously in a git worktree. Work through ALL deliverables in the phase specification above.

For each deliverable:
1. Read existing code to understand current patterns
2. Implement the deliverable following the constraints
3. Write tests where specified
4. Commit your work with a descriptive message referencing the phase and deliverable

When ALL deliverables are complete:
- Run any tests you wrote
- Verify the acceptance criteria
- Create a final summary commit

Do not ask questions. Make reasonable decisions and document assumptions in code comments.
Do not skip deliverables. Work through them in order.
Commit after each major deliverable, not all at once.""")

    return "\n\n".join(parts)


def _find_command_file(command: str, phase_id: str) -> Optional[Path]:
    """Find the .claude/commands/ file for a phase."""
    if command:
        slug = command.lstrip("/")
        candidate = COMMANDS_DIR / f"{slug}.md"
        if candidate.exists():
            return candidate
    for f in COMMANDS_DIR.glob("ns-phase*.md"):
        if str(phase_id) in f.stem:
            return f
    return None


def _extract_boot_files(cmd_content: str) -> List[str]:
    """Extract file paths from Boot Procedure section."""
    import re
    files = []
    in_boot = False
    for line in cmd_content.split("\n"):
        if "Boot Procedure" in line:
            in_boot = True
            continue
        if in_boot and line.startswith("##"):
            break
        if in_boot:
            paths = re.findall(r'`(C:\\[^`]+|[a-zA-Z]/[^`]+)`', line)
            for p in paths:
                files.append(p)
            md_paths = re.findall(r'Read\s+(.+\.(?:md|py|ts|json))', line)
            for p in md_paths:
                p = p.strip().strip('`')
                if not p.startswith("C:"):
                    p = str(REPO_ROOT / p)
                files.append(p)
    return files

def _extract_usage(session: Dict[str, Any], event: Dict[str, Any]) -> None:
    if "total_cost_usd" in event:
        session["cost_usd"] = event["total_cost_usd"]
    elif "cost_usd" in event:
        session["cost_usd"] = event["cost_usd"]
    usage = event.get("usage") or (event.get("message", {}) or {}).get("usage")
    if isinstance(usage, dict):
        session["tokens_in"] = usage.get("input_tokens", session.get("tokens_in", 0))
        session["tokens_out"] = usage.get("output_tokens", session.get("tokens_out", 0))
    model_usage = event.get("modelUsage")
    if isinstance(model_usage, dict):
        for _, mu in model_usage.items():
            if isinstance(mu, dict):
                session["tokens_in"] = mu.get("inputTokens", session.get("tokens_in", 0))
                session["tokens_out"] = mu.get("outputTokens", session.get("tokens_out", 0))
                if "costUSD" in mu:
                    session["cost_usd"] = mu["costUSD"]

def _create_worktree(session: Dict[str, Any]) -> Path:
    sid = session["id"]
    branch = session["branch"]
    wt_path = SESSIONS_DIR / sid
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    gi = SESSIONS_DIR / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")
    subprocess.run(
        ["git", "worktree", "add", str(wt_path), "-b", branch],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=True,
    )
    return wt_path

def _remove_worktree(session: Dict[str, Any]) -> None:
    wt_path = SESSIONS_DIR / session["id"]
    branch = session.get("branch", "")
    if wt_path.exists():
        subprocess.run(["git", "worktree", "remove", str(wt_path), "--force"],
                       cwd=str(REPO_ROOT), capture_output=True, text=True)
    if branch:
        subprocess.run(["git", "branch", "-D", branch],
                       cwd=str(REPO_ROOT), capture_output=True, text=True)

def _run_session(sid: str) -> None:
    with _lock:
        session = _sessions.get(sid)
        if not session or session["status"] == "cancelled":
            return
        session["status"] = "running"
        session["started_at"] = _now_iso()
        _flush_state()

    prompt = _build_prompt(session)
    budget = str(session.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"]))
    model = session.get("model", DEFAULT_CONFIG["default_model"])
    timeout_min = session.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])

    working_dir = str(REPO_ROOT)
    if session.get("use_worktree"):
        try:
            wt = _create_worktree(session)
            working_dir = str(wt)
        except subprocess.CalledProcessError as exc:
            with _lock:
                session["status"] = "failed"
                session["error"] = f"Worktree failed: {exc.stderr or exc}"
                session["ended_at"] = _now_iso()
                _flush_state()
            return

    SESSIONS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_file = SESSIONS_DATA_DIR / f"{sid}.jsonl"

    cmd = [
        "claude", "-p", "--verbose",
        "--output-format", "stream-json",
        "--max-turns", "50",
        "--max-budget-usd", budget,
        "--model", model,
    ]
    if session.get("use_worktree"):
        cmd.append("--dangerously-skip-permissions")
    else:
        cmd.extend(["--permission-mode", "auto"])

    env = {**os.environ, "NO_COLOR": "1"}
    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=working_dir, bufsize=0, env=env,
        )
    except (FileNotFoundError, OSError) as exc:
        with _lock:
            session["status"] = "failed"
            session["error"] = f"Failed to launch claude: {exc}"
            session["ended_at"] = _now_iso()
            _flush_state()
        return

    with _lock:
        _procs[sid] = proc

    try:
        proc.stdin.write(prompt.encode("utf-8"))
        proc.stdin.close()
    except OSError:
        pass

    def _timeout_kill():
        with _lock:
            if _sessions.get(sid, {}).get("status") == "running":
                _sessions[sid]["status"] = "timeout"
                _sessions[sid]["error"] = f"Exceeded {timeout_min}min timeout"
                _sessions[sid]["ended_at"] = _now_iso()
                _flush_state()
        _kill_proc(sid)

    timer = threading.Timer(timeout_min * 60, _timeout_kill)
    with _lock:
        _timers[sid] = timer
    timer.start()

    line_count = 0
    got_result = False
    with open(output_file, "w", encoding="utf-8") as fout:
        while True:
            raw = proc.stdout.readline()
            if not raw:
                break
            try:
                line_str = raw.decode("utf-8", errors="replace")
            except Exception:
                continue
            fout.write(line_str)
            fout.flush()
            line_count += 1
            try:
                event = json.loads(line_str)
            except (json.JSONDecodeError, ValueError):
                continue
            with _lock:
                session["output_lines"] = line_count
                _extract_usage(session, event)
            if event.get("type") == "result":
                got_result = True
                print(f"[neurospect] Session {sid}: result event")
                break

    timer.cancel()
    try:
        exit_code = proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            exit_code = proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            exit_code = proc.wait()

    if got_result:
        exit_code = 0

    files_changed: List[str] = []
    if session.get("use_worktree"):
        wt_path = SESSIONS_DIR / sid
        if wt_path.exists():
            try:
                diff = subprocess.run(
                    ["git", "diff", "--name-only", "HEAD"],
                    cwd=str(wt_path), capture_output=True, text=True,
                )
                if diff.returncode == 0:
                    files_changed = [f for f in diff.stdout.strip().split("\n") if f]
            except OSError:
                pass

    with _lock:
        if got_result:
            session["status"] = "succeeded"
            session["error"] = None
        elif session["status"] == "running":
            session["status"] = "succeeded" if exit_code == 0 else "failed"
            if exit_code != 0:
                try:
                    stderr_bytes = proc.stderr.read()
                    if stderr_bytes:
                        session["error"] = stderr_bytes.decode("utf-8", errors="replace")[:2000]
                except OSError:
                    pass
        session["ended_at"] = _now_iso()
        session["output_lines"] = line_count
        session["files_changed"] = files_changed
        _procs.pop(sid, None)
        _timers.pop(sid, None)
        _flush_state()

    print(f"[neurospect] Session {sid}: {session['status']}, "
          f"${session.get('cost_usd', 0):.4f}, "
          f"in={session.get('tokens_in', 0)} out={session.get('tokens_out', 0)}")

def _kill_proc(sid: str) -> None:
    proc = _procs.get(sid)
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


class OrchestratorHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_ROOT), **kwargs)

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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, message: str) -> None:
        self._send_json({"error": message}, status)

    def _match_route(self) -> Optional[tuple]:
        path = self.path.split("?")[0]
        m = re.match(r"^/api/sessions/(ses_[a-f0-9]+)(?:/(\w+))?$", path)
        return (m.group(1), m.group(2)) if m else None

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        path = self.path.split("?")[0]
        if path == "/api/sessions":
            with _lock:
                return self._send_json({"sessions": list(_sessions.values()), "config": DEFAULT_CONFIG})
        if path == "/api/config":
            return self._send_json(DEFAULT_CONFIG)
        match = self._match_route()
        if match:
            sid, action = match
            with _lock:
                session = _sessions.get(sid)
            if not session:
                return self._send_error_json(404, "Not found")
            if action is None:
                return self._send_json(session)
            if action == "output":
                query = self.path.split("?", 1)[1] if "?" in self.path else ""
                params = dict(p.split("=", 1) for p in query.split("&") if "=" in p)
                max_lines = int(params.get("lines", "200"))
                output_file = SESSIONS_DATA_DIR / f"{sid}.jsonl"
                if not output_file.exists():
                    return self._send_json({"lines": [], "total": 0})
                try:
                    all_lines = output_file.read_text(encoding="utf-8").splitlines()
                except OSError:
                    return self._send_json({"lines": [], "total": 0})
                total = len(all_lines)
                lines = all_lines[-max_lines:] if max_lines < total else all_lines
                return self._send_json({"lines": lines, "total": total})
        return super().do_GET()

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        if path == "/api/sessions":
            body = self._json_body()
            if not body:
                return self._send_error_json(400, "Body required")
            phase_id = body.get("phase_id", "0")
            short = _short_id()
            sid = f"ses_{short}"
            safe_phase = re.sub(r"[^a-zA-Z0-9_-]", "-", str(phase_id))
            template = body.get("template", "implement")
            exec_mode = body.get("exec_mode", "autonomous")
            read_only = template in ("analyze", "review")
            use_worktree = exec_mode == "autonomous" and not read_only

            session: Dict[str, Any] = {
                "id": sid,
                "phase_id": phase_id,
                "phase_name": body.get("phase_name", ""),
                "command": body.get("command", ""),
                "prompt": body.get("prompt", ""),
                "model": body.get("model", DEFAULT_CONFIG["default_model"]),
                "budget_usd": float(body.get("budget_usd", DEFAULT_CONFIG["default_budget_usd"])),
                "timeout_min": int(body.get("timeout_min", DEFAULT_CONFIG["default_timeout_min"])),
                "use_worktree": use_worktree,
                "exec_mode": exec_mode,
                "template": template,
                "status": "queued",
                "created_at": _now_iso(),
                "started_at": None, "ended_at": None,
                "cost_usd": 0.0, "tokens_in": 0, "tokens_out": 0,
                "worktree_path": f".sessions/{sid}" if use_worktree else None,
                "branch": f"session/phase-{safe_phase}-{short}" if use_worktree else None,
                "output_lines": 0, "files_changed": [],
                "quality_gates": {"compiles": None, "tests_pass": None, "requirements_met": None, "no_security": None},
                "learnings": "", "error": None,
            }
            with _lock:
                _sessions[sid] = session
                _flush_state()
            _pool.submit(_run_session, sid)
            print(f"[neurospect] Session {sid} created for Phase {phase_id}")
            return self._send_json(session, 201)

        match = self._match_route()
        if match:
            sid, action = match
            if action == "cancel":
                with _lock:
                    session = _sessions.get(sid)
                    if not session:
                        return self._send_error_json(404, "Not found")
                    if session["status"] not in ("running", "queued"):
                        return self._send_error_json(409, f"Cannot cancel: {session['status']}")
                    session["status"] = "cancelled"
                    session["ended_at"] = _now_iso()
                    _flush_state()
                _kill_proc(sid)
                timer = _timers.pop(sid, None)
                if timer:
                    timer.cancel()
                return self._send_json({"ok": True})
        return self._send_error_json(404, "Not found")

    def do_PATCH(self) -> None:
        match = self._match_route()
        if match:
            sid, action = match
            if action is None:
                body = self._json_body()
                if not body:
                    return self._send_error_json(400, "Body required")
                with _lock:
                    session = _sessions.get(sid)
                    if not session:
                        return self._send_error_json(404, "Not found")
                    if "quality_gates" in body and isinstance(body["quality_gates"], dict):
                        session["quality_gates"].update(body["quality_gates"])
                    if "learnings" in body:
                        session["learnings"] = str(body["learnings"])
                    if "status" in body and body["status"] in ("reviewing", "merged", "rejected"):
                        session["status"] = body["status"]
                    _flush_state()
                return self._send_json(session)
        return self._send_error_json(404, "Not found")

    def do_DELETE(self) -> None:
        match = self._match_route()
        if match:
            sid, _ = match
            with _lock:
                session = _sessions.get(sid)
                if not session:
                    return self._send_error_json(404, "Not found")
                if session["status"] in ("running", "queued"):
                    session["status"] = "cancelled"
                    session["ended_at"] = _now_iso()
            _kill_proc(sid)
            timer = _timers.pop(sid, None)
            if timer:
                timer.cancel()
            if session.get("use_worktree"):
                _remove_worktree(session)
            output_file = SESSIONS_DATA_DIR / f"{sid}.jsonl"
            if output_file.exists():
                try:
                    output_file.unlink()
                except OSError:
                    pass
            with _lock:
                _sessions.pop(sid, None)
                _procs.pop(sid, None)
                _flush_state()
            return self._send_json({"ok": True})
        return self._send_error_json(404, "Not found")

    def log_message(self, format, *args) -> None:
        if "/api/" in self.path:
            super().log_message(format, *args)


class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def _shutdown() -> None:
    print("[neurospect] Shutting down...")
    with _lock:
        for sid, session in list(_sessions.items()):
            if session["status"] in ("running", "queued"):
                session["status"] = "cancelled"
                session["ended_at"] = _now_iso()
                session["error"] = "Server shutdown"
                _kill_proc(sid)
            timer = _timers.pop(sid, None)
            if timer:
                timer.cancel()
            if session.get("use_worktree") and session.get("error") == "Server shutdown":
                _remove_worktree(session)
        _flush_state()
    _pool.shutdown(wait=False)

atexit.register(_shutdown)


def main() -> None:
    _load_state()
    SESSIONS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    gi = SESSIONS_DIR / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")

    print(f"[neurospect] NeuroSpect Orchestrator")
    print(f"[neurospect] Static:  {STATIC_ROOT}")
    print(f"[neurospect] UI:      http://127.0.0.1:{PORT}/")
    print(f"[neurospect] API:     http://127.0.0.1:{PORT}/api/sessions")
    print(f"[neurospect] Workers: {DEFAULT_CONFIG['max_parallel']} parallel")
    print()

    server = ThreadingHTTPServer(("127.0.0.1", PORT), OrchestratorHandler)
    def _sigint(sig, frame):
        print("\n[neurospect] SIGINT — shutting down...")
        server.shutdown()
    signal.signal(signal.SIGINT, _sigint)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
