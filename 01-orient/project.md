# project.md

*Draft PRD skeleton — starting point only, not a finished document.*

> **Note:** This is the original Module 1 exercise artifact, kept as-is for the record. The **canonical, actively-maintained** `project.md`, `strategy.md`, and `change_log.md` live at the **repo root**, not here — see those for current state.

## Problem Statement

Day-7 retention has dropped from 48% to 39% since the streak redesign shipped. The drop is sharpest among users who break their streak in week 1 — once a user misses two days in a row, churn is almost double. When a streak breaks, the app resets the counter to zero with no acknowledgment of prior progress, and the "you lost your streak" push notification has a harsh tone. Users appear to go passive because breaking a streak feels like failure, and there is no graceful way back in.

## Goals

- Give users a specific, personal reason to come back after breaking a streak, rather than a generic "keep going!" message.
- Acknowledge a user's prior progress instead of a cold reset to zero.

## Non-Goals

*Not discussed in the thread.*

## Success Metrics

*Not discussed in the thread — Day-7 retention (currently 39%, down from 48%) is the metric under investigation, but no target or measurement plan was specified.*

---

**Open question raised by Marcus:** is the core problem the streak reset itself, the notification tone, or the lack of any acknowledgment/path back after a break? Team leaned toward "what happens after the break" as the bigger issue, but this wasn't fully resolved before Thursday's meeting.
