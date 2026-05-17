"""Generalized Claude Code session manager.

Thread-safe session lifecycle (create, run, cancel, delete), subprocess
management for ``claude -p``, worktree isolation, cost/token tracking,
and atomic state persistence.  Extracted from the ALDC Launchpad
orchestrator and stripped of all domain-specific logic.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Module-level configuration — call configure() before first use
# ---------------------------------------------------------------------------
_data_dir: Path = Path(".")
_sessions_dir: Path = Path(".sessions")
_sessions_data_dir: Path = Path(".")

_config: Dict[str, Any] = {
    "max_parallel": 8,
    "default_budget_usd": 5.0,
    "default_timeout_min": 60,
    "default_model": "sonnet",
}

_state_file: Path = Path("sessions.json")


def configure(
    data_dir: Path,
    sessions_dir: Path,
    default_config: Optional[Dict[str, Any]] = None,
) -> None:
    """Initialize module paths and config.  Must be called before creating sessions."""
    global _data_dir, _sessions_dir, _sessions_data_dir, _state_file, _config, _pool

    _data_dir = Path(data_dir)
    _sessions_dir = Path(sessions_dir)
    _sessions_data_dir = _data_dir / "sessions"
    _state_file = _data_dir / "sessions.json"

    if default_config:
        _config.update(default_config)

    # Rebuild pool if max_parallel changed
    _pool = ThreadPoolExecutor(max_workers=_config["max_parallel"])

    # Ensure directories
    _data_dir.mkdir(parents=True, exist_ok=True)
    _sessions_data_dir.mkdir(parents=True, exist_ok=True)
    _sessions_dir.mkdir(parents=True, exist_ok=True)
    gi = _sessions_dir / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Callbacks — set by the host application
# ---------------------------------------------------------------------------
_prompt_builder: Optional[Callable[[Dict[str, Any]], str]] = None
_on_session_complete: Optional[Callable[[Dict[str, Any]], None]] = None


def set_prompt_builder(fn: Callable[[Dict[str, Any]], str]) -> None:
    """Register a callback that builds the full prompt from a session dict.

    Signature: fn(session) -> str
    If not set, the default builder uses template + user prompt.
    """
    global _prompt_builder
    _prompt_builder = fn


def set_on_complete(fn: Callable[[Dict[str, Any]], None]) -> None:
    """Register a callback invoked after a session finishes.

    Signature: fn(session) -> None
    Called with the final session dict (status, cost, files_changed, etc.).
    """
    global _on_session_complete
    _on_session_complete = fn


# ---------------------------------------------------------------------------
# Session store (thread-safe)
# ---------------------------------------------------------------------------
_lock = threading.Lock()
_sessions: Dict[str, Dict[str, Any]] = {}
_procs: Dict[str, subprocess.Popen] = {}
_timers: Dict[str, threading.Timer] = {}
_pool = ThreadPoolExecutor(max_workers=_config["max_parallel"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------
_TEMPLATES: Dict[str, str] = {
    "plan": (
        "You are an autonomous Claude Code agent. Read the context below. "
        "Create a plan with: What needs to change, Why, Where (which files), "
        "Constraints, and Open Questions. Propose 2-3 implementation approaches "
        "with effort estimates and trade-offs. Do NOT implement — plan only."
    ),
    "implement": (
        "You are an autonomous Claude Code agent working on a task. "
        "Read the codebase first, understand the existing patterns, then make "
        "the changes. Commit your work when done. Do not ask clarifying "
        "questions — make reasonable decisions and note assumptions in comments."
    ),
    "fix_bug": (
        "You are an autonomous Claude Code agent. Investigate and fix the "
        "following bug. Start by reading the relevant code and reproducing "
        "the issue. Then fix it and verify the fix. Commit when done."
    ),
    "code_review": (
        "You are an autonomous Claude Code agent reviewing code changes. "
        "Review the diff on the current branch for correctness, security, "
        "performance, and style. Summarize findings."
    ),
    "analyze": (
        "You are an autonomous Claude Code agent. Analyze the following area "
        "of the codebase. Do NOT make any changes. Report your findings: "
        "architecture, patterns, potential issues, and recommendations."
    ),
    "investigate": (
        "You are an autonomous Claude Code agent investigating a task. "
        "Research the codebase, identify the relevant files and patterns, and "
        "produce a detailed plan (do NOT implement — plan only)."
    ),
}

# Read-only templates that don't require worktree isolation
_READ_ONLY_TEMPLATES = frozenset({"analyze", "code_review", "investigate"})


def get_templates() -> Dict[str, str]:
    """Return a copy of the prompt template registry."""
    return dict(_TEMPLATES)


def register_template(name: str, text: str) -> None:
    """Add or replace a prompt template."""
    _TEMPLATES[name] = text


# ---------------------------------------------------------------------------
# State persistence — atomic writes via tmp + replace
# ---------------------------------------------------------------------------
def _flush_state() -> None:
    """Write current sessions dict to disk.  Caller must hold _lock."""
    _data_dir.mkdir(parents=True, exist_ok=True)
    _sessions_data_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "sessions": list(_sessions.values()),
        "config": _config,
    }
    tmp = _state_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(_state_file)


def _load_state() -> None:
    """Resume sessions from disk.  Running/queued sessions become failed."""
    if not _state_file.exists():
        return
    try:
        data = json.loads(_state_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    for sess in data.get("sessions", []):
        sid = sess.get("id")
        if not sid:
            continue
        if sess.get("status") in ("running", "queued"):
            sess["status"] = "failed"
            sess["error"] = "Server restarted — session did not complete"
            sess["ended_at"] = _now_iso()
        _sessions[sid] = sess


def load_state() -> None:
    """Public entry point: load persisted state on startup."""
    with _lock:
        _load_state()


# ---------------------------------------------------------------------------
# Usage extraction from stream-json events
# ---------------------------------------------------------------------------
def _extract_usage(session: Dict[str, Any], event: Dict[str, Any]) -> None:
    """Parse cost and token usage from a stream-json event.  Caller must hold _lock."""
    if "total_cost_usd" in event:
        session["cost_usd"] = event["total_cost_usd"]
    elif "cost_usd" in event:
        session["cost_usd"] = event["cost_usd"]

    usage = None
    if "usage" in event and isinstance(event["usage"], dict):
        usage = event["usage"]
    elif "message" in event and isinstance(event.get("message"), dict):
        msg = event["message"]
        if "usage" in msg and isinstance(msg["usage"], dict):
            usage = msg["usage"]

    if usage:
        if "input_tokens" in usage:
            session["tokens_in"] = usage["input_tokens"]
        if "output_tokens" in usage:
            session["tokens_out"] = usage["output_tokens"]

    model_usage = event.get("modelUsage")
    if isinstance(model_usage, dict):
        for _model, mu in model_usage.items():
            if isinstance(mu, dict):
                if "inputTokens" in mu:
                    session["tokens_in"] = mu["inputTokens"]
                if "outputTokens" in mu:
                    session["tokens_out"] = mu["outputTokens"]
                if "costUSD" in mu:
                    session["cost_usd"] = mu["costUSD"]


# ---------------------------------------------------------------------------
# Prompt building — default or custom
# ---------------------------------------------------------------------------
def _build_prompt(session: Dict[str, Any]) -> str:
    """Build the full prompt for a session.

    If a prompt_builder callback is registered, delegates to it.
    Otherwise: template text + user prompt.
    """
    if _prompt_builder is not None:
        return _prompt_builder(session)

    template_key = session.get("template", "implement")
    template_text = _TEMPLATES.get(template_key, _TEMPLATES["implement"])
    user_prompt = session.get("prompt", "").strip()

    parts = [template_text]
    if user_prompt:
        parts.append(f"## Instructions\n{user_prompt}")
    if session.get("task_id"):
        parts.append(f"Task: {session['task_id']} — {session.get('task_title', '')}")

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Worktree management
# ---------------------------------------------------------------------------
def _create_worktree(session: Dict[str, Any], repo_root: Path) -> Path:
    """Create a git worktree for isolated session work."""
    wt_rel = session.get("worktree_path", "")
    wt_dir = wt_rel.replace(".sessions/", "") if wt_rel else session["id"]
    branch = session["branch"]
    wt_path = _sessions_dir / wt_dir

    _sessions_dir.mkdir(parents=True, exist_ok=True)
    gi = _sessions_dir / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")

    subprocess.run(
        ["git", "worktree", "add", str(wt_path), "-b", branch],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=True,
    )
    # Initialize submodules if present
    subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=str(wt_path),
        capture_output=True,
        text=True,
    )
    return wt_path


def _reuse_worktree(wt_path: Path) -> Path:
    """Return an existing worktree path (e.g. for pipeline stage chaining)."""
    if not wt_path.exists():
        raise FileNotFoundError(f"Worktree {wt_path} does not exist")
    return wt_path


def _remove_worktree(session: Dict[str, Any], repo_root: Path) -> None:
    """Remove a session's worktree and its branch."""
    wt_rel = session.get("worktree_path", "")
    wt_dir = wt_rel.replace(".sessions/", "") if wt_rel else session["id"]
    wt_path = _sessions_dir / wt_dir
    branch = session.get("branch", "")

    if wt_path.exists():
        subprocess.run(
            ["git", "worktree", "remove", str(wt_path), "--force"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
    if branch:
        subprocess.run(
            ["git", "branch", "-D", branch],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )


# ---------------------------------------------------------------------------
# Process management
# ---------------------------------------------------------------------------
def _kill_proc(sid: str) -> None:
    """Terminate (then kill) a session's subprocess."""
    proc = _procs.get(sid)
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ---------------------------------------------------------------------------
# Session runner — executes in the thread pool
# ---------------------------------------------------------------------------
def _run_session(sid: str) -> None:
    with _lock:
        session = _sessions.get(sid)
        if not session or session["status"] == "cancelled":
            return
        session["status"] = "running"
        session["started_at"] = _now_iso()
        _flush_state()

    prompt = _build_prompt(session)
    budget = str(session.get("budget_usd", _config["default_budget_usd"]))
    model = session.get("model", _config["default_model"])
    timeout_min = session.get("timeout_min", _config["default_timeout_min"])
    repo_path = session.get("repo_path", ".")

    # Determine working directory — worktree or repo root
    working_dir = repo_path
    repo_root = Path(repo_path)
    if session.get("use_worktree"):
        is_first = session.pop("_pipeline_first_stage", True)
        wt_path = _sessions_dir / (
            session["worktree_path"].replace(".sessions/", "")
            if session.get("worktree_path")
            else session["id"]
        )
        if not is_first and wt_path.exists():
            working_dir = str(wt_path)
        else:
            try:
                wt = _create_worktree(session, repo_root)
                working_dir = str(wt)
            except subprocess.CalledProcessError as exc:
                with _lock:
                    session["status"] = "failed"
                    session["error"] = f"Worktree creation failed: {exc.stderr or exc}"
                    session["ended_at"] = _now_iso()
                    _flush_state()
                return

    # Ensure output directory
    _sessions_data_dir.mkdir(parents=True, exist_ok=True)
    output_file = _sessions_data_dir / f"{sid}.jsonl"

    # Build command — binary mode pipes (bufsize=0) for Windows compatibility
    cmd = [
        "claude", "-p",
        "--verbose",
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
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_dir,
            bufsize=0,
            env=env,
        )
    except FileNotFoundError:
        with _lock:
            session["status"] = "failed"
            session["error"] = "claude CLI not found on PATH"
            session["ended_at"] = _now_iso()
            _flush_state()
        return
    except OSError as exc:
        with _lock:
            session["status"] = "failed"
            session["error"] = f"Failed to launch claude: {exc}"
            session["ended_at"] = _now_iso()
            _flush_state()
        return

    with _lock:
        _procs[sid] = proc

    # Send prompt via stdin (binary mode — no text=True)
    try:
        proc.stdin.write(prompt.encode("utf-8"))
        proc.stdin.close()
    except OSError:
        pass

    # Watchdog timer for timeout enforcement
    def _timeout_kill():
        with _lock:
            if _sessions.get(sid, {}).get("status") == "running":
                _sessions[sid]["status"] = "timeout"
                _sessions[sid]["error"] = f"Exceeded {timeout_min} minute timeout"
                _sessions[sid]["ended_at"] = _now_iso()
                _flush_state()
        _kill_proc(sid)

    timer = threading.Timer(timeout_min * 60, _timeout_kill)
    with _lock:
        _timers[sid] = timer
    timer.start()

    # Read stdout line-by-line in binary mode to avoid Windows pipe buffering
    line_count = 0
    got_result = False
    with open(output_file, "w", encoding="utf-8") as fout:
        while True:
            raw_bytes = proc.stdout.readline()
            if not raw_bytes:
                break
            try:
                line_str = raw_bytes.decode("utf-8", errors="replace")
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

            etype = event.get("type", "")
            if etype == "result":
                got_result = True
                break

    # Cancel watchdog before proc.wait() which may hang
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

    # If stream-json emitted a result event, the session succeeded regardless of exit code
    if got_result:
        exit_code = 0

    # Collect files changed via git diff in the worktree
    files_changed: List[str] = []
    if session.get("use_worktree"):
        wt_check = _sessions_dir / (
            session["worktree_path"].replace(".sessions/", "")
            if session.get("worktree_path")
            else sid
        )
        if wt_check.exists():
            try:
                diff_result = subprocess.run(
                    ["git", "diff", "--name-only", "HEAD"],
                    cwd=str(wt_check),
                    capture_output=True,
                    text=True,
                )
                if diff_result.returncode == 0:
                    files_changed = [f for f in diff_result.stdout.strip().split("\n") if f]
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

    # Notify host application
    if _on_session_complete is not None:
        try:
            _on_session_complete(session)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Public API — session lifecycle
# ---------------------------------------------------------------------------
def create_session(
    project_slug: str,
    repo_path: str,
    prompt: str,
    template: str = "implement",
    model: str = "sonnet",
    budget_usd: float = 5.0,
    timeout_min: int = 60,
    use_worktree: bool = True,
    task_id: str = "",
    task_title: str = "",
) -> Dict[str, Any]:
    """Create a new session and enqueue it for execution.  Returns the session dict."""
    short = _short_id()
    sid = f"ses_{short}"
    safe_task = re.sub(r"[^a-zA-Z0-9_-]", "-", task_id) if task_id else short

    # Read-only templates don't need worktree isolation unless explicitly requested
    if template in _READ_ONLY_TEMPLATES and use_worktree is True:
        use_worktree = False

    session: Dict[str, Any] = {
        "id": sid,
        "project_slug": project_slug,
        "repo_path": repo_path,
        "task_id": task_id,
        "task_title": task_title,
        "prompt": prompt,
        "model": model or _config["default_model"],
        "budget_usd": float(budget_usd or _config["default_budget_usd"]),
        "timeout_min": int(timeout_min or _config["default_timeout_min"]),
        "use_worktree": use_worktree,
        "template": template,
        "status": "queued",
        "created_at": _now_iso(),
        "started_at": None,
        "ended_at": None,
        "cost_usd": 0.0,
        "tokens_in": 0,
        "tokens_out": 0,
        "worktree_path": f".sessions/{sid}" if use_worktree else None,
        "branch": f"session/{safe_task}-{short}" if use_worktree else None,
        "output_lines": 0,
        "files_changed": [],
        "quality_gates": {
            "compiles": None,
            "tests_pass": None,
            "requirements_met": None,
            "no_security_issues": None,
        },
        "learnings": "",
        "error": None,
    }

    with _lock:
        _sessions[sid] = session
        _flush_state()

    _pool.submit(_run_session, sid)
    return session


def get_session(sid: str) -> Optional[Dict[str, Any]]:
    """Return a session dict by ID, or None."""
    with _lock:
        s = _sessions.get(sid)
        return dict(s) if s else None


def list_sessions(
    project_slug: Optional[str] = None,
    status: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return all sessions, optionally filtered by project and/or status."""
    with _lock:
        result = list(_sessions.values())
    if project_slug:
        result = [s for s in result if s.get("project_slug") == project_slug]
    if status:
        result = [s for s in result if s.get("status") == status]
    return result


def cancel_session(sid: str) -> bool:
    """Cancel a running or queued session.  Returns True if cancelled."""
    with _lock:
        session = _sessions.get(sid)
        if not session:
            return False
        if session["status"] not in ("running", "queued"):
            return False
        session["status"] = "cancelled"
        session["ended_at"] = _now_iso()
        _flush_state()

    _kill_proc(sid)
    timer = _timers.pop(sid, None)
    if timer:
        timer.cancel()
    return True


def delete_session(sid: str) -> bool:
    """Delete a session: cancel if running, remove worktree, purge output.  Returns True if found."""
    with _lock:
        session = _sessions.get(sid)
        if not session:
            return False
        if session["status"] in ("running", "queued"):
            session["status"] = "cancelled"
            session["ended_at"] = _now_iso()

    _kill_proc(sid)
    timer = _timers.pop(sid, None)
    if timer:
        timer.cancel()

    # Clean up worktree
    if session.get("use_worktree") and session.get("repo_path"):
        _remove_worktree(session, Path(session["repo_path"]))

    # Delete JSONL output file
    output_file = _sessions_data_dir / f"{sid}.jsonl"
    if output_file.exists():
        try:
            output_file.unlink()
        except OSError:
            pass

    with _lock:
        _sessions.pop(sid, None)
        _procs.pop(sid, None)
        _flush_state()

    return True


def update_session(sid: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Patch mutable fields on a session (quality_gates, learnings, status)."""
    with _lock:
        session = _sessions.get(sid)
        if not session:
            return None

        if "quality_gates" in updates and isinstance(updates["quality_gates"], dict):
            session["quality_gates"].update(updates["quality_gates"])
        if "learnings" in updates:
            session["learnings"] = str(updates["learnings"])
        if "status" in updates:
            allowed = {"reviewing", "merged", "rejected"}
            if updates["status"] in allowed:
                session["status"] = updates["status"]

        _flush_state()
        return dict(session)


def get_session_output(sid: str, max_lines: int = 100) -> Optional[Dict[str, Any]]:
    """Read the JSONL output for a session.  Returns {lines, total}."""
    with _lock:
        if sid not in _sessions:
            return None

    output_file = _sessions_data_dir / f"{sid}.jsonl"
    if not output_file.exists():
        return {"lines": [], "total": 0}

    try:
        all_lines = output_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return {"lines": [], "total": 0}

    total = len(all_lines)
    lines = all_lines[-max_lines:] if max_lines < total else all_lines
    return {"lines": lines, "total": total}


# ---------------------------------------------------------------------------
# Shutdown helper — call from atexit or signal handler in the host server
# ---------------------------------------------------------------------------
def shutdown() -> None:
    """Kill all running sessions and flush state.  Does NOT remove worktrees."""
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
        _flush_state()
    _pool.shutdown(wait=False)


def shutdown_and_cleanup() -> None:
    """Kill all sessions AND remove worktrees for sessions cancelled by shutdown."""
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
            if (
                session.get("use_worktree")
                and session.get("error") == "Server shutdown"
                and session.get("repo_path")
            ):
                _remove_worktree(session, Path(session["repo_path"]))
        _flush_state()
    _pool.shutdown(wait=False)


# ---------------------------------------------------------------------------
# Accessors for internal state (useful for host server status endpoints)
# ---------------------------------------------------------------------------
def get_config() -> Dict[str, Any]:
    """Return the current config dict."""
    return dict(_config)


def get_all_sessions_snapshot() -> Dict[str, Any]:
    """Return {sessions: [...], config: {...}} for serialization."""
    with _lock:
        return {
            "sessions": list(_sessions.values()),
            "config": _config,
        }
