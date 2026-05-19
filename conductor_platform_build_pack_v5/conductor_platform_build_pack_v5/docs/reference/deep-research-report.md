# Secure self-improving memory system for Conductor

## Executive overview

### A Executive summary

Conductor should treat memory promotion as a software release process, not as an automatic note-taking feature. NIST’s Secure Software Development Framework recommends integrating security into the development lifecycle and addressing the root causes of defects, while OWASP’s AI agent guidance specifically recommends validating and sanitising agent memory before persistence, isolating memory between users and sessions, auditing stored memory for sensitive data, and using integrity checks for long-term memory. In practice, that means every proposed memory, prompt patch, retrieval heuristic, agent recommendation, and “lesson learned” must begin life as a candidate artefact, remain quarantined by default, and only become active after it passes evaluation and approval. citeturn24view0turn10view7turn12view10

The safest design is a **two-plane system**. The first plane is the local Conductor memory plane, which holds `PROJECT`, `WORKSPACE`, and `ORGANIZATION` knowledge inside the tenant environment. The second is an **optional** `GLOBAL_ZEUS` plane that is physically and logically separated, accessed through an adapter interface, and allowed to contain only sanitised, generalised, approved patterns. OpenFeature’s provider model is a good precedent here: the integration point is abstracted behind a provider, the underlying implementation can change without major refactoring, and when no provider is configured the system can fall back to default behaviour rather than failing hard. That is exactly the behaviour Conductor needs for local-first and offline operation. citeturn23view0turn23view1

For tenant isolation, use a **hybrid tenancy model**: pooled/shared-database tables with strong row-level security for most tenants and projects, plus an escape hatch to database-per-tenant for high-compliance, high-value, or noisy tenants. Microsoft and AWS both describe this hybrid as the practical middle ground between strong isolation and manageable cost. Within the pooled tier, PostgreSQL row-level security should be the primary enforcement boundary, not application-side filtering, and runtime roles should never own tables or carry `BYPASSRLS`. citeturn11view0turn11view1turn11view3turn12view0turn10view0turn7search1

The MVP should therefore stop short of “self-improving global intelligence”. Build project-scoped self-improvement first, keep `GLOBAL_ZEUS` read-only or disabled by default, and require human approval for any organisation-wide or global promotion. The core architectural stance is simple: **memory changes are configuration releases with benchmarks, gates, rollbacks, and audit trails**.

## Memory scopes and isolation

### B Dual-scope memory architecture

Conductor’s memory system should expose four scopes, but only two memory planes. The **local plane** contains `PROJECT`, `WORKSPACE`, and `ORGANIZATION` records, all stored inside the customer-controlled Conductor environment. The **global plane** contains `GLOBAL_ZEUS` records only, and should live in a separate store with no tenant, client, project, or repository identifiers. OWASP’s agent-memory guidance is explicit that memory contents should be validated, isolated, size-limited, and audited before persistence; OWASP’s prompt-injection guidance is equally explicit that LLM systems process instructions and data in the same channel unless the application deliberately separates them. Those two facts together strongly support a design in which raw project material never becomes globally reusable memory by default. citeturn10view7turn12view5

Each memory-like record should carry at least these control fields: `scope`, `origin_scope`, `candidate_kind`, `status`, `source_ids`, `sensitivity`, `portal_visibility`, `authority_rank`, `benchmark_suite`, `benchmark_result`, `promotion_decision_id`, `rollback_manifest_id`, `created_by`, `approved_by`, `valid_from`, `expires_at`, and `content_hash`. This design lets one schema handle true memory notes, prompt diffs, retrieval-rule changes, agent rubrics, review heuristics, and deployment heuristics without pretending they are all the same kind of artefact.

The design rule should be: **project truth always outranks global convenience**. The current repository, project documentation, and project architecture decisions are authoritative for that project even when a global pattern appears more statistically useful. That is partly a product requirement, and partly a security requirement: prompt-injection risks and agent-memory poisoning both get worse when lower-authority retrieved content can silently override higher-authority local truth. citeturn12view5turn26view0turn10view7

### C Project workspace organization global memory responsibility split

The scope split below is the safest workable default for Conductor.

| Scope | What belongs here | Typical examples | What must never live here | Promotion path |
|---|---|---|---|---|
| `PROJECT` | Repository-specific truth, implementation decisions, product semantics, operational quirks, project review and testing lessons | ADR summaries, feature flag caveats, naming conventions, local deployment gotchas, recurring code-review findings for this repo | Anything from another tenant; uncited summaries; raw secrets; raw portal-restricted content in agent-ready form | Can nominate upward after safety scan and benchmark pass |
| `WORKSPACE` | Knowledge shared by several projects in one team, programme, or environment | Shared libraries, shared CI jobs, platform conventions, common service topology | Customer-specific incidents from other workspaces; repo-private details that are not actually shared | Promote from project if reused across workspace projects |
| `ORGANIZATION` | Company standards, governance, approved templates, common review and security rules | Coding standards, threat-modelling checklist, approved PR template, release governance | Tenant-external data; client-specific contract terms; project-specific path or repo assumptions | Promote from workspace or project with org approval |
| `GLOBAL_ZEUS` | Sanitised, generalised, cross-project patterns only | Prompt phrasing that improves citation discipline, generic migration-review heuristics, reusable deployment-risk checks | Client names, tenant IDs, repo URLs, file paths, incident details, domain-specific vocabulary, private code, proprietary architecture patterns | Publish only after de-identification, cross-project validation, and human approval |

This split lines up with Microsoft’s guidance that a “tenant” is a business and isolation concept, not merely a deployment shape, and that some customers may need multiple tenants because of region, environment, or compliance requirements. It also aligns with NIST’s zero-trust position that access should be granted per request and at the minimum privilege required. In other words, scope is not just a retrieval convenience; it is part of the access-control model. citeturn13view0turn20view0

A project learning should only be nominated to `GLOBAL_ZEUS` after a **generalisation step** that rewrites it into a reusable pattern with three required sections: applicability, contraindications, and benchmark evidence. If that rewrite still contains unique identifiers, customer language, repo paths, or project-specific assumptions, it should fall back to `PROJECT`, `WORKSPACE`, or `ORGANIZATION` instead of trying to become global. Sensitive-data classification and de-identification are well-established controls for this kind of step, and both NIST and Google document the need to discover, classify, and de-identify sensitive data before broader downstream use. citeturn12view8turn12view9turn25view0turn25view1

### D Multi-tenant architecture recommendation

The best fit for Conductor is a **hybrid architecture**:

