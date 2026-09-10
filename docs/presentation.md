# Quarterly Review Deck: Streakly Comeback Experience

Narrative structure. Sources: [docs/decision-brief.md](decision-brief.md), [docs/recommendation-memo.md](recommendation-memo.md), [data/metric-findings.md](../data/metric-findings.md), [02-research/interview-synthesis.md](../02-research/interview-synthesis.md), [CLAUDE.md](../CLAUDE.md), [stakeholders/marcus.md](../stakeholders/marcus.md). No numbers or insights beyond what these files contain.

---

## Slide 1: The Problem

**1 number:** Day-7 retention dropped from **48% to 39%** following the v2 streak redesign. (decision-brief.md)

**1 insight:** Breaking a streak currently reads as final, not recoverable — a silent reset with no acknowledgment or way back is the clearest, most-repeated driver of this drop across every research source in hand. (decision-brief.md)

---

## Slide 2: Why Now

**What changed:** We moved from research to a real pilot — a personalized comeback experience was tested against a control group. (recommendation-memo.md)

**What we learned:**
- Strong signal in the pilot: +30 points Day-7 retention, +14 points Day-30, in the treatment group. (recommendation-memo.md / metric-findings.md)
- The engagement lift is sustained across multiple touchpoints, not a one-time novelty spike. (metric-findings.md)
- We also caught a real data-quality issue (a pre-existing imbalance between test groups) before it could distort a scale decision — evidence the result is being pressure-tested, not just celebrated. (recommendation-memo.md)

**Why now:** every week without action, new cohorts keep landing at the declining baseline instead of the lift we saw in the pilot. (recommendation-memo.md)

---

## Slide 3: The Proposal

**What it is:** A personalized comeback experience — acknowledging a user's prior progress and offering a real way back in — replacing the current silent reset. (decision-brief.md: "personalized comeback experience... progress acknowledgment + forgiveness mechanic")

**What it isn't:**
- Not a fix for notification tone or cadence — tracked as a separate, secondary workstream. (decision-brief.md)
- Not a decision to scale on the raw pilot number as-is — the recommendation is to correct for the data-quality issue first, then scale. (recommendation-memo.md)

---

## Slide 4: Evidence

**Data:**
- Day-7: 76% (treatment) vs. 46% (control), +30 points. Day-30: 36% vs. 22%, +14 points. (metric-findings.md)
- Engagement lift sustained across sends: open rate climbed 28% → 56% for treatment, while control stayed flat at 4-6%. (metric-findings.md)

**User voice, grounding the "why" behind the numbers:**
- Tom: *"There was no way to recover it, nothing. So I gave up."* / *"I switched to Duolingo... a streak freeze feels forgiving."* (interview-synthesis.md)
- Priya: *"The thing that made it stick was hitting a 30-day streak and the app actually celebrating it."* (interview-synthesis.md)

**Prototype:** A working, testable version of this experience exists and has been through iterative review — this isn't a concept on paper only.

---

## Slide 5: The Plan

**Honest state of the plan — this is a known gap, not a hidden one:** a full rollout timeline is not yet defined. (stakeholders/marcus.md: flagged open item)

**Milestones proposed:**
1. Correct the pilot analysis for the data-quality issue found (goal-setting imbalance). (recommendation-memo.md)
2. Decision checkpoint — confirm the corrected effect size before committing further.
3. Scaled rollout — timeline to be set as part of this review, not before it.

**Risks:**
- The raw pilot number may be inflated by the pre-existing imbalance — presenting it uncorrected risks committing to a figure that doesn't hold at scale. (recommendation-memo.md)
- Waiting costs real retention — every week of delay is another cohort at the declining baseline. (recommendation-memo.md)

---

## Slide 6: The Ask

Approval to move into a larger, corrected rollout of the comeback experience — and a decision from Marcus on timeline, so the corrected re-analysis and scale-up can be slotted into the sprint plan. (recommendation-memo.md: "Ask")
