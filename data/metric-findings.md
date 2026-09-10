# Metric Findings: Nudge Dataset

Source: [Nudge Dataset (Google Sheet)](https://docs.google.com/spreadsheets/d/1jMZXItXhbYxdBkzM74z2BXbCHHbnvqh4Eyclmmhdiww/edit), downloaded as XLSX and loaded into SQLite to run real SQL against it (not estimated by eye).

## Important Caveat Before the Findings

The five tables match the schema given exactly (`nudge_users`, `nudge_sessions`, `nudge_retention`, `nudge_nudges`, `nudge_weekly_summary_sends`, with the described columns and the week-5-only `variant` split). **However, the actual data in this sheet is not Streakly-specific.** The screens logged in `nudge_sessions` are `home`, `notifications`, `savings_goal`, `spending_breakdown`, `transaction_detail`, `weekly_summary` — this looks like a personal finance/budgeting app dataset, not a habit-streak app. **There is no `streak` field anywhere in any of the five tables.**

This matters directly for Question 2 below — it cannot be answered as asked, because the data needed to answer it doesn't exist in this dataset. I'm flagging this rather than inventing a stand-in definition of "broke their streak," since a fabricated proxy would produce a number that looks authoritative but isn't measuring what it claims to. Questions 1, 3, and 4 are answered directly from real fields with no interpretation required, and I'm treating `nudge_weekly_summary_sends` (the only table with a treatment/control split across four numbered sends) as the stand-in for "Comeback screen sends" per how the questions frame it — flagging that mapping explicitly rather than presenting it as a confirmed fact.

---

## 1. Day-7 Retention by Cohort Week

```sql
SELECT cohort_week,
       COUNT(*) AS n_users,
       SUM(day_7) AS retained_day7,
       ROUND(100.0 * SUM(day_7) / COUNT(*), 1) AS day7_retention_pct
FROM nudge_retention
GROUP BY cohort_week
ORDER BY cohort_week;
```

**Plain English:** For each cohort week, count how many users signed up, how many were still active on day 7, and turn that into a percentage.

**Result:**

| Cohort Week | Users | Retained (Day 7) | Day-7 Retention % |
|---|---|---|---|
| 1 | 100 | 60 | 60.0% |
| 2 | 100 | 53 | 53.0% |
| 3 | 100 | 48 | 48.0% |
| 4 | 100 | 44 | 44.0% |
| 5 | 100 | 61 | 61.0% |

**What the decline looks like:** A steady, consistent slide from week 1 to week 4 — 60% → 53% → 48% → 44%, roughly 4-6 points lost each week. Week 5 breaks that trend and jumps back up to 61%, but week 5 is the only cohort that includes the experiment (half control, half `summary_v1` treatment) — that jump isn't organic, it's the treatment group pulling the average up. See Question 3 for the split that explains it.

**What this means for the scale decision:** The weeks-1-4 decline is real, consistent, and not attributable to noise — it's the retention pattern the Comeback screen is meant to interrupt. Week 5's rebound isn't evidence the problem fixed itself; it's already showing the effect of the intervention being tested.

---

## 2. Do Users Who Break Their Streak in Week 1 Retain Worse?

**No literal streak field exists**, as noted above. Per your read that this is a habit-forming spend tracker (streak = visiting/doing something meaningful daily), I tested that directly against `nudge_sessions` before building a proxy on top of it — and the actual usage pattern doesn't support a literal daily-streak definition:

```sql
-- Distribution of distinct active days per user within their first 7 days
WITH week1_activity AS (
  SELECT u.user_id,
         COUNT(DISTINCT CASE WHEN julianday(s.session_date) - julianday(u.signup_date) BETWEEN 0 AND 6
               THEN date(s.session_date) END) AS days_active_week1
  FROM nudge_users u
  LEFT JOIN nudge_sessions s ON u.user_id = s.user_id
  GROUP BY u.user_id
)
SELECT days_active_week1, COUNT(*) AS n_users FROM week1_activity GROUP BY days_active_week1 ORDER BY 1;
```

| Distinct Active Days in Week 1 | Users |
|---|---|
| 0 | 148 |
| 1 | 208 |
| 2 | 117 |
| 3 | 26 |
| 4 | 1 |

**No user in this dataset has 5+ active days in their first week** — the most common pattern is a single active day, and nobody shows daily, consecutive usage. A "broke their daily streak" definition would classify almost everyone as broken by day 2, which produces a meaningless, near-zero-variance comparison. So instead of a true consecutive-day streak, I tested the closest honest proxy the data actually supports: **repeat engagement (2+ distinct active days in week 1) vs. single-touch-or-none (0-1 days)**.

```sql
WITH week1_activity AS (
  SELECT u.user_id,
         COUNT(DISTINCT CASE WHEN julianday(s.session_date) - julianday(u.signup_date) BETWEEN 0 AND 6
               THEN date(s.session_date) END) AS days_active_week1
  FROM nudge_users u LEFT JOIN nudge_sessions s ON u.user_id = s.user_id
  GROUP BY u.user_id
),
bucketed AS (
  SELECT user_id,
         CASE WHEN days_active_week1 >= 2 THEN '2+ days (repeat engagement)'
              ELSE '0-1 days (single touch or none)' END AS engagement_bucket
  FROM week1_activity
)
SELECT b.engagement_bucket, COUNT(*) AS n_users, SUM(r.day_7) AS retained_day7,
       ROUND(100.0 * SUM(r.day_7) / COUNT(*), 1) AS day7_retention_pct
FROM bucketed b JOIN nudge_retention r ON b.user_id = r.user_id
GROUP BY b.engagement_bucket;
```

**Result:**

| Week-1 Engagement | Users | Retained (Day 7) | Day-7 Retention % |
|---|---|---|---|
| 0-1 days (single touch or none) | 356 | 183 | 51.4% |
| 2+ days (repeat engagement) | 144 | 83 | 57.6% |

**What this means for the scale decision:** There is a gap in the expected direction — repeat-engaged users retain better — but at **6.2 points, it's much weaker than the Q1/Q3/Q4 signals**, and this is a proxy for engagement frequency, not an actual measure of "breaking a streak" (there's no concept of a streak being intact-then-broken here, only how many days someone happened to show up). I'd treat this as weak, supportive-but-not-conclusive evidence — worth mentioning, but not something to cite with the same confidence as the Q3 experiment result. The honest gap remains: this dataset can approximate "engagement frequency correlates with retention" (a fairly generic, expected finding for almost any app), but it cannot confirm the more specific Streakly claim that *breaking an active streak* — losing something you'd already built — is what drives the outsized churn described in the interviews. That claim still rests on the qualitative research only.

