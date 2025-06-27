# 🧠 Design Journal

---

## ✅ Locked-In Systems and Philosophies

### ⏱️ Tick-Based Action System

- 1 tick ≈ 1 second (abstract time unit)
- Minimum action time = 1 tick (even for superhuman actors)
- Supports hybrid real-time / turn-based design via event scheduling

### ⚔️ Weapon Timing Model

- Timing and control always governed by **separate stats** (except low-damage exceptions)
- **Melee**: STR (timing), DEX (control)
- **Bows**: STR (timing), DEX + PER (control)
- **Rifles**:
  - .22 Rifle: DEX (timing + control)
  - Bolt-Action & Hunting Rifle: STR/DEX (timing), PER (control)
  - Sniper Rifle: STR/DEX (timing), PER (control)
- **SMGs & PDWs**: STR (timing), DEX (control)
- **Pistols**: STR or DEX (timing), DEX or DEX+PER (control)
- **Ultra-tech (plasma/laser/gauss)**: timing follows modern analogues
  - Recoilless weapons fire 20% faster than modern counterparts

### 🎲 Damage Roll Curve

- Uses 2d6 base roll
- Outcome zones:
  - 2–5: Miss (hard fail, zero damage)
  - 6–8: Graze
  - 9–10: Solid hit
  - 11–12: Critical hit
- Formula:
  ```
  multiplier(roll) = 1.72 / (-0.43 × roll + 5.59)
  ```
- Allows continuous, smooth scaling and supports roll modifiers

### 📈 Stat vs Skill System

- **Skills**: Always influence dice roll (quality of outcome)
- **Stats**: Influence speed (timing) or precision (control), never both for same weapon
- Exceeding stat requirements grants speed or control bonuses
- Failing stat requirements may degrade outcome:
  - Slower timing (low STR)
  - Loss of control (low DEX)
- INT governs complexity (e.g. chainswords)
- PER governs ranged accuracy

### 🔁 Action Queueing

- Queued actions supported (e.g. attack multiple times, repeat reload)
- Repeat actions allowed
- Queue only flushed on:
  - Weapon/ammo stolen
  - Disarm
  - Maiming affecting capability
- Overwatch supported (MVP form: C1, optional future C3 expansion)

### 🕓 Action Model and Tick Economy

- ✅ Adopted **Action-Based Delay Scheduling** as core execution loop
- ❌ Rejected phase-based turn loop in favor of continuous delay queue
- ✅ Tick cost tables locked in by weapon category and tech tier
- ✅ Superman-vs-Caveman test passed: supports large disparity in action speeds
- ✅ Queueing is **player convenience**, AI makes decisions per tick
- ✅ No "out of range" abstractions — projectiles always travel; range impacts accuracy only
- ❗ Parked fractional-tick support in favor of batch modeling (e.g. triple-strike)
- ✅ Recoil-less weapons: 20% faster tick costs
- ✅ Rapid fire (blazing revolver, full mag dump) modeled as low-control, low-timing burst
- ✅ Timing table is for **base spec humans** — modifiers applied via skills, stats, tech

---

## 🔜 In-Progress or Deferred

- Techniques: very large system, deferred to separate discussion
- Damage tier and final per-weapon base damage values: pending
- Armor/soak model: pending
- Body zone maiming system: not finalized
- Inventory constraints and weight penalties: deferred

---

## 🧱 Architecture Notes (Previously Locked)

- Messaging routed via `messaging.py` only
- Separation of flow and logic: all core logic lives outside `engine.py`
- All debug output via `debug_utils.py`
- Use of `Zone`, `observe()`, light levels, and perception penalties locked in
- Tactical tiles = 2m x 2m
- Map stored as (x, y) dict with top-left origin
- Static zone labels at generation time

---

## ⚠️ Reminder: DO NOT embed raw messaging or print() calls inside logic modules

