# definitions/thing.py

"""
THING_DB: Canonical definitions for all placeable or interactable tactical objects.
These include physical obstacles, props, and devices — not environmental effects like fire or fog.

Design Philosophy:
- Only includes tangible objects occupying tile space
- Effects like fog, fire, smoke are stored separately in tile["env"]
- Avoids mixing environmental and interactable state in a single system

Conventions:
- `cover_rating >= 99` is considered full visual block
- `blocks_sight = True` short-circuits line-of-sight
- `destructible = False` means invulnerable
- `flammable = True` can be set on fire by external logic
"""

THING_DB = {
    "crate": {
        "blocks_sight": False,
        "cover_rating": 2,
        "destructible": True,
        "hp": 20,
        "flammable": False,
    },
    "wall": {
        "blocks_sight": True,
        "cover_rating": 99,
        "destructible": False,
    },
    "barrel": {
        "blocks_sight": False,
        "cover_rating": 1,
        "destructible": True,
        "hp": 10,
        "flammable": True,
    },
    "door_closed": {
        "blocks_sight": True,
        "cover_rating": 40,
        "destructible": True,
        "hp": 30,
    },
    "door_open": {
        "blocks_sight": False,
        "cover_rating": 0,
        "destructible": True,
        "hp": 30,
    }
}


# TODO:
# - Add tags like 'flammable', 'movable', 'fragile' where relevant
# - Link to procedural map placement system
# - Add door state transitions (open <-> closed) under interaction rules
# - Design interaction interface: open, burn, destroy, block
