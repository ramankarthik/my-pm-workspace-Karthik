# Objection Log: Streakly Comeback Screen PRD

Pressure-testing [docs/prd.md](prd.md) against [stakeholders/raj.md](../stakeholders/raj.md), [stakeholders/marcus.md](../stakeholders/marcus.md), and Tom R.'s real interview ([02-research/interview-synthesis.md](../02-research/interview-synthesis.md)).

## 1. Raj (Engineering Lead)

**Hardest question 1:** "'Best streak ever' doesn't exist as a field — the PRD says that outright. Before I put an estimate on this, has anyone actually decided how we backfill existing users, or does every current user just start at a 0 best-streak the day this ships? Because those are very different tickets, and right now I don't have an answer to size against."

**Hardest question 2:** "You're naming Day-7 retention as the primary success metric, but there's no experiment design in this doc — no holdback percentage, no test duration, no sample size. I've asked this before and I'm asking it again: how will we actually know if this worked? I can build the feature, but I can't tell you what 'done' means for QA without a measurement plan attached to it."

## 2. Marcus (Head of Product)

**Hardest question 1:** "There's no rollout timeline anywhere in this document. I've said before I need one before I'll commit sprint time to this — when does this actually ship, and what happens if it slips past the date I need for Q3?"

**Hardest question 2:** "This tells me what we're building, but not what it costs us to wait. If we hold this a quarter instead of shipping it, what happens to the Day-7 number specifically — not retention in general, the actual number this PRD says we're targeting? I need that before I can prioritize this against everything else competing for the same sprint."

## 3. Tom R. (Churned User — broke a 12-day streak, switched to Duolingo)

**Hardest question 1:** "Why do I have to do a lesson before I get my streak back? I never asked to earn forgiveness — I asked for it to exist. Making me do something first still feels like a hoop, not a fix. That's not what made me leave Duolingo's freeze feel forgiving — theirs was just *there*."

**Hardest question 2:** "The thing that actually made me quit was the notification — 'you lost your streak,' sent right when I was already feeling bad. This PRD explicitly says fixing that notification is *not* in scope. So what happens to me in this new version — do I still get the same gut-punch message, and only *then* see this nicer screen after the damage is already done? If the trigger doesn't change, I'm not sure this reaches me before I've already decided to leave."

---

## Which Objection Is Most Likely to Kill the Initiative

**Tom's second objection.** Raj's and Marcus's objections are real, but both are process gaps — a missing data-migration decision and a missing timeline are things that get resolved with a conversation and a follow-up, not things that threaten whether the feature is the right idea. Tom's objection is different in kind: it points out that the PRD's own **Non-Goals explicitly exclude the exact moment that caused his churn** (the notification). That means this feature could ship perfectly, on time, fully spec'd, and still fail to reach a user like Tom before he's already decided to leave — because the fix arrives *after* the harm the harsh notification already did. That's not a delivery risk, it's a validity risk to the core premise: if the trigger event stays untouched, the Comeback screen may be solving a problem after the user most likely to churn has already disengaged from seeing it at all. Worth addressing directly in the PRD — even if the notification-tone fix stays a separate workstream, the sequencing/timing relationship between "harsh notification" and "later, nicer screen" needs an explicit answer before this ships, not an assumption that fixing the aftermath is enough.
