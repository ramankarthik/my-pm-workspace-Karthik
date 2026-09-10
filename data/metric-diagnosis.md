# Metric Diagnosis: Day-7 Retention

Builds on [data/metric-findings.md](metric-findings.md). All numbers below are freshly queried from the same dataset (downloaded and run through SQLite), not reused estimates.

**Standing caveat, carried forward:** this dataset has no literal streak field and no field literally labeled "Comeback screen" — `nudge_weekly_summary_sends` (`summary_v1` vs `control`) is being used as the closest available analog, per the mapping discussion earlier in this conversation. Everything below that references "the treatment" or "the Comeback screen" is really describing this weekly-summary-send experiment.

---

## 1. Metric Tree: What Actually Moves Day-7 Retention

```
Day-7 Retention
│
├── Streak-Start Rate (% of new users who ever begin a streak/meaningful habit loop)
│     └── NOT MEASURABLE in this dataset — no streak-start field exists.
│
├── Streak-Break Rate in Week 1 (% of streak-starters who break it before day 7)
│     └── NOT MEASURABLE directly — no streak field.
│         Weak proxy available: week-1 session frequency (0-1 vs 2+ active days) —
│         see metric-findings.md Q2. Proxy showed only a 6-point retention gap,
│         too weak to treat as a real stand-in for an actual streak-break signal.
│
├── Comeback Rate (once broken, % who see + engage with a recovery experience)
│     └── NOT MEASURABLE as literally defined — no Comeback-screen-specific field.
│         Closest analog: nudge_weekly_summary_sends opened/acted_on rates
│         (week 5 only, summary_v1 vs control) — see Sections 3-4 below.
│
├── Notification Opt-In Rate (gates whether any nudge/comeback message can reach the user)
│     └── NOT DIRECTLY MEASURABLE — no opt-in boolean field exists.
│         Indirect signal: a 'notifications' screen exists in nudge_sessions,
│         but visiting it isn't the same as an opt-in state, and this wasn't
│         queried as reliable — flagging as a real data gap, not computing a
│         number I can't stand behind.
│
└── Baseline Engagement / Habit-Formation Signal (measurable proxy actually found in this data)
      ├── Sessions per user — MEASURABLE, and the strongest cohort-level correlate
      │     of the weeks 1-4 decline found (Section 2).
      └── Goal-Set Rate — MEASURABLE, and the strongest individual-level predictor
            of Day-7 retention found in the entire dataset (Section 2).
```

**Honest summary of this tree:** the levers the business actually cares about (streak-start, streak-break, comeback rate, notification opt-in) are the right decomposition conceptually, but **this dataset cannot populate three of the four nodes.** What it *can* measure — session volume and goal-setting — turned out to be the most useful diagnostic signals available, even though they're once removed from the literal streak framing. Any real diagnosis work going forward should prioritize instrumenting the actual streak/comeback/opt-in fields in production, not just working around their absence the way this analysis had to.

---

## 2. What Caused the Decline in Weeks 1 Through 4 — Specifically

Ruled out first, so the remaining explanation isn't diluted by things that *didn't* move:

