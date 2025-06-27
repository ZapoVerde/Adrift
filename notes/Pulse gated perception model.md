# Pulse-Gated Perception Model

## 📍 Status: Locked

Perception in Adrift is not continuous. It is event-driven and aligned to a global simulation pulse. Actors only reassess their awareness of the tactical map under specific conditions related to their action timing and the pulse system.

---

## 🎯 Core Principles

* **Perception is not passive.** It only occurs when an actor engages the simulation to act.
* **Perception is reassessed at action start** — every actor sees the world anew when beginning an action.
* **Perception may also be reassessed mid-action** — but only on **pulse-aligned ticks**, and only if the action is interruptible.
* **The global pulse occurs every 10 ticks.** It serves as an opportunity for long-running actions to reassess their environment.
* **Non-interruptible actions do not reassess mid-action**, even if pulse ticks occur.

---

## ⏱️ Timing Behavior Table

| Actor    | Action Duration | Reassesses On...                | Notes                                      |
| -------- | --------------- | ------------------------------- | ------------------------------------------ |
| Superman | 1 tick          | Every tick                      | Fast actor — acts and perceives constantly |
| Villager | 10 ticks        | Tick 0                          | Action finishes before next pulse          |
| Ogre     | 30 ticks        | Tick 0 + 10 + 20                | Reassesses mid-action via pulses           |
| Sniper   | 30 ticks        | Tick 0 only (non-interruptible) | Cannot adapt mid-scope — locked in         |

---

## 🧠 Reassessment Logic

```python
def maybe_reassess_perception(actor, tick):
    if tick == actor.next_action_tick:
        reassess_perception(actor)
    elif tick % 10 == 0 and actor.action_end_tick > tick:
        if actor.current_action.interruptible:
            reassess_perception(actor)
```

* `actor.next_action_tick`: tick when the actor begins a new action
* `interruptible`: boolean flag per action (default = True)
* Pulse ticks (every 10) trigger reassessment **only if the action is still ongoing and allows it**

---

## 🔧 Action-Level Interruptibility

Each action has a flag:

```python
class Action:
    def __init__(...):
        self.interruptible = True
```

Used to define tactical rigidity:

* **Sniper shot** → `interruptible = False`
* **Swing weapon** → `interruptible = True`
* **Reload** → `interruptible = True`

---

## 🧠 Tactical Implications

| Behavior                       | Outcome                                                 |
| ------------------------------ | ------------------------------------------------------- |
| Fast actors (1–2 tick actions) | See constantly — always up-to-date                      |
| Long but interruptible actions | May reassess and abort mid-action if battlefield shifts |
| Non-interruptible actions      | Tactical commitment — high risk, high payoff            |
| Stealth and timing             | Exploitable windows between enemy perception updates    |

---

## ✅ Summary

* Actors do not perceive the world passively
* Perception is reassessed **at action start**, and again on **10-tick pulses** if the action is **still in progress and interruptible**
* This model supports long actions, tactical commitment, and stealth timing windows

This entry governs all future logic related to tactical awareness, vision resolution, and reaction timing.
