### 🕵️ Stealth & Detection Mechanics

**Status:** Locked

* Stealth is modeled as a continuous visibility challenge, not a binary on/off state.
* Detection is governed by a combination of: actor size, stealth, observer PER, tile light level, and environmental effects.
* `observe()` is the baseline passive scan. `search()` is an active skill-based action that boosts detection.
* Rationale: Enables emergent stealth mechanics with skill expression, tile-based occlusion, and uncertainty.

**📐 Architectural Implications**

* Actor fields:
  - `size`: integer (1–10)
  - `stealth`: flat modifier (e.g. `-2` = harder to detect)
  - `PER`: perception stat (used by observers)

* Skills:
  - `stealth` (on target): passively reduces detectability, affects perceived size
  - `observe` (on observer): passively improves clarity and reaction radius
  - `search` (on observer): action-based skill to boost temporary detection radius and strength

* Tiles pass through `observe()` vision tracing — detection only runs on visible tiles.
* Special `search()` action flags a temporary PER bonus for the actor (`duration = 1 round`).

* Detection logic:
  - `can_detect(observer, target, tile)`  
    → `PER + bonus` vs. `size + stealth + env penalty + light tier`

**🔄 Flow Integration**

* `observe()` is automatically called during the Perception phase → determines baseline visibility.
* `search()` is a player/AI action that applies a `+X PER` bonus for that actor this round.
* `can_detect()` is invoked for each visible tile with an actor present.
* Visibility state (`seen`, `visible`, or `unseen`) is cached to actor memory.

**🧠 Design Philosophy**

* Stealth is always beatable, but never trivial — depends on timing, light, cover, and skills.
* Allows underdog tactics: small actor in darkness can hide from high-level enemy.
* Supports environmental interaction: fire, fog, terrain all modify outcome.
* Avoids full invisibility logic — instead prefers believable sight mechanics.

**📝 Unstructured Notes**

* Stealth skill growth yields major impact in darkness or during night raids.
* `search()` action opens room-clearing mechanics, scout behavior, overwatch logic.
* System is symmetric: AI can use stealth to ambush player.
* `stealth` could also influence noise-based detection in the future.
* Faintly seen actors may generate vague message: `"You sense movement in the mist."`
