### 🧮 Damage Multiplier Model

**Status:** Locked, Implemented

* Rolls of 2–5 result in no damage. Rolls 6–12 use a smooth exponential curve.
* Formula: `multiplier = 1.72 / (-0.43 × roll + 5.59)`, anchored at roll 9 = ×1.0.
* Balances realism and game tension: low rolls are unreliable, high rolls can cleave limbs.
* Fully supports decimal-modified rolls (skills/techniques).
* Rationale: avoids tiered damage brackets, provides graceful scaling and critical overkill.

**📐 Architectural Implications**

* This multiplier model is applied in `combat_utils.resolve_attack()` post-roll.
* Multiplier affects raw base damage of the weapon or unarmed attack.
* Allows seamless integration of techniques that modify roll outcomes without needing to alter formula.

**🔄 Flow Integration**

* Plugged in directly after hit chance and body part targeting.
* Interacts with weapon base damage and actor attributes to produce final wound.
* Critical failures or environmental modifiers (e.g. smoke) may reduce the effective roll before applying the multiplier.

**🧠 Design Philosophy**

* Anchoring at roll 9 avoids the feel of "just numbers" and makes high-skill characters noticeably more dangerous.
* Enables a consistent probabilistic scale: rare high rolls reward the player dramatically.
* Supports overkill moments without requiring separate critical hit logic — the multiplier naturally expresses it.

**📝 Unstructured Notes**

* The shift from flat tiers to a continuous exponential curve originated from a concern that discrete 2d6 brackets produced overly chunky outcomes.
* Decimal roll modifiers (e.g. 8.7) were introduced to smooth skill and technique integration without inflating die mechanics.
* Rolls under 6 were hard-coded to zero for clarity and gameplay tension: no partial hits in this range, mirroring a 'swing and a miss' tone.
* Critical hits aren't separate — the high tail of the curve *is* the crit. This avoids layering a secondary crit system.
* Overkill results are absorbed naturally — high multiplier × high base damage = potential instant maim/death.
* There was a tradeoff between mathematical elegance and narrative flavor — ultimately curve clarity and scalability won.
* Combat logs use `describe_roll()` to add thematic messaging to each roll outcome based on multiplier tier.
* Skill growth may later shift rolls upward (e.g. +0.3 PER modifier = 9.3 average), making player power intuitive and math-based.
* Anchoring at roll 9 avoids the feel of "just numbers" and makes high-skill characters noticeably more dangerous.
* Enables a consistent probabilistic scale: rare high rolls reward the player dramatically.
* Supports overkill moments without requiring separate critical hit logic — the multiplier naturally expresses it.