| Tenancy model | Isolation | Operational complexity | Cost efficiency | Customisation | Fit for Conductor |
|---|---|---|---|---|---|
| Shared database with `tenant_id` and shared tables | Moderate, if RLS is excellent | Low to moderate | High | Low to moderate | Good default for most tenants and internal analytics |
| Schema-per-tenant | Better blast-radius control than shared tables, but not true physical isolation | High | Moderate | Moderate | Poor default; migrations and tooling get awkward quickly |
| Database-per-tenant | High | Moderate to high, but automatable | Lower efficiency at small scale | High | Best for regulated, noisy, or premium tenants |
| Hybrid pooled plus silo | Tunable | Moderate | Good | High where needed | **Recommended** |

Microsoft documents strong tenant isolation and easy per-tenant customisation for database-per-tenant, lower cost but weaker isolation for shared multitenant databases, and a hybrid model that allows individual tenants to move between shared and dedicated databases. AWS uses similar **silo / bridge / pool** language and frames tenant isolation as enforcement based on tenant context. For Conductor, that means shared pooled infrastructure for the control plane, shared RLS-protected metadata for most tenants, and optional tenant silos for exceptional cases. citeturn11view0turn11view1turn11view2turn11view3turn12view0

Concretely, define the isolation hierarchy like this:

- **Tenant**: the top commercial and compliance boundary.
- **Organization**: a business grouping inside the tenant; often but not always the same as the tenant.
- **Workspace**: a team, programme, or environment grouping.
- **Project**: the repository or product boundary.
- **User**: a human principal with scoped memberships.
- **Client portal user**: an external or semi-external read-only principal with stricter visibility limits.
- **Agent principal**: a service identity tied to one agent type, one workload, and one permission set.

This interpretation follows Microsoft’s warning that one customer may legitimately map to multiple tenants or deployments depending on requirements, and NIST’s zero-trust principle that access should be based on identity and assigned attributes rather than broad implicit trust. citeturn13view0turn20view0

Use a **separate read-only API surface** for client portals, even if it hits the same database. Portal principals should only query `security_invoker` views that expose `portal_safe` material. Agent identities should be more granular still: a `qa_agent` should not inherit the same reach as an `infra_agent`, and a `deploy_agent` should not inherit the same read path as a `requirements_agent`. Zero trust is explicit that resource access decisions should be per request, identity-aware, and as granular as possible. citeturn20view0turn20view1

### E Row-level security model

PostgreSQL is the right primary store for the governed memory plane because it gives Conductor first-class row-level security, full-text search, and an ecosystem around `pgvector`. Native RLS matters here: when enabled, PostgreSQL applies policies per row; if no policy exists, the default is deny; and policies are enforced before ordinary user predicates. Runtime roles must not be table owners, must not have `BYPASSRLS`, and tables should use `FORCE ROW LEVEL SECURITY` so that even owners are subject to policy during controlled verification paths. Security-invoker views are also important because, by default, views apply the view owner’s policy context unless `security_invoker = true` is set. citeturn10view0turn7search1turn7search4turn10view2turn13view2

A crucial operational warning: PostgreSQL disclosed a row-security vulnerability in late 2024 affecting reused query plans, role changes, security-invoker views, and role-specific policies. For Conductor, the implication is simple: run a fully patched supported PostgreSQL release, avoid making `SET ROLE` your main tenant-isolation primitive, and bind request context transaction-locally instead. PostgreSQL’s own `set_config(..., is_local => true)` mechanism is suited to that pattern because it limits context to the current transaction. citeturn16view0turn10view3

The schema should be RLS-ready by construction. Every governed table should carry the narrowest meaningful scope columns, rather than relying on joins to infer them later.

| Table family | Core tables | Minimum scope columns | Important extra columns |
|---|---|---|---|
| Identity and hierarchy | `organizations`, `workspaces`, `projects`, `memberships` | `tenant_id`, `organization_id`, optional `workspace_id`, optional `project_id` | `role`, `portal_role`, `status`, `tier`, `is_siloed` |
| Source material | `project_contexts`, `context_sources`, `chunks` | `tenant_id`, `organization_id`, `workspace_id`, `project_id` | `source_type`, `checksum`, `commit_sha`, `authority_rank`, `sensitivity`, `portal_visibility`, `stale_after_ts`, `citation_locator` |
| Memory lifecycle | `candidate_memories`, `active_memories`, `quarantined_memories` | same as above, except truly global records have no tenant columns and should be stored separately | `candidate_kind`, `status`, `content_hash`, `source_ids`, `benchmark_result`, `anonymisation_state`, `tombstone_hash` |
| Evaluation and control | `evaluation_runs`, `promotion_decisions`, `rollback_points` | same as candidate scope | `baseline_manifest_id`, `treatment_manifest_id`, `suite_name`, `overall_score_delta`, `decision_reason`, `trigger_reason` |
| Execution signals | `tasks`, `agent_runs`, `approvals`, `pr_metadata`, `deployment_records`, `build_reports` | same as project scope | `agent_type`, `trace_id`, `prompt_version`, `review_outcome`, `deployment_strategy`, `build_status` |
| Governance | `audit_logs` | scope columns matching the acted-on object | `interaction_id`, `actor_type`, `actor_id`, `action`, `object_type`, `object_id`, `before_hash`, `after_hash`, `reason_code` |

Use one naming concession: `candidate_memories`, `active_memories`, and `quarantined_memories` should be **umbrella tables** that carry a `candidate_kind` or `memory_kind` enum, so they can store prompt deltas, retrieval-rule deltas, and agent recommendations as governed “memory artefacts” without inventing half a dozen parallel lifecycle tables.

A good policy skeleton looks like this:

```sql
-- request-scoped context, set at transaction start
select set_config('app.tenant_id',      :tenant_id, true);
select set_config('app.organization_id', :org_id,   true);
select set_config('app.workspace_id',    coalesce(:workspace_id, ''), true);
select set_config('app.project_id',      coalesce(:project_id, ''), true);
select set_config('app.principal_id',    :principal_id, true);
select set_config('app.agent_type',      :agent_type, true);
select set_config('app.portal_mode',     :portal_mode, true);

alter table app.active_memories enable row level security;
alter table app.active_memories force row level security;

create policy active_memories_read
on app.active_memories
as permissive
for select
to app_runtime
using (
  tenant_id = app.current_tenant_id()
  and app.can_read_project(project_id)
  and status = 'active'
  and tombstoned = false
  and app.can_read_sensitivity(sensitivity)
  and app.can_read_visibility(portal_visibility)
);

create policy active_memories_write
on app.active_memories
as restrictive
for insert, update, delete
to app_runtime
using (app.can_write_project(project_id))
with check (
  tenant_id = app.current_tenant_id()
  and app.can_write_project(project_id)
  and scope <> 'GLOBAL_ZEUS'
);
```

