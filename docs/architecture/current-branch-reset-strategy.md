# Current Branch Reset Strategy

When a branch contains abandoned app work, use the safest option that matches the situation.

## Option A — Abandon the branch and start fresh
Best when the branch contains no useful Conductor core changes.

Suggested flow:

```bash
git fetch origin
git switch main
git pull
git switch -c conductor-platform-spine
mkdir -p docs/conductor-platform
unzip conductor_platform_build_pack_v3.zip -d docs/conductor-platform
```

## Option B — Clean the current branch
Best when the branch contains useful Conductor runtime changes that should be preserved.

Run the cleanup prompt:

```text
docs/conductor-platform/conductor_platform_build_pack_v3/docs/prompts/00-clean-current-branch-and-ingest-roadmap.md
```

## Option C — Extract useful commits into a new branch
Best when only a few commits/files are useful.

Suggested flow:

```bash
git fetch origin
git switch main
git pull
git switch -c conductor-platform-spine
# selectively cherry-pick or copy only confirmed Conductor core files
```

## Rule of Thumb
If the old branch is mostly abandoned product code, Option A is safest. If it contains pipeline/session/server improvements you need, use Option B or C.
