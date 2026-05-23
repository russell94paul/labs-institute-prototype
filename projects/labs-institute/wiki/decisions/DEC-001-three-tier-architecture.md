---
tags: [decision, architecture]
status: accepted
created: 2026-05-23
updated: 2026-05-23
---

# DEC-001: Three-Tier Application Architecture

## Context

Labs Institute needs both a public marketing presence and internal management tools. Different users (public visitors, label owner, individual DJs) have different needs and access levels.

## Decision

Build three tiers:

1. **Marketing Site** (labs.institute) — public-facing. Attracts DJs and promoters. Showcases roster, services, proof of value, events. Content populated via the Site Content Builder in Conductor.

2. **Owner Portal** — internal admin for the Labs Institute owner/team. Manages DJ roster, venues, events, contracts, finances, bookings, commissions. Full visibility across all artists.

3. **DJ Portal** — per-artist dashboard. Each DJ manages their own content, social media, calendar, gig tracker, metrics. Sees their own data, not other artists'.

## Consequences

- Marketing site is a separate build (Squarespace or custom static site) fed by Conductor's structured content output
- Owner portal and DJ portal can share the same Conductor-hosted app with role-based views
- Authentication/identity needed for portals but not for marketing site
- Data model must support per-DJ scoping from the start
