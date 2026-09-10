# PRD: Streakly Comeback Screen

*Note: `02-research/competitive-reddit.md` was requested but does not exist in this workspace and is excluded below.*

## Problem Statement

Day-7 retention dropped from 48% to 39%, concentrated in users who break their streak in week 1 and don't return. Breaking a streak currently resets the counter to zero with no acknowledgment of prior progress, and the "you lost your streak" notification lands with no way back in (interview-synthesis.md: Tom R.). This is the top NPS theme by frequency (nps-analysis.md: 3 of 10 verbatims cite the silent reset as the reason for disengaging), and no competitor combines a forgiveness mechanic with a personalized comeback experience (competitive-matrix.md) — this is unaddressed white space, not a solved problem elsewhere.

## User

**Who:** A user who has built real progress (a multi-day streak) and then missed one or more days.

**Job to be done:** Get back in without feeling they lost everything (interview-synthesis.md: Tom — "There was no way to recover it, nothing. So I gave up"; nps-analysis.md — "I wish it would make coming back easier instead of making me feel like I failed").

## Goals

- Acknowledge the user's prior progress instead of a silent reset to zero (nps-analysis.md: top complaint — "Nothing acknowledges where I am").
- Offer a concrete way back in (streak-freeze) rather than leaving the user at zero with no recovery path (interview-synthesis.md: Tom — wanted a Duolingo-style streak freeze).
- Make the app read as a coach, not a scorekeeper (nps-analysis.md: tied top theme).

## Non-Goals

- **Not fixing notification tone/cadence in this feature.** Corroborated as a real, related issue (nps-analysis.md: 2 of 10 verbatims cite nagging notifications) but scoped as a separate workstream (decision-brief.md).
- **Not addressing anticipatory pre-break anxiety.** One interview (Amara L., 4 days in) shows streak stress before any break occurs (interview-synthesis.md). Single-source, not corroborated — explicitly out of scope for this version, flagged as a future consideration (hypothesis.md).
- **Not changing the underlying reset mechanic.** This feature acknowledges and offers recovery after a reset; it does not change whether or how the streak counter resets. Whether the mechanic itself needs to change is an open, unresolved question (hypothesis.md).

## Success Metrics

- **Primary:** Day-7 retention among users who break a streak (decision-brief.md).
- Full funnel logging required per screen: freeze offered, freeze used, lesson completed, screen dismissed — needed to diagnose the metric, not just report it (per Raj's standing question: "how will we know if this is working after it ships?").

## User Stories

1. **As a user who broke a streak I had invested in,** I see my prior progress acknowledged (not a blank reset) when I return, so the app doesn't feel like it erased what I built.
2. **As that same user,** I can complete a short comeback activity to unlock a one-tap streak-freeze, so I have a concrete, low-effort way back in rather than starting over.
3. **As a user who declines the offer ("Not now"),** I'm told clearly whether and how long the offer remains available, so I'm not left guessing whether I've lost the chance permanently.
4. **As a user who already used a streak-freeze and breaks another streak within the cooldown window,** I see an explanation of why the freeze isn't available right now, rather than the app silently reverting to the old, unacknowledged reset behavior.
5. **As a user who has never held a streak,** I never see this screen, so it isn't shown in a context where it doesn't apply.

## Open Questions

*For Raj — feasibility, data, and edge cases (per raj.md: needs acceptance criteria, edge cases, and rollback clarity before saying yes):*

- **Minimum streak length to qualify for the offer** — not yet defined; needs to be configurable, not hardcoded.
- **Streak-freeze cooldown:** 30 days after use before it's available again — confirmed. The "freeze unavailable, here's why" screen for a repeat break inside that window does not exist yet and is new scope, not a variant of the current design.
- **Data model gap:** "best streak ever" is not currently a stored field in a codebase shaped like this (see codebase-summary.md) — needs a new field and a migration/backfill decision for existing users. This is very likely the first question Raj raises.
- **Measurement plan:** controlled test on users who break a streak, Day-7 retention within that cohort as the success metric, full funnel logging — confirmed, but holdback %, test duration, and minimum sample size are not yet defined.

*For Lena — evidence and experience quality (per lena.md: needs real-user evidence, not assumptions, and a defined empty state):*

- **What happens after the user completes the flow** (lands on "Done") is currently an assumption (home screen), not something drawn from user research — no interview subject stated a preference here.
- **The lesson-gate itself (earn the freeze vs. simply offering it) is an unvalidated hypothesis**, not something requested by any research subject — it directly contradicts Tom's stated experience, where the *absence* of a way back, not a lack of a gate, is what drove him to churn. Needs real-user validation before being treated as settled.
- **This screen is reactive only** — it does nothing for a user like Amara, who is anxious before ever breaking a streak. A proactive version is an explicit, separate follow-up, not part of this scope.
