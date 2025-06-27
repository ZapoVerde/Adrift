
# Design Journal (Structured Full Version)

This is the authoritative reference for all finalized systems, structured in full sections for traceability, clarity, and system integration.

---

## 1. Architecture and Conventions

**Status:** Locked

**Rationale:** Ensures project consistency, modifiability, and testability as scope expands.

📐 Architectural Implications:
- Modular layout: logic in `utils/`, flow in `core/`, data in `definitions/`
- All files begin with `# filename.py`
- No raw strings in logic — all user-facing text routed through `messaging.py`

🔄 Flow Integration:
- `engine.py` only controls phase flow; no embedded logic
- All debug routed through `debug_utils.debug()`
- Configuration toggles defined in `config.py`

🧠 Design Philosophy:
- Prioritize clarity, traceability, and extensibility
- Encourage long-term maintainability

📝 Unstructured Notes:
- Inherited from legacy Adrift repo, cleaned and hardened through 2025 redesign

---

## 2. Stealth and Detection

**Status:** Locked

**Rationale:** Establishes perception-driven encounter system grounded in skills and actor scale.

📐 Architectural Implications:
- PER (stat) governs Range of Perception
- `stealth`, `observe`, `search` are skills
- Actor size scale: 1 (ant) to 10 (elephant)

🔄 Flow Integration:
- Passive perception uses PER × observe
- Active searching uses PER × (observe + search bonus)
- Detected targets are surfaced to tactical view

🧠 Design Philosophy:
- Symmetric stealth model — works for both player and AI
- Encourages scouting, concealment, and information asymmetry

📝 Unstructured Notes:
- Size scaling supports small swarms and large monsters
- Useful in AI scripting for ambush logic and detection thresholds

---

## 3. Zone and Vision System

**Status:** Locked

**Rationale:** Supports realistic fog-of-war, range-limited vision, and light-dependent behavior.

📐 Architectural Implications:
- Zones are linked (x, y) tiles with automatic adjacency
- Visibility determined by light tier
  - Clear = light ÷ 2, Vague = light

🔄 Flow Integration:
- `trace_visibility_path()` accumulates penalties from fog, fire, etc.
- Actors store `visited_zones` as fog-of-war cache

🧠 Design Philosophy:
- Emphasizes imperfect information and lighting strategy
- Omnidirectional vision — no cone-of-view system

📝 Unstructured Notes:
- Trace path also useful for projectile logic
- Future: include sensory pathing (sound/scent)

---

## 4. Combat Model (2d6 + Modifiers)

**Status:** Locked

**Rationale:** Offers clean scaling, readability, and risk-reward balancing via smooth damage curve.

📐 Architectural Implications:
- Uses decimal-enhanced 2d6 rolls
- Multiplier function:
  ```
  multiplier = 1.72 / (-0.43 × roll + 5.59)
  ```

🔄 Flow Integration:
- Rolls 2–5: miss (0 damage)
- Rolls 6–12: smooth multiplier from ~0.2 to 1.7+
- Multiplier applied to base weapon damage

🧠 Design Philosophy:
- Makes high rolls feel impactful
- Misses and glancing blows remain frequent without being flat

📝 Unstructured Notes:
- May support deterministic called shots in high skill
- Works cleanly with post-roll modifiers and skill effects

---

## 5. Weapon Timing and Stats

**Status:** Locked

**Rationale:** Balances pacing and tactical depth through tick-based action costs and stat dependencies.

📐 Architectural Implications:
- Weapons defined with:
  - `strike_speed_stat`
  - `reload_speed_stat`
  - `control_stat`
  - `size`
  - `capped_stat` (optional)

🔄 Flow Integration:
- Strike and reload actions consume ticks
- Timing reduced by high relevant stat (STR, DEX)
- Control affects hit consistency and critical failure rate

🧠 Design Philosophy:
- Large weapons are powerful but costly to ready/fire
- Skill and stat investment rewarded through speedup

📝 Unstructured Notes:
- Supports overheat, jam, or panic mechanics at high tick cost
- May allow interruptible ready phase

---

## 6. Fog of War and Actor Memory

**Status:** Locked

**Rationale:** Models what the player/AI knows vs what is real, allowing narrative tension and informed uncertainty.

📐 Architectural Implications:
- Tile visibility state per actor:
  - `visible`, `seen`, `unseen`
- Memory persists across turns but can degrade in future

🔄 Flow Integration:
- Every turn, actor runs `observe()`
- `visited_zones` updated based on light and RoP

🧠 Design Philosophy:
- Supports ambushes, deception, and partial knowledge
- Keeps memory per-actor to allow hallucinations, fear, confusion

📝 Unstructured Notes:
- May integrate with rumor or fake sightings
- Future: heat/flashback trails for AI prediction

---

## 7. Overkill Weapons

**Status:** Locked

**Rationale:** Introduces narrative drama, supports tactical high-stakes decisions, and rewards opportunistic play.

📐 Architectural Implications:
- Defined in `ITEM_DB` with flags like `overkill: true`
- High stat requirements, extreme effects on crit fail

🔄 Flow Integration:
- Treated as normal weapons in roll logic
- May inflict collateral, backlash, self-injury on failure
- Rare loot category or scenario script injection

🧠 Design Philosophy:
- Designed for cinematic moments, not balance
- Risk-heavy; ideal for siege or desperation use

📝 Unstructured Notes:
- Rocket launcher, orbital lance, unstable plasma
- May breach walls or kill wielder — use sparingly

---

## 8. Tables

### 8.1 Tick Timing Table

| Action           | Ticks |
|------------------|-------|
| Strike (melee)   | 8     |
| Strike (ranged)  | 12    |
| Reload (short)   | 6     |
| Reload (long)    | 10    |
| Ready weapon     | 4     |

### 8.2 Weapon Stat Table (Samples)

| Weapon        | Type   | Size | Strike | Reload | Strike Stat | Reload Stat | Control Stat |
|---------------|--------|------|--------|--------|--------------|--------------|----------------|
| Knife         | Melee  | 1    | 6      | —      | DEX          | —            | STR            |
| Battle Rifle  | Ranged | 3    | 12     | 10     | STR/DEX      | STR/DEX      | PER            |
| Sniper Rifle  | Ranged | 4    | 14     | 10     | STR/DEX      | STR/DEX      | PER            |

---

