## 🎯 Technique Mutation System – Player-Driven Evolution with Strategic Boosts

### Status: Locked

Techniques are composed of modular components (e.g., effects, triggers, modifiers) and may mutate over time. The system rewards skill use and grants the player mutation opportunities, allowing strategic growth and refinement of their combat style.

---

### 📐 Mutation Mechanics

- **Technique Structure**:
  - `skill`: Origin skill of the technique
  - `trigger`: Optional trigger condition (e.g., low health)
  - `effects`: One or more functional payloads (e.g., push, bleed)
  - `modifier`: Optional damage or timing alteration

- **Mutation Events**:
  - Triggered at **2× the probability** of a skill level-up.
  - Player is presented with **four mutation options**:
    1. **Replace effect** (always available)
    2. **Add effect** (available if skill level ≥ 30)
    3. **Change modifier** (slight chance to remove it)
    4. **Bank this mutation**

- **Replace Effect**:
  - Replaces one effect with another of the same rarity.
  - Never re-offers an effect already present on the technique.

- **Add Effect**:
  - Adds a second effect to the technique.
  - Only available if the relevant skill is level 30 or higher.
  - Effect must not already exist on the technique.

- **Change Modifier**:
  - Replaces the existing modifier with a new one.
  - Small chance to completely remove the modifier (reward event).

---

### 🔁 Technique Evolution: Boost Mechanics

#### Banking System

- Player may select “Bank this mutation” instead of choosing an upgrade.
- Each bank increases a **global counter**: `actor["mutation_bank"]`
- Banks are **not tied to specific skills**.

#### Boosting Offers

- If bank total ≥ 3, player is prompted:
  > “Spend 3 banks to boost next mutation offer for [skill]?”

- If accepted:
  - Subtract 3 from `mutation_bank`
  - Increment `skill_mutation_boosts[skill]` by 1

- Boost effects:
  - **Boost applies only to that skill**
  - **Boost persists** until a mutation offer is accepted for that skill
  - **Players may stack boosts** (double or triple boost)
  - Additional banking is still allowed during a boost

#### Boosted Rarity Tiers

| Boost Level | Available Tiers            | Weight Distribution     |
|-------------|-----------------------------|--------------------------|
| 0           | Common, Uncommon, Rare, Epic | 60 / 25 / 10 / 5         |
| 1           | Uncommon, Rare, Epic         | 50 / 35 / 15             |
| 2           | Rare, Epic                   | 75 / 25                  |
| 3           | Epic Only                    | 100                     |

---

### 💾 Data Model

```python
actor["mutation_bank"] = 5
actor["skill_mutation_boosts"] = {
    "sword": 2,  # This skill has double boost active
    "melee": 0,
}
```

---

### 🔄 Flow Integration

1. **Trigger event** after successful skill use (based on chance)
2. Present player with four mutation options
3. If player banks:
   - Increment `mutation_bank`
   - If total ≥ 3, offer upgrade chance
4. If player accepts a boosted offer:
   - Reset `skill_mutation_boosts[skill] = 0`
5. Apply boost weights during offer generation

---

### 🧠 Design Philosophy

- Mutation is **reward-driven**, not mandatory
- Strategic banking allows **custom pacing** of power growth
- **Boosted rarity** provides high-end upgrades without requiring RNG farming
- Adds a **deliberate layer** of build refinement via player agency

---

This is the full locked system. Future changes must be journaled and justified with changelog + audit entries.
