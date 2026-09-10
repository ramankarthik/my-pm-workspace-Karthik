---
name: write-prd
description: Write a one-page, research-grounded PRD for an engineering/design audience, with open questions calibrated to each reader's stakeholder profile.
---

# Write PRD

## Input

- A set of research files to ground the PRD in (interviews, NPS/feedback analysis, competitive research, decision briefs, hypotheses — whatever exists in the workspace).
- The stakeholder(s) who will read the spec, with profiles if available (e.g., `stakeholders/*.md`).
- The feature or problem the PRD covers.

## Process

1. **Read every research file named**, don't rely on memory or assumption. If a named file doesn't exist at the given path, check for it under an adjacent/likely path (e.g., a differently-cased folder) before concluding it's missing. If a file genuinely doesn't exist, say so explicitly in the output — don't silently skip it or invent its content.
2. **Ground every claim in a specific source.** Every sentence in Problem Statement, Goals, and Non-Goals should be traceable to a specific research file (cited inline, e.g., "(nps-analysis.md: ...)"). Don't state something as fact if it's actually an assumption, a single-source signal, or an unvalidated hypothesis — label it as such instead.
3. **Calibrate Open Questions per reader.** If multiple stakeholders will read this PRD, split Open Questions into a subsection per person, and shape each subsection to what that person's profile says they need before saying yes (e.g., an engineering lead who needs feasibility/edge cases gets technical, data-model, and measurement questions; a designer who needs real-user evidence gets questions about unvalidated assumptions and missing user-research coverage).
4. **Explicitly flag scope traps.** Anything that sounds like it's in scope but isn't validated by research (e.g., a mechanic the team designed rather than one users asked for) belongs in Non-Goals or Open Questions, not stated as settled.
5. **Keep it to one page.** Plain, declarative language. No opinions, no hedging language beyond what's needed to mark something as unconfirmed.

## Output Structure

```markdown
# PRD: [Feature Name]

*Note any requested source files that don't exist in the workspace, here, up front.*

## Problem Statement
[Grounded in research, cited inline.]

## User
**Who:** [...]
**Job to be done:** [...]

## Goals
- [Each goal cited to a source.]

## Non-Goals
- [Explicitly out of scope, with why — including anything corroborated-but-descoped, single-source-and-unconfirmed, or structurally out of reach for this version.]

## Success Metrics
- [Primary metric, plus any logging/instrumentation needed to diagnose it, not just report it.]

## User Stories
[3-5, in "As a [user], I [action], so [outcome]" form, each traceable to a real user need from research.]

## Open Questions
*For [Stakeholder 1] — [what their profile says they need]:*
- [...]

*For [Stakeholder 2] — [what their profile says they need]:*
- [...]
```

## Example

See [docs/prd.md](../docs/prd.md) (Streakly Comeback screen) for a worked example — Problem/Goals grounded in `02-research/interview-synthesis.md`, `02-research/nps-analysis.md`, and `02-research/competitive-matrix.md`; Open Questions split between Raj (feasibility/data-model/measurement) and Lena (unvalidated assumptions/evidence gaps), calibrated to `stakeholders/raj.md` and `stakeholders/lena.md`.
