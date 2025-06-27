# cover_utils.py

"""
This module provides utilities for calculating cover and line-of-sight interference
from things located on tactical tiles. Cover is determined by the presence of objects
with defined cover_rating or blocks_sight attributes.

Design Philosophy:
- Cover and visibility are tile-centric but determined by objects ('things')
- Modular: Does not assume or enforce actor/team logic
- Lightweight: Only operates on floorplan and things, does not invoke perception or combat systems

Dependencies:
- floorplan.get_tile(x, y): returns tile at (x, y)
- Each tile: tile["things"] is a list of dicts representing things
- Each thing may define: "cover_rating": int, "blocks_sight": bool

Output:
- calculate_cover_between returns list of cover-relevant things, with positions
- Can be used by perception, combat, AI modules
"""

from typing import List, Tuple, Dict


def get_cover_objects_along_path(path: List[Tuple[int, int]], floorplan: Dict) -> List[Dict]:
    """
    Scans the tiles along the given path and returns all objects that influence cover.

    Args:
        path (List[Tuple[int, int]]): List of (x, y) positions from observer to target
        floorplan (Dict): Dict of (x, y): tile

    Returns:
        List[Dict]: List of {"pos": (x, y), "thing": <thing dict>} entries that affect cover
    """
    cover_items = []
    for (x, y) in path:
        tile = floorplan.get((x, y))
        if not tile:
            continue
        for thing in tile.get("things", []):
            if thing.get("cover_rating") or thing.get("blocks_sight"):
                cover_items.append({"pos": (x, y), "thing": thing})
    return cover_items


def calculate_total_cover(path: List[Tuple[int, int]], floorplan: Dict) -> int:
    """
    Computes the total cover_rating from objects along the path.
    Ignores cover that is at the source or destination.

    Args:
        path (List[Tuple[int, int]]): Ordered list from observer to target (inclusive)
        floorplan (Dict): Tactical map of tiles

    Returns:
        int: Total cover penalty from all intervening things
    """
    if len(path) <= 2:
        return 0  # Nothing between source and target

    intervening = path[1:-1]  # exclude observer and target tiles
    cover_objects = get_cover_objects_along_path(intervening, floorplan)
    total = sum(
    rating for obj in cover_objects
    if isinstance((rating := obj["thing"].get("cover_rating")), int)
    )

    return total


# TODO:
# - Define standard cover_rating values in thing_definitions.py
# - Add blocks_sight handling in visibility tracing (not just passive penalty)
# - Optional: Handle destructible cover interactions here or delegate to combat
# - Add test suite to validate against various layouts and thing placements
