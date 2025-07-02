# 🧠 Adrift Architecture — Conceptual Status Report

_Last updated: 2025-07-01_

---

## ✅ HIGH-LEVEL SYSTEM OVERVIEW

### 🌍 WORLD LAYER  
**Purpose:** Generate and simulate the physical world environment.

| Subsystem     | Status | Notes |
|---------------|--------|-------|
| Zones & Biomes | ✅     | Fully implemented in `floorplan_generator`, `discovery`.
| Dungeons       | ✅     | Procedurally generated tactical floors.
| Towns & Cities | 🟡 GAP | Concept exists; lacks simulation or metadata.
| Factions       | 🟡 GAP | Tiers (T1–T5) defined in journal, not modeled in code.

---

### 🧍 ACTOR LAYER  
**Purpose:** Represent player, NPCs, and their internal state.

| Subsystem        | Status  | Notes |
|------------------|---------|-------|
| Visibility Memory| ✅       | Implemented via `observe()` and zone visit tracking.
| XP & Skill Tree  | ✅       | Probabilistic learning and technique mutation.
| Followers        | 🟡 GAP  | No structure for recruiting, controlling, or storing followers.
| Social Stats     | 🟡 GAP  | No charm/persuasion/leadership mechanics.
| Loyalty Tracking | 🟡 GAP  | Not yet modeled; required for betrayal or morale systems.

---

### 🎮 GAME FLOW LAYER  
**Purpose:** Drive per-turn logic, decisions, and world advancement.

| Subsystem         | Status | Notes |
|-------------------|--------|-------|
| Turn Phases       | ✅      | Perception → Initiative → Action → Cleanup pipeline.
| Quest Hooks       | 🟡 GAP | No quest scheduling, progression, or flow scaffolding.
| Follower Commands | 🟡 GAP | Would require partial AI override / action injection.
| Mutation Flow     | ✅      | Fully implemented and tested.

---

### 🧠 SOCIAL SYSTEMS  
**Purpose:** Enable interpersonal gameplay and dynamic reactions.

| Subsystem         | Status  | Notes |
|-------------------|---------|-------|
| Relationships     | 🟡 GAP  | No affinity or emotional memory structure.
| Persuasion System | 🟡 GAP  | No skill rolls, social resistance, or reaction evaluation.
| Hostility / Betrayal | 🟡 GAP  | Not tied into loyalty or faction alignment.

---

### 📜 QUEST ENGINE  
**Purpose:** Generate meaningful tasks, goals, and story arcs.

| Subsystem         | Status  | Notes |
|-------------------|---------|-------|
| Procedural Quests | 🟡 GAP  | System outlined; no generator implemented.
| Authored Hooks    | 🟡 GAP  | No support for pre-authored arcs or triggers.
| Faction Interlocks| 🟡 GAP  | Quests not influenced by or bound to factions.

---

### 🏛️ FACTION SYSTEM  
**Purpose:** Drive macro-level conflict, influence, and world evolution.

| Subsystem         | Status  | Notes |
|-------------------|---------|-------|
| Tiered Factions   | ✅       | Described in journal: T1 (indigenous) to T5 (imperials).
| World Integration | 🟡 GAP  | No zone ownership or political impact modeled.
| Interfaction Goals| 🟡 GAP  | No simulation or inter-faction AI.

---

### 💬 MESSAGING SYSTEM  
**Purpose:** Provide feedback to player across all systems.

| Subsystem         | Status  | Notes |
|-------------------|---------|-------|
| Combat Feedback   | ✅       | Routed through `messaging.py`.
| Mutation Narration| ✅       | Full narration for evolution/mutation events.
| Quest/NPC Dialogue| 🟡 GAP  | No dialogue engine or interaction scaffolding.

---

## 🚨 GAP CLUSTERS

### 1. **Social Simulation**
- No `SocialContext` or relationship model.
- No way to persuade, intimidate, charm, or betray.

### 2. **Quest Infrastructure**
- No timeline model, no issuer/resolver logic.
- No reward tables, stage tracking, or fail conditions.

### 3. **Faction Influence**
- No zone ownership or influence propagation.
- No resource flow, conquest, or diplomacy simulation.

### 4. **Follower Management**
- No morale, command structure, or AI override logic.
- No UI support for controlling groups.

---

## 🎯 NEXT STEPS

### 🔹 Phase 1: Social Foundations
- Create `SocialContext` object per actor
- Add `reputation`, `affinity`, and `tags` to track social status
- Implement `roll_social_check(actor, target, skill)`

### 🔹 Phase 2: Faction Scaffolding
- Create `Faction` data model (tier, goals, regions)
- Assign zone ownership metadata
- Add passive influence propagation

### 🔹 Phase 3: Quest Engine Stub
- Define `QuestStub`: issuer, target, requirements, reward
- Integrate with phase loop to trigger quest updates

### 🔹 Phase 4: Follower Model
- Flag actors as `follower`
- Add loyalty/morale field
- Enable basic command routing

---

## 🧠 Architectural Principle
> "Every new system must be testable, narratable, and linked to actor or world state."

This ensures extensibility without dead ends or unreachable logic.

---

## ⏲️ Maintenance Reminder
🔁 **Refresh the Entity Graph regularly** as the source of truth.

