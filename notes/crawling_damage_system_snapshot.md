# ✅ Crawling Damage + Weapon System Snapshot (June 2025)

---

## 🎲 ROLL SYSTEM

* **Base roll**: 2d6
* **Modifiers**: Stats, skills, techniques modify the total roll (can exceed 12)
* **Baseline anchor**: A roll of **9 = ×1.0 multiplier**
* **Final damage formula**:

```python
damage = base_weapon_damage × roll_quality_multiplier × (1 + damage_mods)
```

* Where:

  * `base_weapon_damage`: Defined per weapon (at roll 9)
  * `roll_quality_multiplier`: Derived from curve below
  * `damage_mods`: Additive bonuses from stats/skills/traits

---

## 📈 DAMAGE MULTIPLIER MODEL

* Rolls ≤ 5: ×0.0 (miss)
* Rolls 6–12+: Multiplier scales inversely to roll probability, using:

```python
multiplier(roll) = 1.72 / (-0.43 × roll + 5.59)
```

* Roll 6 ≈ 0.40
* Roll 9 = 1.0
* Roll 12 ≈ 4.0
* Smoothly supports decimal rolls from stat/technique bonuses

---

## 🎯 BODY ZONE MODEL

* **Flat, weighted zone system** (no nesting)
* Each zone has:

  * `coverage_weight`: For hit probability
  * `hp`: Damage threshold
  * `vital`: Whether zone causes death if destroyed
  * `tags`: Functional purpose (e.g. `grasp`, `sight`, `movement`)

### Sample Zones

| Zone        | HP | Weight | Vital | Tags               |
| ----------- | -- | ------ | ----- | ------------------ |
| Head        | 8  | 10     | ✅     | sight, brain       |
| Eye (L)     | 2  | 4      | ❌     | sight              |
| Jaw         | 3  | 3      | ❌     | speech             |
| Neck        | 4  | 3      | ✅     | breathing          |
| Torso       | 12 | 30     | ✅     | core               |
| Arm (L)     | 6  | 6      | ❌     | limb               |
| Hand (R)    | 3  | 3      | ❌     | grasp              |
| Fingers (R) | 2  | 2      | ❌     | fine\_manipulation |
| Leg (R)     | 6  | 6      | ❌     | movement           |
| Foot (L)    | 3  | 2      | ❌     | balance            |

---

## 🦴 FUNCTIONAL DEPENDENCIES

* Zones are **functionally linked** (not structurally nested)
* Maiming a parent zone invalidates all dependents

### Sample Dependency Tree

```python
"fingers_R": ["hand_R"],
"hand_R": ["arm_R"],
"eye_L": ["head"],
"jaw": ["head"]
```

### Example Logic

```python
is_functional("fingers_R")  # False if hand_R or arm_R is maimed
```

Used to determine if actions (e.g. grasping, aiming) are possible.

---

## 🔫 WEAPON DAMAGE SCAFFOLD

* Uses **descriptive archetypes**, not calibers
* `base_damage` is the amount dealt on a roll of 9
* Multiplier curve scales result up or down

### Sample Archetypes

| Weapon         | Base Dmg | Notes                         |
| -------------- | -------- | ----------------------------- |
| Target Pistol  | 6        | Weak, rarely maims            |
| Service Pistol | 10       | Can maim on high rolls        |
| Hunting Rifle  | 16       | Good stopping power           |
| Shotgun (slug) | 24       | Maims limbs/torso on 9+       |
| Sniper Rifle   | 28       | Headshot = death              |
| Plasma Rifle   | 40       | Graze = maim; crit = overkill |

---

## ⏱️ WEAPON SPEED MODEL (DESIGN ONLY)

* Each weapon will have a `base_speed` (e.g. 1.0 to 3.0)
* Speed is influenced by user stats:

  * STR/DEX for melee
  * DEX/PER or INT for firearms (based on tech)
* Techniques and encumbrance may affect timing
* Timing determines **true DPS**, not just action cost

---

## 🔐 SYSTEM DESIGN PRINCIPLES

* Flat zone model: no nested damage propagation
* Maim = damage ≥ zone HP
* Wound = damage < zone HP (supports bleeding/pain)
* Roll modifier = only affects roll total (not flat damage)
* Damage curve = smooth, anchored at 9, scales to 12+
* Functional loss is handled via dependency tags, not anatomy
* Weapon balance is emergent from: base\_damage × roll × speed × user stats
* No level locking — power comes from skill and stat access

---

## 🧭 DESIGN PHILOSOPHY EXTENSIONS

* **Descriptive weapon categorization** (e.g. "target pistol", "sniper rifle") is used instead of calibers or numerical classes.
* **Roll of 9 is the universal tuning anchor** — all weapon base damage is defined at roll 9, which maps to ×1.0 multiplier.
* **Damage multiplier model is continuous** and supports decimal values and rolls above 12 (e.g. 10.3, 13.1) using the locked multiplier formula.
* **Weapon and damage balance is deferred** — placeholder base damage values are acceptable, final tuning will occur later based on functional testing and system interactions.
