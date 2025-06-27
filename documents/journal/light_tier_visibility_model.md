### 💡 Light Tier Visibility Model

**Status:** Locked

* Light levels capped at tier 10. Each level defines max clear and vague zones.
* Scaling is fixed 1:2 ratio: e.g. clear 5 → vague 10.
* PER stat governs how far you *can* see, but light governs how far you *may* see.
* Rationale: encourages torch use, supports stealth, enables environmental puzzles.

**📐 Architectural Implications**

* Each tile has a `light_level` field (0–10) updated at runtime.
* `trace_visibility_path()` respects zone chaining but applies per-tile light limits.
* Light level determines zone visibility caps, not actual actor range.
* Decouples lighting from PER stat — light constrains, PER reaches.

**🔄 Flow Integration**

* During perception, light level is checked after pathing and environment penalties.
* Zone is only marked as `visible` or `vague` if light permits, even if range allows.
* Dynamic lights (e.g. torches, fires) update tile light level and trigger perception re-evaluation.
* Light interacts with stealth: dim areas reduce detection probability.

**🧠 Design Philosophy**

* Avoids all-seeing vision: even high PER can’t see through pitch dark.
* Scaling up to tier 10 allows daylight scenes, while tier 0 supports horror/suspense.
* Tiers are linear for clarity, not realism — favors game feel.
* Keeps player decisions meaningful (carry light source vs. stealth)

**📝 Unstructured Notes**

* Originally considered continuous lux model — rejected for granularity and design control.
* Fixed 1:2 scaling avoids messy curve fitting and supports quick estimation.
* Tiered model aligns with narrative scenes: candlelit dungeon, torchlit hallway, moonlit field.
* Integration with `describe_tile()` could yield atmospheric messages ("a faint flicker illuminates...”).
* May support colored or flickering light modifiers later for mood and puzzles.
* Tier 0 explicitly blocks vision, regardless of range or effects.
* Tier 10 enables entire-room vision, suitable for artificial lighting scenes.
* Model is compatible with future destructible light sources or flash-based visibility effects.
* Tested in perception testbeds with multiple actors, dynamic sources, and environmental overlays.