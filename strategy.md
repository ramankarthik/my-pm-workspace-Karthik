# strategy.md

## Hypothesis: Recovering the 9-Point Day-7 Retention Drop

Users go passive after breaking a streak because the break feels like failure and there's no graceful way back in — the app resets the counter to zero with no acknowledgment of prior progress, and the "you lost your streak" notification lands right when users are most likely to quit.

We believe a comeback experience that pulls users back with something specific to their own progress — not a generic "keep going!" — will reduce the churn spike currently seen after a broken streak.

**Corroborated by NPS analysis (10 verbatims, see [02-research/nps-analysis.md](02-research/nps-analysis.md)):** two of the top themes directly support this hypothesis — (1) breaking a streak leads to disengagement/churn because there's no recovery mechanic (streak freeze), and (2) the app doesn't acknowledge user state (same static home screen whether on day 2 or returning after weeks away), which reads as punishing rather than supportive. These are now the two leading, multi-source-backed drivers.

**Not yet resolved:** whether the primary driver is the reset mechanic itself or the lack of acknowledgment — both are strongly supported, but their relative weight isn't yet clear. Notification tone/fatigue is also corroborated in the NPS data, but is being tracked as a secondary, related workstream rather than folded into the core hypothesis (see NPS analysis for Marcus).

**Signal to watch (single-source, not yet corroborated):** one week-1 user interview (Amara L., 4 days in) showed anticipatory streak anxiety before ever breaking a streak — "what happens if I miss a day?" turning the experience into "a chore instead of a game." If this pattern shows up in more feedback, the driver of week-1 churn may not be limited to the post-break moment — the all-or-nothing streak mechanic itself may create pressure from day one. Treating this as a possible outlier for now; worth re-testing as more interview/feedback data comes in.

**Competitive white space (see [02-research/competitive-matrix.md](02-research/competitive-matrix.md)):** across Duolingo, Babbel, Elevate, and Headway, no competitor pairs a forgiveness mechanic with a personalized, acknowledgment-based comeback experience — Duolingo's closest analog ("streak repair") is a paid, transactional purchase, not a personalized re-entry. This is the clearest opening for the Comeback screen concept. Also notable: every competitor's forgiveness mechanic is reactive (offered only after a break) or, in Babbel's case, avoided entirely by not gamifying loss at all — none proactively reduce streak pressure *before* a break happens. This reinforces the anticipatory-anxiety signal above as a possible differentiator worth validating, not dismissing.
