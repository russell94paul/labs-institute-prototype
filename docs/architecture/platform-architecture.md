# Platform Architecture

Conductor is a control plane for building and operating products.

```text
Conductor Platform
├── Build Studio
├── Product Onboarding Studio
├── Client Product Portal
├── Trust-Aware Discovery & Access Manager
├── Data Platform Modernization Studio
├── Market Intelligence + Growth Engine
├── Context + Memory Engine
├── Infrastructure / Deploy / Ops
└── Self-Improvement Engine
```

The client data plane should usually remain in client systems such as Snowflake, Power BI/Fabric, databases, APIs, SaaS platforms, or cloud accounts. Conductor stores metadata, decisions, approvals, reports, validation results, context summaries, and build state.
