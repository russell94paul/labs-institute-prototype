# Questions for Deep Research

These questions map to the Deep Research prompts in `docs/research/prompts/`. Copy the full prompt from the corresponding file when running Deep Research.

## Topic 1: Multi-Tenant SaaS Architecture
- How do modern SaaS platforms implement tenant isolation with shared infrastructure?
- What are the trade-offs between schema-per-tenant vs. RLS vs. database-per-tenant?
- How do client portals handle project workspaces with RBAC?
- What audit log patterns are required for SOC 2?

**Prompt file**: `docs/research/prompts/01-multi-tenant-saas-rls-client-portals.md`

## Topic 2: Agent Orchestration & DAG Engines
- What are the best approaches for building a DAG engine that supports both human and AI agents?
- How do modern orchestrators handle branch/worktree isolation per task?
- What event streaming patterns work for real-time progress dashboards?
- How do approval gates and rollback work in agent orchestration?

**Prompt file**: `docs/research/prompts/02-agent-orchestration-dag-parallelization.md`

## Topic 3: AI-Guided Onboarding & Decision Simulation
- How do product configurators handle multi-dimensional trade-offs?
- What scoring models work for recommending product scope and features?
- How do budget/timeline/feature simulators present trade-offs to non-technical users?
- What cost/ROI models work for software development estimation?

**Prompt file**: `docs/research/prompts/03-ai-product-onboarding-decision-simulation.md`

## Topic 4: Data Platform Modernization
- What are proven migration patterns for Prefect + Snowflake + Power BI stacks?
- How do dual-run strategies work for data pipeline migrations?
- What parity testing frameworks exist for data platform migrations?
- How do you handle credential migration without exposing secrets?

**Prompt file**: `docs/research/prompts/04-data-platform-modernization-factory.md`

## Topic 5: Context, Memory & Self-Improvement
- How do multi-level memory systems prevent bad memories from degrading AI performance?
- What vector DB designs support RLS-aware retrieval?
- How do evaluation gates and quarantine processes work for AI memory?
- What regression testing strategies exist for AI context systems?

**Prompt file**: `docs/research/prompts/05-context-memory-vector-db-self-improvement.md`

## Topic 6: Secure Credential Workflows
- How do platforms handle secure client credential handoff without exposing secrets?
- What vault integration patterns work for multi-tenant SaaS?
- How do approval workflows for credential access work?
- What audit models are required for credential management?

**Prompt file**: `docs/research/prompts/06-secure-credential-artifact-workflows.md`

## Topic 7: Market Intelligence & Growth
- How do product platforms incorporate market research into feature prioritization?
- What models translate market gaps into product features with cost/ROI estimates?
- How do growth experiment frameworks work inside product development platforms?
- What pricing strategy models work for B2B SaaS with AI components?

**Prompt file**: `docs/research/prompts/07-market-intelligence-growth-engine.md`
