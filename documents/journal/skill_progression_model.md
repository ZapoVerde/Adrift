## 🎯 Skill Progression Model – Probabilistic, Cumulative, and Risk-Gated

### Status: Locked

Actor skills increase through use, but only when the following conditions are met:

* The action is successful
* The skill contributes to the result via tag linkage
* The action carries some inherent risk (e.g. chance of failure or exposure)

XP is accumulated cumulatively and permanently. Each successful skill-tagged action adds XP and triggers a probabilistic level-up roll. There are no thresholds, no bars to fill — only momentum and rising probability.

---

### 📐 Growth Mechanics

* **XP is gained per successful action**, per relevant skill tag

* **XP is never reset** — it accumulates over time and contributes to all future level-up rolls

* On each success:

  ```python
  chance = xp / (xp + difficulty(level))
  ```

  If this roll succeeds, the skill level increases by 1

* The `difficulty(level)` function grows exponentially:

  ```python
  difficulty(level) = base_difficulty * (growth_factor ** level)
  ```

  Sample values:

  * `base_difficulty = 100`
  * `growth_factor = 2.0`

* This model ensures:

  * Low levels are fast but not free
  * High levels are rare and meaningful
  * Skill growth remains continuous, with **no hard caps**
  * **Soft caps emerge naturally** from the curve, typically near level 50+

---

### 🎭 Skill Impact on Rolls

* Each skill level contributes **+0.01** to rolls involving that skill’s tag
* Most items/actions involve 3–5 tags
* Roll bonuses of +0.30 to +1.50 are typical, but not capped
* **No roll bonus cap** is enforced — stacking is limited by careful tag structure, not mechanical ceilings
* Result: more skill levels → better odds → more progression → smoother, richer success curve

---

### 🕵️ Stealth XP Logic

* Stealth XP only triggers during **tile-to-tile movement** that causes a detection check
* Remaining still or hiding in a corner will never generate XP
* Detection chance must be non-trivial to qualify (optional threshold)
* Repeating the same stealth route degrades XP rewards via contextual memory

This guarantees stealth growth comes from **intentional, active navigation under threat**, not idle proximity.

---

### ⚠️ Anti-Farming Defenses

The system inherently deters abuse through design:

1. **Movement-Gated Checks** – Trivial loops (e.g. spinning in place) do nothing
2. **Success-Only Gain** – Failed actions grant no XP
3. **Critical Failures Exist** – Repetitive low-skill use incurs increasing risk

> There is no need for XP decay — the system resists overuse via **diminishing returns** and **failure consequences**.

---

### 💬 Feedback Messaging

Every XP gain triggers a context-aware message from `messaging.py`, tied to skill and level tier.

Example for `bolt_action`:

* Level 0–4: *"You fumble with the bolt... but it gets smoother."*
* Level 5–14: *"Your shoulder begins to anticipate the recoil."*
* Level 15–29: *"You brace the rifle like you've done it a dozen times."*
* Level 30–49: *"The bolt glides under practiced fingers."*
* Level 50+: *"You could cycle this rifle blindfolded."*

This system reinforces **progression as story**, not as math.

---

### 🔍 Design Philosophy

* **No deterministic XP bars**: every success is a roll, not a guarantee
* **No grind loops**: context-sensitive gates eliminate safe-farming
* **Crit fails create risk**: low-skill spam is self-punishing
* **No skill cap**: exponential scaling naturally curbs runaway growth
* **No bonus cap**: tag architecture controls how much can influence a roll
* **Frequent, satisfying level-ups**: level 1 to 50+ feels impactful and clear

---

### ✅ Implementation Hooks

* `skill_utils.py`:

  * `record_xp(skill_name, actor, context)`
  * `check_level_up(skill_name, xp, level)`

* `stealth_utils.py`:

  * `resolve_stealth_check(actor, observers, moved_tile)`
  * `award_stealth_xp_if_successful()`

* `messaging.py`:

  * `get_skill_feedback(skill_name, level)`
  * `queue_feedback_message(actor, message)`

---

### 📌 Unstructured Notes

* Player-facing UI may optionally show XP bars or probability curves
* Traits may influence XP gain rate or crit fail odds
* All gain events should include narrative feedback
* TODO: perform Monte Carlo testing to validate probabilistic pacing and detect anomalies