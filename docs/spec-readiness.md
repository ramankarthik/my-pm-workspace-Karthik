# Spec Readiness: Streakly Comeback Screen

Reviewed against: [docs/decision-brief.md](decision-brief.md), [docs/pm-brief.md](pm-brief.md), [docs/hypothesis.md](hypothesis.md), [docs/triad-session.md](triad-session.md), [docs/codebase-summary.md](codebase-summary.md), [prototype/](../prototype/), via a role-play review as Raj (Eng Lead) using [stakeholders/raj.md](../stakeholders/raj.md).

## 1. Spec Readiness Summary

**What was solid:**
- The problem framing and research backing (decision brief, hypothesis, NPS/interview synthesis) — multi-source, well-corroborated, no complaints raised here.
- The prototype itself as a walkthrough of the intended experience — clear enough to review and react to.
- The core mechanic (best-streak acknowledgment, lesson-gated freeze) was understandable without much clarification needed.

**What needed work (resolved during this session):**
- **Edge cases were entirely undefined** before this conversation: minimum streak length to qualify for a freeze, repeat-break behavior within a cooldown window, and the zero-best-streak state. All three now have answers (see rewritten section below).
- **No measurement plan existed.** Nothing in the spec said whether this ships to everyone or a controlled cohort, what the specific success metric is, or what gets logged. This was the primary blocker — without it, there's no way to define "done" for QA or know if the feature worked post-launch.

**What still needs work (open, not blocking kickoff):**
- The exact minimum-streak-length number is still pending (agreed: build it as a configurable value, not hardcoded).
- A new screen — explaining to a user why their streak-freeze is unavailable during the 30-day cooldown — is **newly identified scope**, not in the current prototype. Needs a decision on whether it's in this sprint or a follow-up, and needs design input from Lena either way.
- Rough experiment parameters (holdback %, test duration, minimum sample size) aren't defined yet — needed before engineering can build the logging correctly, though not needed to start sprint planning.

## 2. Rewritten Sections

### Streak-Freeze Eligibility & Edge Cases *(new section — did not exist before)*

- **Minimum streak length:** A configurable threshold (not hardcoded) determines whether a broken streak qualifies for a Comeback screen / freeze offer at all. Exact value TBD.
- **Repeat breaks / cooldown:** Once a user completes the lesson and uses a streak-freeze, the offer is unavailable for **30 days** from that use.
  - On unfreeze, the user is told explicitly that the offer won't be available again for 30 days.
  - If the user breaks another streak within that 30-day window, they see a distinct screen explaining the freeze is currently unavailable and why — **this screen does not exist yet and is new scope**, not a variant of the current prototype.
- **Zero best-streak state:** If a user's best-streak-ever value is 0 (i.e., they've never completed a streak), the "best streak" card is omitted entirely from the screen.
- **Trigger condition:** The Comeback screen only fires for users who had an active streak and broke it — not simply "current streak is 0" (which would incorrectly include users who've never started one).

### Success Measurement *(new section — did not exist before)*

- **Rollout:** Controlled test — not a full rollout. Cohort: users who break a streak.
- **Success metric:** Day-7 retention specifically among users who broke a streak (not overall Day-7 retention).
- **Logging required:** Freeze offered, freeze used, lesson completed, screen dismissed ("Not now") — full funnel instrumentation, not just the end outcome.
- **Still open:** Holdback/control group size, test duration, and minimum sample size are not yet defined — needed before logging can be finalized, but not blocking sprint kickoff.

## 3. Async Slack Message to Confirm Scope Before Sprint Kickoff

> Hey Raj — recapping where we landed so we're aligned before kickoff:
>
> **Resolved:**
> - Min streak length to qualify for a freeze: configurable, exact number coming from me soon.
> - Cooldown: 30 days after a freeze is used before it's available again. On unfreeze, we tell the user that upfront.
> - If they break again inside the 30-day window: they see an explanation screen instead of the freeze offer. **This is a new screen, not in the current prototype** — need your read on whether it's in this sprint or a fast-follow, and I'll loop Lena in either way.
> - Zero best-streak users: we just don't show that card, no other special-casing needed.
> - This is a controlled test, not a full rollout — cohort is users who break a streak, success metric is Day-7 retention within that cohort specifically, and we log the full funnel (offered / used / lesson completed / dismissed).
>
> **Still need from me before you can finalize logging:** holdback %, test duration, minimum sample size — will bring rough numbers by [date].
>
> Let me know if this matches what you need to size the ticket, or if anything above needs more detail before sprint planning.
