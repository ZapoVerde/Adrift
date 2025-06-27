# movement_utils.py
# ─────────────────────────────────────────────────────────────
# 🧠 ROLE: Handles all actor movement logic within rooms and zones.
#
# This module implements:
# - Low-level zone movement (with adjacency validation)
# - High-level pathing toward features or other actors
# - Resolution of human-readable navigation targets
#
# 🧭 DESIGN PHILOSOPHY:
# - Movement must always resolve to a target Zone.
# - Features and actors are abstract *navigation targets* that map to zones.
# - All actual movement happens zone-to-zone with validation.
# - No direct I/O is performed; all feedback is externalized via messaging.
# - Debug output is routed through debug_utils for centralized control.
#
# This separation ensures movement logic is testable, extendable,
# and future-proof for pacing, pathfinding, or multi-turn traversal.
# ─────────────────────────────────────────────────────────────

from Adrift.utils.debug_utils import debug
from collections import deque

# ─────────────────────────────────────────────────────────────
# 🔹 LOW-LEVEL: Core atomic movement step
# ─────────────────────────────────────────────────────────────

def move_actor_to_zone(actor, destination_zone):
    """
    🚶 Low-level zone transition function. Moves an actor from their current
    zone to an *adjacent* zone, with full validation.

    This is the core atomic movement step, and is used by all higher-level
    movement logic. It ensures:
    - The destination zone is adjacent to the current one
    - The actor is removed from the old zone and added to the new one
    - The actor's `current_zone` reference is updated

    Parameters:
    - actor: any object with `.name` and `.current_zone`
    - destination_zone: Zone object

    Returns:
    - True if move succeeds
    - False if destination is not adjacent
    """
    current_zone = actor.current_zone

    debug(f"Attempting to move {actor.name} from {current_zone.internal_name} to {destination_zone.internal_name}")

    if destination_zone not in current_zone.connected_zones:
        debug(f"Move failed: {destination_zone.internal_name} is not connected to {current_zone.internal_name}")
        return False

    if actor in current_zone.actors:
        current_zone.actors.remove(actor)
        debug(f"{actor.name} removed from {current_zone.internal_name}")

    destination_zone.actors.append(actor)
    actor.current_zone = destination_zone
    debug(f"{actor.name} added to {destination_zone.internal_name}")
    return True

# ─────────────────────────────────────────────────────────────
# 🔹 LOOKUP: Resolve navigation target to Zone
# ─────────────────────────────────────────────────────────────

def get_zone_by_feature(room, feature_string):
    """
    Resolves a string like "broken pillar" or "pile of crates"
    to the first Zone in the room that contains that feature.

    Parameters:
    - room: Room object containing zones
    - feature_string: exact string to match in zone.features

    Returns:
    - Zone object if found
    - None if not found
    """
    for zone in room.zones.values():
        if feature_string in zone.features:
            debug(f"Resolved feature '{feature_string}' to zone '{zone.internal_name}'")
            return zone
    debug(f"Feature '{feature_string}' not found in any zone")
    return None

def resolve_target_to_zone(target, room):
    """
    Resolves any navigation target to a Zone.

    Accepted target types:
    - str: treated as a feature name
    - any object with `.current_zone`: treated as an actor

    Parameters:
    - target: str or actor object
    - room: Room object used for feature resolution

    Returns:
    - Zone object or None
    """
    if isinstance(target, str):
        return get_zone_by_feature(room, target)
    if hasattr(target, "current_zone"):
        return target.current_zone
    debug(f"Unsupported target type for zone resolution: {type(target)}")
    return None

# ─────────────────────────────────────────────────────────────
# 🔹 PATHFINDING: Simple zone-to-zone traversal
# ─────────────────────────────────────────────────────────────

def find_path_between_zones(start_zone, target_zone):
    """
    Returns a list of zones connecting start_zone to target_zone
    using breadth-first search.

    This allows navigation across multi-zone rooms based on connectivity.

    Returns:
    - List of Zone objects [start, ..., target]
    - Empty list if no valid path exists
    """
    from collections import deque

    queue = deque([[start_zone]])
    visited = set()

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == target_zone:
            debug(f"Path found: {[z.internal_name for z in path]}")
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in current.connected_zones:
            if neighbor not in visited:
                queue.append(path + [neighbor])

    debug(f"No path from {start_zone.internal_name} to {target_zone.internal_name}")
    return []

def distance_between_zones(start_zone, target_zone):
    """
    Returns the number of hops between two zones using breadth-first search.
    If no path exists (e.g. blocked or disconnected), returns None.
    """

    if start_zone == target_zone:
        return 0

    visited = set()
    queue = deque([(start_zone, 0)])

    while queue:
        current, dist = queue.popleft()
        if current == target_zone:
            return dist

        visited.add(current)

        for neighbor in current.connections:
            if neighbor not in visited:
                queue.append((neighbor, dist + 1))

    return None  # Unreachable