That pattern follows PostgreSQL’s policy model: permissive policies widen access, restrictive policies narrow it, and you need at least one permissive policy before restrictive ones can do useful work. Helper functions such as `can_read_project()` and `can_read_visibility()` should live in a private schema and be carefully permissioned. Supabase’s guidance is also relevant here: columns used by RLS predicates should be indexed, and helper functions used in policy logic must be tested for performance. citeturn10view1turn18view0turn18view1

There are three more operational rules worth making explicit. First, use an event trigger or migration guard to ensure RLS is enabled on every new governed table, instead of trusting developers to remember it. Second, bulk ingest should land in **private staging tables** because PostgreSQL does not support `COPY FROM` on RLS-protected tables; promotion into governed tables should happen via controlled `INSERT ... SELECT` after scanning. Third, never store sensitive metadata in PostgreSQL object comments, because comments are visible to any connected user and are not a security boundary. citeturn18view2turn7search18turn17view0

### F Context precedence policy

The precedence order should be exactly as requested, with no hidden exceptions:

| Precedence | Source |
|---|---|
| Highest | Current repository code |
| High | Project source documents |
| High | Project architecture decisions |
| Medium-high | Project active memory |
| Medium | Workspace memory |
| Medium-low | Organization memory |
| Low | Global Zeus Memory |
| Lowest | General best practices |

Conductor should never silently collapse contradictions across these layers. If a lower-precedence source conflicts with a higher-precedence one, the lower-precedence candidate should be suppressed from the assembled context pack and surfaced as a conflict in the UI. If two sources at the same precedence conflict, the pack should include a **conflict banner** and ask the agent to present the discrepancy rather than synthesise a fake consensus. This is partly about correctness and partly about security: prompt injection works precisely because instruction-like text in untrusted sources gets blended with trusted context unless the application preserves source boundaries. citeturn12view5turn10view7

The UI warning model should therefore distinguish four cases: **overridden by higher precedence**, **stale versus newer code or document version**, **same-precedence conflict**, and **unauthorised for current principal**. Those warnings should be visible in the Context Pack Preview and the Context Precedence Inspector, not hidden in logs.

## Evaluation and benchmarks

### G Evaluation gate design

Conductor’s evaluation gate should compare **baseline A** versus **treatment B** under tightly controlled conditions:

- **Baseline A**: current active context pack and current active prompt / retrieval configuration.
- **Treatment B**: the same environment, but with exactly one candidate delta applied.

That single-delta rule is important. If a memory addition, prompt patch, and retrieval heuristic all change at once, Conductor cannot tell which one helped or harmed. The evaluation literature for retrieval-augmented systems also supports decomposing quality into separate dimensions: BEIR exists because narrow benchmarks hide out-of-distribution failure, while RAGAs and TruLens separate retrieval quality, groundedness, and answer relevance. Conductor should copy that discipline rather than rely on one aggregate “looks better” score. citeturn14view0turn12view4turn15view0

The gate should have five phases:

| Phase | What happens | Hard fail conditions |
|---|---|---|
| Safety scan | Secret, PII, sensitivity, stale-source, and conflict checks | Any unauthorised source, secret hit, or unresolved high-precedence conflict |
| Offline paired replay | Same benchmark cases, same model versions, same prompts except for the candidate delta | Critical metric regression |
| Regression suite | Project or cross-project benchmark families run in batch | Any red metric breach |
| Shadow canary | Candidate used on a small controlled fraction of real eligible tasks | Material degradation versus control |
| Promotion decision | Snapshot, approval, rollout, monitoring window | Missing approvals or missing rollback point |

For shadow canaries, use the same operational logic that SRE teams use for releases: expose a small slice of real traffic or work to the candidate, compare it against the control, and roll back quickly if it degrades. Google’s SRE guidance frames the canary as a way to compare a small production segment against the control with reduced blast radius, and AWS recommends starting with a small traffic percentage and a defined bake time before full rollout. Those same principles apply to memory promotions. citeturn12view1turn19view0

A practical default threshold set for **project-level promotion** is:

| Candidate type | Minimum uplift | Maximum tolerated cost increase | Approval default |
|---|---|---|---|
| Project memory note | `OverallScoreDelta >= +0.03` or target metric `>= +0.05` | `p95 latency <= +10%`, context tokens `<= +15%` | Project maintainer for sensitive or high-impact cases |
| Prompt patch | `OverallScoreDelta >= +0.02` | Same as above | Human approval required |
| Retrieval heuristic | `OverallScoreDelta >= +0.02` and retrieval precision uplift | Same as above | Human approval required |
| Review / deploy heuristic | Positive target delta and zero red regressions | Same as above | Human approval required |

For **organization or global promotion**, raise the bar: require positive cross-project median uplift, positive impact on a supermajority of holdout projects, and zero critical regressions anywhere. If the benchmark corpus is too small to justify confidence, do not promote. Keep it project-scoped.

### H Project benchmark suite

The project benchmark suite should be built from the project’s own artefacts: repository history, ADRs, accepted specifications, closed issues, merged PRs, build reports, post-deployment incidents, and approved context packs. This respects the “project-specific truth” rule and prevents generic benchmarks from driving project memory decisions.

| Benchmark family | Canonical gold source | Primary metric | Secondary metric |
|---|---|---|---|
| Product spec retrieval | Product specs, tickets, acceptance criteria | `Precision@k` | Citation coverage |
| Architecture decision retrieval | ADRs, architecture docs | `Precision@k` | Contradiction rate |
| Relevant code file retrieval | Historical PRs and changed files | `Recall@10` | Mean reciprocal rank |
| Similar past task retrieval | Linked tickets / prior task traces | `Precision@5` | Token efficiency |
| Context pack quality | Approved packs for historical tasks | Irrelevant context rate | Source authority score |
| Stale-document detection | Docs with known drift against newer code | Stale detection precision / recall | False-positive rate |
| Conflict detection | Seeded contradictory docs and code | Conflict detection F1 | Escalation quality |
| Citation quality | Human-reviewed answers with source locators | Citation coverage | Citation authority |
| Roadmap planning support | Accepted project plans and milestones | Plan adherence score | Human correction rate |
| Code review recommendation quality | Seeded issue corpus from real PRs | Finding precision / recall | False-alarm rate |
| Test recommendation quality | Known failing paths and historical regressions | Bug-catch rate | Test relevance |
| Deployment risk detection | Past deployments, incidents, rollback records | Risk-detection recall | F2 score |

