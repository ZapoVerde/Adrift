# 🕒 Adrift Timeflow Models — Unified View

This document defines all currently locked-in time systems in Adrift. These are unified under a single tick-based real-time-with-pause simulation architecture, preserving tactical depth, deterministic logic, and continuous world behavior.

---

## ⏳ Canonical Time Model: Real-Time with Pause

**Status:** Locked

Time in Adrift advances in discrete ticks (e.g. 60 ticks/sec). The game simulates continuously in real time, but the player may pause at any moment. All internal systems respect this pause: actors freeze, timers halt, and no actions resolve.

### ✅ Player Superpower: Pause
- The player is the only entity that can pause time.
- Pause is global and total — no actor or system continues while paused.
- Players can inspect, queue commands, and analyze mid-pause.

### 🧱 Implications
- All time-based logic must respond cleanly to pause state.
- All subsystems operate under a unified tick scheduler.
- Systems may operate on sub-tick (event-driven) or multi-tick intervals, but all respect the global tick clock.

---

## 🔁 Legacy Phase Flow: Conceptual Turn Skeleton

**Source:** `turn_based_flow.md`

Original four-phase structure:
```
Perception → Initiative → Action → Cleanup
```
This model no longer drives runtime, but remains the logical scaffold used to route decision-making and resolve system effects.

### 🎯 Role in Real-Time Context
- **Perception:** triggered by actor readiness or pulse (see below)
- **Initiative:** replaced by individual cooldowns / ready-at timers
- **Action:** resolved immediately or queued per actor
- **Cleanup:** distributed across pulse ticks (e.g. status expiry)

### 🧠 Purpose
- Improves code organization
- Aids test coverage structuring
- Supports clear cause-effect timing for narrative/logging

---

## 💉 Status Effects: Pulse-Driven Resolution

**Source:** `status_effects_pulse_driven_centralised_tick.md`

All persistent effects (bleed, poison, healing, etc.) are resolved by a **central global pulse** that runs every 10 ticks. Effects are not queued per actor — they resolve in batch.

### 🔄 Pulse Cycle
- Occurs every `tick % 10 == 0`
- Iterates over all actors and their `status_effects`
- Applies damage/healing/modifiers
- Decrements duration; removes expired statuses

### 🧠 Advantages
- Deterministic, fair, and scalable
- No per-status timers
- Enables player planning against known pulse timing
- Allows mid-action reassessment for AI/followers

---

## 🔍 Perception: Reassessment Gated by Intent

**Source:** `pulse_gated_perception_model.md` (Clarified)

Actors do **not reassess visibility every tick**. Instead, they update their perception when:
- They **start a new action**
- They are mid-action and the action is:
  - **interruptible**, and
  - exceeds the global pulse interval (10 ticks)

### ✅ Not Magical — Just Sensible
- No real-time omniscience
- Vision updates when actors are *able to act* on it
- Interruptible actions can respond to pulse-based changes (e.g. "enemy appeared")
- Non-interruptible actions (e.g. sniping) commit blind

### 🧠 Design Impact
- Enables stealth play via timing
- Makes long actions meaningful and risky
- Prevents performance issues from over-resolving vision
- Models real-world delay in awareness + reaction

---

## ⏸ Unified Tick Scheduler: Central Loop

All timeflow systems (effects, perception, actor readiness) are coordinated by the `tick_engine.py` loop:

```python
TICK_RATE = 60
paused = True

while True:
    if not paused:
        tick()
    sleep(1 / TICK_RATE)
```

- Global `GameClock` tracks ticks, game time, and can be paused
- Speed scaling (1x, 2x, 4x) supported via multiplier
- Pulses and event queues check tick count for alignment

---

## 🧩 System Interlock Summary

| Subsystem            | Timing Driver             | Respects Pause | Uses Pulse | Notes                                  |
|----------------------|----------------------------|----------------|------------|----------------------------------------|
| Actor Actions        | Tick-based cooldowns       | ✅             | ☐          | Future actions may be reevaluated      |
| Status Effects       | Global pulse (every 10t)   | ✅             | ✅         | Reassessed at intervals                |
| Perception           | At action start, or pulse  | ✅             | ✅         | Caches vision between updates          |
| Dialogue / Events    | Player- or AI-triggered    | ✅             | ☐          | Can be frozen mid-sequence             |
| World Travel         | Tick-scheduled strategic   | ✅             | ☐          | Travel actions resolve per tick        |
| Combat               | Time-continuous            | ✅             | ☐ / ✅     | Reactions / statuses use pulse hooks   |

---

## 🔐 Canonical Design Summary

- Time is **real-time with pause**
- **Tick-based**, but not turn-based
- **Player pause** is sacred and universal
- **Pulses** are for shared-resolution systems (status, perception)
- Legacy turn phases are logical scaffolds, not runtime blocks

All future system designs must integrate cleanly with this time model. Any module that schedules, delays, re-evaluates, or reacts **must declare its tick/pulse alignment**.

