---
tags: [context, architecture, site]
created: 2026-05-23
updated: 2026-05-23
sources: [research/raw/001-mvp-site-architecture.md]
---

# Marketing Site Architecture

## MVP Pages (in order of priority)

1. **Home** — hero with scrolling marquee + tagline, KPI bar, featured artist preview, dual CTAs (Join / Book), social proof
2. **Artists (Roster)** — grid/list of artists linking to individual profiles. Alphabetical, minimal, with photos and genre tags
3. **Artist Profile** (`/artists/luciid`) — full career page: bio, stats, timeline, releases, venues, festivals, embeds, socials, booking CTA
4. **About** — origin story, values (Reputation/Transparency/Reinvestment/Family/Value), "With vs Without Labs" comparison, commission model
5. **Contact** — split into two forms: "Join Labs" (DJ application) and "Book Our Artists" (promoter inquiry)

## Artist Profile Structure (per research)

| Section | Content | Priority |
|---------|---------|----------|
| Header | Name, photo, one-line tagline, genre tags, tier badge | Must-have |
| Stats bar | IG followers, RA followers, Spotify streams, countries played | Must-have |
| Bio | 2-3 paragraph narrative mixing story + credentials | Must-have |
| Quote | Artist quote (authenticity signal) | Should-have |
| Career timeline | Year-by-year milestones, reverse chronological | Must-have |
| Key releases | Title, label, year, stream count | Must-have |
| Supported by | Names of A-list artists who play their tracks | Should-have |
| Venues & festivals | Logos or text list of notable venues/festivals | Must-have |
| Embedded media | SoundCloud/Spotify player for top track, lazy-loaded | Should-have |
| Press | Links to features (Four/Four Magazine, etc.) | Nice-to-have |
| Socials | Linked buttons to all platforms | Must-have |
| CTAs | "Book [Artist]" + "Join Labs" | Must-have |

## Conversion Funnels

**DJ Funnel:** Home → Artists → Artist Profile (career proof) → "Join Labs" application form
**Promoter Funnel:** Home → Roster → Artist Profile (credibility) → "Booking Inquiry" form

## Key Design Decisions

- Static or hybrid site generated from JSON content (fast load, SEO-friendly)
- Single-column mobile layout, large touch targets
- Lazy-load embeds below the fold
- URL structure: `/artists/luciid` (stable, extensible)
- Reserve `/dashboard` path for future portals
