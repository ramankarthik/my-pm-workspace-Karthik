# Experiment Design: Comeback Experience Full Test

Pressure-testing the week-5 pilot result before recommending scale. Builds on [data/metric-findings.md](metric-findings.md), [data/metric-diagnosis.md](metric-diagnosis.md), and [docs/recommendation-memo.md](../docs/recommendation-memo.md).

## 1. Is the Pilot Result Statistically Significant?

**What significance means for a go/no-go decision:** it tells you whether an observed gap is unlikely to be random luck — not whether the gap is big, important, or fully understood.

**Pilot data:** 76% (treatment, 38/50) vs. 46% (control, 23/50), Day-7 retention.

| Statistic | Value |
|---|---|
| z-score | 3.08 |
| p-value | 0.0021 |
| 95% CI on the gap | +11.8 to +48.2 points |

**Verdict: statistically significant** (p < 0.05, comfortably). But the confidence interval is wide — the true effect could be as small as 12 points or as large as 48 points. **Significant ≠ precisely sized.** With n=50/variant, you can trust that *something real* happened; you cannot yet trust the specific magnitude (76% vs. 46%) as the number to commit to publicly.

## 2. Minimum Detectable Effect (MDE)

**What it means:** the smallest effect size worth caring about, fixed *before* running the test — set in advance so the target isn't unconsciously reverse-engineered from results you've already seen.

**MDE for this test: 5 percentage points** (i.e., detecting a true lift as small as 46% → 51%).

## 3. Required Sample Size

**What power means:** the probability of detecting a real effect if one truly exists; too low, and a genuinely working treatment can produce a "no significant result" test purely from being underpowered — a false negative that kills a good idea for the wrong reason.

**Inputs:** baseline 46%, MDE 5pts (→51%), significance 95%, power 80%.

**Required sample size: ≈1,565 users per variant (≈3,130 total).**

## 4. Test Duration

**Assumption (stated explicitly, not confirmed):** the 85,000 WAU figure is treated as the pool available for enrollment each week. Flagging this because at that scale, the ≈3,130 required total is reached in well under a week — meaning **sample size is not the constraint that determines test length. Measurement time is.**

- **Day-7 as the primary decision metric:** enroll for up to ~7 weeks, reserve the final week to observe Day-7 for the last-enrolled cohort. **Fits within the 8-week cap.**
- **Day-30 as a full-coverage secondary metric:** would require enrollment to stop by roughly week 3-4 so every cohort matures to day 30 within the 8-week window — otherwise Day-30 is a partial/rolling read, not a clean gate, for later-enrolled users.
- **Sensitivity flag:** this holds only if at least ~3.7% of WAU are genuinely eligible for this flow weekly (i.e., break a streak). If the real eligibility rate is lower, sample size — not measurement time — becomes the binding constraint. This rate isn't confirmed anywhere in the data currently in hand and should be checked before finalizing the plan.

**Answer: yes, the full test fits within 8 weeks, gated by Day-7 measurement time rather than enrollment volume — pending confirmation of the real weekly-eligible rate.**

## 5. The Decision

**Recommendation: run the full test before scaling. Do not commit to a number off the pilot alone.**

- **Risk of scaling now:** the pilot's true effect could be anywhere from 12 to 48 points (wide CI) and carries a known, uncorrected confound (the pre-existing goal-setting imbalance between arms) — risk of committing roadmap and reporting a number the full rollout doesn't hold up.
- **Risk of waiting for the full test:** 8 weeks is a real opportunity cost — every week of delay keeps new cohorts landing at the declining ~44-48% baseline instead of a potentially much better number, against a live Q3 timeline pressure.

## 6. Leading Indicators to Monitor Weekly

| Metric | What would make this nervous | Why |
|---|---|---|
| Open rate by variant, weekly | Treatment doesn't reach the pilot's ~28-56% range in the first 2 weeks, or trends back toward control | Signals the pilot effect isn't replicating at scale |
| Baseline covariate balance (esp. goal-setting rate) between arms | Treatment and control diverge on goal-setting or session count *before* any treatment exposure, echoing the pilot's imbalance | Would mean randomization is broken again, undermining causal validity from week one |
| Day-1 retention gap by variant | Gap is small, flat, or negative | Earliest available signal, days ahead of Day-7 — a weak Day-1 read is an early warning the Day-7 result won't hold |

## Summary

| Question | Answer |
|---|---|
| Is the pilot significant? | Yes (p=0.0021), but with a wide 12-48pt confidence interval |
| MDE | 5 points |
| Required sample size | ≈1,565 per variant (≈3,130 total) |
| Fits in 8 weeks? | Yes — bound by Day-7 measurement time, not sample size (pending eligibility-rate confirmation) |
| Scale now or wait? | Wait for the full test — pilot CI too wide and confounded to commit to a specific number |
| Watch weekly | Open rate by variant, baseline covariate balance, Day-1 retention gap |
