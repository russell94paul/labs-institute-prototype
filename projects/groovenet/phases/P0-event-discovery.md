---
phase_number: 0
phase_name: "Event Discovery + DJ Set Tracker"
goal: "Build the core event discovery feed and set tracking system so DJs can find gigs, record their sets, and ensure every performance gets documented and posted."
deliverables:
  - Event discovery feed with filtering (genre, location, paid/unpaid, open-deck)
  - DJ set tracker — log every performance with venue, date, type, recording link
  - Auto-prompt to post/upload recordings after a set
  - Event matching — surface gigs suited to a DJ based on their genre, location, availability
  - Open-deck night tracking — ensure unpaid sets still get recorded and promoted
estimated_complexity: "medium"
risk_level: "low"
acceptance_criteria:
  - A DJ can browse upcoming events filtered by type and location
  - A DJ can log a set they played with metadata
  - The system suggests events matched to a DJ's profile
  - Open-deck sets are tracked and flagged for recording/posting
  - Event data persists across sessions
constraints:
  - No external API integrations in P0 — events are manually entered or seeded
  - No auth system yet — single-user or simple name-based identity
  - Responsive web UI, no native mobile
---

## Context

DJs — especially in the underground/grassroots scene — play a mix of paid gigs, unpaid open-deck nights, guest slots, and collaborative events. Many of these go unrecorded and unposted, losing promotional value. GrooveNet's first job is to make sure every set a DJ plays gets tracked, recorded, and shared.

## Event Discovery Feed

The feed shows upcoming events that a DJ might want to play or attend. Events have:

- **Title** — name of the event/night
- **Venue** — where it's happening
- **Date/Time** — when
- **Type** — paid gig, open-deck, guest slot, collab, residency
- **Genre tags** — what music fits
- **Promoter/Collective** — who's running it
- **Capacity** — expected attendance
- **Status** — open for applications, confirmed lineup, past

DJs can filter by genre, location, event type, and date range.

## Event Matching

The system suggests events to a DJ based on:
- Their genre preferences
- Their location
- Past events they've played
- Their availability (if set)

This is rule-based in P0 — ML/AI matching comes in later phases.

## Set Tracker

After a DJ plays a set, they log it:
- Event name + venue
- Date played
- Set type (headliner, support, open-deck, b2b, guest)
- Duration
- Recording link (SoundCloud, Mixcloud, YouTube, file upload)
- Posted? (yes/no — if no, system reminds them)

## Open-Deck Tracking

Open-deck nights are valuable for emerging DJs but often go undocumented. The system:
- Flags open-deck events in the feed
- After the event date, prompts DJs who attended to log their set
- Tracks which open-deck sets have recordings vs. which don't
- Encourages posting with a "your set from [event] isn't posted yet" nudge
