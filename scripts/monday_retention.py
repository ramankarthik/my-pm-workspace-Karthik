#!/usr/bin/env python3
"""
Monday Retention Digest — Streakly

Pulls this week's metrics, compares against last week's stored baseline,
and produces a plain-English Slack digest.

DATA SOURCE NOTE: this currently reads from the "Nudge Dataset" Google Sheet
used for the earlier pilot analysis (data/metric-findings.md /
data/metric-diagnosis.md) — a static, historical dataset, not a live
production feed. In a real deployment, replace fetch_data() with a query
against the actual production analytics warehouse. Everything downstream
(metric computation, baseline comparison, digest formatting) is written to
work the same way regardless of where the data comes from.

STREAK-BREAK RATE NOTE: there is no literal streak field in the available
data (same limitation documented in data/metric-findings.md Q2). This script
uses an explicit, labeled proxy: the "lapse rate" — the percentage of users
who were active last week but have zero sessions this week. This is NOT the
same as a true streak-break rate and should be replaced with a real query
once a streak field exists in production.

USAGE:
    python3 monday_retention.py --week-end YYYY-MM-DD [--baseline-file PATH] [--no-save]

    --week-end     The Monday-morning reference date. "This week" = the 7
                    days ending the day before this date. "Last week" = the
                    7 days before that.
    --baseline-file  Where to read/write the stored snapshot for comparison.
                    Defaults to data/snapshots/monday-baseline.json.
    --no-save      Don't overwrite the baseline file (useful for a dry run).
"""
import argparse
import csv
import io
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta

SHEET_ID = "1jMZXItXhbYxdBkzM74z2BXbCHHbnvqh4Eyclmmhdiww"
SHEET_TABLE_MAP = {
    "nudge_users": "Users",
    "nudge_sessions": "Sessions",
    "nudge_retention": "Retention",
    "nudge_nudges": "Nudges",
}


def fetch_sheet_csv(sheet_name):
    """Fetch one tab of the source Google Sheet as parsed CSV rows (dicts)."""
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}"
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


import urllib.parse  # noqa: E402  (kept near use for clarity)


def fetch_data():
    """Fetch all tables needed for this digest. Swap this out for a real
    production query in a live deployment."""
    users = fetch_sheet_csv(SHEET_TABLE_MAP["nudge_users"])
    sessions = fetch_sheet_csv(SHEET_TABLE_MAP["nudge_sessions"])
    retention = fetch_sheet_csv(SHEET_TABLE_MAP["nudge_retention"])
    nudges = fetch_sheet_csv(SHEET_TABLE_MAP["nudge_nudges"])
    return users, sessions, retention, nudges


def parse_date(s):
    if not s:
        return None
    return datetime.strptime(s.split(" ")[0], "%Y-%m-%d")


def compute_week_metrics(sessions, retention, nudges, week_start, week_end):
    """Compute this window's metrics: session count, active users, lapse
    candidates, push open rate. week_end is exclusive."""
    sessions_in_window = [
        s for s in sessions
        if s.get("session_date") and week_start <= parse_date(s["session_date"]) < week_end
    ]
    users_active_in_window = {s["user_id"] for s in sessions_in_window}

    nudges_in_window = [
        n for n in nudges
        if n.get("sent_date") and week_start <= parse_date(n["sent_date"]) < week_end
    ]
    n_sent = len(nudges_in_window)
    n_opened = sum(1 for n in nudges_in_window if n.get("opened") in ("1", "1.0"))
    open_rate = round(100 * n_opened / n_sent, 1) if n_sent else None

    return {
        "session_count": len(sessions_in_window),
        "active_users": users_active_in_window,
        "n_active_users": len(users_active_in_window),
        "push_sent": n_sent,
        "push_opened": n_opened,
        "push_open_rate_pct": open_rate,
    }


def compute_day7_retention(retention, cohort_week_filter=None):
    """Day-7 retention across the retention table (optionally filtered to a
    cohort_week, since that's the only cohort dimension the source data has).

    KNOWN LIMITATION OF THIS DEMO DATA SOURCE: this dataset's retention table
    is keyed to each user's original signup cohort_week, not a rolling
    7-day window — so this number does NOT actually vary by --week-end in
    this demo, which is why the headline can show 'flat' across runs even
    when session/lapse metrics move. A real production query should compute
    Day-7 retention for the cohort of users who signed up ~7 days before
    the run date, which genuinely varies week to week. Flagging this rather
    than hiding it — it is a property of the demo dataset, not a bug."""
    rows = retention
    if cohort_week_filter is not None:
        rows = [r for r in rows if r.get("cohort_week") == str(cohort_week_filter)]
    if not rows:
        return None
    n = len(rows)
    retained = sum(1 for r in rows if r.get("day_7") in ("1", "1.0"))
    return round(100 * retained / n, 1)


def compute_lapse_rate(prev_active_users, curr_active_users):
    """Proxy for 'streak-break rate': % of last-week-active users who have
    zero sessions this week. See module docstring for why this is a proxy,
    not a true streak-break measure."""
    if not prev_active_users:
        return None
    lapsed = prev_active_users - curr_active_users
    return round(100 * len(lapsed) / len(prev_active_users), 1)


