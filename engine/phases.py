"""Phase definition loader — reads markdown phase specs with YAML frontmatter.

Converts structured phase definitions into pipeline stage configurations that
the DAG engine can consume.  Supports variable interpolation for pipeline
templates.
"""
from __future__ import annotations

import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_phase_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Extract YAML frontmatter and body from a markdown file.

    Returns (frontmatter_dict, body_text).
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fm = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, match.group(2)


def load_phase_spec(path: Path) -> Optional[Dict[str, Any]]:
    """Load a phase spec from a markdown file with frontmatter.

    Expected frontmatter keys:
        phase_number, phase_name, goal, deliverables, constraints,
        acceptance_criteria, estimated_complexity, risk_level

    Returns a dict with frontmatter + body, or None if file doesn't exist.
    """
    if not path.exists():
        return None
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    fm, body = parse_phase_frontmatter(content)
    return {
        "phase_number": fm.get("phase_number", ""),
        "phase_name": fm.get("phase_name", path.stem),
        "goal": fm.get("goal", ""),
        "deliverables": fm.get("deliverables", []),
        "constraints": fm.get("constraints", []),
        "acceptance_criteria": fm.get("acceptance_criteria", []),
        "estimated_complexity": fm.get("estimated_complexity", "M"),
        "risk_level": fm.get("risk_level", "medium"),
        "body": body.strip(),
        "source_path": str(path),
    }


def phase_to_variables(phase_spec: Dict[str, Any]) -> Dict[str, str]:
    """Convert a phase spec dict into template variables for pipeline creation.

    These variables are substituted into pipeline template prompt_template fields.
    """
    deliverables = phase_spec.get("deliverables", [])
    if isinstance(deliverables, list):
        deliverables_str = "\n".join(f"- {d}" for d in deliverables)
    else:
        deliverables_str = str(deliverables)

    constraints = phase_spec.get("constraints", [])
    if isinstance(constraints, list):
        constraints_str = "\n".join(f"- {c}" for c in constraints)
    else:
        constraints_str = str(constraints)

    acceptance = phase_spec.get("acceptance_criteria", [])
    if isinstance(acceptance, list):
        acceptance_str = "\n".join(f"- {a}" for a in acceptance)
    else:
        acceptance_str = str(acceptance)

    phase_readme = phase_spec.get("body", "")
    if not phase_readme:
        parts = []
        if phase_spec.get("goal"):
            parts.append(f"## Goal\n{phase_spec['goal']}")
        if deliverables_str:
            parts.append(f"## Deliverables\n{deliverables_str}")
        if constraints_str:
            parts.append(f"## Constraints\n{constraints_str}")
        if acceptance_str:
            parts.append(f"## Acceptance Criteria\n{acceptance_str}")
        phase_readme = "\n\n".join(parts)

    return {
        "phase_number": str(phase_spec.get("phase_number", "")),
        "phase_name": str(phase_spec.get("phase_name", "")),
        "phase_readme": phase_readme,
        "phase_goal": str(phase_spec.get("goal", "")),
        "phase_deliverables": deliverables_str,
        "phase_constraints": constraints_str,
        "phase_acceptance": acceptance_str,
    }


def scan_phase_specs(directory: Path) -> List[Dict[str, Any]]:
    """Scan a directory for markdown files with phase frontmatter.

    Returns a list of phase spec dicts, sorted by phase_number.
    """
    if not directory.exists():
        return []

    specs = []
    for f in sorted(directory.glob("*.md")):
        spec = load_phase_spec(f)
        if spec and (spec.get("phase_number") or spec.get("phase_name")):
            specs.append(spec)

    specs.sort(key=lambda s: str(s.get("phase_number", "zz")))
    return specs
