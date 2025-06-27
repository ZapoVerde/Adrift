## 🎯 Tick Scheduler Design – Deferred Execution Hybrid

### 🧾 Status

**Finalized.** This is the locked-in model for actor scheduling and turn flow in the tactical engine.

---

### 🧠 Design Philosophy

Inspired by the "Superman vs Caveman" analogy and admiration for real-time/turn-based hybrid systems (e.g. Door Kickers, Frozen Synapse), this model supports asymmetrical actor speed, tactical planning, and continuous tick-based pacing.

Actors act **one at a time**, and each action has a **tick cost**. The global scheduler simulates time by maintaining a timeline of scheduled actions. There are no rounds. Actors are prompted when they are next eligible to act.

This model supports:

* High-speed characters chaining actions rapidly
* Slow characters taking infrequent, heavy actions
* Interrupts, triggers, and delayed effects naturally
* A neutral scheduler where all actors operate on the same time continuum

---

### ⚙️ Core Model – Deferred Execution Queue + Global Pulse

#### 🧱 Timeline

Time is a continuous counter: `global_tick: int`

A **global pulse** is triggered every 10 ticks (`PULSE_INTERVAL = 10`).

#### 🎭 Actor State:

* `next_action`: planned action (optional, can be decided at execution)
* `action_ready_tick`: when actor becomes available for next action
* `initiative`: rolled at start of combat to break ties

#### 📦 Scheduled Action Queue (priority queue):

Each entry is a tuple:

```python
(tick_to_execute: int, actor_id, action_fn, action_args)
```

The scheduler always pops the soonest event:

1. Advances `global_tick` to `tick_to_execute`
2. Executes the action
3. Prompts the actor to schedule their next action
4. Enqueues the next action at `global_tick + action_duration`

---

### 🧩 Global Pulse Logic (Every 10 Ticks)

At every `tick % 10 == 0`:

* All **Damage-Over-Time (DOT)** and **Heal-Over-Time (HOT)** effects are triggered
* **Statuses** that update periodically (e.g. bleed, poison, regen) resolve here
* **Actors whose next action is more than 10 ticks away** must **reassess** their action:

  * If situation has changed, they may cancel or switch actions
  * If committed, action continues as planned
* In case of **tie resolution** (multiple effects/actors firing at the same tick), actor **initiative** determines priority

---

### 🔍 Rationale

* **No Rounds**: Time flows continuously. No arbitrary reset points.
* **Pulse for Status Effects**: Regular timing without overwhelming queue volume
* **Immediate vs Deferred**: Actions are selected immediately, but resolved later
* **Mid-Action Reassessment**: Long actions may get re-evaluated mid-way
* **Interrupt-Friendly**: Adding an interrupt is as simple as injecting a new item into the action queue

---

### 🧩 Architectural Implications

* Tick queue must be globally accessible and modifiable.
* Actors need no internal clock — just `action_ready_tick`.
* Effects and buffs should store `expires_at_tick` or respond to pulses.
* Paused or stunned actors are handled by simply not scheduling the next action.
* A `run_pulse()` system must iterate through actors and statuses every 10 ticks.

---

### 🚫 Deprecated Models

* **Timebank System**: Rejected in favor of per-action scheduling.
* **Round-Based Flow**: Removed due to artificial synchronization and poor alignment with speed-based asymmetry.
* **Fully Distributed Status Ticks**: Rejected in favor of centralized pulse ticking.

---

### ⏭️ Next Steps

* Implement `tick_scheduler.py` with priority queue loop
* Define action interface: `action_fn(actor, **kwargs)`
* Add `run_pulse()` support every 10 ticks for DOT/HOT logic
* Implement action reassessment logic for long-duration actions
* Build helper functions for scheduling, modifying, and cancelling queued actions
* Establish debug tooling for visibility into future tick timeline