def load_baseline(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def save_baseline(path, snapshot):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(snapshot, f, indent=2, default=str)


def save_digest(docs_dir, digest_text, week_end_str):
    """Save the formatted digest to docs/, versioned by the actual run
    timestamp (not just the --week-end date) so multiple runs in one day
    don't collide and the filename reflects when it was actually generated."""
    os.makedirs(docs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"monday-digest-{timestamp}.md"
    path = os.path.join(docs_dir, filename)
    with open(path, "w") as f:
        f.write(f"# Monday Retention Digest\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(f"Reference week-end: {week_end_str}\n\n")
        f.write("---\n\n")
        f.write(digest_text)
        f.write("\n")
    return path


def fmt_delta(curr, prev, unit="pts", higher_is_better=True):
    if curr is None or prev is None:
        return "n/a (no baseline yet)"
    delta = round(curr - prev, 1)
    if delta == 0:
        return f"flat ({curr})"
    direction = "up" if delta > 0 else "down"
    good = (delta > 0) == higher_is_better
    tag = "🟢" if good else "🔴"
    sign = "+" if delta > 0 else ""
    return f"{tag} {direction} {sign}{delta}{unit} ({prev} → {curr})"


def build_digest(curr, prev, week_label):
    lines = []
    lines.append(f"*Monday Retention Digest — {week_label}*")
    lines.append("")

    # Headline number
    lines.append(f"*Headline: Day-7 retention* — {fmt_delta(curr['day7_retention'], prev.get('day7_retention') if prev else None)}")
    lines.append("")

    # Find biggest mover across the tracked metrics (by absolute delta, normalized where possible)
    movers = []
    if prev:
        candidates = {
            "Day-7 retention": (curr["day7_retention"], prev.get("day7_retention"), "pts", True),
            "Lapse rate (streak-break proxy)": (curr["lapse_rate"], prev.get("lapse_rate"), "pts", False),
            "Session count": (curr["session_count"], prev.get("session_count"), "", True),
            "Push open rate": (curr["push_open_rate_pct"], prev.get("push_open_rate_pct"), "pts", True),
        }
        for name, (c, p, unit, higher_better) in candidates.items():
            if c is not None and p is not None and p != 0:
                pct_change = abs((c - p) / p) * 100
                movers.append((pct_change, name, c, p, unit, higher_better))
        movers.sort(reverse=True)

    if movers:
        _, name, c, p, unit, higher_better = movers[0]
        lines.append(f"*Signal to watch:* {name} — {fmt_delta(c, p, unit, higher_better)}")
    else:
        lines.append("*Signal to watch:* no baseline yet — this is the first run, nothing to compare against.")
    lines.append("")

    # Suggested action — simple rule-based heuristic, not a model judgment call beyond the numbers
    action = suggest_action(curr, prev)
    lines.append(f"*Suggested action this week:* {action}")

    return "\n".join(lines)


def suggest_action(curr, prev):
    if not prev:
        return "First run — no baseline yet. Re-run next Monday to get the first real comparison."
    if curr["lapse_rate"] is not None and prev.get("lapse_rate") is not None and curr["lapse_rate"] > prev["lapse_rate"] + 3:
        return "Lapse rate (streak-break proxy) jumped — worth checking if this tracks with the Comeback screen rollout status or a recent product change."
    if curr["day7_retention"] is not None and prev.get("day7_retention") is not None and curr["day7_retention"] < prev["day7_retention"] - 3:
        return "Day-7 retention dropped meaningfully — pull this week's cohort and check if it's concentrated in a specific channel or platform before assuming it's the same root cause as before."
    if curr["push_open_rate_pct"] is not None and prev.get("push_open_rate_pct") is not None and curr["push_open_rate_pct"] < prev["push_open_rate_pct"] - 5:
        return "Push open rate dropped — check notification content/timing before assuming it's a retention-driven effect rather than a delivery issue."
    return "Nothing moved sharply this week — routine check only, no action needed beyond normal monitoring."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--week-end", required=True, help="Reference Monday date, YYYY-MM-DD")
    parser.add_argument("--baseline-file", default="data/snapshots/monday-baseline.json")
    parser.add_argument("--no-save", action="store_true")
    parser.add_argument("--docs-dir", default="docs",
                         help="Folder under docs/ to save the formatted digest (default: docs/monday-digests)")
    args = parser.parse_args()

    week_end = datetime.strptime(args.week_end, "%Y-%m-%d")
    week_start = week_end - timedelta(days=7)
    prev_week_start = week_start - timedelta(days=7)

    users, sessions, retention, nudges = fetch_data()

    curr_week = compute_week_metrics(sessions, retention, nudges, week_start, week_end)
    prev_week = compute_week_metrics(sessions, retention, nudges, prev_week_start, week_start)

    curr = {
        "day7_retention": compute_day7_retention(retention),
        "session_count": curr_week["session_count"],
        "push_open_rate_pct": curr_week["push_open_rate_pct"],
        "lapse_rate": compute_lapse_rate(prev_week["active_users"], curr_week["active_users"]),
    }

    baseline = load_baseline(args.baseline_file)
    prev = baseline.get("metrics") if baseline else None

    digest = build_digest(curr, prev, f"week of {week_start.date()} to {week_end.date()}")

    print(digest)
    print()
    print("--- raw metrics (for the record) ---")
    print(json.dumps(curr, indent=2))

    if not args.no_save:
        save_baseline(args.baseline_file, {
            "week_end": args.week_end,
            "metrics": curr,
        })
        print(f"\n[Saved baseline to {args.baseline_file} for next week's comparison]")

        digest_path = save_digest(args.docs_dir, digest, args.week_end)
        print(f"[Saved formatted digest to {digest_path}]")


if __name__ == "__main__":
    main()
