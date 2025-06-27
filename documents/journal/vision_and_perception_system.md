### 👁️ Vision & Perception System

**Status:** Locked, Implemented

* Actors use PER stat to define Range of Perception (RoP).
* BFS scan traces line-of-sight; environment effects penalize visibility (e.g. smoke).
* Lighting caps clear and vague zone detection (1:2 ratio). Max at light tier 10.
* Rationale: Merges tactical depth with realistic detection. Keeps implementation efficient.

**📐 Architectural Implications**

* PER stat sets max RoP, but light tiers and environmental penalties modify visibility at runtime.
* Vision pathing uses a custom BFS (`trace_visibility_path`) that accumulates penalties and respects zone connectivity.
* Light and perception logic decoupled: light sets hard caps, perception determines reach.

**🔄 Flow Integration**

* Invoked during perception phase (`engine.perception_phase()`), before action or combat.
* `observe()` function updates each actor’s `visible_zones` and `seen_zones` memory.
* Detection checks (e.g. stealth) run against current `visible_zones` context.

**🧠 Design Philosophy**

* Avoids angular/facing mechanics: omnidirectional detection encourages spatial reasoning over micromanagement.
* Designed to scale from low-light caves to open-air firefights with spotlighting.
* Integration with stealth, lighting, fog-of-war enables rich tactical scenarios.

**📝 Unstructured Notes**

* Initial versions reused movement pathfinding, but were rejected for lacking perceptual nuance.
* Observation range is *not* symmetric: you might see them, they might not see you.
* `visited_zones` lets each actor track their own memory — supports deception, illusions, sneaking.
* Environmental effects (e.g. fog) can completely block zones even within range.
* Visibility zones are categorized as `visible`, `vague`, or `unseen`.
* Faint light may show silhouettes, but not allow target confirmation.
* Multiple actors scanning simultaneously requires independent RoP resolution per actor.
* Vision remains tile-based but world-scale distances are supported: e.g. spotting a torch 20 zones away.