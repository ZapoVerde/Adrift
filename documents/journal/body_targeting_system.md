### 🩻 Body Targeting System

**Status:** Locked

* Each body zone (e.g. head, arm, torso) has a `coverage_weight`. Flat weighted probability pool.
* No hierarchical nesting (no parent → child part targeting).
* Functional dependencies still apply: severing an arm disables the hand.
* Rationale: Simplifies targeting logic, supports frequent maiming, aligns with narrative tone.

**📐 Architectural Implications**

* All actors (player, AI) have a `body_structure` with zone weights.
* `combat_utils.choose_target_zone()` selects the zone based on flat weighting.
* Secondary systems (e.g. wound effects, status checks) hook into this zone post-selection.

**🔄 Flow Integration**

* After an attack hits, a body part is chosen using the weighted table.
* Damage is resolved *after* zone is known — enabling location-specific reactions (e.g. headshot = instant death).
* Interacts with multiplier and injury model to apply penalties, disable limbs, trigger shock.

**🧠 Design Philosophy**

* Avoids complexity of hierarchical body trees — arms and fingers coexist in a shared pool.
* Supports future effects like "called shots" by biasing the weighted pool.
* Realistic enough to be narratively evocative without requiring anatomical simulation.

**📝 Unstructured Notes**

* Nested part models were rejected early: they produce weird dissonance when a parent is destroyed but children persist (e.g. floating hands).
* This model prioritizes player understanding: simpler hit logic = clearer outcome.
* Encourages narrative maiming (e.g. lost leg, crippled arm) without always going for instant kills.
* The flat weight pool ensures small zones like fingers are *technically* possible to hit — but rare.
* Future evolution may allow part-specific defenses (e.g. armored torso vs unarmored head).
* Some weapons or attacks may restrict pool (e.g. explosion may avoid legs, or favor torso).