# ─────────────────────────────────────────────────────────────
# 🔹 HIGH-LEVEL: Target-oriented movement
# ─────────────────────────────────────────────────────────────

def move_actor_toward_target(actor, room, target):
    """
    Generalized movement function that handles:
    - Moving toward a feature (str)
    - Moving toward another actor

    It resolves the target to a destination zone, computes the shortest
    path from the actor's current zone, and moves one step toward it.

    This enables natural language-style inputs:
    - "move to pile of crates"
    - "approach the automaton"

    Movement is only one step per call to enforce tactical pacing.

    Parameters:
    - actor: object with .name and .current_zone
    - room: Room object the actor is in
    - target: str (feature) or object with .current_zone

    Returns:
    - True if movement occurred
    - False if move invalid, unreachable, or already there
    """
    destination_zone = resolve_target_to_zone(target, room)
    if destination_zone is None:
        debug(f"Could not resolve target: {target}")
        return False

    if destination_zone == actor.current_zone:
        debug(f"{actor.name} is already in zone '{destination_zone.internal_name}'")
        return False

    path = find_path_between_zones(actor.current_zone, destination_zone)
    if len(path) < 2:
        debug(f"{actor.name} cannot reach zone '{destination_zone.internal_name}' from '{actor.current_zone.internal_name}'")
        return False

    next_zone = path[1]
    return move_actor_to_zone(actor, next_zone)

def start_movement_to_target(actor, room, target):
    """
    Initializes multi-turn movement toward a feature or actor.
    Stores the zone path in actor.movement_path.

    This replaces immediate movement — nothing happens this turn,
    but actor is now committed to a path.

    Parameters:
    - actor: actor object
    - room: the current Room
    - target: feature string or another actor

    Returns:
    - True if movement path created
    - False if target invalid or unreachable
    """
    destination_zone = resolve_target_to_zone(target, room)
    if destination_zone is None or destination_zone == actor.current_zone:
        debug(f"[MOVE INIT] Invalid or redundant move for {actor.name}")
        return False

    path = find_path_between_zones(actor.current_zone, destination_zone)
    if len(path) < 2:
        debug(f"[MOVE INIT] No valid path from {actor.current_zone.internal_name} to {destination_zone.internal_name}")
        return False

    actor.movement_path = path[1:]  # skip current zone
    actor.movement_progress = 0
    debug(f"[MOVE INIT] {actor.name} begins moving toward {destination_zone.internal_name} via {[z.internal_name for z in actor.movement_path]}")
    return True

def advance_actor_movement(actor):
    """
    Advances movement along actor's movement_path by one turn.
    - Adds 1 to progress
    - Moves to next zone when cost is met
    - Resets progress
    - Continues until path is empty

    Returns:
    - True if actor moved to a new zone this turn
    - False if still progressing or path empty
    """
    if not actor.movement_path:
        debug(f"[MOVE STEP] {actor.name} has no movement path")
        return False

    next_zone = actor.movement_path[0]
    actor.movement_progress += 1
    debug(f"[MOVE STEP] {actor.name} progressing toward {next_zone.internal_name}: {actor.movement_progress}/{next_zone.movement_cost}")

    if actor.movement_progress >= next_zone.movement_cost:
        move_actor_to_zone(actor, next_zone)
        actor.movement_path.pop(0)
        actor.movement_progress = 0
        debug(f"[MOVE STEP] {actor.name} arrived at {next_zone.internal_name}")
        return True

    return False
# ─────────────────────────────────────────────────────────────
# 🧭 MOVEMENT SYSTEM TODOs
# These enhancements build on the core pacing logic already in place.
# Track these as modular next steps.
# ─────────────────────────────────────────────────────────────

# TODO 1: Support zone-specific movement_cost delays
# - Already supported via `Zone.movement_cost`
# - Consider dynamic modifiers: slow terrain, suppression fire, debuffs

# TODO 2: Add movement interruption logic
# - Hook into perception changes mid-path
# - Trigger interrupt prompt if actor sees new threat
# - Clear movement_path if interrupted

# TODO 3: Route movement feedback through messaging.py
# - Announce movement start ("You begin moving toward the control room.")
# - Notify zone arrival ("You reach the flickering panel.")
# - Optional: show partial progress if `DEBUG_MODE = True`

# TODO 4: Allow mid-path override
# - Issuing a new movement command cancels the existing path
# - Might re-use `start_movement_to_target(...)` to overwrite safely

# TODO 5: Handle blocked zones or dynamic rerouting
# - If a zone becomes inaccessible during movement_path
#   → recalculate path or halt with warning