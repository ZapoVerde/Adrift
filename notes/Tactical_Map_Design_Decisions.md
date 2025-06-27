
# Tactical Map Design Decisions

This document captures all locked-in architectural and gameplay decisions made during the tactical map and floorplan development session.

---

## ✅ General Tactical Layer Principles

- **Top-down grid system** with tiles representing 2m x 2m real-world space.
- Tactical detail is intentionally **low resolution**, prioritizing clarity over fidelity.
- Interface will follow a **RimWorld-style layout** with visibility across long distances.

---

## 📏 Tile Model

- Each tile is implemented as a **dict**, not a class instance.
- Rationale: flexibility, serialization simplicity, extensibility, and performance.
- All tiles include:
  - `terrain`, `light`, `actor`, `items`, `things`, `env`, `zone`, `memory`

---

## 🧱 Storage Model

- Floorplans are stored as a **dict of tiles**, keyed by `(x, y)` tuples.
- Rationale: avoids sparse list inefficiencies, clearer than 2D lists for tactical use.
- Map origin: `(0, 0)` is **top-left**, and Y **increases downward**.

---

## 🧭 World Architecture and Floorplans

- Floorplans are **self-contained tactical maps**.
- No seamless stitching between zones; transitions are **explicit**.
- Migration to **full 2D graphical interface** is locked in (text UI remains for now).

---

## 🔲 Fog of War (FoW)

- Minimal model implemented:
  - `visible`: tile seen this tick
  - `seen`: tile seen previously
  - `unseen`: never seen
- Stored **per actor** to support memory-based vision.
- Infrastructure supports later expansion (rumors, memory decay, hallucinations, etc.).

---

## 🌐 Tile Size and Multi-Occupancy

- Standard tiles are 2m x 2m.
- Most tiles will support **one actor only**.
- Small actors (e.g. rats) may be modeled as **swarms** for high-density support.

---

## 🌍 Environmental Effects

- Stored in the `env` list per tile.
- Each effect is a dict:
  ```python
  {"type": "fog", "visibility_penalty": 2}
  ```
- Effects are:
  - **Transient**
  - **Can overlap**
  - **Require logic** to resolve conflicts (e.g. fire vs. smoke vs. water)

---

## 🏷️ Zones and Labels

- Each tile may be part of a `zone` (assigned post-floorplan generation).
- Zones can be labeled (e.g. "Storage Closet", "Guard Post").
- Labels are **static**, unless manually changed by narrative events.

---

## 🧱 Map Size Model

- Map dimensions are **dynamic**, set per floorplan.
- Large maps are allowed but may contain **unused areas**.
- Efficient for both tight indoor and broad outdoor spaces.

---

## 📦 Thing vs Item

- **Things** = permanent/tactical objects (walls, doors, cover, crates)
- **Items** = movable/inventory objects (weapons, loot)
- Cover is provided by **things**, not tiles.

---

## 🗃️ Item Source Model

- Items defined in a central **ITEM_DB** or list.
- Supports procedural generation layered on top of base definitions.

---

## 🧱 Wall and Cover Model

- Walls, crates, and obstacles are **things** in the `things` list.
- Walls block LoS and movement.
- Crates can provide partial cover, be destructible, etc.

---

## 🔍 Floorplan Parser

- Maps can be created using ASCII templates.
- ASCII symbols map to terrain, actors, and things.
- Fully tested and validated via `test_floorplan_parser.py`.

---

## 🧪 Test Floorplan

- A 10x6 corridor-room layout with wall boundaries and a crate.
- Includes player and goblin actors.
- Provides working visual output and validates parsing.

---

## 🧠 Philosophy Reminder

- `engine.py` contains **flow only**, no logic.
- All calculations delegated to utils or handlers.
- All player-facing output routed through `messaging.py`.

---

## 🔐 Locked In Directives

- Always alert user when best practices are violated.
- Avoid embedding output or logic in flow modules.
- Preserve exhaustive commentary explaining intent, architecture, and tradeoffs.
