# Triad Working Session: Streakly Comeback Screen

**Attendees:** PM (Engagement squad), Raj (Eng lead), Lena (Design)
**Duration:** 30 minutes
**Prototype:** [prototype/index.html](../prototype/index.html)

## 1. Session Agenda

**Objective:** Align on technical feasibility, design/tone, and open UX questions before moving from prototype to a build-ready spec.

| Time | What |
|------|------|
| 0–5 min | Recap: Day-7 retention drop (48%→39%), the hypothesis, why this screen — see [docs/decision-brief.md](decision-brief.md) and [docs/hypothesis.md](hypothesis.md) for anyone who needs the full context afterward. |
| 5–15 min | Live walkthrough of the prototype — all five screens: Comeback → 60-second lesson → freeze unlock → restored streak, plus the "Not now" exit path. Call out what changed across testing rounds (the "Not now" bug fix, the "Free, always" trust copy). |
| 15–25 min | Discussion — feasibility questions for Raj, design/tone questions for Lena, and the two open questions below. |
| 25–30 min | Recap decisions and owners; confirm next steps. |

### What to Show

- The full interactive flow, end to end (not just static screens).
- The two states that changed based on testing: the fixed "Not now" exit, and the added "Free, always — no catch" reassurance copy.
- The two things we're *not* showing as finished: the entry point into this screen (undefined — notification? home-screen state?) and the reset-mechanic-vs-acknowledgment open question below.

### Questions for Raj (Engineering)

- Is retroactively restoring the streak count (12 days, not reset to 0) feasible with data we already have, per the "no new integrations" constraint?
- What's actually needed to implement the streak-freeze mechanic — new backend logic, or does it build on what was already scoped as "technically doable" in the original retention Slack thread?
- Who's eligible to see this screen, and for how long? The prototype shows a 48-hour offer window — is that a real constraint or an arbitrary placeholder we need engineering input on?
- Any constraints on how/where this screen gets triggered (push notification vs. detecting home-screen state on open)?

### Questions for Lena (Design)

- Does the "playful, coach not scorekeeper" tone hold up against our actual design language, or does it need adjustment?
- The lesson-gated streak-freeze (you have to finish a lesson to unlock it) — does that friction feel intentional and fair, or does it risk reading as a toll? (Flagging: a round of simulated persona testing raised this as a trust risk with churned-user types — not yet validated with real users.)
- Any refinement needed on how we visually distinguish "where you left off" (12 days) from "your best ever" (18 days) — real usability testing showed the original version conflated these before a copy fix.
- Who owns designing the entry point (notification vs. home-screen state) — that's currently undefined.

### Decisions to Walk Out With

1. **Go/no-go** on this direction moving from prototype to a build-ready spec.
2. **Reset mechanic vs. acknowledgment:** do we resolve this now, defer it, or scope a way to test it (e.g., an experiment variant)? See [strategy.md](../strategy.md) for the open framing.
3. **Entry point:** who owns designing how a user actually arrives at this screen, and by when?
4. **Lesson-gated freeze:** keep as-is, simplify, or flag for real-user validation before deciding? (Currently only simulated/persona-tested, not real-user-tested.)
5. **Notification cadence:** confirm it stays a separate workstream and isn't blocking this build.

---

## 2. Post-Session Alignment Doc Template

*Fill in and save after the session — recommended path: `docs/triad-session-notes-[date].md`.*

```markdown
# Triad Session Notes — Streakly Comeback Screen

**Date:**
**Attendees:**

## Decisions Made

| Decision | Owner | Notes |
|----------|-------|-------|
| | | |

## Open Questions (Not Resolved Today)

| Question | Owner | Next step |
|----------|-------|-----------|
| | | |

## Risks / Concerns Raised

-

## Next Steps

| Action | Owner | Due |
|--------|-------|-----|
| | | |

## Changes to Scope (if any)

-
```
