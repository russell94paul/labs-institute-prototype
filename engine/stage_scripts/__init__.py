"""Stage script interface for pipeline automation."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class ScriptContext:
    pipeline_id: str
    stage_name: str
    task_id: str
    project_slug: str
    environment: str
    params: Dict[str, str]
    prior_results: Dict[str, Dict[str, Any]]
    worktree_path: Optional[Path]
    script_args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScriptResult:
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    summary: str = ""
