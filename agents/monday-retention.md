# Agent Spec: Monday Retention Digest

Runs before standup every Monday. Checks Streakly Day-7 retention and streak-break rate against last week's baseline, compares session counts and push open rates, and produces a plain-English Slack digest.

## Status: Spec + Working Script, Not Yet Deployed

This is a working script (`scripts/monday_retention.py`) that's been run manually and verified — it is **not** wired to a real cron/n8n schedule or a real Slack webhook yet. Both are one-time setup steps outside what I can configure directly in this session (no Slack integration is connected here). See "Path to Production" below.

## Data Source (Important Limitation)

The script currently reads from the **Nudge Dataset Google Sheet** used for the earlier pilot analysis ([data/metric-findings.md](../data/metric-findings.md), [data/metric-diagnosis.md](../data/metric-diagnosis.md)) — a **static, historical dataset**, not a live production feed. In a real deployment, `fetch_data()` needs to be swapped for a query against the actual production analytics warehouse. Everything downstream (metric computation, baseline comparison, digest formatting) works identically regardless of the data source.

**Known consequence of this:** because this dataset's Day-7 retention is keyed to each user's original signup cohort rather than a rolling window, the headline number doesn't actually vary run-to-run in this demo — it will in production, where "Day-7 retention" should be computed for the cohort of users who signed up ~7 days before the run date.

## Metric Definitions

| Metric | Definition | Note |
|---|---|---|
| Day-7 retention | % of the retention table with `day_7 = 1` | Swap for a real rolling-cohort query in production |
| Streak-break rate | **Proxied as "lapse rate"**: % of users active last week who have zero sessions this week | No literal streak field exists in the data (same limitation as [data/metric-findings.md](../data/metric-findings.md) Q2) — replace with a real streak-break query once that field exists |
| Session count | Total sessions in the 7-day window | Direct count from `nudge_sessions` |
| Push open rate | % of `nudge_nudges` sent in-window that were opened | Direct calculation |

## How It Runs

1. **Fetch data** — pulls Users, Sessions, Retention, and Nudges tables.
2. **Compute this week's metrics** for the 7-day window ending the run date.
3. **Load last week's baseline** from `data/snapshots/monday-baseline.json` (if none exists, this is a first run — say so, don't fabricate a comparison).
4. **Find the biggest mover** — the metric with the largest relative change vs. baseline, tagged 🟢/🔴 based on whether the direction is good or bad for that specific metric (e.g., a lapse-rate increase is 🔴 even though the number went up).
5. **Generate a suggested action** — a simple rule-based check (not a model judgment call beyond the numbers): flags whichever tracked metric crossed a meaningful threshold, or says "no action needed" if nothing moved.
6. **Save this week's snapshot** as the new baseline for next week (`data/snapshots/monday-baseline.json`).
7. **Save the formatted digest** to `docs/monday-digest-YYYY-MM-DD_HHMM.md`, versioned by the actual run timestamp (not the `--week-end` date), so repeated runs don't collide and the filename reflects when it was actually generated. This is a stand-in for real Slack delivery — see step 8.
8. **Post to Slack** — currently only saved to `docs/` per step 7, not posted anywhere (see Path to Production).

## Manual Run (Verify Output Before Trusting It)

```bash
python3 scripts/monday_retention.py --week-end 2026-02-16
```

- `--week-end` is the Monday reference date. First run establishes a baseline with no comparison; every run after that compares against the saved snapshot.
- Add `--no-save` to do a dry run without overwriting the baseline or saving a digest file.
- Add `--baseline-file <path>` to point at a different snapshot file (useful for testing without disturbing the real one).
- Add `--docs-dir <path>` to change where the formatted digest gets saved (default: `docs/`).

**Verified output from an actual run** (two consecutive weeks in the source data):

```
*Monday Retention Digest — week of 2026-02-09 to 2026-02-16*

*Headline: Day-7 retention* — flat (53.2)

*Signal to watch:* Session count — 🔴 down -135 (471 → 336)

*Suggested action this week:* Lapse rate (streak-break proxy) jumped — worth checking if this tracks with the Comeback screen rollout status or a recent product change.
```

## Slack Message Template

```
*Monday Retention Digest — week of {week_start} to {week_end}*

*Headline: Day-7 retention* — {emoji} {direction} {delta}pts ({last_week} → {this_week})

*Signal to watch:* {metric_name} — {emoji} {direction} {delta}{unit} ({last_week} → {this_week})

*Suggested action this week:* {action_text}
```

- `{emoji}` is 🟢 if the movement is good for that metric, 🔴 if bad (a rising lapse rate is bad even though the number went up — the script accounts for this per-metric, not just "up = green").
- On a first run (no baseline), the headline and signal both read `n/a (no baseline yet)` and the action reads "First run — no baseline yet. Re-run next Monday to get the first real comparison." — never a fabricated comparison.
- If nothing moved meaningfully, the action line reads "Nothing moved sharply this week — routine check only, no action needed beyond normal monitoring." rather than manufacturing urgency.

## Path to Production

To actually run this unattended every Monday morning:

1. **Real data source:** replace `fetch_data()` in `scripts/monday_retention.py` with a query against the production analytics warehouse (or an API), keeping the same return shape (users, sessions, retention, nudges as lists of dicts).
2. **Real Slack delivery:** add a Slack incoming webhook URL and POST the digest text to it (a few lines with `requests.post`) — not configured here since no webhook is connected to this session.
3. **Scheduling:** either a cron job (`0 8 * * 1` for 8am Monday) calling the script directly, or an n8n workflow with a Cron trigger node → HTTP Request/Python node running this logic → Slack node. A Python script on a timer (e.g., `schedule` library or a simple always-on loop) also works for something lighter-weight than infrastructure-grade cron.
4. **Baseline storage:** `data/snapshots/monday-baseline.json` works fine locally; in a real deployment this should live somewhere persistent across runs (not tied to a single machine) — a small database row or a cloud storage object, not a local file, if this runs on ephemeral infrastructure.
