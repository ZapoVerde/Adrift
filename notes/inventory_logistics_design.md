## 📦 Inventory & Logistics Design — Locked Specification

### 🧠 Core Philosophy

Inventory is not just what you carry, it's what you can *reach*. Tactical loadouts and strategic caches define player capabilities moment-to-moment.

Oversized items are **tactical commitments**, not just larger objects. Carriers are **narrative entities**, vulnerable to environmental and AI-driven events. What you bring into a fight—and what you leave behind—defines your options and your story.

---

## ✅ Primary Inventory Model

### ➕ On-Person Inventory (Combat-Accessible)

* Constrained by total `size`
* Hard cap on `oversized` items (usually 1)
* Quick access for weapons, meds, grenades
* Items not on-person may require turn delay or be fully inaccessible during combat

```python
actor.inventory = {
  "on_person": [...],
  "max_size": 30,
  "oversized_limit": 1
}
```

### 📊 Item Schema

```python
item = {
  "name": "Sniper Rifle",
  "size": 8,
  "weight": 12,
  "bulk_class": "oversize",  # optional
  "tags": ["weapon", "ranged"]
}
```

Oversized items define **loadout identity** and should be pre-selected before missions or combat entries. Mid-combat swaps from storage are disallowed or penalized.

---

## 🐴 Logistics Layer: Carriers

### ➕ Pack Animals, Mechs, Carts

* Can carry items not currently accessible in combat
* Limited `max_size` and `max_oversized`
* **Some carriers may omit `max_size` entirely**, allowing only a fixed number of oversized slots
* Must be physically present and calm to allow access
* Treated as physical, targetable entities on the map
* **AI-controlled behavior under stress**: may flee, drop gear, or be killed

### 🔧 Carrier Structure

```python
InventoryCarrier = {
  "name": "Donkey",
  "inventory": [...],
  "max_size": 80,
  "max_oversized": 2,
  "location": (x, y),
  "status": "waiting"  # or 'fleeing', 'dead', etc.
}
```

### ❌ Combat Access Rule

```python
def is_item_accessible(item, context, actor_location):
    for carrier in actor.carriers:
        if carrier.location != actor_location:
            continue
        if carrier.status != "waiting":
            continue
        if item in carrier.inventory:
            return True
    return item in actor.inventory["on_person"]
```

Swapping items from carriers may require multi-turn retrieval actions or may be outright blocked in combat.

---

## 🧪 Tactical Scenarios Supported

| Situation        | Narrative                        | Mechanic                      |
| ---------------- | -------------------------------- | ----------------------------- |
| Dungeon Raid     | Leave pack outside               | Inventory locked on entry     |
| Ambush           | Donkey flees, gear lost          | Carrier flees, drops items    |
| Cave-In          | Pack animal dies, gear buried    | Mark gear as lost/recoverable |
| Stealth Cache    | Hide rocket launcher near site   | Zone-level item stashes       |
| Recovery Mission | Return to retrieve stashed items | Re-activate abandoned carrier |

---

## 🧱 Inventory Caching & Retrieval

* Items may be stashed manually in specific world zones
* Caches are remembered per zone, recoverable later
* May require dedicated action to bury, conceal, or retrieve

---

## 🔐 Future Extensions

* Zone-based caching and retrieval system
* Status effects for carriers (panic, poison, broken leg)
* Time or turn cost to access remote gear
* Carrier skill: better handling = safer logistics
* Carrier behavior modes: follow, wait, flee, defend

---

## 🔒 Status: Locked

This model is approved and locked into the design. Tactical inventory is separate from strategic storage. Oversized items are restricted and meaningful. Carriers are physicalized in the world and can be lost or repositioned. Their behavior and accessibility are context-sensitive and shaped by threat, location, and player command.

Use this structure as the foundation for all logistics, equipment access, and world-item interaction going forward.