The benchmark philosophy should borrow from BEIR and the RAG-evaluation stack without becoming dependent on them. Use **retrieval metrics** like `Precision@k` and `Recall@k`, **RAG quality metrics** like context relevance, groundedness, and answer relevance, and **agent-trace metrics** for tool use, plan quality, and execution efficiency. TruLens already frames these dimensions clearly, including agentic scorers such as `ToolSelection`, `ToolCalling`, `PlanQuality`, and `ExecutionEfficiency`, while RAGAs adds fast reference-free checks that are useful for iteration. citeturn15view0turn15view1turn12view4turn14view0

The sceptical rule is: **LLM-as-judge is a screening layer, not a promotion authority**. It can speed up iteration, but blocking regressions should still rely on gold-labelled project cases and deterministic checks wherever possible.

### I Global Zeus benchmark suite

Global Zeus should use a stricter benchmark philosophy than project memory because the main risk is **false generalisation**. BEIR’s core lesson is that homogeneous, narrow evaluation tells you too little about out-of-distribution performance. That directly applies to global memory: if a candidate only helps the project that produced it, it is not global memory; it is project memory with dangerous ambitions. citeturn14view0turn14view3

A candidate should only be promotable to `GLOBAL_ZEUS` if it passes all of the following classes of tests:

| Global benchmark family | What it proves | Minimum requirement |
|---|---|---|
| Cross-project generalisation | The pattern helps other projects, not just its home project | Positive median delta on holdout projects |
| Overfitting prevention | The pattern is not secretly tied to repo or tenant identifiers | Zero identifier leakage and low specificity score |
| Reusable pattern validation | The pattern is meaningfully portable | Positive impact across at least three unrelated projects |
| Company standards validation | The candidate aligns with published organisational rules if relevant | No conflict with org policy |
| Prompt improvement validation | Prompt wording improves groundedness / relevance across projects | Positive cross-project groundedness delta |
| Retrieval heuristic validation | Retrieval rule changes help diverse corpora | Positive retrieval-quality delta with no authority degradation |
| Code review heuristic validation | Review rubrics detect issues beyond the origin codebase | Positive precision / recall on holdout PR corpora |
| Deployment heuristic validation | Deployment rules catch general risks across services | Positive recall with acceptable false-alarm rate |

The simplest robust protocol is **leave-origin-project-out** evaluation. A candidate originating in Project Alpha must be benchmarked on Projects Beta, Gamma, and Delta without seeing their benchmark labels during generalisation. If the pattern helps only Alpha, keep it local. If it helps Alpha and Beta but harms Gamma, keep it at `ORGANIZATION` or `WORKSPACE` scope until the contradiction is understood.

Prompt and retrieval changes deserve special suspicion. They often look globally useful because they are centrally applied, but they can easily damage groundedness or token efficiency in specific stacks. Conductor should therefore require **two independent positives** before global promotion: one on answer quality and one on retrieval or trace quality. A prompt that sounds cleaner but worsens citation quality or tool choice should fail. citeturn15view0turn15view1turn12view4

### J Metrics and scoring formulas

The metric set below gives Conductor enough structure to make promotion decisions legible.

| Metric | Formula | Notes |
|---|---|---|
| Retrieval precision | `Precision@k = relevant_chunks_in_top_k / k` | Use per benchmark family |
| Citation coverage | `claims_with_valid_citations / nontrivial_claims` | Must validate locator and source access |
| Source authority | `sum(authority_weight(cited_source)) / cited_source_count` | Weight code and ADRs above memories and globals |
| Stale context rate | `stale_chunks_used / total_chunks_used` | Lower is better |
| Contradiction rate | `contradicted_claims / cited_claims` | Lower is better |
| Irrelevant context rate | `irrelevant_context_tokens / total_context_tokens` | Lower is better |
| Token efficiency | `task_success_proxy / context_tokens_used` | Higher is better |
| Latency | `p95 end_to_end_ms` | Lower is better |
| Task success proxy | `weighted_case_passes / weighted_cases` | Use gold labels where possible |
| Code review quality proxy | `(true_positives - 0.5 * false_positives) / seeded_issues` | Penalise noisy reviewers |
| Test pass proxy | `bugs_caught_by_recommended_tests / known_testable_bugs` | Coverage of recommended tests matters |
| Deployment risk proxy | `F2(precision, recall)` | Recall matters more than precision |
| Human correction rate | `substantive_human_edits / reviewed_outputs` | Lower is better |
| Regression count | `count(metrics_below_guardrail)` | Must be zero on hard metrics |
| Overall score delta | `sum(w_i * norm_delta_i) - penalty_regressions - penalty_security` | Promotion uses this plus hard-fail rules |

A good default authority weighting is: code `1.00`, project ADR `0.95`, signed project doc `0.90`, project active memory with citations `0.80`, workspace memory `0.72`, organization memory `0.68`, global memory `0.55`, uncited memory `0.00`. That weighting is deliberately conservative against global creep.

Use one aggregate formula for convenience, but never let it override hard blockers. A candidate should fail immediately if any of the following are true: unauthorised source included, secret or sensitive-data finding, unresolved conflict with higher-precedence truth, citation coverage below the policy minimum, or critical benchmark regression. SRE-style rollout and DORA-style operational outcomes reinforce the same idea: change velocity matters less than the cost of bad changes and the ability to recover quickly. citeturn12view1turn19view0turn12view2

## Promotion lifecycle and agent learning

### K Promotion and rejection policy

The lifecycle should be immutable and auditable:

```text
draft -> candidate -> safety_scanned -> evaluated -> approved -> active -> monitored
                                              \-> quarantined -> tombstoned or reconsidered
```

Promotion rules should be simple enough to enforce automatically and strict enough to be trusted by operators:

| Rule | Project | Workspace / Organization | Global Zeus |
|---|---|---|---|
| Valid source citations required | Yes | Yes | Yes |
| Safety scan pass required | Yes | Yes | Yes |
| Benchmark improvement required | Yes | Yes | Yes |
| Zero hard regressions required | Yes | Yes | Yes |
| Human approval required | High-risk only by default | Yes | Yes, always |
| Rollback point created first | Yes | Yes | Yes |
| Post-promotion monitoring window | Yes | Yes | Yes |

