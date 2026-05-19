# Conductor Platform Build Pack v5

This pack contains the roadmap, prompts, policies, templates, and safety controls for restarting Conductor as a clean, reusable product-building platform.

v5 adds:

- autonomy and escalation policy
- approval queue template
- blocker template
- change manifest template
- phase rollback template
- pre-start safety checklist
- bootstrap console requirements for approvals, rollback, modified files, and parallelization status
- seed `phase-status` and `autonomy-policy` config files

## Strategy

Build Conductor as the reusable platform first. Then use Conductor to build products across domains, including the CEO enterprise knowledge-base / analytics product as a proof case.

## Core onboarding modes

1. New Product Build
2. Existing Product Improvement
3. Data Platform / Service Modernization

## Recommended prompt order

Start with this optional but recommended preflight prompt:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-preflight-autonomy-rollback-policy.md
```

Then run:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-clean-start-reset-branch.md
```

Then run:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-repo-restructure-and-roadmap-ingestion.md
```

Then run:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/00-bootstrap-orchestration-console.md
```

Then run:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/P0-pipeline-dag-engine.md
```

Then run:

```text
docs/conductor-platform/conductor_platform_build_pack_v5/docs/prompts/P0-validation-review.md
```

## Build principle

Do not build every advanced feature first. Build the platform spine first: repo cleanup, repo restructure, bootstrap coordination UI, pipeline engine, events/dashboard, Build Studio, onboarding/decision simulator, phase templates, multi-tenant security, client portal, trust-aware data/access, data modernization, market/growth, context/memory, infra/ops, and self-improvement.

## Autonomy principle

Give agents broad autonomy for reversible work inside a safe branch, but require approval for destructive, security-sensitive, production-sensitive, IP/legal-sensitive, paid-resource, deployment, and high-uncertainty actions.

Use this rule:

```text
Low risk + reversible → proceed and document.
Medium risk + uncertain → quarantine and report.
High risk or irreversible → request approval.
```
