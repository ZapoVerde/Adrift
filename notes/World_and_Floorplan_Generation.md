
# World and Floorplan Generation – Full Detail

This document captures all finalized decisions, assumptions, and structures related to world generation and tactical floorplan architecture.

---

## 🌍 World Structure and Architecture

### 🔁 World vs. Tactical Layer
- **World layer** handles meta-location, overworld logic, and transitions.
- **Tactical layer** handles moment-to-moment gameplay (combat, exploration).
- Players transition **explicitly** from world to floorplan and back.

### 📦 Floorplans as Tactical Maps
- A `Floorplan` is a self-contained, rectangular map.
- Internally structured as a `dict[(x, y)] -> tile`.
- No runtime stitching of floorplans (XCOM model, not Dwarf Fortress).

---

## 🧭 Floorplan Composition

### 📐 Dimensions
- Each floorplan declares:
  - `width` (int)
  - `height` (int)
- Dynamic per-map. Allows both large outdoors and tight interiors.
- Unused map space is allowed (partial population of tile data).

### 🗺️ Coordinate System
- Top-left origin: (0, 0)
- X increases rightward
- Y increases downward

### 📦 Tile Storage Format
```python
{
    (x, y): {
        "terrain": "stone",
        "things": [],        # Walls, doors, crates (blocks movement, LoS, cover)
        "items": [],         # Lootable or interactive items
        "actor": None,       # Actor (player or NPC)
        "env": [],           # Environmental effects (e.g. fog, fire)
        "light": 1.0,        # Light level (0–10)
        "memory": "unseen",  # FoW: 'unseen', 'seen', 'visible'
        "zone": None         # Optional zone label
    }
}
```

---

## 🧱 Terrain and Features

### 🧱 Things
- Stored per-tile as list of dicts.
- Represent physical obstacles or interactables:
```python
{"type": "wall", "blocks_los": True, "blocks_movement": True}
{"type": "crate", "cover": "partial", "destructible": True}
```

### 💡 Light
- Default: `1.0` (normal indoor light)
- Used in visibility checks, applies perception modifiers.

### 🔥 Environmental Effects
- Each is a dict in the `env` list:
```python
{"type": "fog", "visibility_penalty": 2}
```
- Transient, overlapping, and potentially conflicting (e.g. fog vs fire).
- Penalties are cumulative across the visual path.

---

## 🚧 Zones and Labels

### 🏷️ Zone Field
- Each tile may optionally belong to a `zone` (a logical room or area).
- Zones may be labeled (e.g. `"Entrance Hall"`, `"Guard Room"`).
- Labels are static unless explicitly changed through narrative logic.

---

## 🧪 Floorplan Generation & Parsing

### 🧰 ASCII Parser
- Test maps defined using ASCII:
```
##################
#....C..g....... #
#............... #
#....@.......... #
##################
```

- Mappings are defined to convert symbols to:
  - Terrain
  - Actors (e.g. `'@'` for player)
  - Things (e.g. `'#'` for wall, `'C'` for crate)

### ✅ Test Floorplan
- 10x6 test corridor/room layout
- Includes walls, player, goblin, and crate
- Fully functional and visually output via `pprint` or ASCII preview

---

## 🔐 Locked-In Design Principles

- ✅ Tiles are dicts, not class instances.
- ✅ Stored in a `(x, y)` dict for sparse, flexible representation.
- ✅ Visual system assumes rectangular floorplans.
- ✅ Tactical maps will support fog-of-war and perception.
- ✅ Modular parsing and construction (not hardcoded map layouts).

---

## 🔮 Planned Extensions

- Auto-linking of adjacent zones
- Procedural generation hooks
- Integration with overworld location metadata
- Region memory persistence and revisitation logic