Rejection reasons should be codified, not free-text only. Recommended reason codes are: `secret_detected`, `pii_detected`, `unauthorised_scope`, `low_citation_coverage`, `low_source_authority`, `stale_source`, `higher_precedence_conflict`, `benchmark_no_gain`, `critical_regression`, `overfit_origin_project`, `insufficient_holdout_projects`, `duplicate_candidate`, and `global_leakage_risk`. OWASP’s AI agent guidance, OWASP’s prompt-injection guidance, and the OWASP LLM Top 10 all point in the same direction: assume memory poisoning, instruction confusion, sensitive-information disclosure, and excessive autonomy are real risks, not corner cases. citeturn10view7turn12view5turn26view0

### L Quarantine strategy

Quarantine should be both a **workflow state** and a **storage boundary**. Do not merely flag rejected candidates in-place inside tables that the runtime can already see. Put candidate and quarantined artefacts in a separate schema, separate read path, and preferably separate indexes so that runtime retrieval cannot accidentally touch them.

A good quarantine record should store: original candidate payload, extracted candidate text, generalised global rewrite if any, source excerpts, source hashes, secret-scan findings, PII findings, classification labels, failed benchmark traces, reviewer notes, rejection codes, `reconsider_after`, and `tombstone_hash`. Long-term rejected candidates should be tombstoned by hash so that trivial re-submission does not churn the queue.

Sensitive-source detection should combine several layers: repository secret scanning, custom secret patterns, text-level PII detection, source classification labels, and portal-visibility checks. GitHub documents secret scanning across repository history and custom pattern support; NIST documents the need to identify, classify, and protect PII and unstructured sensitive data; Google documents detector-driven de-identification and obfuscation workflows. Conductor should replicate the control pattern locally, even if the specific detector implementation differs. citeturn12view7turn12view8turn12view9turn25view0turn25view1

Stale-source detection belongs in quarantine too. A candidate derived from documentation that predates contradictory repository code should be blocked until refreshed. Conflict detection should compare candidate claims against higher-precedence sources, not only against peer memories. Reconsideration should only be allowed when the source materially changes, the benchmark suite changes, or a reviewer explicitly overrides with justification. Rejected and quarantined candidates must never appear in active context packs; the easiest technical guarantee is that the context pack builder only queries manifest-backed active views and has no grants on candidate or quarantine schemas.

### M Rollback strategy

Rollback should work by **manifest pointer swap**, not by mutating rows in place. Every promotion should create a new immutable manifest per scope that captures the active memory IDs, prompt version IDs, retrieval-rule versions, embedding model version, reranker version, and any pack-building configuration. A rollback simply flips the active manifest pointer back to a previous snapshot and records the event in audit history.

Use these default rollback scopes and approvers:

| Scope | Automatic rollback allowed | Manual approver default | Monitoring window |
|---|---|---|---|
| Project | Yes, on hard failures | Project maintainer or on-call | First 50 eligible tasks or 7 days |
| Workspace | Limited | Workspace owner | First 100 eligible tasks or 14 days |
| Organization | Emergency only | Platform / security approver | First 250 eligible tasks or 21 days |
| Global Zeus | Emergency disable only | Global reviewer plus security | First 500 eligible tasks or 30 days |

The triggers should mirror canary-release practice: latency degradation, citation collapse, higher correction rate, deployment-risk misses, operational complaints, or any security incident should trigger rollback review; severe failures should trigger immediate rollback. Google and AWS both recommend explicit bake times, comparative monitoring, and automatic rollback triggers for canary deployments, while DORA treats rollback-triggering failures as part of change fail rate. The same logic applies to memory promotions because they alter production behaviour. citeturn12view1turn19view0turn12view2

### N Agent-specific self-improvement matrix

All agents may **propose** candidates, but none should be able to **promote** them without the evaluation and approval path.

| Agent | What it may learn and propose | What must stay project-level | What may be nominated upward | Main validating benchmark | Approval requirement | Forbidden data |
|---|---|---|---|---|---|---|
| Requirements | Glossaries, acceptance-criteria patterns, ambiguity flags | Product terminology, stakeholder-specific wording, client commitments | Generic requirement-clarity prompts and ambiguity checklist | Spec retrieval, roadmap planning, citation quality | Global and org always human-approved | Secrets, deployment credentials, raw production logs |
| Planning | Task decomposition, dependency order, PR slicing | Repo topology, team cadence, release-specific workaround steps | Generic planning templates and decomposition heuristics | Similar task retrieval, roadmap support, token efficiency | Human approval for all promoted heuristics | Unrelated client documents, secrets |
| Frontend | Design-system usage, accessibility pitfalls, component test patterns | Brand specifics, local route names, feature-flag quirks | Generic accessibility and review heuristics | Relevant file retrieval, code review, test recommendations | Human approval above project | Backend secrets, infra credentials |
| Backend | API patterns, migration rules, idempotency checks | Exact schema quirks, service-specific invariants | Generic migration, auth, idempotency, and retry checks | ADR retrieval, code review, test recommendations | Human approval above project | Secrets, unrelated tenant data |
| Infrastructure | IaC conventions, rollout steps, health checks | Exact environment names, cluster details, customer blackout windows | Generic canary and rollback heuristics | Deployment risk detection, rollback success | Human approval always | Raw secret values, unrelated project docs |
| QA | Flaky-test mapping, fixture patterns, regression hotspots | Exact test fixtures, private datasets, environment quirks | Generic test-selection and regression heuristics | Test recommendation quality | Human approval above project | Production PII, secrets |
| Code Review | Recurring bug patterns, important touched-file hints | Service-specific invariants and reviewer preferences | Generic security, migration, concurrency, and API-review heuristics | Seeded issue detection precision / recall | Human approval above project | Secrets, other private repos |
| Deploy | Release checks, rollback conditions, health thresholds | Environment-specific steps and windows | Generic deployment-risk rules | Deployment risk proxy, rollback outcomes | Human approval always | Credentials, unrelated logs |
| Observability | Alert triage patterns, dashboard queries, SLO hints | Service names, customer incident details, private metrics queries | Generic incident-triage playbooks | Deployment risk and stale/conflict detection | Human approval above project | Raw customer telemetry and PII |
| Approval | Risk-rubric consistency, evidence sufficiency | Approver roster, exception history, customer-specific policy | Generic approval rubric only | Citation completeness and decision consistency | Human approval by definition | Raw secret values, unrelated project content |

This matrix follows the same least-privilege and memory-isolation philosophy recommended by NIST zero trust and OWASP agent-security guidance: each agent’s read access should be narrower than its task type suggests, and each proposed “learning” should be tied to a benchmark family before it becomes reusable. citeturn20view0turn10view7

## Context delivery and governance

### O RLS-aware Context Pack Builder design

