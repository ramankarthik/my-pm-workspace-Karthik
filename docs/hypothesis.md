# Learning Synthesis & Hypothesis

Sources: [change_log.md](../change_log.md), [docs/decision-brief.md](decision-brief.md).

## What We Know

- Day-7 retention dropped from 48% to 39% following the v2 streak redesign, concentrated in users who break their streak in week 1 and don't return.
- Breaking a streak currently reads as final — silent reset, no acknowledgment, no way back. This is the top NPS theme (3 of 10 verbatims) and the clearest interview evidence (Tom R.'s churn story).
- Users explicitly want the app to act like a coach, not a scorekeeper — tied for the top NPS theme, echoed by Priya's interview (celebration of progress is what made her habit stick).
- No competitor (Duolingo, Babbel, Elevate, Headway) combines a forgiveness mechanic with a personalized comeback — this is genuine, confirmed competitive white space, not a guess.
- Notification fatigue is a real, secondary complaint (2 of 10 NPS verbatims) — compounding but not the primary driver of the post-break churn.
- In the one real usability round run so far (5 participants), nobody objected to the lesson-gated streak-freeze mechanic itself — the core comprehension and motivation logic of the Comeback screen landed as intended.
- A "Not now" navigation bug was found and fixed in that same round — pressing it incorrectly routed into the lesson instead of exiting.

## What We Assume

- That the Comeback screen concept — acknowledgment + earn-gated forgiveness — will actually move Day-7 retention behaviorally, not just test well in a walkthrough. No experiment has been run yet; all evidence so far is qualitative.
- That gating the streak-freeze behind a 60-second lesson won't create new drop-off at scale. The real usability sample (n=5) didn't flag this, but a separate round of *simulated* persona role-play (not real users) surfaced a churned-user-type persona reading the gate as a possible paywall — flagged as a lower-confidence, directional signal worth re-testing with real users, not yet confirmed either way.
- That the "Free, always — no catch, no subscription" reassurance copy (added in response to that role-play signal) actually resolves the trust concern it was written for — untested with real users.
- That fixing the reactive, post-break moment is sufficient on its own, without also addressing anticipatory pressure before a break happens.

## What We Still Don't Know

- Whether the primary driver of churn is the reset mechanic itself or the lack of acknowledgment — both are strongly supported by research, but their relative weight is unresolved (see [strategy.md](../strategy.md)).
- Whether the anticipatory streak-anxiety signal (Amara L., single interview source) generalizes across more users, or is an outlier specific to her.
- The actual entry point into the Comeback screen — how users arrive at it (notification vs. home-screen state) hasn't been designed or tested.
- Whether the earn-gated lesson requirement holds up with a larger, more skeptical sample of real churned users, given the role-play signal above.
- The real, quantitative impact of this feature on Day-7 retention — that's what the next experiment needs to answer.

## Hypothesis

We believe that **a personalized Comeback screen — acknowledging a user's prior progress and offering a free, one-tap streak-freeze unlocked by a 60-second comeback lesson** — will deliver **higher return and continued engagement from users who break their streak** for Streakly users in their first 7 days, as measured by **Day-7 retention rate**.
