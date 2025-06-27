# engine.py

"""
Main game loop and core flow controller.
This file orchestrates the high-level progression of gameplay phases:
- World entry
- Tactical exploration
- Combat resolution

⚙️ Architectural Philosophy:
- `engine.py` defines flow, not logic.
- All calculations, rules, and simulation updates are offloaded to utils (e.g. combat_utils.py, player_utils.py).
- No embedded string output. All messaging routed through messaging.py or debug_utils.py.
- Tactical and world maps operate as separate layers: engine manages transitions.
- Designed to be modular, testable, and cleanly extensible.

📦 Current Flow Phases (subject to extension):
1. World Entry
2. Tactical Floorplan Load
3. Perception Pass
4. Initiative Queue
5. Actor Turns (player and AI)
6. Cleanup & Effects

This scaffolding will evolve with additional modules and rendering layers, but core responsibility remains orchestration only.
"""

from definitions.floorplan import create_floorplan, get_tile, set_tile

# === Test Stub: Map Entry Phase ===
def enter_test_map():
    """
    Stub function to simulate entering a test tactical map.
    Constructs a minimal map instance using dict-based tiles.
    """
    fp = create_floorplan(width=10, height=10, map_id="test_entry", seed=42, label="Test Zone")
    tile = get_tile(fp, (2, 2))
    if tile:
        tile["terrain"] = "mud"
        tile["light"] = 0.3
        set_tile(fp, (2, 2), tile)

    return fp

# === Future: Turn-Based Phase Controller ===
# Placeholder for phase-driven orchestration:
# - perform_perception()
# - roll_initiative()
# - resolve_actor_turns()
# - apply_status_effects()
# - check_combat_end()

if __name__ == "__main__":
    test_fp = enter_test_map()
    from pprint import pprint
    pprint(test_fp["tiles"][(2, 2)])
