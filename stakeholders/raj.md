# Raj — Engineering Lead

## From the Workspace (directly sourced)

- Ran the initial data analysis that framed this whole effort: churn is concentrated in users who break their streak in week 1 (source: [project.md](../project.md), synthesized from the original Slack thread).
- In the triad session prep ([docs/triad-session.md](../docs/triad-session.md)), the questions drafted for him center on: technical feasibility of retroactively restoring a streak count, whether the streak-freeze mechanic needs new backend logic or builds on prior scoping, streak-freeze eligibility/timing rules, and entry-point trigger mechanics (notification vs. app-open detection).
- The Habitica codebase research ([docs/codebase-summary.md](../docs/codebase-summary.md)) directly surfaces what is likely to be his first real question: a "best streak ever" field almost certainly doesn't exist yet in a system shaped like this, and would need a new field plus a migration/backfill decision for existing users. That research explicitly frames this as *"the one thing engineers will ask before kickoff."*

## From Default Profile (not yet confirmed in workspace — flag if inaccurate)

- **Role:** Owns technical architecture, sprint scope, and feasibility decisions for the Streakly squad.
- **Pushes back on:** Underspecified requirements, scope that grows mid-sprint, anything touching the streak/notification pipeline without a clear rollback plan.
- **Needs before saying yes:** Clear acceptance criteria, edge cases called out upfront, an answer to "what does done look like."
- **Has asked before that was hard to answer:** "How will we know if this is working after it ships?" and "What happens if the user has never set a streak, or breaks it twice in a week?"
- **Communication preference:** Async first, short messages, bullet points over paragraphs; does not like being surprised in standups.
- **Open items:** Still waiting on data model clarification for the streak-freeze field.

## Notable Confirmation

The default profile's open item — "waiting on data model clarification for the streak-freeze field" — lines up directly with what the codebase research independently found: the streak-freeze/best-streak field doesn't exist yet. This isn't a coincidence to ignore; it means his open item has a concrete, ready answer (or at least a concrete question to bring him) rather than being a vague ask.
