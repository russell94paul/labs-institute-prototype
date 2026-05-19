"""Event system — in-memory event log with SSE pub/sub.

Thread-safe event emission, ring-buffer history, and subscriber management
for server-sent events.  No external dependencies.
"""
from __future__ import annotations

import json
import threading
import uuid
from collections import deque
from datetime import datetime, timezone
from queue import Queue, Empty, Full
from typing import Any, Deque, Dict, List, Optional, Set


_lock = threading.Lock()
_events: Deque[Dict[str, Any]] = deque(maxlen=500)
_subscribers: Set[Queue] = set()
_shutdown_flag = threading.Event()


def configure(max_events: int = 500) -> None:
    global _events
    with _lock:
        _events = deque(_events, maxlen=max_events)


def emit(event_type: str, data: Optional[Dict[str, Any]] = None, source: str = "") -> Dict[str, Any]:
    """Emit an event to all subscribers and append to history."""
    event: Dict[str, Any] = {
        "id": uuid.uuid4().hex[:12],
        "type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "source": source,
        "data": data or {},
    }

    with _lock:
        _events.append(event)
        dead: List[Queue] = []
        for q in _subscribers:
            try:
                q.put_nowait(event)
            except Full:
                dead.append(q)
        for q in dead:
            _subscribers.discard(q)

    return event


def subscribe() -> Queue:
    """Create a subscriber queue for SSE streaming."""
    q: Queue = Queue(maxsize=200)
    with _lock:
        _subscribers.add(q)
    return q


def unsubscribe(q: Queue) -> None:
    with _lock:
        _subscribers.discard(q)


def get_history(
    limit: int = 50,
    event_type: Optional[str] = None,
    since: Optional[str] = None,
) -> List[Dict[str, Any]]:
    with _lock:
        result = list(_events)

    if event_type:
        result = [
            e for e in result
            if e["type"] == event_type or e["type"].startswith(event_type + ".")
        ]

    if since:
        result = [e for e in result if e["timestamp"] > since]

    return result[-limit:]


def get_stats() -> Dict[str, Any]:
    with _lock:
        total = len(_events)
        max_size = _events.maxlen
        sub_count = len(_subscribers)
        snapshot = list(_events)

    type_counts: Dict[str, int] = {}
    for e in snapshot:
        t = e.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    return {
        "totalEvents": total,
        "maxEvents": max_size,
        "subscribers": sub_count,
        "typeCounts": type_counts,
    }


def is_shutdown() -> bool:
    return _shutdown_flag.is_set()


def shutdown() -> None:
    """Signal all SSE subscribers to disconnect."""
    _shutdown_flag.set()
    with _lock:
        sentinel: Dict[str, Any] = {"type": "__shutdown__", "id": "", "timestamp": "", "source": "", "data": {}}
        for q in _subscribers:
            try:
                q.put_nowait(sentinel)
            except Full:
                pass
        _subscribers.clear()
