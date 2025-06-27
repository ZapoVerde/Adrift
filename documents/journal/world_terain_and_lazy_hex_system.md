### 🌍 World, Terrain & Lazy Hex System

**Status:** Locked

* The World is a global container for all discovered and undiscovered Floorplan objects.
* Only one Floorplan is active at a time during runtime — no seamless overworld stitching.
* Tactical Floorplans are loaded lazily when the player enters an unexplored region.
* Previously visited Floorplans are stored and can be reloaded with full tile state.
* World may be divided into large-scale regions, sectors, or hexes — model pending.
* Rationale: Allows high-level exploration without loading all tactical maps into memory.

**📐 Architectural Implications**

* World stores a registry of known Floorplans, indexed by ID or coordinates.
* Each Floorplan contains its own tile map and simulation context.
* Terrain-level data (e.g. desert, mountains) may gate access or affect travel cost.
* Floorplan generation is triggered by movement or event-based transition.
* May support a hex or sector wrapper if required for travel or region simulation.

**🔄 Flow Integration**

* Player movement at the world level triggers: load cached Floorplan or generate new.
* World state is saved independently of any active tactical map.
* No actor exists outside the current Floorplan — other maps are inert until entered.
* All high-level travel decisions resolve before loading a tactical map.

**🧠 Design Philosophy**

* Keeps world lightweight and declarative — Floorplans are atomic simulation spaces.
* Encourages procedural exploration while allowing revisiting old maps.
* Tactical and overworld systems are cleanly separated — no global actor movement logic.
* Lazy loading model supports sprawling, discoverable worlds with minimal overhead.

**📝 Unstructured Notes**

* World map may be visualized via abstract UI (e.g. node graph, hex map).
* May support biome tags or climate data per region, but unused in core simulation.
* Transition logic can include narrative triggers or environmental gating (e.g. mountain pass).
* No pathfinding or fog-of-war at the world level — all state lives in Floorplan tiles.