- **Acquisition channel mix is roughly stable across cohorts 1-4** (organic ~42-56%, paid ~31-42%, referral ~12-22% each week — no dramatic compositional shift). This is not a "we started buying worse traffic" story.
- **Platform mix is similarly stable** (android/iOS/web proportions don't shift meaningfully week to week).
- **Goal-setting rate does not monotonically track the decline** — it's 32% (wk1) → 29% (wk2) → 44% (wk3) → 27% (wk4), which doesn't line up with the smooth 60%→53%→48%→44% retention slide (week 3 has the *highest* goal-setting rate but *below-week-1* retention). So goal-setting, despite being a strong individual-level predictor (below), isn't *the* explanation for the cross-cohort trend by itself.
- **Within a cohort, week-1 session frequency is a weak predictor of Day-7 outcome** (50%, 51%, 49%, 68% retention across 0/1/2/3 active days — noisy, not a clean gradient). So "this specific user was less active in week 1" doesn't reliably predict "this specific user churned."

**What does line up, cleanly and specifically:**

**Total session volume per user declines almost in lockstep with retention, cohort over cohort:**

| Cohort Week | Sessions per User | Day-7 Retention |
|---|---|---|
| 1 | 5.74 | 60.0% |
| 2 | 5.08 | 53.0% |
| 3 | 4.48 | 48.0% |
| 4 | 3.69 | 44.0% |

Both series decline in the same proportion, cohort over cohort — roughly a 36% drop in sessions/user from week 1 to week 4, against a roughly 27% relative drop in Day-7 retention over the same span. This is a **cohort-level co-movement**, not a proven individual-level causal chain (the weak within-cohort correlation above means I can't say "give this user one more session and they'll retain") — but it's the single most specific, consistently-directional pattern in the dataset, and a much cleaner story than goal-setting or channel mix.

**What this means, specifically, not generically:** something is causing each successive cohort of new users to use the product *less often overall* from the start — not just in week 1, but across their whole observed lifecycle — and that declining engagement volume is the variable most tightly correlated with the retention slide. This dataset can't say *why* engagement volume itself is eroding cohort over cohort (product friction, a marketing message that's drifted off-target, seasonal fatigue, a change nobody logged) — that requires investigation outside this dataset (e.g., checking if anything shipped or changed in marketing/onboarding across this window). What it can say is that "engagement is declining" isn't a vague restatement of the retention problem — it's a specific, independently-measured, tightly-correlated leading indicator of it.

---

## 3. What the Week 5 Treatment vs. Control Split Tells Us

Recapping the headline result: `summary_v1` Day-7 retention was 76.0% vs. control's 46.0% (+30 points), Day-30 was 36.0% vs. 22.0% (+14 points).

**What plausibly drove it, mechanistically:**

`acted_on` rate (not just opened) by week, treatment vs. control:

| Week | Control | summary_v1 |
|---|---|---|
| 1 | 0.0% | 12.0% |
| 2 | 4.0% | 22.0% |
| 3 | 2.0% | 22.0% |
| 4 | 2.0% | 14.0% |

Control essentially never acted on anything across all 4 weeks (0-4%). The treatment group didn't just open more (already shown in `metric-findings.md`) — they **took action** at meaningfully higher rates, consistently, across all 4 sends. This is the most plausible mechanism: the treatment didn't just get looked at more, it prompted actual behavior more, repeatedly.

**A critical caveat that materially affects how much of this to trust as causal:**

Goal-setting rate — the strongest individual-level retention predictor found anywhere in this dataset (66.7% vs. 43.7%, all cohorts) — was **not balanced between the two week-5 groups**: 44% of `summary_v1` users had set a goal, vs. only 22% of control. Checking the timing: goal-setting happens on average ~2.5 days after signup, while the first weekly-summary send goes out around day 7 — **goal-setting precedes the treatment for both groups**, meaning the treatment itself cannot have caused this imbalance. This looks like a pre-existing imbalance between the two randomized groups, not a treatment effect.

**What this means for the scale decision:** the treatment group was already meaningfully more likely to be a "sets a goal" type of user before a single summary email was ever sent. Some portion of the +30-point Day-7 gap is very likely attributable to this imbalance, not to the summary emails/Comeback experience itself. This doesn't mean the treatment didn't work — the `acted_on` funnel gap is real and independent of goal-setting — but the *raw* 76% vs. 46% gap should not be presented to Marcus as a clean, fully-isolated causal effect without at least a stratified re-check (e.g., comparing retention within "set a goal" and "didn't set a goal" subgroups separately, across variant) before treating the size of that number as final.

---

## 4. Four Ranked Hypotheses: Why Some Treatment Users Still Churned

12 of the 50 `summary_v1` users churned by Day 7 despite the treatment. Baseline checks first: churned-treatment users and retained-treatment users had **nearly identical** goal-setting rates (41.7% vs. 44.7%) and overall session counts (5.42 vs. 5.24 avg) — meaning whatever separates them, it isn't a pre-existing engagement or goal-setting gap. That rules out the most obvious explanation and points somewhere more specific.

### H1 (Rank 1): Progressive disengagement across the 4 sends predicts churn, even with a strong early start

**Prediction:** Treatment users who still churn show an open-rate pattern that peaks early (by week 2) and then declines through weeks 3-4, while users who retain show open rates that climb steadily across all 4 sends.

**Data support (real, computed from the funnel):**

| Week | Churned (day_7=0, n=12) Open Rate | Retained (day_7=1, n=38) Open Rate |
|---|---|---|
| 1 | 33.3% | 26.3% |
| 2 | 66.7% | 47.4% |
| 3 | 41.7% | 55.3% |
| 4 | 33.3% | 63.2% |

The churned group actually opens *more* than the retained group in weeks 1-2, then reverses hard — while the retained group's open rate climbs the entire time. This is a distinct, specific, and consistent shape difference, not a vague "they engaged less" story.

**Likelihood:** Highest of the four — this is the only hypothesis with a clean, consistent directional pattern across multiple weeks in the actual funnel data.
**Confidence: 7/10** — the shape is clear and consistent (3 of 4 weeks move the "expected" way), but n=12 churned users is small, so this could partly be noise rather than a robust behavioral signal.
**Would confirm it:** A larger sample (more weeks 5-style cohorts) showing the same peak-then-decay shape specifically among churners, holding at a larger n.
**Would rule it out:** If a larger sample showed churned and retained users converging to similar week-over-week open-rate trajectories — i.e., this 12-person pattern was just noise.

### H2 (Rank 2): Opening isn't enough — action-taking on later sends specifically distinguishes outcomes

**Prediction:** Users who open later sends (weeks 3-4) but don't act on them are more likely to churn than users who both open *and* act on later sends.

**Data support:** Churned-treatment users averaged 0.5 `acted_on` out of 4 sends; retained-treatment users averaged 0.76 — a real gap, but smaller and less crisp than the open-rate shape in H1.

**Likelihood:** Second — directionally supportive, real gap, but less distinctive a pattern than H1.
**Confidence: 5/10** — the direction is right but the gap is modest and could partly just reflect the same underlying disengagement H1 already captures, rather than being an independent factor.
**Would confirm it:** Users who open weeks 3-4 sends but don't act showing meaningfully worse retention than users who open *and* act on those same sends, isolated from H1's pattern.
**Would rule it out:** If action-taking rate on later sends turned out to be statistically indistinguishable between churned and retained once open-rate (H1) is controlled for — i.e., action is just a byproduct of opening, not an independent signal.

### H3 (Rank 3): Baseline goal-setting or overall engagement predisposes treatment users to still churn

**Prediction:** Treatment users without a set goal, or with lower overall session activity, are more likely to churn despite the treatment.

**Data support:** This is **already substantially contradicted** by the data gathered for this diagnosis — goal-set rate (41.7% vs. 44.7%) and average session count (5.42 vs. 5.24) are nearly identical between churned and retained treatment users. Including this because it's the hypothesis someone would reasonably raise first, and it's valuable to show it doesn't hold up, not because it's a live lead.

**Likelihood:** Low — actively undercut by the baseline comparison already run.
**Confidence: 2/10** — the data checked so far points the other way; would need a much larger sample to overturn that.
**Would confirm it:** A larger sample showing a real gap in goal-setting or session count between churned and retained treatment users that this small n=50 group happened to obscure.
**Would rule it out:** Already effectively ruled out at this sample size — a repeat check at larger scale showing the same near-identical rates would close this out for good.

### H4 (Rank 4): Churn despite treatment is driven by factors outside anything this dataset captures

**Prediction:** The remaining churned-despite-treatment users are explained by external factors (life circumstances, cost sensitivity, a competing app) that leave no trace in session, nudge, or send data.

**Data support:** None directly — this is the "unexplained residual" hypothesis, included because H1-H3 together still don't fully account for all 12 churned users, and it would be dishonest to imply the dataset explains 100% of the outcome.

**Likelihood:** Lowest to act on, but not to believe — it's likely true for *some* fraction of the 12, just not testable with what's here.
**Confidence: 3/10** — not because it's unlikely to be true, but because it's close to unfalsifiable with this data; low confidence reflects how little this dataset can say about it, not a belief that it's wrong.
**Would confirm it:** Direct user research (exit surveys, interviews) with the specific churned-despite-treatment cohort — something this quantitative dataset cannot produce on its own.
**Would rule it out:** If H1 and H2, once tested at scale, together accounted for nearly all churned-despite-treatment users, leaving little unexplained residual.

---

## 5. Which Hypothesis to Test Next Sprint

**H1 — progressive disengagement across sends — is the one to act on first.**

Reasons:
- It's the most data-supported of the four (clean, consistent pattern across weeks, not a single noisy data point).
- It's directly actionable at product-design scale: if churn concentrates among users whose engagement peaks early and fades, that suggests a concrete intervention — e.g., a targeted re-engagement touch specifically triggered by a week-2-to-week-3 open-rate drop, rather than a uniform weekly send treated identically for everyone.
- It's testable within a normal sprint scope: instrument a trigger on the open-rate drop-off pattern itself and run a small experiment on that specific at-risk slice, rather than needing new qualitative research (H4) or a much larger sample before any signal emerges (H3).

**Important parallel work, not a substitute:** H3's underlying issue — the goal-setting imbalance flagged in Section 3 — isn't a product hypothesis to A/B test, it's a **data/experiment-design problem** that should be fixed before the next retention read is presented as causal. That's a rerun-the-analysis task for whoever owns the experiment, not a sprint feature bet, but it shouldn't be dropped just because it's not "the hypothesis to test" in the product sense.
