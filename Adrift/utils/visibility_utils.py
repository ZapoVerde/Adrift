from Adrift.utils.debug_utils import debug
from Adrift.utils.movement_utils import distance_between_zones
from collections import deque
from Adrift.utils.general_utils import trace_line
from typing import List, Dict, Any


def get_visibility_caps(light_level):
    """
    Returns (max_clear, max_vague) based on light level.
    Includes overexposure collapse at high intensity.
    """
    if light_level <= 0:
        return (0, 0)
    elif light_level == 1:
        return (0, 1)
    elif light_level == 2:
        return (1, 2)
    elif light_level == 3:
        return (2, 4)
    elif light_level == 4:
        return (4, 8)
    elif light_level == 5:
        return (8, 16)
    elif light_level == 6:
        return (16, 32)
    elif light_level == 7:
        return (10, 20)  # washed-out overlit zones
    elif light_level == 8:
        return (4, 8)  # glare
    elif light_level == 9:
        return (1, 2)  # whiteout
    else:
        return (0, 0)  # retina burn: total sensory loss


def visual_coverage(observer_zone, target_zone):
    """
    Estimate how much of the target zone is visible from the observer.
    Uses number of blocking zones along the visibility path as a proxy for visual obstruction.

    Returns a float between 0.0 and 1.0:
    - >= 0.9 → clear visibility
    - >= 0.3 → vague
    - < 0.3 → unseen
    """
    path = trace_visibility_path(observer_zone, target_zone)
    if not path:
        return 0.0

    blockers = 0
    for zone in path:
        if zone.blocks_vision:
            blockers += 1

    return 1.0 - (blockers / len(path)) if path else 1.0


def observe(observer):
    """
    Perception scan with:
    - Light-based visibility caps
    - Vague fallback awareness
    - Tiered resolution: clear, vague, or unknown
    """
    origin = observer.current_zone
    room = origin.parent_room
    visible_entities = []
    vague_sightings = []

    perception_stat = observer.stats.get("PER", 0)
    perception_radius = max(1, perception_stat // 2)

    for zone in room.zones:
        dist = distance_between_zones(origin, zone)
        if dist is None:
            continue

        light_level = getattr(zone, "light_level", 2)
        max_clear, max_vague = get_visibility_caps(light_level)

        # Calculate visibility penalties from all zones in vision path
        path = trace_visibility_path(origin, zone)
        env_penalty = 0
        if path:
            for z in path:
                for effect in getattr(z, "environment_effects", []):
                    env_penalty += effect.get("visibility_penalty", 0)

        adjusted_distance = dist + env_penalty

        if dist > max_vague or adjusted_distance > perception_radius:
            continue  # too far or fully blocked

        if dist > max_clear:
            # Zone is outside clear range — apply vague visibility rules
            coverage = visual_coverage(origin, zone)

            for actor in zone.actors:
                if actor != observer:
                    if coverage >= 0.3:
                        vague_sightings.append({
                            "zone": zone,
                            "type": "actor",
                            "source": actor,
                            "distance": adjusted_distance
                        })
                        debug(
                            f"[OBSERVE-VAGUE] {observer.name} senses movement in {zone.display_name}"
                        )
                    else:
                        continue  # Too obscured to detect

            for item in zone.items:
                if coverage >= 0.3:
                    vague_sightings.append({
                        "zone": zone,
                        "type": "item",
                        "source": item,
                        "distance": adjusted_distance
                    })
                    debug(
                        f"[OBSERVE-VAGUE] {observer.name} senses object in {zone.display_name}"
                    )
                else:
                    continue  # Too obscured to detect

            continue  # Skip clear visibility logic for this zone

        # Full visibility
        for actor in zone.actors:
            if actor != observer:
                coverage = visual_coverage(origin, zone)
                if coverage >= 0.9:
                    visible_entities.append(actor)
                debug(
                    f"[OBSERVE] {observer.name} sees {actor.name} in {zone.display_name} [{adjusted_distance}]"
                )
        for item in zone.items:
            coverage = visual_coverage(origin, zone)
            if coverage >= 0.9:
                visible_entities.append(item)
            debug(
                f"[OBSERVE] {observer.name} sees item '{item}' in {zone.display_name} [{adjusted_distance}]"
            )

    return visible_entities, vague_sightings


def trace_visibility_path(origin, target):
    """
    Returns the list of intermediate zones (excluding origin and target)
    along the shortest line-of-vision path between origin and target.
    This is a vision-safe BFS path that ignores movement-specific obstacles.

    If no path is found (e.g. disconnected zones), returns None.
    """
    if origin == target:
        return []

    visited = set()
    queue = deque([[origin]])

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == target:
            return path[1:-1]

        if current in visited:
            continue
        visited.add(current)

        for neighbor in current.connections:
            if neighbor not in visited:
                queue.append(path + [neighbor])

    return None  # No path found


def compute_visibility_penalty_along_path(
        traced_path: List[Dict[str, Any]]) -> int:
    if not isinstance(traced_path, list):
        raise TypeError("traced_path must be a list of tile step dicts")

    total_penalty = 0
    for step in traced_path:
        if not isinstance(step, dict):
            raise TypeError("Each step must be a dict with a 'tile' key")
        tile = step.get("tile", {})
        if not isinstance(tile, dict):
            raise TypeError("Each 'tile' must be a dict")
        env_list = tile.get("env", [])
        if not isinstance(env_list, list):
            raise TypeError("tile['env'] must be a list")
        for env in env_list:
            if not isinstance(env, dict):
                raise TypeError("Each env entry must be a dict")
            total_penalty += env.get("visibility_penalty", 0)
    return total_penalty
