
# Pulse-Gated Perception Model

### 🧾 Status

**Locked**

Perception in Adrift is governed by a **pulse-driven, action-triggered model**. Actors do **not perceive continuously** — instead, they reassess their awareness of the tactical map at action start and optionally during long actions aligned to the global simulation pulse.

This system balances realism, performance, and tactical commitment:

* **Fast actors** reassess constantly
* **Slow actors** reassess only on key intervals
* **Some actions are uninterruptible**, and ignore perception updates once started

---

### 🧠 Design Philosophy

* Tactical perception is **discrete**, not continuous
* Reassessment only occurs when meaningful (i.e. action start or pulse tick)
* Avoids redundant per-tick updates, scales cleanly with actor count
* Preserves meaningful **reaction windows** and **stealth timing**
* Enforces **commitment under pressure** for long or non-interruptible actions

---

### ⚙️ Core Model – Perception Timing

* All actors reassess perception **at the start of their action**
* If an action **lasts longer than 10 ticks**, a **global perception pulse** (every 10 ticks) allows **mid-action reassessment**
* Actions marked `interruptible = False` do **not** respond to pulses once started

```python
class Action:
    def __init__(self, ...):
        self.interruptible = True
```

```python
def maybe_reassess_perception(actor, tick):
    if tick == actor.next_action_tick:
        reassess_perception(actor)
    elif tick % 10 == 0 and actor.action_end_tick > tick:
        if actor.current_action.interruptible:
            reassess_perception(actor)
```

---

### 📐 Architectural Implications

* Perception resolution logic (`can_actor_see_target`) is only called:

  * When actor starts a new action
  * During long actions (if interruptible and aligned to pulse)
* Vision state is **cached per actor** until next reassessment
* Supports future systems like `observe()`, `search()`, or AI `overwatch`
* Enables stealth via timing: actors can pass through gaps between awareness ticks

---

### 🔄 Flow Integration

* `engine.py` triggers `maybe_reassess_perception()` when advancing actor actions
* `visible_targets` and `visible_tiles` are cached results used during current action
* Interruptible actions may be aborted or modified mid-way based on new visibility
* Non-interruptible actions (e.g. sniper shot) proceed blindly once begun

---

### 🧪 Test Coverage Requirements

* Fast actor (1-tick actions): reassesses every tick
* Slow interruptible actor (30-tick action): reassesses at tick 0, 10, 20
* Non-interruptible action: reassesses only at tick 0
* Ensure correct visibility recalculation on pulse ticks
* Confirm no reassessment occurs outside these bounds

---

### 📝 Unstructured Notes

* Pulse period is fixed at 10 ticks for MVP, could be tunable per actor or context
* Perception reassessment is side-effectful — actor memory and decisions may change
* Interruptibility may later be dynamic (e.g. via panic, stun, or adrenaline states)
* Could expose perception log to UI or AI debug layers
* Snipers, spellcasters, or rituals are good default examples of `interruptible = False`
* Stealth actions may include prediction of opponent’s pulse cycle to time movement