The Context Pack Builder should be the **policy enforcement point** for runtime retrieval, while PostgreSQL RLS remains the underlying data enforcement boundary. NIST’s zero-trust model uses the language of policy decision points and policy enforcement points; for Conductor, the database and the pack builder should work together in exactly that pattern. PostgreSQL’s `security_invoker` views are important here because they ensure the caller’s permissions and row policies apply during pack assembly rather than the view owner’s. citeturn20view0turn10view2

The builder should execute six stages:

| Stage | What the builder does | Non-negotiable enforcement |
|---|---|---|
| Identity resolution | Resolve `tenant_id`, `organization_id`, `workspace_id`, `project_id`, principal type, role, agent type, portal mode | Must happen per request / transaction |
| Eligibility filter | Query only active, non-tombstoned, non-expired rows through RLS-aware views | No candidate or quarantine paths in runtime |
| Precedence ranking | Rank by precedence first, then source authority, then task relevance, then freshness | Lower-precedence hits cannot silently override higher-precedence truth |
| Safety filtering | Remove sources above sensitivity or portal visibility; remove blocked global items | No unauthorised context enters the pack |
| Pack assembly | Build sections with citations, source labels, and token budget accounting | All nontrivial claims must remain sourceable |
| Attestation | Persist `context_pack_manifest` with included/excluded items, reasons, token count, and trace ID | Required for audit and rollback analysis |

Pack items should carry these runtime fields: `source_id`, `scope`, `precedence_rank`, `authority_rank`, `sensitivity`, `portal_visibility`, `stale_flag`, `conflict_state`, `token_count`, and `citation_locator`. The assembled prompt should keep retrieved content in a clearly marked **data/evidence section**, with the system prompt explicitly instructing agents to treat retrieved text as untrusted evidence rather than instructions. That directly addresses the instruction/data-mixing risk highlighted in OWASP’s prompt-injection guidance. citeturn12view5

Global Zeus safety filtering should be stricter than ordinary scope filtering. A global record must be `approved`, `active`, `generalised`, `anonymised`, and marked `global_safe` before the builder can even consider it. Portal mode should add another filter: only `portal_safe` source rows and memory rows are eligible. The builder should also produce an **exclusion ledger** so the RLS / Access Inspector can show why an item did not enter the pack.

### P UI and UX recommendations

The UI should make memory operations look less like “AI magic” and more like change management. The following views are the minimum useful set.

| View | What it should show | Why it matters |
|---|---|---|
| Project Self-Improvement Queue | Candidate kind, origin agent, source count, target metric, safety flags, current status | Day-to-day triage for project owners |
| Global Zeus Improvement Queue | Origin projects, generalisation text, anonymisation score, holdout results, approvals | Prevents unsafe global lift-and-shift |
| Candidate Detail View | Raw source links, extracted lesson, generalised rewrite, baseline vs treatment diff, rejection reasons | Makes decisions inspectable |
| Evaluation Runs | Run config, benchmark suites, seeds, score deltas, traces | Shows whether a candidate really helped |
| Promotion Decision Log | Decision, approvers, effective manifest, monitoring window | Governance and traceability |
| Quarantine View | Failure reasons, sensitive-data hits, tombstone status, reconsideration date | Keeps rejected items out of the runtime path |
| Rollback History | Scope, trigger, previous and restored manifests, operator notes | Makes rollback routine, not exceptional |
| Context Pack Preview | Exact included items in order, citations, tokens, stale/conflict flags | Lets humans inspect what the agent will actually see |
| Scope Filter | Toggle project, workspace, organisation, and global layers | Makes retrieval behaviour intelligible |
| Regression Warnings | Hard fails, metric drops, latency regressions, correction-rate rises | Stops overconfident promotion |
| Context Precedence Inspector | Conflict pairs, winner source, loser source, reason | Enforces the precedence contract visibly |
| RLS / Access Inspector | Resolved principal, allowed scopes, blocked rows, visibility reductions | Critical for security debugging |
| Tenant Isolation Warning Panel | Any cross-tenant identifiers, unsafe global candidate markers, portal-unsuitable content | Prevents leak-through before promotion |
| Audit Log Viewer | Filter by interaction ID, actor, object, action, and scope | Supports investigation and compliance |

The key UX principle is that every promotion, rejection, and rollback decision should be supported by visible evidence: sources, metrics, approval history, and current pack composition. The worst possible UX for this system is a one-click “auto-learned improvement” button with no explainer.

### Q Security and governance model

The governance baseline should combine secure software development, zero trust, agent-memory hygiene, prompt-injection resistance, and disciplined audit logging. NIST’s SSDF and its GenAI profile both position secure development practices as lifecycle controls, not last-minute checks; NIST’s zero-trust model emphasises granular, per-request authorisation; OWASP’s AI agent guidance adds memory sanitisation, isolation, and integrity; and OWASP’s prompt-injection guidance highlights the need to separate untrusted data from instructions. citeturn24view0turn12view10turn20view0turn10view7turn12view5

The concrete governance controls should be:

| Control area | Required control |
|---|---|
| Secret exclusion | Scan candidate sources and payloads for credentials; block persistence on detection |
| PII avoidance | Detect, classify, and redact or pseudonymise PII before candidate persistence or global nomination |
| Sensitive source detection | Carry explicit sensitivity labels and visibility flags on every source and chunk |
| Approval gates | Human approval mandatory for organisation and global promotions, deploy heuristics, and prompt changes |
| Source citations | Every nontrivial active memory must preserve source links and locators |
| Project and tenant isolation | Enforce in database with RLS and in runtime with pack-builder filtering |
| Role-based access | Use separate human, portal, and agent principals with explicit allowed scopes |
| Audit history | Log promotion, rejection, access, rollout, rollback, and approval actions |
| Local / offline mode | Local plane must work without Zeus and without cloud-only services |
| Optional Zeus adapter | Zeus absent must degrade to local-only behaviour, not runtime failure |
| No irreversible writes without approval | Promotion creates new manifests and snapshots; destructive deletion is separate and governed |

The sensitive-data control path is well supported by the available guidance. GitHub documents secret scanning for hard-coded secrets across repository history. NIST documents practical protection expectations for PII and unstructured sensitive data. Google documents detector-based de-identification, masking, tokenisation, and redaction workflows that are directly applicable to AI prompts and responses. Conductor does not need those exact products to adopt the pattern. It does need the pattern. citeturn12view7turn12view8turn12view9turn25view0turn25view1

