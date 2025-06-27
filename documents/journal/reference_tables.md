### 📊 Reference Tables

#### 🧍 Body Zone Coverage Weights

| Body Zone  | Coverage Weight | Notes                    |
| ---------- | --------------- | ------------------------ |
| Torso      | 40              | Largest and most central |
| Head       | 10              | High-value, lower chance |
| Arm (L/R)  | 15 each         | Moderate chance          |
| Hand (L/R) | 5 each          | Smaller, still relevant  |
| Leg (L/R)  | 10 each         | Common limb hit          |
| Foot (L/R) | 2.5 each        | Rare, peripheral         |

* Used in `choose_target_zone()` for hit resolution.
* Does not include nesting logic. If arm is destroyed, hand is implicitly affected.

**Status:** Locked
These are standardized baseline values used by multiple systems for consistency and balance. These are fixed during design finalization and may only be altered via formal changelog entry.

#### 📈 Damage Roll → Multiplier Table (Summary)

| Roll | Multiplier | Notes                     |
| ---- | ---------- | ------------------------- |
| 2–5  | 0.00       | Glancing/no hit           |
| 6    | \~0.25     | Minor wound               |
| 9    | 1.00       | Median hit                |
| 12   | \~1.72     | Max result, high overkill |

#### 💡 Light Tier Model (Range Caps)

| Tier   | Clear Zones   | Vague Zones   | Notes                       |
| ------ | ------------- | ------------- | --------------------------- |
| 0      | 0             | 0             | Pitch black                 |
| 1      | 0             | 1             | Faint ember, near blindness |
| 2      | 1             | 2             | Dim candlelight             |
| 3      | 2             | 4             | Weak torchlight             |
| 4      | 3             | 6             | Good torchlight             |
| 5      | 5             | 10            | Well-lit interior           |
| 6      | 7             | 14            | Direct lamplight            |
| 7      | 10            | 20            | Bright exterior dusk        |
| 8      | 14            | 28            | Full daylight               |
| 9      | 17            | 34            | Harsh artificial light      |
| 10     | 20            | 40            | Blinding spotlight          |
| Tier   | Clear Zones   | Vague Zones   | Notes                       |
| ------ | ------------- | ------------- | --------------------------- |
| 2      | 1             | 2             | Dim candlelight             |
| 5      | 5             | 10            | Well-lit interior           |
| 10     | 20            | 40            | Blinding spotlight          |

#### 🎒 Inventory Item Sizes

| Item               | Size | Notes                            |
| ------------------ | ---- | -------------------------------- |
| Knife              | 0.2  | Can be concealed                 |
| Rifle (hunting)    | 1.2  | Too long for quick inventory use |
| Glittertech Cannon | 2.5  | Overkill weapon, huge penalty    |

#### 🧠 Stat Requirement Examples

| Item            | STR | DEX | PER | Notes                 |
| --------------- | --- | --- | --- | --------------------- |
| Precision Rifle | 2   | 3   | 5   | Requires high control |
| Sword           | 3   | 4   | 0   | Dexterity favored     |
| Axe             | 6   | 2   | 0   | Brutal, clumsy        |

These tables are referenced by combat, inventory, and skill systems and updated only through coordinated design change.

---

This reflects the **true full scope** of current design commitments.
All entries are traceable to chat history and audit trail.
Further changes must follow governance: changelog + audit + rationale.
