"""Conductor — AI conversational onboarding via Claude API or CLI."""
from __future__ import annotations

import json
import os
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "dashboard" / "data"
SESSIONS_FILE = DATA_DIR / "onboarding-sessions.json"

_env_file = REPO_ROOT / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

SYSTEM_PROMPT = """You are a senior technical architect helping plan software projects through natural conversation.

## Approach
1. Understand the problem first — ask what they're building, who it's for, what problem it solves.
2. Ask focused questions, one or two at a time. Never dump a wall of questions.
3. Surface implicit requirements (e.g. "marketplace" implies payments, trust/safety, two-sided UX).
4. Challenge assumptions constructively. Push back on over-engineering.
5. Think in phases. Every project should ship incrementally.

## Flow
- First 2-3 exchanges: understand problem, users, goals
- Next 2-3: explore technical constraints, existing systems, scale
- Then: propose architecture and phase plan
- Finally: refine based on feedback, produce final blueprint

## Structured Output
Include JSON blocks (```json) with a `type` field for the UI to render specially.

**`phase_proposal`** — propose phases:
```json
{"type":"phase_proposal","phases":[{"id":"P0","name":"Foundation","description":"Core infra and auth","complexity":"M","risk":"low","dependencies":[],"deliverables":["Auth flow","API structure"]}]}
```

**`architecture`** — propose tech stack:
```json
{"type":"architecture","title":"Proposed Architecture","stack":{"frontend":"React","backend":"FastAPI","database":"PostgreSQL","hosting":"AWS"},"components":[{"name":"API Gateway","purpose":"Route requests"}],"rationale":"Why this fits"}
```

**`blueprint`** — final project definition (only after user approves plan):
```json
{"type":"blueprint","name":"Project Name","slug":"project-name","description":"Description","stack":{"frontend":"...","backend":"...","database":"...","hosting":"..."},"phases":[{"id":"P0","name":"Phase Name","description":"Delivers X","status":"planned","complexity":"M","risk":"low","dependencies":[],"deliverables":["..."],"acceptance_criteria":["..."]}],"decisions":[{"topic":"Database","choice":"PostgreSQL","reason":"..."}]}
```

## Rules
- Be conversational. You're a consultant, not a form.
- Explain reasoning around JSON blocks. Don't output blueprint until user approves phases.
- Phase IDs: P0, P1, P2... Complexity: S(<1wk), M(1-2wk), L(2-4wk), XL(4+wk). Risk: low/medium/high.
- 4-15 phases. Always include P0 Foundation. Slug: lowercase-hyphenated.
- Allow iteration on phases. When asked to finalize, output the blueprint block."""

CHAT_MODEL = os.environ.get("ONBOARDING_MODEL", "claude-sonnet-4-6-20250514")

_sessions: Dict[str, Dict[str, Any]] = {}


def _has_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY", ""))


def _load_sessions() -> None:
    global _sessions
    if SESSIONS_FILE.exists():
        try:
            _sessions = json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            _sessions = {}


def _save_sessions() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = SESSIONS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(_sessions, indent=2), encoding="utf-8")
    tmp.replace(SESSIONS_FILE)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_structured_blocks(text: str) -> List[Dict[str, Any]]:
    blocks = []
    for m in re.finditer(r"```json\s*\n(.*?)\n```", text, re.DOTALL):
        try:
            parsed = json.loads(m.group(1))
            if isinstance(parsed, dict) and "type" in parsed:
                blocks.append(parsed)
        except (json.JSONDecodeError, ValueError):
            pass
    return blocks


def create_session() -> Dict[str, Any]:
    _load_sessions()
    sid = f"onb_{uuid.uuid4().hex[:12]}"
    session = {
        "id": sid,
        "created": _now_iso(),
        "updated": _now_iso(),
        "messages": [],
        "blueprint": None,
        "status": "active",
    }
    _sessions[sid] = session
    _save_sessions()
    return session


def get_session(sid: str) -> Optional[Dict[str, Any]]:
    _load_sessions()
    return _sessions.get(sid)


