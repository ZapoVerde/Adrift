# floorplan.py

"""
This module defines the Floorplan structure and creation utilities.
Floorplans are tactical maps composed of dict-based Tiles, each identified by (x, y).

Design Philosophy:
- Tiles are modeled as plain dictionaries to reduce overhead and increase flexibility.
- All relevant tile state is embedded explicitly for clarity and easier serialization.
- Floorplans are maps of arbitrary size, created dynamically as needed.
- This module avoids using classes or object methods to preserve modularity and data transparency.
- Commenting is exhaustive to support learning, maintainability, and extensibility.
"""

from typing import Dict, Tuple, Any

# Type alias for coordinates and tiles.
# Tactical maps are square grids, using (x, y) tuples as keys.
Coord = Tuple[int, int]
Tile = Dict[str, Any]


def create_empty_tile() -> Tile:
    """
    Create a blank tile with default fields.

    This function defines the atomic unit of tactical gameplay.
    All tiles are assumed to exist in a uniform dict format, with every field explicitly present.
    Avoids lazy or implicit defaults to reduce edge-case bugs and enhance testability.
    """
    return {
        "terrain": "stone",        # Base terrain type. Used for movement cost, noise, etc.
        "things": [],              # Objects in tile. Each is a dict with tags (e.g., wall, crate).
        "items": [],               # Loose inventory objects or pickups.
        "actor": None,             # The actor currently occupying the tile, or None.
        "env": [],                 # Environmental effects (e.g., smoke, fire). Transient, stackable.
        "light": 1.0,              # Light level from 0.0 (pitch black) to 10.0 (eye-searing).
        "memory": "unseen",       # Fog-of-war state. Can be: unseen / seen / visible.
        "zone": None               # Optional semantic label, e.g. "Hallway" or "Main Gate".
    }


def create_floorplan(width: int, height: int, map_id: str, seed: int = 0, label: str = "") -> Dict[str, Any]:
    """
    Generate a new floorplan map with initialized tiles.

    Floorplans are rectangular regions defined by width and height.
    Each tile is prepopulated with a clean state to avoid on-demand logic elsewhere.
    The floorplan itself is returned as a dict with metadata and tile dictionary.

    Args:
        width: Number of tiles in the horizontal direction
        height: Number of tiles in the vertical direction
        map_id: Unique identifier string for the map instance
        seed: Optional integer seed for map-specific RNG or procedural behavior
        label: Human-readable label, used in UI or debug contexts
    """
    tiles = {}
    for y in range(height):
        for x in range(width):
            tiles[(x, y)] = create_empty_tile()

    return {
        "id": map_id,             # Unique map identifier
        "seed": seed,             # RNG seed used in map generation
        "width": width,
        "height": height,
        "tiles": tiles,           # Core tile dictionary, keyed by (x, y)
        "metadata": {
            "label": label        # Optional label for debug/GUI
        }
    }


def get_tile(floorplan: Dict[str, Any], coord: Coord) -> Tile:
    """
    Retrieve a tile safely from the floorplan.

    This wrapper protects against direct dictionary access to allow future logic hooks,
    validation, or lazy fallback behavior.

    Args:
        floorplan: The full floorplan dictionary
        coord: Tuple (x, y) representing the tile location

    Returns:
        Tile dictionary at given coordinates, or None if out-of-bounds.
    """
    return floorplan["tiles"].get(coord)


def set_tile(floorplan: Dict[str, Any], coord: Coord, tile_data: Tile) -> None:
    """
    Overwrite a tile in the floorplan.

    Used to inject modified tiles, e.g., after applying damage or building destruction.
    No validation is performed — it assumes tile_data is well-formed.

    Args:
        floorplan: Floorplan dict
        coord: (x, y) coordinate
        tile_data: New tile dict to replace existing entry
    """
    floorplan["tiles"][coord] = tile_data
