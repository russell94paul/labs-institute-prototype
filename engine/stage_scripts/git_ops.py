"""Git automation for pipeline stages."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Optional

from . import ScriptContext, ScriptResult


def commit_changes(ctx: ScriptContext) -> ScriptResult:
    """Stage and commit all changes in the worktree."""
    if not ctx.worktree_path or not ctx.worktree_path.exists():
        return ScriptResult(success=False, error="No worktree path")

    message = ctx.script_args.get("message", f"conductor: {ctx.stage_name} for {ctx.task_id}")
    cwd = str(ctx.worktree_path)

    r = subprocess.run(["git", "add", "-A"], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        return ScriptResult(success=False, error=f"git add failed: {r.stderr}")

    r = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=cwd, capture_output=True, text=True,
    )
    if r.returncode == 0:
        return ScriptResult(success=True, summary="No changes to commit", data={"files": []})

    r = subprocess.run(
        ["git", "commit", "-m", message], cwd=cwd, capture_output=True, text=True,
    )
    if r.returncode != 0:
        return ScriptResult(success=False, error=f"git commit failed: {r.stderr}")

    return ScriptResult(success=True, summary=f"Committed: {message}", data={"message": message})


def get_changed_files(worktree_path: Path, base_ref: str = "HEAD") -> List[str]:
    """Return list of changed file paths relative to base_ref."""
    try:
        r = subprocess.run(
            ["git", "diff", "--name-only", base_ref],
            cwd=str(worktree_path), capture_output=True, text=True,
        )
        if r.returncode == 0:
            return [f for f in r.stdout.strip().split("\n") if f]
    except OSError:
        pass
    return []


def create_pr(ctx: ScriptContext) -> ScriptResult:
    """Create a GitHub PR from the pipeline branch."""
    if not ctx.worktree_path or not ctx.worktree_path.exists():
        return ScriptResult(success=False, error="No worktree path")

    cwd = str(ctx.worktree_path)
    title = ctx.script_args.get("title", f"[{ctx.task_id}] {ctx.stage_name}")
    body = ctx.script_args.get("body", f"Automated PR from conductor pipeline {ctx.pipeline_id}")

    r = subprocess.run(["git", "push", "-u", "origin", "HEAD"], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        return ScriptResult(success=False, error=f"git push failed: {r.stderr}")

    r = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body],
        cwd=cwd, capture_output=True, text=True,
    )
    if r.returncode != 0:
        return ScriptResult(success=False, error=f"gh pr create failed: {r.stderr}")

    pr_url = r.stdout.strip()
    return ScriptResult(success=True, summary=f"PR created: {pr_url}", data={"pr_url": pr_url})