def _call_api(system: str, messages: List[Dict]) -> str:
    """Call Claude via the Anthropic Python SDK."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=CHAT_MODEL,
        max_tokens=4096,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def _call_cli(system: str, messages: List[Dict]) -> str:
    """Call Claude via the claude CLI subprocess."""
    prompt_parts = [system, "\n---\n\nConversation so far:\n"]
    for msg in messages:
        role = msg["role"].upper()
        prompt_parts.append(f"\n{role}: {msg['content']}")
    prompt_parts.append("\n\nASSISTANT:")
    full_prompt = "\n".join(prompt_parts)

    proc = subprocess.run(
        ["claude", "-p", "--model", "sonnet", "--max-turns", "10"],
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(REPO_ROOT),
        env={**os.environ, "NO_COLOR": "1"},
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(proc.stderr or f"claude exited with code {proc.returncode}")
    return proc.stdout.strip()


def chat(sid: str, user_message: str) -> Dict[str, Any]:
    _load_sessions()
    session = _sessions.get(sid)
    if not session:
        return {"error": "Session not found"}

    session["messages"].append({
        "role": "user",
        "content": user_message,
        "timestamp": _now_iso(),
    })

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in session["messages"]
    ]

    blueprint_context = ""
    if session.get("blueprint"):
        blueprint_context = (
            "\n\nCurrent blueprint state:\n```json\n"
            + json.dumps(session["blueprint"], indent=2)
            + "\n```"
        )

    system = SYSTEM_PROMPT + blueprint_context

    try:
        if _has_api_key():
            assistant_text = _call_api(system, api_messages)
        else:
            assistant_text = _call_cli(system, api_messages)
    except Exception as e:
        session["messages"].pop()
        _save_sessions()
        return {"error": f"Claude error: {e}"}

    structured_blocks = _extract_structured_blocks(assistant_text)

    for block in structured_blocks:
        if block.get("type") == "blueprint":
            session["blueprint"] = block
        elif block.get("type") == "phase_proposal":
            if not session.get("blueprint"):
                session["blueprint"] = {}
            session["blueprint"]["phases"] = block.get("phases", [])
        elif block.get("type") == "architecture":
            if not session.get("blueprint"):
                session["blueprint"] = {}
            session["blueprint"]["stack"] = block.get("stack", {})
            session["blueprint"]["components"] = block.get("components", [])

    session["messages"].append({
        "role": "assistant",
        "content": assistant_text,
        "timestamp": _now_iso(),
        "structured": structured_blocks,
    })
    session["updated"] = _now_iso()
    _save_sessions()

    return {
        "message": assistant_text,
        "structured": structured_blocks,
        "blueprint": session.get("blueprint"),
    }


def create_project_from_blueprint(sid: str) -> Dict[str, Any]:
    _load_sessions()
    session = _sessions.get(sid)
    if not session:
        return {"error": "Session not found"}

    bp = session.get("blueprint")
    if not bp:
        return {"error": "No blueprint finalized yet"}

    slug = bp.get("slug", "")
    name = bp.get("name", "")
    if not slug or not name:
        return {"error": "Blueprint missing name or slug"}

    project_dir = REPO_ROOT / "projects" / slug
    if (project_dir / "project.json").exists():
        return {"error": f"Project {slug} already exists"}

    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "wiki").mkdir(exist_ok=True)
    (project_dir / "phases").mkdir(exist_ok=True)
    (project_dir / "memory").mkdir(exist_ok=True)

    phases = []
    for ph in bp.get("phases", []):
        phases.append({
            "id": ph.get("id", ""),
            "name": ph.get("name", ""),
            "description": ph.get("description", ""),
            "status": ph.get("status", "planned"),
            "complexity": ph.get("complexity", "M"),
            "risk": ph.get("risk", "low"),
            "dependencies": ph.get("dependencies", []),
            "deliverables": ph.get("deliverables", []),
            "acceptance_criteria": ph.get("acceptance_criteria", []),
        })

    project = {
        "name": name,
        "slug": slug,
        "description": bp.get("description", ""),
        "status": "active",
        "created": _now_iso()[:10],
        "platform": "web-responsive",
        "stack": bp.get("stack", {}),
        "phases": phases,
        "onboarding": {
            "method": "chat",
            "session_id": sid,
            "decisions": bp.get("decisions", []),
        },
    }

    pj = project_dir / "project.json"
    tmp = pj.with_suffix(".tmp")
    tmp.write_text(json.dumps(project, indent=2), encoding="utf-8")
    tmp.replace(pj)

    _write_phase_status(slug, phases)
    _seed_memory(project_dir, name, bp)
    _copy_wiki_template(project_dir)

    session["status"] = "completed"
    _save_sessions()

    return {"project": project, "slug": slug}


def _compute_parallel_flags(phases: List[Dict]) -> Dict[str, bool]:
    """Phases can run in parallel if they share no dependency relationship with each other."""
    ids = {ph.get("id", "") for ph in phases}
    deps_of = {ph.get("id", ""): set(ph.get("dependencies", [])) for ph in phases}
    all_ancestors: Dict[str, set] = {}
    def ancestors(pid: str) -> set:
        if pid in all_ancestors:
            return all_ancestors[pid]
        result = set(deps_of.get(pid, []))
        for dep in list(result):
            result |= ancestors(dep)
        all_ancestors[pid] = result
        return result
    for pid in ids:
        ancestors(pid)
    parallel = {}
    for ph in phases:
        pid = ph.get("id", "")
        has_sibling = False
        for other in phases:
            oid = other.get("id", "")
            if oid == pid:
                continue
            if deps_of[pid] == deps_of[oid] and pid not in all_ancestors.get(oid, set()) and oid not in all_ancestors.get(pid, set()):
                has_sibling = True
                break
        parallel[pid] = has_sibling
    return parallel


def _write_phase_status(slug: str, phases: List[Dict]) -> None:
    status_file = REPO_ROOT / "config" / "phase-status.json"
    existing = []
    if status_file.exists():
        try:
            existing = json.loads(status_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            pass
    prefix = slug[:2]
    parallel_flags = _compute_parallel_flags(phases)
    for ph in phases:
        pid = ph.get("id", "")
        phase_id = f"{prefix}-{pid}" if not pid.startswith(prefix) else pid
        existing.append({
            "phaseId": phase_id, "name": ph.get("name", ""), "project": slug,
            "status": "planned", "dependencies": ph.get("dependencies", []),
            "blockedBy": [], "blocks": [],
            "estimatedComplexity": ph.get("complexity", "M"),
            "riskLevel": ph.get("risk", "low"), "approvalRequired": False,
            "canRunInParallel": parallel_flags.get(pid, False),
            "description": ph.get("description", ""),
            "lastUpdated": _now_iso()[:10],
        })
    tmp = status_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    tmp.replace(status_file)


def _seed_memory(project_dir: Path, name: str, blueprint: Dict) -> None:
    mem_dir = project_dir / "memory"
    mem_dir.mkdir(exist_ok=True)
    now = _now_iso()
    memories = [{"id": f"mem_{uuid.uuid4().hex[:8]}", "type": "decision",
                 "content": f"Project {name} created via AI chat onboarding",
                 "source": "onboarding", "tags": ["onboarding", "project-creation"],
                 "status": "active", "created": now}]
    for d in blueprint.get("decisions", []):
        memories.append({"id": f"mem_{uuid.uuid4().hex[:8]}", "type": "decision",
                         "content": f"{d.get('topic','')}: {d.get('choice','')} — {d.get('reason','')}",
                         "source": "onboarding", "tags": ["onboarding", "architecture"],
                         "status": "active", "created": now})
    _atomic_write(mem_dir / "memories.json", json.dumps(memories, indent=2))
    ef = mem_dir / "evidence.json"
    if not ef.exists():
        _atomic_write(ef, "[]")


def _copy_wiki_template(project_dir: Path) -> None:
    wiki_dir = project_dir / "wiki"
    wiki_dir.mkdir(exist_ok=True)
    index = wiki_dir / "index.md"
    if not index.exists():
        index.write_text("# Wiki\n\nProject wiki — decisions, patterns, learnings.\n", encoding="utf-8")


def _atomic_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
