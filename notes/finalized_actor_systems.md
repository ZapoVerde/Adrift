
# ✅ Actor Autonomy, Faction Dynamics, and Tactical Commands

This document summarizes all finalized, locked-in, or committed decisions made in the chat regarding actor behavior, faction interactions, and tactical command structures.

---

## 🧍 Player vs Actor Distinctions

- **No structural difference** is required between player and actors at base level.
- The game supports both **MC mode** (single-player-character) and **sandbox mode** (multiple controllable actors).
- MC mode implies **game over on MC death**.
- Sandbox mode may allow continued control across remaining actors.
- Differences emerge **only in UI, messaging, and input controller**.

---

## 🧠 Cognitive Load & Fog-of-War Visibility

- **Only the player** sees and controls tactical zone observation.
- AI actors do **not generate observation or fog-of-war updates** by default.
- Shared visibility is supported only via specific items **and** skill requirements.
- Example: Tech-based vision gear requires both equipment and relevant skill to contribute to shared vision.
- This prevents unearned perfect coordination without cost or tech justification.

---

## 🐶 Partial Control Actors

- Three classes of followers:
  1. **Allies** – fight alongside you but are not commandable.
  2. **Followers** – conditionally loyal, may refuse commands.
  3. **Low-cognition units** – pets, robots; receive simple commands, act with autonomy.
- AI model should support **team-based tactics**, not bespoke per-follower logic.
- Controller modes: `human`, `ai`, `semi_autonomous`, `delegated`.

---

## 👤 MC vs No-MC Mode

- Explicit support for both playstyles:
  - **MC Mode**: player controls a named, central character. Game ends on death.
  - **No-MC Mode**: player may control multiple pawns. Game continues if one dies.
- MC mode requires:
  - `player_actor_id` to track the MC
- Sandbox mode requires:
  - `player_identity` object for global player-affiliated reputation

---

## 🧭 Faction-Based Reputation System

- No global fame or infamy metric.
- Actors log local events: e.g. “Timmy stole from Fred”
- Victim’s faction responds by increasing hostility **to actor's faction**
- Reputation propagates **through faction**, not world-wide memory.
- Local consequences, emergent diplomacy, and betrayal are all supported.

---

## 🔥 Faction Disavowal

- A faction may **disavow** or expel one of its members to de-escalate conflict with another faction.
- Triggered by:
  - Hostile event by actor
  - Victim faction power superiority
  - Faction diplomatic traits (e.g. low pride, high pragmatism)
- Actor receives `disavowed_by` tag.
- Dialogue, trust, and social access are all affected.
- Designed for systemic betrayal, outlaw gameplay, or emergent quests.

---

## 🎯 Tactical Delegation MVP

- Delegation is scoped to **combat/tactical intent**, not job systems.
- Tasks are assigned via:
  ```python
  actor["current_task"] = {
      "type": "scout",
      "target_zone": "room_A",
      "fallback": {"type": "hold", "position": (3, 2)}
  }
  ```
- Supported tasks:
  - `scout`
  - `guard`
  - `follow`
  - `charge`
  - `hold`
  - `patrol` (looping optional, fallback supported)
- Delegated actors use `controller = delegated`
- Patrolling is a repeatable behavior, not a schedule
- All feedback routed through `messaging.py`

---

## 🪓 Explicitly Rejected or Deferred Systems

- ❌ Global fame/infamy
- ❌ Actor-to-actor gossip or automatic memory propagation
- ❌ RimWorld-style job tables or work priorities
- ❌ Full actor schedule logic (e.g. sleep/eat/work)
- ❌ Task queues (MVP only supports a single task)
