
# ✅ Finalized Design Elements — Combat Timing and Weapon Model

This document summarizes all confirmed decisions made during the design process for the action timing, stat influences, and foundational combat model.

---

## ⏱️ Tick-Based Action System

- **Tick = ~1s equivalent** (abstract time unit)
- **Minimum Action Time = 1 tick**
- Actions are scheduled with tick-delay.
- Fast actions (e.g. hasty pistol shots) modeled as low-tick cost.
- Actions like bandaging take up to 20 ticks.
- Superhuman actors can perform multiple actions in the time it takes others to do one.
- Real-time/turn-based hybrid support through event-driven scheduling.

---

## ⚔️ Weapon Timing Tiers (Locked)

Weapons grouped and timed by tech tier and complexity:

### Melee
- **Control:** DEX
- **Timing:** STR

### Bows
- **Control:** DEX + PER
- **Timing:** STR
- Shortbow, Longbow, Compound bow defined
- Final bow timings doubled from initial proposal

### Thrown
- **Control:** DEX
- **Timing:** STR or DEX based on weight

### Firearms (General Rules)
- **Control and Timing are stat-separated**
- **Low-damage weapons** (e.g., .22) may double dip DEX for both timing and control
- **Control** is mostly PER for guns
- **Timing** is STR or hybrid STR/DEX

### SMGs & PDWs
- Merged into single category
- Short range, fast fire
- Timing = STR, Control = DEX

### Pistols
- Revolver: STR-timed, DEX-controlled
- Pocket: DEX-timed/controlled (low damage cap)
- Auto pistol: STR-timed, DEX + PER control

### Rifles
- Bolt-Action, Hunting Rifle: **STR/DEX timing**, PER control
- Sniper Rifle: **STR/DEX timing**, PER control
- .22 Rifle: DEX timing + control

### Shotguns
- Pump & Break-action differentiated by complexity
- Reload time tripled from early estimates

### Ultra-tech
- Plasma, Laser, Gauss weapons modeled
- Recoil-less weapons fire 20% faster than gunpowder analogues

---

## 🎲 Hit Resolution Curve

- 2d6-based roll
- Rolls partitioned:
  - 2–5: Miss
  - 6–8: Graze
  - 9–10: Solid
  - 11–12: Critical

- Formula:
  ```
  multiplier(roll) = 1.72 / (-0.43 × roll + 5.59)
  ```
  Used for non-zero rolls to produce a smooth curve

---

## 📈 Stats & Skills Model

- **Skills always affect roll outcome**
- **Stats**:
  - Timing: governs speed
  - Control: governs hit quality
  - Never shared unless low damage
- STR = speed for heavy weapons
- DEX = control for fine weapons
- PER = ranged accuracy
- INT = complexity handling (chainsword, etc.)
- Exceeding stat minimums gives benefit
- Falling short imposes penalty (not a binary block)

---

## 🔁 Action Queuing

- Supported: multiple queue, repeat action, overwatch (MVP: c1, optional c3)
- Missed attack doesn’t cancel queue unless critical conditions hit:
  - Weapon lost
  - Ammo stolen
  - Actor disarmed or maimed

---

## 📝 Notes & Placeholders

- Techniques = future thread
- Damage curves = under development
- Inventory management deferred
- Body part system and maiming not finalized
- Full accuracy and cover modeling deferred

---
