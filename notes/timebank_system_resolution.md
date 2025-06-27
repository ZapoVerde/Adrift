## ⏳ Timebank System Resolution – Abandoned in Favor of Deferred Scheduling

### 🧾 Status
**Resolved and Deprecated**

The previously considered "timebank" system — where actors accrue a pool of ticks and spend them over multiple actions — has been rejected in favor of a cleaner, deferred execution model with global pulse support.

No actor holds a persistent reservoir of ticks. Instead, each actor:
- Selects one action at a time
- Commits to an execution duration
- Is placed in the global action queue with a `tick_to_execute`

This eliminates the need for tick accounting or recovery logic and enables consistent, transparent scheduling.

---

### 🧠 Rationale

- Timebanks added unnecessary complexity without increasing clarity or tactical depth
- Resource management (fatigue, stamina, momentum) can be handled through action selection, not tick reserves
- The deferred model better aligns with the core principle of one actor, one action, one execution time
- Combined with the global pulse model, actor reassessment ensures reactivity without needing a banked energy buffer

---

### 🧱 Architectural Implications

- Actor logic no longer requires a `timebank` field or tick regen logic
- Tick resolution is centralized in the action queue, not distributed per actor
- Long-term action planning is handled via rescheduling and mid-action reassessment, not multi-action queuing
- Interrupts and delays are cleaner to handle since they affect one action at a time

---

### 🔄 Flow Impacts

- Actors no longer gain or lose ticks as a persistent resource
- `tick_scheduler` evaluates only scheduled actions and global pulses
- Actors are idle until scheduled or reassessed
- Time pacing is shaped by action duration, not accumulation

---

### ❌ Deprecated Models

- **Fixed-tick Refill**: Rejected due to implicit round logic
- **Per-actor Refill Schedule**: Rejected for unnecessary state tracking
- **Continuous trickle regen**: Rejected for simulation weight and unclear benefit

---

### 📝 Unstructured Notes

- Timebank-like pacing (e.g. stamina/momentum) may return in skill trees or specific actions
- Replaced with structural tick economy where action duration is the pacing constraint
- System remains extensible via pulses, interrupts, conditional actions

