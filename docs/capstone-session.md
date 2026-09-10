# Capstone Review Session

A full-workspace review: what's been built, confidence per artifact, fixes applied, a reusable meta-prompt, and a plan for stakeholder templates.

## 1. What's Been Built

- **Research:** interview synthesis (Priya/Tom/Amara), NPS analysis, competitive matrix — grounded in real inputs, no invented data.
- **Strategy:** `project.md`, `strategy.md` (hypothesis evolved across 3 rounds of new evidence), `change_log.md`.
- **Prototype:** a real, interactive `prototype/index.html`, through two usability rounds (one real, one simulated persona role-play).
- **Spec:** `docs/prd.md`, pressure-tested against Raj, Lena, and Marcus via role-play (`spec-readiness.md`, `design-review.md`, `objection-log.md`).
- **Data/experiment:** real SQL run against a real downloaded dataset — `metric-findings.md`, `metric-diagnosis.md`, `experiment-design.md` (actual z-tests, sample-size math).
- **Leadership comms:** `recommendation-memo.md`, `presentation.md/-notes.md/.pptx`.
- **Stakeholder profiles:** `stakeholders/{raj,lena,marcus}.md`, now with a `TEMPLATE.md` for future ones.
- **Reusable skills:** `weekly-status.md`, `write-prd.md` (also packaged as an installable global skill), `friday-status.md`, `research-pulse.md`, `competitive-pulse.md`.
- **Automation:** `agents/monday-retention.md` + `scripts/monday_retention.py` — a real, working, twice-verified script.
- **Workspace hygiene:** `workspace-audit.md`, `CLAUDE.md`.

## 2. Confidence Per Artifact

| Artifact | Confidence | What would get it to 95% |
|---|---|---|
| Interview synthesis, NPS analysis | 90% | Faithful to what was given, but n=3 and n=10 are thin — more raw data, not better writing |
| Competitive matrix | 85% | Cross-verify against competitors' own pricing pages directly; re-run `competitive-pulse` periodically |
| Prototype | **90% (was 70%)** | Lesson-gating bug fixed and verified this session; remaining gap is the unvalidated lesson-gate hypothesis itself (real-user testing needed) |
| PRD | 65% | Every stakeholder pressure-test surfaced a real open question (data model, rollout timeline, unvalidated lesson-gate) — documented, not resolved |
| Data/experiment findings | 95% on methodology, ~60% on real-world validity | The math is correct; the dataset is a synthetic stand-in with no real streak field — needs actual Streakly production telemetry to trust the *conclusions*, not just the *calculations* |
| Recommendation memo / deck | 75% | Inherits the data's validity ceiling above; honest about the confound, which is a real strength |
| Stakeholder profiles | 80% | These are your defaults/inference, never confirmed by the actual Raj/Lena/Marcus |
| Skills: `weekly-status`, `write-prd` | 90% | Both have real run history in this session |
| Skills: `friday-status`, `research-pulse`, `competitive-pulse` | 60% | Written but never actually run — untested specs |
| Monday retention agent | 80% as a local tool, 30% against the original ask | No Slack webhook, no real schedule, synthetic data source |

## 3. Fixes Applied This Session

1. **Committed and pushed the uncommitted backlog** — `agents/`, `data/`, `scripts/`, and ~10 files in `docs/`/`skills/` were sitting uncommitted, including the entire pilot analysis, the PRD, and the leadership deck.
2. **Fixed the prototype's lesson-gating bug** — `pick()` in `prototype/index.html` previously advanced to the freeze-unlock screen regardless of which answer was chosen. Now a wrong answer shows a red "incorrect" state and blocks advancement; only the correct answer proceeds. Verified in-browser (both paths). `docs/qa-checklist.md` updated to reflect the fix — no longer blocking launch.
3. **Workspace hygiene cleanup** — deleted the stray `docs/~$debase-summary.md` Office lock file; added disambiguation notes to `01-orient/project.md` and `01-orient/orientation.md` pointing to the canonical root-level `project.md`/`strategy.md`/`change_log.md`.
4. **Added `stakeholders/TEMPLATE.md`** — a blank, reusable stakeholder-profile template for future stakeholders (in this project or a forked one).

## 4. Reusable Meta-Prompt (Recreate This Workflow for a Different Product)

```
I'm working on [PRODUCT NAME], a [one-sentence product description]. I want
to set up a Claude Code workspace to take a real product problem from
discovery through a leadership-ready recommendation. Here's how I want to
work:

1. Interview me first about the product, my role, the current phase, the
   key tension I'm navigating, and the open decision I need to resolve.
   Don't build anything until I confirm what you've understood.

2. Save that context to CLAUDE.md so every future session starts oriented,
   not blind.

3. As we go, ground every claim in a named source — research file, data
   query, or explicit user input. If something is an assumption, a
   single-source signal, or unvalidated, label it as such rather than
   stating it as settled. Never invent data, quotes, or numbers.

4. Proactively flag when something we've discussed is worth saving to a
   file, and confirm with me before writing it — don't wait to be asked
   every time.

5. When stakeholders come up (an engineering lead, a designer, a
   leadership sponsor, an actual user), build a profile for each one at
   stakeholders/<name>.md, and use those profiles to calibrate tone,
   format, and the specific objections you'd expect from each person
   whenever you draft something for them or role-play a review with them.

6. When I have real user feedback, competitive research, or product
   data, synthesize it into the workspace rather than the chat — and
   when I ask you to analyze data, actually run the numbers (SQL, real
   statistics) rather than estimating them by eye.

7. Help me build reusable skills for anything we do more than once
   (status updates, research synthesis, spec-writing), and help me spec
   out any recurring automation (a scheduled digest, a weekly pulse
   check) as a real, testable script — not just a description.

8. Periodically audit the workspace: what's missing, what's
   disorganized, what's uncommitted, and what CLAUDE.md needs updated to
   reflect. Ask before restructuring anything.

Let's start with the interview.
```

## 5. Per-User Stakeholder Folders

`stakeholders/{raj,lena,marcus}.md` are specific to this Streakly scenario and get committed straight into the repo — fine here, but breaks for anyone forking this template, since their engineering lead isn't named Raj.

**Applied this session:** added `stakeholders/TEMPLATE.md` — the blank interview format (Role, Pushes back on, Needs before saying yes, Has asked before, Communication preference, Open items) used to build the three real profiles, with placeholders to fill in.

**Still a decision to make (not applied — flagging, not deciding on your behalf):** whether real stakeholder profiles should be gitignored by default in the *template* repo (before anyone forks it), since they may contain real colleagues' real working styles — sensitive enough that a stranger reusing this template probably shouldn't default to committing them publicly. This project's own `stakeholders/*.md` were left committed since this is a personal capstone repo, not a shared team one — but if this repo is meant to be the template others fork, `stakeholders/*.md` (except `TEMPLATE.md`) in `.gitignore` is worth considering as the safer default upstream.