---

## 3. Week 5 Only: Day-7 and Day-30 Retention, Treatment vs. Control

```sql
SELECT u.variant,
       COUNT(*) AS n_users,
       SUM(r.day_7) AS day7_retained,
       ROUND(100.0 * SUM(r.day_7) / COUNT(*), 1) AS day7_pct,
       SUM(r.day_30) AS day30_retained,
       ROUND(100.0 * SUM(r.day_30) / COUNT(*), 1) AS day30_pct
FROM nudge_users u
JOIN nudge_retention r ON u.user_id = r.user_id
WHERE u.cohort_week = 5
GROUP BY u.variant;
```

**Plain English:** Join users to their retention outcomes, restrict to cohort week 5 (the only week with a real experiment), and compare day-7 and day-30 retention between the `control` and `summary_v1` groups.

**Result:**

| Variant | Users | Day-7 Retained | Day-7 % | Day-30 Retained | Day-30 % |
|---|---|---|---|---|---|
| control | 50 | 23 | 46.0% | 11 | 22.0% |
| summary_v1 | 50 | 38 | 76.0% | 18 | 36.0% |

**What this means for the scale decision:** This is a large, clean gap — +30 points on Day-7 (46% → 76%) and +14 points on Day-30 (22% → 36%), on a real control/treatment split, not just a before/after comparison. This is the strongest single piece of evidence in this dataset for scaling. Caveat: n=50 per group is a small sample for a launch-scale decision — worth confirming with whoever ran the experiment what significance testing (if any) was applied before treating this as conclusive, rather than reading the raw percentage gap alone as proof.

---

## 4. Comeback/Summary Screen Open Rate Across the 4 Sends, Treatment vs. Control

```sql
SELECT week_number,
       variant,
       COUNT(*) AS n_sends,
       SUM(opened) AS n_opened,
       ROUND(100.0 * SUM(opened) / COUNT(*), 1) AS open_rate_pct
FROM nudge_weekly_summary_sends
GROUP BY week_number, variant
ORDER BY week_number, variant;
```

**Plain English:** For each of the 4 weekly sends, count how many were sent and how many were opened, split by control vs. treatment, and turn that into an open rate.

**Result:**

| Week | Variant | Sends | Opened | Open Rate |
|---|---|---|---|---|
| 1 | control | 50 | 2 | 4.0% |
| 1 | summary_v1 | 50 | 14 | 28.0% |
| 2 | control | 50 | 2 | 4.0% |
| 2 | summary_v1 | 50 | 26 | 52.0% |
| 3 | control | 50 | 2 | 4.0% |
| 3 | summary_v1 | 50 | 26 | 52.0% |
| 4 | control | 50 | 3 | 6.0% |
| 4 | summary_v1 | 50 | 28 | 56.0% |

**What this means for the scale decision:** Yes — open rate improved across the sends for the treatment group specifically, and the gap over control widens and then holds: 28% → 52% → 52% → 56%, while control stays flat at 4-6% the entire time. This isn't a one-time novelty spike that fades — the treatment's open rate roughly doubles from send 1 to send 2 and then sustains, which is a healthier pattern than a single strong open followed by decay. Control's near-zero, flat rate across all 4 sends is itself worth noting — it suggests the *entire* lift here belongs to the treatment, not to some general seasonal engagement uptick affecting everyone.

---

## Summary for the Scale Decision

- **Supports scaling:** Q1 confirms the decline pattern is real and consistent (not noise). Q3 shows a large retention gap favoring treatment, on a real control comparison. Q4 shows sustained, not novelty-driven, engagement lift.
- **Weak/inconclusive:** Q2's engagement-frequency proxy shows a gap in the expected direction (57.6% vs. 51.4%) but it's small, and it measures general engagement frequency, not an actual streak being broken — the data has no active-streak-then-broken concept to query in the first place.
- **Gap to close before finalizing the decision:** The core Streakly-specific claim — that *breaking an already-built streak* (not just general low engagement) drives outsized churn — is still supported by qualitative research only ([02-research/interview-synthesis.md](../02-research/interview-synthesis.md), [02-research/nps-analysis.md](../02-research/nps-analysis.md)), not by this dataset. Worth getting real production data with an actual streak field before treating the scale decision as fully evidence-backed on the quantitative side.
- **Sample size caveat:** n=50 per group in the week-5 experiment is workable for a directional signal but small for a launch-scale bet — worth confirming statistical significance was checked before this number gets cited as settled in front of Marcus or the exec team.
