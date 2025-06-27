## Visibility Score Model – Distance, Light, Size

### 📜 Status

**Locked**

This entry defines the **core visibility resolution model** used by `can_actor_see_target()` to determine whether a target is visible to an observer. It incorporates three finalized components:

* **Distance**: a tiered penalty based on tile distance (angular resolution falloff)
* **Light**: a curved bonus/penalty based on tile light level (lux-like mapping)
* **Size**: a linear bonus/penalty based on actor size (baseline = 5)

These components combine with perception (PER) and stealth (STEALTH) to produce a final `visibility_score`.

---

### 🧠 Design Philosophy

* Model **realistic visual degradation** without hard cutoffs
* Preserve a human-scale perception model using real-world optics
* Keep each component isolated and testable
* Avoid unnecessary abstraction — use additive modifiers
* Ensure high visibility for large, close, well-lit targets

---

### ⚙️ Core Formula

```python
visibility_score = PER - (env_penalty + distance_penalty) - STEALTH + (size - 5) + light_bonus
```

All terms are integers. A positive `visibility_score` implies visibility. Future thresholds may be tuned.

---

### 📊 Component Breakdown

#### 🔹 Distance Penalty (Tiles)

| Tile Range | Meters    | Penalty |
| ---------- | --------- | ------- |
| 0–10       | 0–20 m    | +0      |
| 11–30      | 22–60 m   | +1      |
| 31–60      | 62–120 m  | +3      |
| 61–90      | 122–180 m | +5      |
| 91–120     | 182–240 m | +7      |
| 121+       | 241+ m    | +10     |

#### 🔹 Light Level Bonus

| Level | Lux (est.) | Bonus | Description             |
| ----- | ---------- | ----- | ----------------------- |
| 0     | 0          | -100  | Pitch black (auto-fail) |
| 1     | \~1        | -4    | Moonlight               |
| 2     | \~10       | -3    | Torchlight              |
| 3     | \~50       | -2    | Dim interior            |
| 4     | \~150      | -1    | Poor daylight           |
| 5     | \~300      | 0     | Functional indoor       |
| 6     | \~1,000    | +1    | Good lighting           |
| 7     | \~10,000   | +2    | Optimal vision          |
| 8     | \~30,000   | +1    | Slight glare            |
| 9     | \~60,000   | -1    | Harsh daylight / glare  |
| 10    | \~100,000+ | -3    | Blinding / flashbang    |

#### 🔹 Size Bonus

| Size | Description          | Bonus |
| ---- | -------------------- | ----- |
| 1    | Insect / mouse       | -4    |
| 2    | Cat                  | -3    |
| 3    | Child / crouched     | -2    |
| 4    | Short adult          | -1    |
| 5    | Baseline human       | 0     |
| 6    | Tall person / armed  | +1    |
| 7    | Bulky / large build  | +2    |
| 8    | Beast / armored suit | +3    |
| 9–10 | Elephant / Mech      | +4/+5 |

---

### 📀 Architectural Implications

* All modifiers are computed during `can_actor_see_target()` resolution
* Trace penalty from `compute_visibility_penalty_along_path()` adds env\_penalty
* Distance and size modeled from angular vision principles
* Light level drawn from `tile['light_level']`
* Future override hooks possible for species, thermal vision, or implants

---

### ♻️ Flow Integration

* Called during **actor perception phase**
* Used by `observe()` to populate `visible_tiles` and `seen_things`
* Will inform AI targeting, fog-of-war updates, and stealth mechanics

---

### 🧪 Test Coverage Requirements

* Confirm all tile thresholds return correct penalties
* Validate light level inputs (0–10) map to expected bonuses
* Ensure actor size modifies score correctly
* Check edge cases: size 1 in total darkness at 200m must be undetectable
* Validate additive behavior of all penalties and bonuses

---

### 📝 Unstructured Notes

* Stealth vs PER is pending final definition
* Vision overlays should expose `visibility_score` for debugging
* Blinding and invisibility may modify light or size directly
* This model assumes tactical-scale visibility only (no long-range scouts yet)