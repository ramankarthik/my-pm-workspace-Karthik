---
name: competitive-pulse
description: Run a weekly web-search check on Streakly's tracked competitors for new moves, cross-checked against the existing competitive matrix so only genuinely new changes are flagged.
---

# Competitive Pulse Check

## Trigger Prompt

Paste exactly this to run it:

> Run my weekly competitive pulse check for Streakly. Search for anything new from our tracked competitors this week, compare against 02-research/competitive-matrix.md, flag only what's actually new, and save it. Don't ask me anything — use web search and what's already in the repo.

## Steps Claude Runs (no further input required)

1. Read `02-research/competitive-matrix.md` to get the tracked competitor list (currently: Duolingo, Babbel, Elevate, Headway) and each one's already-documented "Notable recent changes" — this is the baseline everything gets compared against.
2. Run a web search per competitor for news/changes in roughly the last 7-14 days (pricing changes, feature launches, app store updates, funding/M&A, major reviews) — current date matters here, confirm it before searching so queries use the right year/timeframe.
3. For each finding, check it against the matrix's existing "Notable recent changes" — if it's already documented there, it's not new, skip it or note it's still current.
4. Only include genuinely new findings. If a competitor has nothing new this week, say so explicitly rather than padding the update — a pulse check with nothing to report is a valid, useful result.
5. Cite sources (URL) for every claim, same standard as the original competitive matrix — no uncited claims.
6. Save the result (see Output Location). Do not edit `competitive-matrix.md` directly — that stays the stable reference; the pulse is a dated supplement to it.

## Output Format

```markdown
# Competitive Pulse — [date]

## New This Week

### [Competitor]
- [Finding] — [what it means for Streakly, one sentence, if relevant]

*(Repeat per competitor with new findings; omit competitors with nothing new, but list them under "No changes" below.)*

## No Changes This Week
- [Competitor], [Competitor]

Sources:
- [Title](URL)
```

## Output Location

`02-research/pulses/YYYY-MM-DD-competitive-pulse.md` (same `pulses/` folder as the research pulse — create it if it doesn't exist yet).
