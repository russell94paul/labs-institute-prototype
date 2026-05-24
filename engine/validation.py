"""Validation engine — auto-checks session output against acceptance criteria."""
from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine import events

_data_dir: Optional[Path] = None


def configure(data_dir: Path) -> None:
    global _data_dir
    _data_dir = data_dir
    validations_dir = data_dir / "validations"
    validations_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class ValidationCheck:
    name: str
    check_type: str  # "command", "file_exists", "grep"
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    check_name: str
    passed: bool
    output: str
    duration_ms: int
    timestamp: str = ""


@dataclass
class ValidationReport:
    session_id: str
    pipeline_id: Optional[str]
    results: List[ValidationResult]
    all_passed: bool
    created_at: str = ""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run_command(cmd: str, cwd: str, timeout: int = 120) -> tuple[int, str]:
    try:
        r = subprocess.run(
            cmd, shell=True, cwd=cwd,
            capture_output=True, text=True, timeout=timeout,
        )
        output = (r.stdout + r.stderr).strip()
        return r.returncode, output[:2000]
    except subprocess.TimeoutExpired:
        return 1, f"Command timed out after {timeout}s"
    except OSError as exc:
        return 1, str(exc)


def _resolve_working_dir(session: Dict[str, Any]) -> tuple[Path, Optional[str]]:
    """Return (working_dir, error_message). error_message is None on success."""
    wt_path = session.get("worktree_path", "")
    repo_path = session.get("repo_path", ".")

    if wt_path:
        sessions_dir = Path(repo_path).parent / ".conductor-sessions"
        # Strip the ".sessions/" prefix safely without replacing all occurrences
        wt_rel = wt_path
        for prefix in (".sessions/", ".conductor-sessions/"):
            if prefix in wt_rel:
                wt_rel = wt_rel.split(prefix, 1)[-1]
                break
        working_dir = sessions_dir / wt_rel
    else:
        working_dir = Path(repo_path)

    if not working_dir.exists():
        return working_dir, f"Working directory not found: {working_dir}"

    return working_dir, None


def run_validation(
    session: Dict[str, Any],
    checks: List[ValidationCheck],
) -> ValidationReport:
    """Run all checks against a session's worktree."""
    if not checks:
        return ValidationReport(
            session_id=session.get("id", ""),
            pipeline_id=None,
            results=[],
            all_passed=True,
            created_at=_now_iso(),
        )

    working_dir, err = _resolve_working_dir(session)
    if err:
        report = ValidationReport(
            session_id=session.get("id", ""),
            pipeline_id=None,
            results=[ValidationResult(
                check_name="setup",
                passed=False,
                output=err,
                duration_ms=0,
                timestamp=_now_iso(),
            )],
            all_passed=False,
            created_at=_now_iso(),
        )
        _store_report(report)
        return report

    results = []
    for check in checks:
        start = time.monotonic()
        if check.check_type == "command":
            code, output = _run_command(
                check.config.get("command", "echo no command"),
                str(working_dir),
                check.config.get("timeout", 120),
            )
            passed = code == 0
        elif check.check_type == "file_exists":
            paths = check.config.get("paths", [])
            missing = [p for p in paths if not (working_dir / p).exists()]
            passed = len(missing) == 0
            output = f"Missing: {', '.join(missing)}" if missing else "All files present"
        elif check.check_type == "grep":
            pattern = check.config.get("pattern", "")
            target = check.config.get("file", ".")
            code, output = _run_command(
                f'grep -rl "{pattern}" {target}',
                str(working_dir), 30,
            )
            passed = code == 0
        else:
            passed = False
            output = f"Unknown check type: {check.check_type}"

        elapsed = int((time.monotonic() - start) * 1000)
        results.append(ValidationResult(
            check_name=check.name,
            passed=passed,
            output=output,
            duration_ms=elapsed,
            timestamp=_now_iso(),
        ))

    report = ValidationReport(
        session_id=session.get("id", ""),
        pipeline_id=session.get("task_id", "").split("/")[0] if "/" in session.get("task_id", "") else None,
        results=results,
        all_passed=all(r.passed for r in results),
        created_at=_now_iso(),
    )

    _store_report(report)
    return report


def default_checks(session: Dict[str, Any]) -> List[ValidationCheck]:
    """Auto-detect project type and return appropriate checks."""
    working_dir, err = _resolve_working_dir(session)

    checks = []

    if err:
        return checks

    if (working_dir / "pyproject.toml").exists() or (working_dir / "setup.py").exists():
        checks.append(ValidationCheck(
            name="tests_pass",
            check_type="command",
            config={"command": "python -m pytest --tb=short -q", "timeout": 120},
        ))

    if (working_dir / "package.json").exists():
        checks.append(ValidationCheck(
            name="tests_pass",
            check_type="command",
            config={"command": "npm test", "timeout": 120},
        ))

    if session.get("files_changed"):
        checks.append(ValidationCheck(
            name="files_exist",
            check_type="file_exists",
            config={"paths": session["files_changed"][:20]},
        ))

    return checks


def apply_to_quality_gates(session: Dict[str, Any], report: ValidationReport) -> None:
    """Map validation results to the session's quality_gates dict."""
    gates = session.get("quality_gates", {})
    for result in report.results:
        if result.check_name == "tests_pass":
            gates["tests_pass"] = result.passed
        elif result.check_name == "compiles":
            gates["compiles"] = result.passed
        elif result.check_name == "files_exist":
            gates["requirements_met"] = result.passed
    session["quality_gates"] = gates


def store_evidence(project_slug: str, session_id: str, report: ValidationReport) -> None:
    """Store validation results as evidence via the memory system."""
    try:
        from engine import memory
        memory.add_evidence(
            project_slug=project_slug,
            memory_id=f"validation-{session_id}",
            evidence_type="validation_record",
            reference=f"session:{session_id}",
            description=f"Validation: {'PASSED' if report.all_passed else 'FAILED'} "
                        f"({sum(1 for r in report.results if r.passed)}/{len(report.results)} checks)",
        )
    except Exception:
        pass


def _store_report(report: ValidationReport) -> None:
    if not _data_dir:
        return
    try:
        validations_dir = _data_dir / "validations"
        validations_dir.mkdir(parents=True, exist_ok=True)
        path = validations_dir / f"{report.session_id}.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        tmp.replace(path)
    except OSError:
        pass


def get_report(session_id: str) -> Optional[Dict[str, Any]]:
    if not _data_dir:
        return None
    path = _data_dir / "validations" / f"{session_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
