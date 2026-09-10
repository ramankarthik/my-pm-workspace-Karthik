# CLAUDE.md — Persistent Memory

> The file Claude Code reads at the start of every session. Short, true, current — the difference between Claude building blind and building with context.

## The Product

Streakly — consumer habit + micro-learning app. Users pick a track, do a 5-minute daily lesson, and build a streak; the streak is the core habit loop.

Launched 4 years ago. Series B funded ($42M). 2.1M registered users, 340K MAU, growing 28% YoY on MAU.

**Current focus:** the Streakly Comeback screen — recovering Day-7 retention, which dropped from 48% to 39% after the v2 streak redesign shipped.

## Who I Am

PM, Engagement squad. Phase: moving from discovery into spec/build — research, prototype, and a pilot experiment are done; PRD is drafted and pressure-tested; not yet built/shipped at scale.

## Stakeholders

Profiles at `stakeholders/{raj,lena,marcus}.md` — read before drafting anything for them.

- **Raj** — Engineering lead. Needs feasibility, edge cases, acceptance criteria before saying yes. Open item: streak-freeze/"best streak ever" data model isn't built yet.
- **Lena** — Designer. Needs real-user evidence, not assumptions. Flagged the lesson-gate mechanic as unvalidated (contradicts Tom's actual stated experience).
- **Marcus** — Head of Product. Needs a clear ask + deadline, recommendation up front. Open item: no rollout timeline exists yet anywhere in the workspace.

## Key Artifacts (Where Things Live)

- **Research:** `02-research/interview-synthesis.md` (Priya, Tom, Amara), `nps-analysis.md`, `competitive-matrix.md`
- **Strategy / hypothesis:** `strategy.md` (root — canonical, see note below), `docs/hypothesis.md`
- **Decision & recommendation docs:** `docs/decision-brief.md` (what Marcus approved to start), `docs/recommendation-memo.md` (pilot results memo)
- **Pilot / experiment data:** `data/metric-findings.md`, `data/metric-diagnosis.md`, `data/experiment-design.md` — real SQL against a real downloaded dataset, but the dataset itself is a synthetic stand-in with no true streak field (flagged throughout those files). Trust the methodology; treat the specific conclusions as directional until run against real production data.
- **Spec:** `docs/prd.md`, `docs/spec-readiness.md` (Raj pressure-test), `docs/design-review.md` (Lena pressure-test), `docs/objection-log.md` (Raj/Marcus/Tom objections)
- **Prototype:** `prototype/index.html` + `prototype/README.md`. Lesson-gating bug found in QA is fixed as of this session.
- **QA:** `docs/qa-checklist.md`
- **Leadership deck:** `docs/presentation.md` + `presentation-notes.md` + `presentation.pptx`
- **Automation:** `agents/monday-retention.md` + `scripts/monday_retention.py` — working, verified script for a weekly retention digest. Not yet scheduled or wired to real Slack/production data (see the spec's "Path to Production").
- **Reusable skills:** `skills/weekly-status.md`, `skills/write-prd.md` (run and verified), `skills/friday-status.md`, `skills/research-pulse.md`, `skills/competitive-pulse.md` (written but never actually run — treat as draft specs until exercised once)
- **Stakeholder template:** `stakeholders/TEMPLATE.md` — copy for any new stakeholder profile.
- **Workspace audit:** `workspace-audit.md`, `docs/capstone-session.md` — periodic self-review of the workspace's own state; worth rereading before assuming file locations or status.

**Note on duplicate files:** `01-orient/project.md`, `strategy.md`, and `change_log.md` also exist as separate Module 1 course-exercise files under `01-orient/` (now marked with a note pointing to the canonical versions). The **root-level** `project.md`, `strategy.md`, and `change_log.md` are the canonical, actively-maintained versions.

## Current State / Next Steps

- PRD (`docs/prd.md`) is drafted and has been pressure-tested against Raj, Lena, and Marcus's profiles (see `spec-readiness.md`, `design-review.md`, `objection-log.md`) — not yet reviewed by them in real life. Real open items from that pressure-testing: the streak-freeze data model doesn't exist yet (Raj), the lesson-gate mechanic is unvalidated (Lena), no rollout timeline exists (Marcus).
- Pilot experiment (`summary_v1` vs. control, week-5 cohort) shows a strong signal but has a known, uncorrected confound (goal-setting imbalance between groups) — `docs/recommendation-memo.md` recommends re-running the corrected analysis before scaling, not scaling off the raw number.
- The Monday retention agent works locally but isn't deployed — no real Slack webhook, no cron/n8n schedule, synthetic data source. See `agents/monday-retention.md` "Path to Production."
- Three new skills (`friday-status`, `research-pulse`, `competitive-pulse`) are specced but unrun — dry-run each once before trusting the output format.
- Check `git status` at the start of a session — this workspace has repeatedly accumulated large uncommitted batches of real work; don't assume the working tree is already pushed.

## How I Want Claude to Work With Me

- **Interview first:** ask clarifying questions before building.
- **Tone:** ___
- **Defaults:** Proactively flag when something we've discussed is save-worthy (to an existing or new file) and confirm before writing it — don't wait to be asked each time.
- **Never:** Invent data, quotes, or numbers not present in a named source file. If a requested file doesn't exist, or a claim can't be traced to a source, say so explicitly rather than filling the gap — this has been the standing rule throughout the project and should hold going forward without being re-asked.

## Glossary (my product's words)

| Term | Meaning |
|------|---------|
| Comeback screen | The feature under development: acknowledges a user's progress after a broken streak and offers a way back in (best-streak stat, comeback lesson, one-tap streak-freeze). |
| Streak-freeze | The forgiveness mechanic — retroactively restores a broken streak. Currently earn-gated behind completing a short lesson; this gate is an unvalidated hypothesis, not something users asked for. |
| `summary_v1` / `control` | The two arms of the week-5 pilot experiment (`data/metric-findings.md`). `summary_v1` is the treatment, standing in for the Comeback screen concept in the data — not a literal field labeled "Comeback screen" in the dataset. |
| Week-5 cohort | The specific cohort the pilot experiment ran on — the only cohort with a `variant` split in the data. |

## Operational Notes (This Machine)

- No Node.js, no LibreOffice, no `gh` CLI installed locally. `.pptx` decks are built with `python-pptx` (install via pip) rather than `pptxgenjs`; no automated visual-render QA is available — do manual layout review and ask the user to sanity-check in PowerPoint/Keynote.
- No stored GitHub credentials — pushing requires the user to paste a fresh personal access token each session (revoke after use). `gh` CLI is not available, use `git push` with the token embedded in the URL, and redact it from any command output.