Audit logging needs equal care. OWASP recommends that application logs record **when, where, who, and what** for each event, include an interaction identifier for correlation, and avoid directly logging access tokens, passwords, connection strings, encryption keys, sensitive PII, or other high-classification secrets. OWASP also recommends tamper detection, read-only storage or copying as soon as possible, and logging and monitoring all access to logs themselves. Conductor’s audit model should therefore be append-only, hash-linked where practical, and queryable by interaction ID from the Audit Log Viewer. citeturn21view0turn21view3turn22view0turn22view2turn22view3

## Technical architecture and delivery plan

### R Technical architecture

The core retrieval stack should be **hybrid lexical plus vector plus reranker**, implemented locally first. BEIR found that BM25 remains a robust baseline and that reranking / late-interaction approaches often produce the best zero-shot performance, albeit at higher computational cost. PostgreSQL already provides native full-text search with ranked retrieval over `tsvector` / `tsquery`, recommends GIN as the preferred index type for regular text search, and `pgvector` adds vector similarity search inside Postgres. For Conductor, that means one storage engine can support governed metadata, lexical retrieval, and vector retrieval without turning Zeus or any cloud vector service into a hard dependency. citeturn14view0turn14view1turn28search2turn28search4turn28search6turn13view2

Use these model roles rather than baking in any single vendor or checkpoint:

| Model role | Recommendation |
|---|---|
| Embedding model | One local text-and-code embedding model behind an adapter |
| Reranker | One local reranker or small hosted opt-in reranker behind an adapter |
| Judge model | A deterministic evaluation model used only in the evaluation harness |
| Sensitive-data classifier | Rules first, ML second; must run locally in MVP |
| Task model | Existing Conductor agent model(s), unchanged by the memory core |

The key design point is not the model brand name. It is the **adapter boundary** and the benchmark harness that decides whether a model or heuristic deserves production use.

The recommended service set is:

| Component | Responsibility |
|---|---|
| Memory Scope Manager | Resolves scope rules, precedence, and upward-nomination eligibility |
| Source Ingestion Service | Pulls repo, doc, PR, build, and deploy artefacts into governed source tables |
| Candidate Extractor | Converts agent outputs and human feedback into candidate artefacts with citations |
| Sensitive Data Scanner | Secret, PII, classification, and portal-visibility checks |
| Benchmark Registry | Stores suites, cases, gold labels, and benchmark metadata |
| Evaluation Harness | Runs paired A/B, regression suites, and shadow-canary instrumentation |
| Promotion Policy Engine | Applies rules, thresholds, approval checks, and manifest publication |
| Rollback Manager | Creates snapshots, activates prior manifests, records rollback history |
| Context Pack Builder | Produces RLS-aware context packs and preview manifests |
| Zeus Nomination Service | Generalises safe project lessons and submits them to global review |
| Zeus Memory Adapter | Optional provider for reading approved global patterns |
| Local / Mock Memory Adapter | Default local-only implementation for offline mode |
| Vector Store Adapter | Wraps Postgres / `pgvector` and keeps room for future stores |
| Audit and Trace Service | Emits audit logs and OpenTelemetry traces / metrics / logs |

For the optional Zeus integration, follow the same abstraction shape that OpenFeature uses for providers and hooks. Providers isolate the underlying implementation from the application, hooks let you add logging, telemetry, and evaluation-context mutation at the evaluation lifecycle boundaries, and the API is designed to return defaults rather than throw when evaluation fails. That is a strong pattern for an optional global-memory subsystem: when Zeus is absent or unreachable, Conductor should default to local-only packs and carry on. citeturn23view0turn23view1turn23view2

Instrumentation should use OpenTelemetry from the start. OTel gives Conductor a vendor-neutral path to traces, metrics, and logs, and OpenFeature’s own observability appendix documents how feature-flag evaluation events map into OpenTelemetry signals. That makes it a natural fit for tracing context-pack assembly, candidate evaluation runs, promotion decisions, and rollbacks in one coherent telemetry model. citeturn12view11turn23view3

A practical event flow looks like this:

```text
repo/docs/build signals
  -> source ingestion
  -> governed source tables
  -> candidate extractor
  -> safety scan
  -> candidate store
  -> evaluation harness + benchmark registry
  -> promotion policy engine
  -> scope manifest publication
  -> context pack builder
  -> agent runtime
  -> post-promotion monitoring
  -> rollback manager if needed
```

### S MVP scope

The MVP should be intentionally narrow and safe.

| Included in MVP | Deliberately excluded from MVP |
|---|---|
| `PROJECT`, `WORKSPACE`, and `ORGANIZATION` scopes | Automatic global promotion |
| Optional **read-only** `GLOBAL_ZEUS` adapter or fully disabled Zeus | Autonomous writeback into Zeus |
| PostgreSQL with RLS, full-text search, and `pgvector` | Cross-tenant shared analytics beyond governed reporting |
| Candidate / active / quarantine lifecycle | Free-form “AI learns from every run” behaviour |
| Project benchmark suite for top-value use cases | Complex online multi-armed bandits |
| Manual approval workflow | Automatic approval except for tightly bounded emergency rollback |
| Rollback manifests and audit logs | In-place mutation of active memory without snapshots |
| Context Pack Preview and Access Inspector | Opaque runtime retrieval |

The MVP objective is not “self-improving intelligence”. It is **safe governed improvement at project scope** with enough architecture to grow into workspace, organisation, and optional global reuse later.

### T Advanced roadmap

The advanced roadmap should begin only after the MVP has a reliable benchmark corpus and operators trust the rollback story.

| Advanced capability | Preconditions |
|---|---|
| Cross-project global nomination | At least several mature projects and a stable holdout suite |
| Online canary promotions | Traceability, rollback automation, and operator dashboards working well |
| Automated low-risk project promotions | Proven benchmark quality and low false-positive rate in review |
| Learned reranking weights | Strong offline benchmark suite and reproducible evaluation harness |
| Tenant tier auto-siloing | Clear cost and compliance triggers |
| Richer client-portal memory products | Proven portal-safe visibility model and redaction quality |
| More automated approval routing | Stable organisation policy model and audit confidence |

### U Risks and trade-offs

| Risk | Why it matters | Mitigation |
|---|---|---|
| RLS correctness risk | A policy mistake can become a data leak | Use patched PostgreSQL, FORCE RLS, `security_invoker` views, and adversarial tests |
| Benchmark gaming | The system may optimise for the suite instead of the work | Refresh cases and keep hidden holdouts |
| LLM-as-judge overconfidence | Easy to get plausible but wrong scores | Use gold-labelled blocker cases and human review |
| Global overreach | “Reusable” lessons may really be local quirks | Require holdout-project gains and generalisation review |
| Token bloat | More memory can still make answers worse | Track irrelevant-context rate and token efficiency |
| Operator fatigue | Too many candidates create queue debt | Prioritise by impact and deduplicate aggressively |
| Local-first model quality gaps | Offline models may underperform cloud models | Keep adapters pluggable and benchmark-driven |
| Audit/privacy tension | Rich traces help debugging but may retain too much | Minimise logged content and retain hashes / pointers where possible |

