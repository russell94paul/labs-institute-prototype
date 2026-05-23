---
tags: [context, admin, ux]
created: 2026-05-23
updated: 2026-05-23
sources: [research/raw/001-mvp-site-architecture.md]
---

# Admin CMS Design

## Approach: Guided Form-Driven Editing

Research confirms: for a solo founder, structured section-by-section forms beat raw WYSIWYG or inline editing. Each page gets its own editor with plain-language fields.

## Artist Page Editor Fields

- Full Name, Stage Name
- Short Bio (1 sentence tagline)
- Full Bio (2-3 paragraphs)
- Genres (multi-select from industry list)
- Tier (dropdown: emerging/developing/established/headliner)
- Milestones (list: year + description)
- Key Releases (list: title, label, year, streams)
- Spotify URL, SoundCloud URL, Instagram handle
- Featured Press/Mix URLs
- Image URL / Photo
- Supported By (list of names)
- Venues Played (list)
- Festivals (list)

## UX Principles (from research)

- Collapsible sections for advanced options (SEO metadata)
- Inline help text on each field
- Conditional logic: hide empty sections
- Minimal dropdowns — avoid decision fatigue
- Immediate preview after save
- Fast admin page load — avoid frustration

## Data Schema

All content stored as JSON (upgrade to Postgres later). Each content edit can trigger static site regeneration or immediate fetch.
