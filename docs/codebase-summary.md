# Codebase Tour: HabitRPG/habitica

Source: [github.com/HabitRPG/habitica](https://github.com/HabitRPG/habitica), cloned locally and inspected directly (not summarized from memory). Stack: Node/Express server, MongoDB/Mongoose, Vue.js client, all in one monorepo.

*Note: this repo's README states it does not accept AI-generated code contributions. This exercise is read-only research to inform a Streakly spec — nothing here is being contributed back to Habitica.*

---

## 1. PM-Level Tour

### What it does, in one sentence

Habitica is an open-source habit tracker that turns your real-life to-do list into an RPG — you level up a character, gain gold and gear, and lose health when you skip your habits/dailies.

### How the codebase is organized

| Folder | What it does |
|--------|---------------|
| `website/server/` | The backend API (Express). `controllers/` = HTTP route handlers, split by API version (`api-v3` is current, `api-v4` is a newer, smaller in-progress API). `models/` = MongoDB schemas (User, Task, Group, etc.). `libs/` = shared server logic, including `cron.js` — the daily reset job. |
| `website/common/script/` | Shared business logic used by both server and client (via a shared npm-style import) — this is where task scoring, streak math, and spell/content definitions actually live, not in the controllers. |
| `website/client/src/` | The Vue.js frontend — `components/` (organized by feature area: `tasks/`, `achievements/`, `header/`, etc.), `store/` (Vuex state), `pages/`, `router/`. |
| `migrations/` | One-off scripts for data migrations (schema changes, backfills) — relevant context for any feature that needs a new field on existing user/task documents. |
| `test/` | Test suite, split by layer (unit, integration, API). |

### The 3 most important files for a PM to know

1. **`website/server/models/user/schema.js`** — the entire User data model. If you ever ask "does the product already track X about a user," this file has the answer before you ask an engineer.
2. **`website/common/script/ops/scoreTask.js`** — where streak increment/reset logic actually lives (not in a controller, not in the model — in shared scoring logic used by both client and server). Any spec involving streak behavior needs to account for this file.
3. **`website/client/src/components/tasks/yesterdailyModal.vue`** — Habitica's own existing "Welcome Back" modal, shown when a user returns after missing days, letting them retroactively check off missed dailies. This is a directly relevant precedent for a Comeback screen — worth reading before designing one from scratch.

### Key data models and what they tell you about product decisions

- **Streak lives on the `Task` (specifically `Daily`) model, not on the `User` model** (`website/server/models/task.js:404`, `streak: { $type: Number, default: 0 }`). This tells you Habitica's product decision was: *streaks are per-habit, not a single app-wide number.* A user can have five dailies with five different streak lengths running in parallel. That's a materially different mental model than Streakly's single, app-wide streak — worth calling out explicitly if you're using Habitica as a reference, since their solutions (below) are built for a different data shape.
- **There's a `user.achievements.streak` counter too** — but it's a *meta-achievement* (incremented every time any daily streak hits a multiple of 21 days, per `scoreTask.js:340`), not the streak count itself. Easy to confuse with the per-task streak field if you're skimming.
- **Streak protection already exists as a spell, not a UI feature**: `user.stats.buffs.streaks` (a boolean) is set by a Wizard-class spell called "Chilling Frost" (`website/common/script/content/spells.js:103-113`) — cast it, and your next unchecked daily won't reset its streak. This is architecturally a *buff flag checked at scoring time*, not a dedicated "streak freeze" object. Relevant if you're designing a similar mechanic: Habitica's version is a consumable, class-gated spell, not a universal, always-available safety net — a different tradeoff than what's described in Streakly's brief (one-tap, unlocked by a lesson, not class-restricted).

---

## 2. Mapping the Comeback Screen to This Codebase

*(Hypothetical — Streakly is a separate codebase. This maps where an equivalent feature would live if it were built inside Habitica's architecture, to inform how you reason about Streakly's own structure.)*

### Where it would live

- **Client:** A new modal/component alongside `yesterdailyModal.vue` in `website/client/src/components/tasks/` — that's the existing precedent for "user returns after a gap" UI.
- **Server:** A new controller action in `controllers/api-v3/tasks.js` (or a new file) to handle the freeze/restore action, plus new logic in `common/script/ops/` (alongside `scoreTask.js`) for the actual streak-restore math, since that's where all scoring logic is centralized — not in the controller.
- **Data:** A new field would be needed on the `Daily` task schema (see Section 3) and likely a new `userNotification` type (`server/models/userNotification.js`) to trigger the in-app prompt.

### What it would touch or depend on

- **Task/streak scoring (`scoreTask.js`)** — any restore logic has to interact with the same code path that currently zeroes a streak on a missed/unchecked daily, or you risk two competing sources of truth for "what is this streak right now."
- **Cron (`server/libs/cron.js`)** — the daily reset job is what determines a daily is "missed" in the first place; the Comeback screen's trigger condition depends on this job's output.
- **Notifications (`userNotification.js`, `pushDevice.js`, `pushNotifications.js` controller)** — both in-app and push notification systems, if the entry point is a notification (as in Streakly's own open question about entry point).
- **Achievements (`achievements.js`, `user.achievements.streak`)** — since streak milestones feed an achievement counter, a "restore" needs to decide whether it also restores/adjusts achievement state, or leaves it alone.

### Blast radius — what else could break

- **Double-counting or achievement corruption:** if a restored streak isn't handled in the same code path as normal scoring, you risk streak milestones (every 21 days) firing incorrectly, or achievement counts drifting from actual streak state.
- **Cron race conditions:** cron is a batch job touching every user's tasks; any restore feature interacting with fields cron also writes needs to be sequenced carefully, or a restore could be silently overwritten by the next cron run.
- **Gold/XP economy:** streak length feeds a scoring bonus (`scoreTask.js:141-144`, "streak bonus: +1% per streak") — in Habitica's case this ties to in-game currency. A bug in restore logic that sets an incorrect streak value doesn't just look wrong, it can improperly grant or deny economic rewards. Streakly likely doesn't have this exact exposure, but it's the shape of risk to look for: *what else silently reads this same field?*

---

## 3. What Would Affect How You Write the Spec

### Data that doesn't exist yet

- **A "streak freeze" object/field does not exist as a standalone concept in this codebase.** The closest analog (`user.stats.buffs.streaks`) is a boolean buff flag tied to a specific spell cast, not a reusable, general-purpose "freeze" entity with its own state (available/used/expiring). If Streakly's data model is similarly a simple `streak: Number` on the user or task, you likely need **new fields**: something like `streakFreezeAvailable`, `streakFreezeExpiresAt`, and a way to record *that* a freeze was applied (for analytics/debugging) — none of which exist for free just because a streak counter does.
- **A "best streak ever" stat isn't visible as its own field in the areas inspected** — only the current, live `streak` counter. If Streakly's Comeback screen needs "your best streak ever" as shown in the prototype, that's likely a **separate historical-max field** that needs to be written whenever a streak is broken (capture the max before reset) — not something you can derive after the fact once a streak has already reset to zero.

### Constraints worth calling out in the ticket

- **Streak logic lives in shared scoring code, not in one obvious place** — any spec should explicitly say "this must integrate with the existing scoring path," or engineers may reasonably build a parallel, disconnected system that drifts out of sync.
- **A batch/cron job determines "missed"** — the spec needs to be explicit about timing: is the Comeback screen triggered by the same job that resets the streak, or does it run independently and risk a race/lag?
- **Existing streak-protection features (even if only conceptually, via Habitica's spell) suggest this space isn't empty** — worth explicitly stating in the ticket whether this feature replaces, coexists with, or is mutually exclusive with any existing forgiveness mechanic in Streakly's own codebase, so engineers don't have to guess.

### The one thing engineers will ask before kickoff

**"Where does 'best streak ever' get written, and does it already exist anywhere in our data — or do we need a new field and a migration/backfill for existing users?"**

This is the question worth having a real answer to before scheduling kickoff. Based on this exploration, the honest answer for a codebase shaped like Habitica's would be "it doesn't exist yet, and existing users would show 0 until their next streak break" — a real product decision (do we backfill somehow, or accept a blank slate for existing users?) that needs to be resolved before Raj can put a sane estimate on the ticket.
