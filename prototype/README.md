# Streakly Comeback Screen — Prototype

A self-contained, interactive HTML/CSS/JS prototype (`index.html`) of the Comeback screen, mocking a mobile app viewport. No build step, no dependencies — open `index.html` directly in a browser.

## PM Brief

**User:** 24-year-old who hit a 12-day streak, missed two days, and has not opened the app since.

**Job to be done:** Get back in without feeling they lost everything.

**Feature:** Personalized Comeback screen — best-streak stat, one 60-second comeback lesson, one-tap streak-freeze offer.

**Constraint:** Use data Streakly already has. No new integrations.

**Grounded in:**
- [02-research/interview-synthesis.md](../02-research/interview-synthesis.md) — what Priya, Tom, and Amara told us
- [02-research/nps-analysis.md](../02-research/nps-analysis.md) — recurring NPS themes
- [02-research/competitive-matrix.md](../02-research/competitive-matrix.md) — gaps in the competitive landscape
- [docs/decision-brief.md](../docs/decision-brief.md) — the recommendation Marcus approved

## Key Decisions Made During the Interview

- **Prototype type:** Interactive (clickable, stateful), not a static mockup — mock/hardcoded data only, per the "no new integrations" constraint.
- **Best-streak stat:** The primary stat is "here's where you left off" (their most recent, broken streak — 12 days). Their longest-ever streak (18 days) is shown as a secondary, inspirational line, not conflated with "where you left off" — an earlier draft mixed the two under one label and was corrected for clarity.
- **Track:** Spanish, used as the example track for the comeback lesson content.
- **Streak-freeze behavior:** Tapping streak-freeze retroactively covers the missed days — the UI restores the streak count (12) rather than showing a generic "protected" confirmation state.
- **Flow structure:** Sequential, not parallel — the streak-freeze offer is explicitly conditional on completing the 60-second comeback lesson first. The Comeback screen tells the user this upfront ("Finish a 60-second comeback lesson and we'll unlock a one-tap streak-freeze").
- **Visual tone:** Playful (Duolingo-adjacent energy — bright gradients, emoji, rounded shapes) but framed as a coach acknowledging progress rather than a scorekeeper resetting to zero, consistent with the "coach not scorekeeper" finding in the NPS analysis.
- **Form factor:** Mobile-app-shaped viewport (phone frame), since Streakly is a consumer mobile app.

## Screens

1. **Comeback** — shows the streak the user left off at (12 days), their longest-ever streak as inspiration (18 days), and the conditional streak-freeze offer explained upfront.
2. **60-Second Lesson** — a single Spanish micro-lesson question with a live countdown timer and progress bar.
3. **Freeze Unlock** — confirms lesson completion and unlocks the one-tap streak-freeze offer.
4. **Restored** — shows the streak count restored to 12 (not reset to 0), with an encouraging next step.
