---
name: research-pulse
description: Turn a raw weekly dump of new user feedback, support tickets, or NPS comments into a themed synthesis, cross-checked against existing Streakly research so only genuinely new signal gets flagged as new.
---

# Weekly Research Synthesis (Research Pulse)

## Trigger Prompt

Paste this, with the raw feedback/tickets/NPS comments pasted directly below it in the same message — this skill can't gather that data on its own, so it has to arrive in the trigger:

> Run my weekly research pulse for Streakly. Here's this week's raw feedback/tickets/NPS comments: [paste raw text here]. Extract themes, compare against 02-research/nps-analysis.md and 02-research/interview-synthesis.md, flag what's new vs. recurring, and save it. Don't ask me anything else — work from what I've pasted and what's already in the repo.

## Steps Claude Runs (no further input required)

1. Read `02-research/nps-analysis.md` and `02-research/interview-synthesis.md` to know what's already been established — this step is what makes "new vs. recurring" possible; skipping it just produces a second, disconnected synthesis.
2. Extract themes from the pasted raw text, ranked by frequency — same method as `02-research/nps-analysis.md` (do not invent themes not present in the pasted text).
3. For each theme, mark it **New** (not present in the existing research files) or **Recurring** (already documented — cite which file/theme it echoes).
4. Split praise from complaints.
5. Flag the single most important thing this week's batch adds to what's already known — if nothing does, say so plainly rather than manufacturing significance.
6. Save the result (see Output Location).

## Output Format

```markdown
# Research Pulse — [date]

Source: [n] raw items pasted this session.

## Themes (Ranked by Frequency)

| Theme | Status | Mentions | Notes |
|---|---|---|---|
| ... | New / Recurring (see [file]) | ... | ... |

## Praise vs. Complaints

**Praise**
- ...

**Complaints**
- ...

## What's New This Week

[One paragraph — what this batch adds that wasn't already known, or "nothing new this week, all themes recur" if true.]
```

## Output Location

`02-research/pulses/YYYY-MM-DD-research-pulse.md` (create the `02-research/pulses/` folder if it doesn't exist yet — keeps weekly pulses separate from the core synthesis docs they're compared against).
