## 15. trace\_line(): Generalized Line Tracer

### 🧾 Status

**Locked**

Originally developed to model **vision line-of-sight**, the `trace_line()` function is now locked in as a **generic grid-based line tracer** supporting multiple tactical systems. This avoids duplication of path logic and supports any mechanic that evaluates tile-by-tile traversal between two coordinates.

Use cases include:

* **Vision**: checking if an actor can see a target zone.
* **Projectiles**: determining hit or collision.
* **Environmental effects**: propagation of fog, gas, or fire.
* **Sound**: alert spread or auditory perception.
* **Trap triggers**: laser tripwires, mine line checks.
* **AI awareness**: determining which allies are alerted.

This system establishes a single tactical utility function for clean, testable, and reusable line stepping.

---

### 🧠 Design Philosophy

* Build once, use everywhere: a unified pathing function simplifies tactical logic.
* Tactical interpretation is externalized: caller decides what counts as a block.
* Avoids duplicated logic for vision, projectile, and hazard systems.
* Naming and structure are generic — this is not vision-specific.
* Outputs must support inspection, filtering, and visualization.

---

### ⚙️ Core Model – Path Tracer

* Function signature: `trace_line(start, end, floorplan)`
* Returns a list of dictionaries for each tile along the path:

```python
[
    {"coord": (x, y), "tile": tile_data, "blocking": False},
    {"coord": (x2, y2), "tile": tile_data, "blocking": True},
    ...
]
```

* Calling function handles interpretation of what counts as blocking:

  * Vision: `tile["terrain"]["blocks_sight"]`, `thing["blocks_sight"]`
  * Projectiles: `thing["blocks_projectiles"]`
  * Spread: may ignore some partial blockers

---

### 📐 Architectural Implications

* Function must be side-effect free and context-agnostic

* Core output is a full ordered list of tiles from origin to target

* Integration points include:

  * `observe()` → determines visibility
  * `resolve_projectile_hit()` → handles bullet travel
  * `apply_environmental_spread()` → spreads fire/gas
  * `tactical_debug_draw()` → path preview overlays

* Environmentally relevant fields:

  * `tile["terrain"]["blocks_sight"]`
  * `thing["blocks_sight"]`, `cover_rating`, `visibility_penalty`
  * `tile["env"]` for fog, fire, smoke

* Blocker rules must be decoupled and caller-defined

---

### 🔄 Flow Integration

* Called during vision check (e.g. `observe()`)
* Used to simulate projectile travel and early block detection
* Enables fog-of-war tracing with light level and visibility modifiers
* Will support destructible cover detection and over-penetration logic

---

### 🧪 Test Coverage Requirements

* Validate 8-way straight and diagonal paths
* Test edge cases (single-tile, same-tile, corners)
* Confirm trace order and blocker flags
* Ensure tiles and things correctly influence `blocking`
* Should test multiple interpretive layers: raw path, filtered for vision, filtered for projectiles

---

### 📝 Unstructured Notes

* Likely rename: `trace_line()` or `trace_grid_line()` for clarity
* Should integrate with debug overlay if `DEBUG_MODE = True`
* May support early termination mode (`stop_at_block = True`)
* Could return multiple views: raw, filtered, or tagged by system
* Priority: stable and predictable output for higher-layer logic
* Should not make assumptions about what a "block" is — always caller-defined