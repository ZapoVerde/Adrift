### 🎯 Tactical Tile & Floorplan Model

**Status:** Locked

* Each Floorplan is a self-contained tactical map composed of tiles.
* A Floorplan is the only spatial unit loaded at runtime — no stitching or multi-map overlay occurs.
* Tiles are stored as a flat dictionary: `(x, y) → tile_dict`, allowing sparse layout and fast lookup.
* Each tile represents 2m x 2m of game space. Coordinates use a top-left origin; Y increases downward.
* Floorplans are referenced by the World, but runtime simulation is scoped to one floorplan at a time.
* Rationale: Enables dynamic, destructible, procedurally generated maps with minimal overhead.

**📊 Architectural Implications**

* Floorplan contains:

  * `width`, `height`: integers
  * `tiles`: `dict[(x, y)] → tile_dict`
  * `id`: unique string identifier (used by World and transitions)

* Each `tile_dict` includes:

  * `terrain`: base tile material (e.g. concrete, soil)
  * `things`: list of persistent map objects (e.g. crates, walls)
  * `items`: list of loose equipment
  * `actor`: reference to occupying unit, if any
  * `env`: list of environment effects (e.g. fog, fire)
  * `light`: local light level (0–10)
  * `memory`: visibility state for each actor (`visible`, `seen`, `unseen`)
  * `zone`: static label for UI purposes (e.g. "Guardpost")

* Tiles are plain dicts — not class instances — to support JSON serialization and modifiability.

* No field is required; tiles may be incomplete or partially defined.

**🔄 Flow Integration**

* Used in movement, combat resolution, visibility scanning, fire spread, and pathfinding.
* `observe()` runs vision trace across the tile map, checking `env`, `light`, and `terrain` fields.
* Fire, explosion, and destruction mutate the tile in-place (e.g. adding scorched terrain).
* ASCII parsers convert layout strings into `tile_dict` structures during dev and testing.

**🧠 Design Philosophy**

* Fully inspectable and debugger-friendly — each tile has a unique key and visible structure.
* Avoids nested grids or spatial wrappers — prioritizes simplicity and direct access.
* Designed to support procedural, destructible, and modular tactical content.
* Maintains a clear separation from overworld or global structures (see entry 7).

**📝 Unstructured Notes**

* Fields may later include tags like `walkable`, `opaque`, or `flammable`, but these will remain tile-local.
* Swarm actors or mass entities (e.g. rats) may share a tile under crowding rules.
* `zone` is strictly cosmetic — it is not a container, trigger, or query target.
* Tile model allows submap reloading and tactical state caching if needed.
