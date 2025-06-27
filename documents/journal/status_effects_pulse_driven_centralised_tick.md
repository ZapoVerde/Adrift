## 💉 14. Status Effect System – Pulse-Driven, Centralized Tick Model

### 🧾 Status

**Locked**

All ongoing effects (e.g. poison, bleed, burn, regeneration) are applied at fixed intervals via a centralized global pulse system. Individual actors do not carry per-effect timers or independent ticking status logic.

All effects that persist over time are handled uniformly during the global pulse, which occurs every 10 ticks. These effects are not scheduled individually into the action queue.

If an actor's scheduled action is set to resolve more than 10 ticks into the future, they pause at the pulse interval and reassess intent. This ensures actions remain valid in the face of changing battlefield conditions.

This model prioritizes clarity, performance, and deterministic behavior in tactical simulation.

---

### 🧠 Design Philosophy

Status effects are a core tactical mechanic. We aim for:

* Consistent timing: every status of a given type (e.g. poison) ticks at the same global interval
* Simplified memory: actors do not track internal timers per effect
* Uniform behavior: DOT and HOT effects are resolved globally and simultaneously
* Performance scaling: avoids queue spam from hundreds of independent effect timers
* **Reactivity during long actions**: by reassessing any action longer than 10 ticks, actors can adapt if the situation changes (e.g. allies die, targets move, status worsens)

This model cleanly separates tactical status simulation from the deferred action queue while preserving precise timing and intelligent actor responsiveness.

---

### ⚙️ Core Model – Global Pulse for Status Effects

* The scheduler triggers a **global pulse every 10 ticks** (`tick % 10 == 0`)

* All actors are scanned during this pulse

* All active status effects on all actors are processed

* Effects apply damage, healing, or modifications during this sweep

* No per-effect timers or queue entries are used

* Actors with scheduled actions that will resolve **more than 10 ticks after the current pulse** are flagged for reassessment

  * AI may cancel or replace actions based on current threats or priorities
  * Player-controlled actors may be prompted or auto-reevaluated depending on settings

---

### 📐 Architectural Implications

* Each actor stores a list of `status_effects`, each with:

  * `type` (e.g. poison, bleed, burn)
  * `source` (optional, for attribution)
  * `duration` (in pulses, not ticks)
  * `intensity` (e.g. damage per pulse, stack count)

* The pulse system iterates over all actors and their status\_effects

* Statuses resolve their effect and decrement their remaining pulse duration

* Statuses are removed when duration hits 0

* Global pulse is coordinated with the tick scheduler and combat loop

* Tie resolution uses actor initiative when simultaneous effects occur

* No status-related actions are inserted into the tick queue

* Actor action reassessment hooks must be callable from the pulse context

* Optional AI logic modules may respond with revised plans or fallback behavior

---

### 🔄 Flow Integration

* `tick_scheduler` calls `run_pulse()` every 10 ticks
* `run_pulse()` iterates through all actors and status effects
* Damage/healing is applied
* Expired effects are pruned
* Actor actions scheduled to complete more than 10 ticks later are re-evaluated and may be canceled or replaced

---

### 🧠 Design Philosophy

* Effects should be **visible, predictable, and deterministic**
* Status logic is unified and compact
* Avoids surprises from out-of-phase DOT timing
* System is scalable and performant for many actors with many statuses
* Long actions are not blindly followed through — actors retain agency

---

### 📝 Unstructured Notes

* Status icons can optionally pulse in sync with effect timing
* Future systems may hook into the pulse (e.g. morale checks, zone triggers)
* Status sources are preserved for death attribution, logs, or achievements
* Optional "next pulse preview" could show players what's about to resolve
* AI modules can evolve to schedule conditional reassessments in reaction to pulse outcomes