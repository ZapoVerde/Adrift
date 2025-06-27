### 🎒 Inventory Size Model

**Status:** Locked

* Every item has a `size` field (e.g. knife = 0.2, rifle = 1.2).
* Actors have a max size capacity. Oversized items (e.g. longbows, laser guns) take multiple slots.
* Pack animals or base storage needed for large weapons or haul loot.
* Rationale: Prevents tactical overloading, enforces weapon role separation, and enables logistical tension.

**📐 Architectural Implications**

* Each `item` entry in ITEM\_DB must include a `size` float.
* Actor inventory logic must sum sizes and compare to `max_capacity`.
* Tactical weight does not affect encumbrance directly (that’s a separate mechanic).

**🔄 Flow Integration**

* Checked when picking up, equipping, or swapping items.
* Influences UI logic for inventory display, especially sort/filter options.
* Governs access to large items in combat — oversized weapons may not be used from inventory.

**🧠 Design Philosophy**

* Promotes preparation and logistical planning before missions.
* Enforces differentiation between pistols, rifles, and oversized tech.
* Unlocks scenarios like leaving a sniper rifle on the donkey while raiding a tight corridor.

**📝 Unstructured Notes**

* Inspired partly by RimWorld, Mount & Blade — but simplified.
* May support role-based storage (e.g. holsters, back slots) in later stages.
* Enables partial inventories and shared carrying (e.g. mule, squad relay).
* No weight simulation here — focus is on *space*, not *mass*.
* UI design will emphasize sort-by-size and group-by-type for player clarity.
* Could allow stacking small items (e.g. ammo, grenades) if under 1.0 unit.
* Combat behavior influenced indirectly: slower weapon swaps, no mid-fight cannon pulls.