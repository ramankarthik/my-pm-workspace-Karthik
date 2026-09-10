# QA Checklist: Streakly Comeback Screen

Sources: [docs/spec-readiness.md](spec-readiness.md), [prototype/README.md](../prototype/README.md), [prototype/index.html](../prototype/index.html).

## 1. Edge Case List

### Empty States

- User has never held a streak — per `spec-readiness.md`, the screen shouldn't fire at all in this case (trigger requires having had *and* broken a streak). Needs explicit test: confirm the screen truly never appears for these users, not just that the best-streak card is hidden.
- Best-streak value is legitimately 0 vs. missing/null due to a data error — these need different handling. A missing value silently rendering as "0-day" would misrepresent a data bug as a real empty state.
- No comeback-lesson content available for the user's track (track discontinued, all lesson variants exhausted, track changed mid-streak) — the prototype hardcodes a single Spanish lesson; production needs a defined fallback.
- Best-streak equals most-recent-streak (e.g., a user's first-ever streak was also their longest) — the "for inspiration" framing may read oddly when both numbers are identical.

### Edge Data Conditions

- Streak of 1 day, broken — does this clear the (still-undefined, per `spec-readiness.md`) minimum streak threshold to qualify for a Comeback screen at all?
- Streak broken twice within the 30-day cooldown window — per `spec-readiness.md`, this requires a distinct "freeze unavailable" screen that **does not exist in the current prototype**.
- Streak-freeze already used, cooldown active — same gap as above.
- Best-streak value lower than the most recent broken streak (data inconsistency that shouldn't happen, but worth a defensive check).
- User with multiple active tracks — which track's streak does this screen reference if the user studies more than one subject? Undefined in both the prototype and the research.
- Negative or non-integer streak values (defensive check against data corruption).

### Timing Scenarios

- Missed exactly 2 days (the scenario the copy is written for) vs. missed weeks or months — "You missed a couple of days — that happens" is inappropriate copy for a long-absence return; needs a variant or threshold.
- Time zone boundaries — is "missed a day" calculated on server time (UTC) or the user's local time? A user near midnight could be incorrectly marked as having missed a day they didn't, in their own time zone.
- Comeback screen shown late — if a user doesn't open the app until well after breaking their streak, is the "offer window" (shown as 48 hours in the prototype) calculated from the break date or from when they actually see the screen? These give different, contradictory answers if not clearly defined.
- Daylight saving time transitions affecting day-boundary calculations.

### Permission States

- Notifications off — if the entry point to this screen is partly notification-driven (per `docs/triad-session.md`, this is still an open question), how does a user with notifications disabled ever discover this screen exists?
- Background refresh off — could mean stale streak state client-side, delaying when the Comeback screen actually triggers relative to the real break.
- Push token invalid/expired — notification delivery failure, same discoverability risk as notifications-off.

## 2. PM QA Walkthrough of `prototype/index.html`

Screen-by-screen review against the 10 most important things to verify before sign-off.

| # | Check | Screen(s) | Result | Notes |
|---|-------|-----------|--------|-------|
| 1 | "Not now" exits without silently routing into the lesson | 1 → 5 | **PASS** | `onclick="goTo(5)"` — confirmed fixed from the earlier usability-round bug. |
| 2 | "Where you left off" (12-day) is visually and textually distinct from "best streak ever" (18-day) | 1 | **PASS** | Two separate elements (`.stat-card` vs. `.best-row`) with different labels — the earlier messaging confusion is resolved. |
| 3 | Streak-freeze visually restores the count rather than showing a generic confirmation | 3 → 4 | **PASS (prototype scope only)** | Screen 4 shows "12" restored. Cannot verify this holds with real backend data — currently hardcoded. |
| 4 | The comeback lesson requires a correct answer before unlocking the freeze | 2 | **FIXED (was FAIL)** | `pick(el, isCorrect)` now only advances on the correct answer — a wrong pick shows a red "incorrect" shake state and stays on the lesson. Verified in-browser: wrong answer blocks, correct answer still proceeds. Fixed as part of the capstone review session. |
| 5 | The 60-second timer has defined behavior at timeout | 2 | **Cannot be determined** | Timer counts down and stops at 0:00, but nothing forces navigation or blocks a late answer — unclear if a hard cutoff is intended or if "60 seconds" is just a soft framing device. Needs a product decision, not just a QA check. |
| 6 | The freeze-offer expiration window is consistent with the defined spec | 5 | **FAIL** | Screen 5 states the offer "stays available for the next 48 hours" — but `docs/spec-readiness.md` only defines a **30-day cooldown after a freeze is used**, not a 48-hour window on the *initial* offer. This is either a real, undefined business rule or a leftover placeholder — either way it's currently unconfirmed and could show users an inaccurate promise. |
| 7 | "Free, always" copy is accurate and durable | 1, 3 | **Cannot be determined** | Not a code-verifiable check — needs product/business confirmation that this claim won't become false if monetization changes later. |
| 8 | Basic accessibility support (screen reader, keyboard nav) | All | **Partial / FAIL** | Buttons are semantic and keyboard-focusable, but the countdown timer and progress bar have no `aria-live` region (a screen-reader user gets no update as time passes), and decorative emoji aren't marked `aria-hidden`. |
| 9 | Rapid double-tap on the freeze button doesn't cause duplicate actions | 3 | **Cannot be determined** | Harmless in the static prototype (just re-triggers a screen swap), but this is exactly the kind of interaction that needs an idempotency check once a real API call is behind this button. |
| 10 | Hardcoded prototype values (12-day, 18-day, Spanish) are clearly mock data, not literal defaults | All | **Flag, not fail** | Nothing in the file marks these as placeholders. Low risk, but worth an explicit engineering confirmation that these get replaced by real data bindings before launch, not shipped as literal fallback values. |

### Blocking vs. Known Issue

**Blocks launch:**
- **#6 — Freeze-offer window copy is inconsistent with the defined spec.** Shipping a specific, user-facing promise ("48 hours") that isn't backed by an actual defined rule is a real risk — either the copy needs to change or the 48-hour rule needs to be confirmed and added to the spec.

**Resolved since the original review:**
- **#4 — Lesson gating.** Fixed — see row above. No longer blocking.

**Can ship as known issues (log and follow up):**
- #5 — Timer timeout behavior is ambiguous but low-severity; can be clarified post-launch.
- #8 — Accessibility gaps should be logged and tracked, not silently dropped, but likely don't block an initial controlled test.
- #9 — Idempotency needs confirmation once real API integration exists, not before — not testable in a static prototype anyway.
- #10 — Low risk; a straightforward pre-launch confirmation with engineering, not a design or logic issue.

## 3. Draft PR Comment for Raj

> Quick question before this merges — I noticed the comeback lesson (`pick()` in `index.html`) unlocks the streak-freeze regardless of which answer the user picks, including the wrong one. Was that intentional (the lesson is meant to be participatory rather than pass/fail), or should it actually require a correct answer before unlocking the freeze? Asking because the whole "earned, not handed out" framing we discussed depends on this actually gating something — if any tap passes, I want to make sure we're not accidentally shipping a lesson that *looks* like a gate but isn't one. Happy to align on intended behavior before this goes further either way.