The biggest strategic trade-off is this: the stricter the governance, the slower the apparent self-improvement. That is acceptable. In Conductor’s domain, **unsafe speed is a liability**, not a capability.

### V Concrete implementation backlog

| Priority band | Work item | Main deliverable |
|---|---|---|
| Foundational | Define scope model and principal claims | Shared type system for tenant / org / workspace / project / agent / portal |
| Foundational | Create PostgreSQL schema and migrations | RLS-ready tables, enums, private schemas, indexes |
| Foundational | Implement request-context helpers | `current_setting`-based helper functions and transaction bootstrap |
| Foundational | Add RLS policies and adversarial tests | Positive and negative access tests across tenants and scopes |
| Core | Build source ingestion pipeline | Ingest repo docs, ADRs, PRs, build reports, deploy records |
| Core | Implement candidate lifecycle store | Candidate, quarantine, active, tombstone behaviour |
| Core | Build sensitive-data scanning stage | Secret, PII, visibility, and stale/conflict checks |
| Core | Implement benchmark registry and evaluator | Project benchmark suites, paired A/B runner, report output |
| Core | Build promotion policy engine | Thresholds, approvals, manifest publishing, monitoring jobs |
| Core | Build rollback manager | Immutable manifests, rollback pointer swap, audit emission |
| Core | Build Context Pack Builder | RLS-aware retrieval, precedence ranking, preview manifests |
| Core | Add audit logs and OTel instrumentation | Interaction IDs, trace IDs, promotion / rollback telemetry |
| Interface | Ship the operator UI | Queues, inspectors, evaluation runs, rollback and audit views |
| Interface | Add optional Zeus read adapter | No-op default, governed global fetch path |
| Later | Add project-to-global nomination service | Generalisation, holdout validation, global review queue |

### W Acceptance criteria

| Acceptance criterion | Pass condition |
|---|---|
| Tenant isolation | A Tenant A principal cannot read Tenant B data through direct table queries, views, or context-pack assembly |
| Project isolation | A project-scoped agent cannot retrieve sibling-project private memory unless explicitly permitted by workspace / organisation policy |
| Portal isolation | A portal principal only sees `portal_safe` sources and memories |
| Candidate safety | Newly created candidates never appear in runtime context packs before approval |
| Quarantine safety | Rejected or quarantined candidates are not reachable by runtime roles or builder queries |
| Promotion gate | No candidate is promoted without a benchmark result, approval record where required, and rollback manifest |
| Regression protection | A candidate with any hard regression is automatically rejected or rolled back |
| Rollback reliability | Restoring a previous manifest returns the prior pack composition and config deterministically |
| Audit completeness | Promotion, rejection, rollback, and access events are recorded with interaction IDs and actor details |
| Local-first operation | Conductor works fully without Zeus configured |
| Optional Zeus behaviour | Disabling Zeus removes only global retrieval; project, workspace, and organisation memory continue to function |
| Citation discipline | Runtime context packs and memory-backed outputs preserve source identifiers and locators for all nontrivial assertions |

### X Recommended next implementation prompt

```text
Implement the MVP secure memory core for Conductor.

Goal
Build a local-first, evaluation-gated memory system that supports PROJECT, WORKSPACE, ORGANIZATION, and optional read-only GLOBAL_ZEUS scopes, with no blind autonomous promotion.

Tech constraints
- Use PostgreSQL with row-level security and pgvector.
- Conductor must work fully when Zeus is disabled or unavailable.
- Project-specific truth outranks all broader scopes.
- No runtime role may own tables or bypass RLS.
- No candidate memory, prompt change, retrieval heuristic, agent recommendation, or lesson learned may become active without evaluation and approval.

Deliverables
- SQL migrations for:
  organizations, workspaces, projects, memberships,
  project_contexts, context_sources, chunks,
  candidate_memories, active_memories, quarantined_memories,
  evaluation_runs, promotion_decisions, rollback_points,
  audit_logs, tasks, agents, approvals, pr_metadata,
  deployment_records, build_reports,
  plus any manifest tables needed for versioned activation and rollback.
- Private helper functions for transaction-scoped request context:
  current tenant/org/workspace/project/principal/agent/portal mode.
- RLS policies for all governed tables.
- security_invoker views for runtime retrieval and portal-safe retrieval.
- Context Pack Builder service that:
  - enforces tenant/org/workspace/project scope,
  - enforces user role and agent permissions,
  - filters by sensitivity and portal visibility,
  - excludes candidates/quarantine/tombstones,
  - applies precedence:
    repo code > project docs > project ADRs > project memory > workspace > organization > global > general best practices,
  - emits preview manifests with citations and reasons.
- Candidate ingestion workflow:
  draft -> candidate -> safety scan -> evaluation -> approval -> active
  with quarantine and tombstoning paths.
- Safety scan stage for:
  secret detection, PII detection hooks, stale-source detection,
  higher-precedence conflict detection, visibility checks.
- Evaluation harness with paired A/B execution:
  baseline = active manifest
  treatment = active manifest + one candidate delta
- Initial project benchmark suite covering:
  product spec retrieval,
  ADR retrieval,
  relevant code file retrieval,
  context pack quality,
  stale-doc detection,
  conflict detection,
  code review recommendation quality,
  test recommendation quality,
  deployment risk detection.
- Promotion policy engine with hard blockers and rollback snapshot creation.
- Rollback manager that restores prior immutable manifests.
- Audit logging for every promotion, rejection, rollback, access-inspector lookup, and context-pack build.
- Integration and adversarial tests proving:
  tenant isolation,
  project isolation,
  portal isolation,
  no candidate leakage into runtime,
  rollback correctness,
  Zeus optional/no-op behaviour.

Implementation rules
- Keep GLOBAL_ZEUS read-only in this MVP.
- Do not build automatic global nomination yet.
- Do not use app-only filtering as the security boundary; enforce in PostgreSQL.
- Use transaction-local request context, not session-persistent role hacks.
- Runtime queries must only hit active manifest-backed views.
- Prefer append-only history and manifest pointer swaps over in-place mutation.
- Every active memory artefact must keep source references.

Output format
Return:
- schema SQL,
- service interfaces,
- pack builder implementation,
- evaluator skeleton,
- promotion policy engine,
- rollback manager,
- tests,
- and a short README explaining how to run everything locally.
```
