# Workspace Audit

A review of the repo structure, file contents, and `CLAUDE.md` as of this session.

## 1. What's Missing That Would Make Claude More Useful Next Session

- **`CLAUDE.md` is badly out of date relative to the actual work.** It still reflects roughly where things stood after the first research phase — no mention of the prototype, the stakeholder profiles (Raj/Lena/Marcus), the PRD, the pilot/experiment results, or the presentation deck. A fresh session reading only `CLAUDE.md` would have no idea most of this exists. (Fixed below.)
- **No index of what exists where.** With 18 files now in `docs/` alone, there's no single place that says "here's the PRD, here's the spec-readiness review, here's the pilot data" — a new session has to discover the structure by listing files rather than being told.
- **No "current state / next action" marker.** Nothing in the workspace says what's actually pending right now (e.g., PRD not yet reviewed by Raj/Lena in real life, rollout timeline still undefined, a large batch of work sitting uncommitted). Without this, a new session might re-derive status from scratch or make stale assumptions.
- **`Tone`, `Defaults`, and `Never` in `CLAUDE.md` are still mostly blank.** One real default was captured earlier (proactively flag save-worthy content), but the pattern that's actually governed most of this project's work — *ground every claim in a source file, flag rather than invent when something's missing or unconfirmed* — was never written down as a standing rule, even though it's been followed consistently and explicitly requested more than once.
- **No glossary**, despite a growing set of project-specific terms a fresh session would benefit from knowing immediately (Comeback screen, streak-freeze, `summary_v1`/`control`, the week-5 cohort, etc.).
- **No note on this machine's tooling gaps** — no Node.js, no LibreOffice, no `gh` CLI, and no stored GitHub credentials (a token has to be pasted fresh each session to push). These were all rediscovered mid-session this time; writing them down once would save that rediscovery next time.

## 2. Uncommitted Work — Flagging as Urgent, Not Just Organizational

A significant amount of real work is currently **uncommitted and unpushed**:

```
?? data/
?? docs/objection-log.md
?? docs/prd.md
?? docs/presentation-notes.md
?? docs/presentation.md
?? docs/presentation.pptx
?? docs/recommendation-memo.md
?? skills/write-prd.md
```

This includes the entire pilot data analysis, the PRD, the objection log, and the leadership deck — none of it is backed up to GitHub yet. Recommend committing and pushing before this grows further.

## 3. Reorganization Suggestions (Not Yet Applied)

**A. Resolve the duplicate `project.md` / `strategy.md` / `change_log.md` problem.** These exist at the repo root (actively used and updated all session) *and* a differently-structured `project.md` exists inside `01-orient/` (the original Module 1 PRD-skeleton exercise). Nothing currently marks which is canonical. Recommend adding a one-line note at the top of `01-orient/project.md` and `01-orient/orientation.md` pointing to the root versions as the living documents, so this doesn't get edited by mistake later.

**B. `docs/` has grown flat and mixed.** 18 files at one level, spanning research synthesis, specs, stakeholder reviews, and leadership deliverables. Consider subfolders once it grows further — e.g., `docs/specs/` (prd.md, spec-readiness.md, qa-checklist.md, objection-log.md), `docs/reviews/` (design-review.md, triad-session.md), `docs/leadership/` (decision-brief.md, recommendation-memo.md, presentation*). Not urgent yet, but worth doing before it doubles again.

**C. Clean up dead weight:**
- `docs/~$debase-summary.md` — a stray Microsoft Office lock file (from `codebase-summary.md` being opened in Word at some point). Safe to delete; not real content.
- `02-research/research.md` — the original course-template placeholder, empty/unfilled and never used since the real research went into `interview-synthesis.md`, `nps-analysis.md`, and `competitive-matrix.md` instead. Either delete it or repurpose it as an index pointing to the three real files.

**D. The course module structure (`01-orient/` through `06-systems/`) is now out of sync with where real work actually lives.** Substantial work that maps conceptually to Module 3 (triad session plan → `docs/triad-session.md`), Module 4 (codebase tour, QA → `docs/codebase-summary.md`, `docs/qa-checklist.md`), and Module 5 (findings/diagnosis/memo → `data/metric-diagnosis.md`, `docs/recommendation-memo.md`) is sitting in `docs/` and `data/` instead of the numbered module folders the README's status table tracks. Either update the README's table to point at the real file locations, or move/duplicate the relevant docs into their module folders — worth a decision before Module 6's final presentation generator has to reconcile this.

## 4. `CLAUDE.md` — Updated

See the rewritten file. Summary of what changed: added the stakeholder roster, an index of key artifacts by category, a current-state/next-step section, filled in `Never` and part of `Tone`, added a glossary, and noted this machine's tooling gaps.
