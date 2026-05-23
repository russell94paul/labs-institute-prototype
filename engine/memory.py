"""Per-project memory store — zeus-memory patterns on a JSON-file backend.

Each project gets its own memory ledger at projects/<slug>/memory/.
Structured to upgrade to postgres/zeus-memory via provider interface later.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"

VALID_MEMORY_TYPES = {"decision", "learning", "pattern", "incident", "context", "fact", "anti-pattern"}


def _memory_dir(project_slug: str) -> Path:
    return PROJECTS_DIR / project_slug / "memory"


def _ledger_path(project_slug: str) -> Path:
    return _memory_dir(project_slug) / "memories.json"


def _evidence_path(project_slug: str) -> Path:
    return _memory_dir(project_slug) / "evidence.json"


def _retrieval_log_path(project_slug: str) -> Path:
    return _memory_dir(project_slug) / "retrieval_log.json"


def _atomic_write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    tmp.replace(path)


def _read_json(path: Path) -> list:
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, ValueError):
        return []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _keyword_score(query_tokens: List[str], content_tokens: set) -> float:
    if not query_tokens:
        return 0.0
    hits = sum(1 for t in query_tokens if t in content_tokens)
    return hits / len(query_tokens)


# --- Public API ---


def store(
    project_slug: str,
    content: str,
    source: str = "",
    memory_type: str = "fact",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    session_id: str = "",
) -> Dict[str, Any]:
    """Store a memory entry. Returns the created record."""
    if memory_type not in VALID_MEMORY_TYPES:
        memory_type = "fact"

    entry = {
        "id": f"mem_{uuid.uuid4().hex[:12]}",
        "project": project_slug,
        "content": content,
        "source": source,
        "type": memory_type,
        "tags": tags or [],
        "metadata": metadata or {},
        "session_id": session_id,
        "status": "active",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "retrieval_count": 0,
    }

    ledger = _read_json(_ledger_path(project_slug))
    ledger.append(entry)
    _atomic_write(_ledger_path(project_slug), ledger)
    return entry


def search(
    project_slug: str,
    query: str,
    limit: int = 10,
    memory_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    status: str = "active",
) -> List[Dict[str, Any]]:
    """Keyword search over project memories. Returns ranked results."""
    ledger = _read_json(_ledger_path(project_slug))
    query_tokens = _tokenize(query)

    scored = []
    for entry in ledger:
        if entry.get("status") != status:
            continue
        if memory_type and entry.get("type") != memory_type:
            continue
        if tags:
            entry_tags = set(entry.get("tags", []))
            if not entry_tags.intersection(tags):
                continue

        content_tokens = set(_tokenize(entry.get("content", "")))
        tag_tokens = set(_tokenize(" ".join(entry.get("tags", []))))
        source_tokens = set(_tokenize(entry.get("source", "")))
        all_tokens = content_tokens | tag_tokens | source_tokens

        score = _keyword_score(query_tokens, all_tokens)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: (-x[0], x[1].get("created_at", "")))

    results = []
    for score, entry in scored[:limit]:
        results.append({**entry, "relevance_score": round(score, 3)})
        _log_retrieval(project_slug, entry["id"], query)

    return results


def recall(project_slug: str, memory_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single memory by ID."""
    ledger = _read_json(_ledger_path(project_slug))
    for entry in ledger:
        if entry["id"] == memory_id:
            _log_retrieval(project_slug, memory_id, f"recall:{memory_id}")
            return entry
    return None


def list_memories(
    project_slug: str,
    memory_type: Optional[str] = None,
    status: str = "active",
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """List memories with pagination and filtering."""
    ledger = _read_json(_ledger_path(project_slug))
    filtered = [
        e for e in ledger
        if e.get("status") == status
        and (memory_type is None or e.get("type") == memory_type)
    ]
    filtered.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {
        "memories": filtered[offset:offset + limit],
        "total": len(filtered),
        "offset": offset,
        "limit": limit,
    }


def update_memory(
    project_slug: str,
    memory_id: str,
    updates: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Update a memory entry. Returns updated record or None."""
    ledger = _read_json(_ledger_path(project_slug))
    allowed_fields = {"content", "source", "type", "tags", "metadata", "status"}

    for entry in ledger:
        if entry["id"] == memory_id:
            for k, v in updates.items():
                if k in allowed_fields:
                    entry[k] = v
            entry["updated_at"] = _now_iso()
            _atomic_write(_ledger_path(project_slug), ledger)
            return entry
    return None


def add_evidence(
    project_slug: str,
    memory_id: str,
    evidence_type: str,
    reference: str,
    description: str = "",
) -> Dict[str, Any]:
    """Link evidence to a memory (PR, test result, session output, etc.)."""
    record = {
        "id": f"evi_{uuid.uuid4().hex[:12]}",
        "memory_id": memory_id,
        "type": evidence_type,
        "reference": reference,
        "description": description,
        "created_at": _now_iso(),
    }

    evidence = _read_json(_evidence_path(project_slug))
    evidence.append(record)
    _atomic_write(_evidence_path(project_slug), evidence)
    return record


def get_evidence(project_slug: str, memory_id: str) -> List[Dict[str, Any]]:
    """Get all evidence linked to a memory."""
    evidence = _read_json(_evidence_path(project_slug))
    return [e for e in evidence if e.get("memory_id") == memory_id]


def get_stats(project_slug: str) -> Dict[str, Any]:
    """Memory store statistics for a project."""
    ledger = _read_json(_ledger_path(project_slug))
    active = [e for e in ledger if e.get("status") == "active"]
    by_type: Dict[str, int] = {}
    for e in active:
        t = e.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    retrieval_log = _read_json(_retrieval_log_path(project_slug))
    evidence = _read_json(_evidence_path(project_slug))

    return {
        "project": project_slug,
        "total_memories": len(ledger),
        "active_memories": len(active),
        "by_type": by_type,
        "total_evidence": len(evidence),
        "total_retrievals": len(retrieval_log),
    }


def _log_retrieval(project_slug: str, memory_id: str, query: str) -> None:
    log = _read_json(_retrieval_log_path(project_slug))
    log.append({
        "memory_id": memory_id,
        "query": query,
        "timestamp": _now_iso(),
    })
    if len(log) > 10000:
        log = log[-5000:]
    _atomic_write(_retrieval_log_path(project_slug), log)

    ledger = _read_json(_ledger_path(project_slug))
    for entry in ledger:
        if entry["id"] == memory_id:
            entry["retrieval_count"] = entry.get("retrieval_count", 0) + 1
            break
    _atomic_write(_ledger_path(project_slug), ledger)
