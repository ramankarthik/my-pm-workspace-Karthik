---
name: friday-status
description: Autonomously compile a Friday status update (Shipped / In Progress / Blocked) by reading the repo's own history and docs — no manual bullet list needed from the user.
---

# Friday Status Update

## Trigger Prompt

Paste exactly this to run it:

> Run my Friday status update for Streakly. Look at git history and the workspace since last Friday (or since the last status update if you can find one), compile Shipped / In Progress / Blocked, and save it. Don't ask me anything — use what's in the repo.

## Steps Claude Runs (no further input required)

1. Find the last status update file in `status/` (see Output Location) to determine the "since" date. If none exists, default to the last 7 days.
2. Run `git log --since=<date> --stat` and `git status` to see what was committed and what's still in progress/uncommitted.
3. Cross-reference recent commits against `change_log.md` for the "why" behind each change — commit messages alone are often too terse to stand as a status line.
4. Scan for blockers: check `stakeholders/*.md` "Open Gap"/"Open Item" sections, and any doc containing "TBD," "not yet defined," "blocked," or "waiting on" that changed or is still open within the window.
5. Compile the raw findings, then apply the formatting rules from `skills/weekly-status.md` (max 3 bullets per section, plain declarative language, no invented items) to produce the final update.
6. Save the result (see Output Location) and tell the user it's ready — don't wait for approval on formatting, since the rules are already fixed by `skills/weekly-status.md`.

## Output Format

```markdown
# Friday Status — [date]

**Shipped**
- ...

**In Progress**
- ...

**Blocked**
- ...
```

If a section has nothing, write "Nothing to report" rather than omitting it (consistent with `skills/weekly-status.md`).

## Output Location

`status/YYYY-MM-DD-friday-status.md` (create the `status/` folder if it doesn't exist yet).
