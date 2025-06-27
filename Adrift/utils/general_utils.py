# general_utils.py

from typing import List, Tuple, Dict, Any
from Adrift.definitions.tag_defs import TAG_DB

# This module contains grid-based line tracing logic used for vision, projectiles,
# and environmental pathing. Pure function — tactical interpretation is always external.

# Assumes (0,0) is top-left, y increases downward
# Floorplan is a dict of (x, y): tile_data

def validate_tags(defs: dict, kind: str):
    """
    Validates that all tags in a given definition dict exist in TAG_DB.
    """
    valid_tags = set(TAG_DB)
    for def_id, defn in defs.items():
        for tag in defn.get("tags", []):
            if tag not in valid_tags:
                raise ValueError(f"[{kind}] '{def_id}' uses unknown tag: '{tag}'")


def validate_all_tags(skill_defs, technique_defs):
    """
    Runs tag validation on both skills and techniques.
    """
    validate_tags(skill_defs, "Skill")
    validate_tags(technique_defs, "Technique")


def trace_line(
    start: Tuple[int, int],
    end: Tuple[int, int],
    floorplan: Dict[Tuple[int, int], Dict[str, Any]],
    stop_at_block: bool = False
) -> List[Dict[str, Any]]:
    """
    Traces a straight line from `start` to `end` using a grid-based algorithm.
    Returns a list of dicts, one for each tile crossed, including blocking status.

    This function does NOT interpret what counts as blocking — it marks the presence
    of potentially blocking features (terrain, things), but leaves interpretation
    to the caller.

    Parameters:
        - start: origin (x, y)
        - end: destination (x, y)
        - floorplan: map of (x, y) to tile dict
        - stop_at_block: if True, halts trace when blocking tile is encountered

    Design constraints:
    - No side effects (pure function)
    - Supports cardinal and diagonal directions
    - Does not skip corners
    - Assumes floorplan is prevalidated and includes full tile data for every coord
    """

    def bresenham_line(x0, y0, x1, y1):
        """Bresenham's line algorithm (integer-based, grid-safe)"""
        path = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = 1 if x1 > x0 else -1
        sy = 1 if y1 > y0 else -1

        if dx > dy:
            err = dx // 2
            while x != x1:
                path.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy // 2
            while y != y1:
                path.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

        path.append((x1, y1))
        return path

    path_coords = bresenham_line(start[0], start[1], end[0], end[1])

    traced = []
    for coord in path_coords:
        tile = floorplan.get(coord)
        if not tile:
            continue  # Skip missing tiles (should not happen in valid maps)

        blocking = False

        # Heuristic marking only — final interpretation is caller's job
        terrain = tile.get("terrain", {})
        if terrain.get("blocks_sight") or terrain.get("blocks_projectiles"):
            blocking = True

        for thing in tile.get("things", []):
            if thing.get("blocks_sight") or thing.get("blocks_projectiles"):
                blocking = True
                break

        traced.append({
            "coord": coord,
            "tile": tile,
            "blocking": blocking
        })

        if stop_at_block and blocking:
            break

    return traced


def compute_visibility_penalty_along_path(traced_path: List[Dict[str, Any]]) -> int:
    """
    Given a traced path from `trace_line`, compute the cumulative visibility penalty
    from all environmental effects (e.g. fog, smoke, fire) on traversed tiles.

    This function does not alter the path or interpret vision outcomes — it merely
    returns the total penalty value for further evaluation.
    """
    total_penalty = 0
    for step in traced_path:
        tile = step.get("tile", {})
        for env in tile.get("env", []):
            total_penalty += env.get("visibility_penalty", 0)
    return total_penalty


# TODO:
# - Allow custom is_blocking filter passed in by caller
# - Add optional debug logging for trace results
# - Optimize for large path lengths (e.g. precache)
# - Add grid bounds check fallback
# - Add unit tests for accumulate_visibility_penalty()

# TODO:
# - Allow custom is_blocking filter passed in by caller
# - Add optional debug logging for trace results
# - Optimize for large path lengths (e.g. precache)
# - Add grid bounds check fallback
