# Design Review: Streakly Comeback Screen

Prepared for a review with Lena. Sources: [prototype/index.html](../prototype/index.html), [02-research/interview-synthesis.md](../02-research/interview-synthesis.md), [docs/spec-readiness.md](spec-readiness.md), [stakeholders/lena.md](../stakeholders/lena.md).

## User Needs: What's Addressed, What Isn't

**Addressed well:**

- **Acknowledgment instead of a cold reset.** Tom: *"came back to a big fat zero... There was no way to recover it, nothing. So I gave up."* The "12-day — here's where you left off" stat directly answers this.
- **Celebrating progress as a retention driver.** Priya: *"The thing that made it stick was hitting a 30-day streak and the app actually celebrating it."* The best-streak-ever stat (18 days) mirrors this pattern.
- **A forgiving way back in.** Tom: *"a streak freeze feels forgiving."* The one-tap freeze is a direct answer to this stated want.

**Not yet addressed:**

- **Anticipatory anxiety before a break.** Amara: *"I'm already stressed about the streak, I keep thinking, what happens if I miss a day?"* This screen is entirely reactive — it does nothing for a user in Amara's state today.
- **The harsh notification moment.** Tom: *"The app sent me this 'you lost your streak' notification that just made me feel bad."* Notification copy/timing is explicitly out of scope for this feature (tracked as a separate workstream).
- **Streak pressure turning content into a chore.** Amara: *"the pressure is starting to feel like a chore instead of a game."* Nothing in this flow reduces pressure — it only responds after a break has already happened.

## Design Review Outcomes

### 1. What happens after "Done"?

**Decision:** User returns to their home screen to continue skill learning.
**Flagged as an assumption, not evidence:** none of the three interview subjects said anything about what should happen next — this is a product decision made without user research backing it specifically. Worth naming explicitly rather than presenting as research-driven.
**Open consideration:** dropping the user on a generic home screen may waste the momentum of having just completed a lesson — routing them into today's actual lesson instead is worth considering, but is a product call, not yet decided.

### 2. Why is the streak-freeze gated behind a lesson?

**Status: unvalidated hypothesis, not evidence-backed.** No interview subject asked for a lesson requirement — Tom asked for a streak freeze, full stop. The working hypothesis is that requiring the lesson makes the freeze feel *earned* rather than *given away*, and that users will value it more as a result. This hypothesis directly runs counter to Tom's stated experience (the *absence* of a way back is what drove him to churn) and should be treated as a real bet requiring validation, not a settled design decision. **Needs to be explicitly flagged as unvalidated in any doc that goes further than this review.**

### 3. Who is this screen actually for?

**Answer: only users who have already broken a streak.** It does nothing for a user like Amara — anxious, still mid-streak, never having broken one. This is a reactive experience by design, not a proactive one. **Proactive softening / expectation-setting for at-risk-but-not-yet-broken users (Amara's segment) is an explicit, named follow-up — not silently out of scope.**

## Single Highest-Impact Change for Week-1 Retention

**Extend the concept proactively to at-risk users before they break a streak, not only after.** Every open question in this review points the same direction: the current screen is a well-built fix for a *symptom* (post-break churn), but Amara's interview is the only evidence in hand about *pre-break* week-1 anxiety, and nothing here touches it. Since week-1 retention is explicitly the metric in question, and a meaningful share of week-1 churn may happen before anyone ever breaks a streak, an early, proactive version of this safety net (e.g., surfacing "you're covered if you ever slip" at day 3-4) is the highest-leverage next move — not a refinement of the reactive screen itself. This should be validated as its own hypothesis before being built, not assumed from Amara's single interview alone.

## Product Decision vs. Lena's Decision

| Decision | Owner |
|---|---|
| Whether the lesson-gate stays, is simplified, or is removed pending validation | **Product** — this is a scope/hypothesis call, tested with real users, not a visual design question. |
| Where the user lands after "Done" (home screen vs. today's lesson) | **Product**, with Lena's input on how to make either destination feel intentional rather than generic. |
| Whether to build the proactive/pre-break experience as a follow-up | **Product** — prioritization and roadmap sequencing. |
| Visual/interaction design of the freeze-unavailable (cooldown) screen, and all copy/tone execution | **Lena** — once product confirms it's in scope (per [docs/spec-readiness.md](spec-readiness.md), this screen doesn't exist yet). |
| Whether the earn-gated mechanic *feels* forgiving vs. punishing in execution (tone, motion, copy) | **Lena** — even if product keeps the gate, how it's designed determines whether it reads as a guilt trip. |
