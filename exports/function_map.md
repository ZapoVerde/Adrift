## 📦 definitions/actor.py

### `initialize_skill_if_missing()` – line 21
_Inputs_: self, skill_id
_Calls_: initialize_skill_if_missing
_Called by_: initialize_skill_if_missing, track_xp_gain

### `initialize_technique_if_missing()` – line 24
_Inputs_: self, skill_id, tech_id
_Calls_: initialize_technique_if_missing
_Called by_: initialize_technique_if_missing, track_xp_gain

### `__init__()` – line 27
_Inputs_: self, name, current_zone

### `has_skill()` – line 47
_Purpose_: Returns True if the actor currently owns the given skill.
_Inputs_: self, skill_id

### `has_technique()` – line 51
_Purpose_: Returns True if the actor has the given technique in their flat cache.
_Inputs_: self, tech_id

### `get_technique()` – line 55
_Purpose_: Safe accessor for a technique the actor owns.
_Inputs_: self, skill_id, tech_id
_Calls_: KeyError

### `add_skill()` – line 69
_Purpose_: Adds a properly initialized skill block to the actor.
_Inputs_: actor, skill_id
_Calls_: ValueError

### `add_technique()` – line 97
_Purpose_: Adds a technique instance to the actor, based on canonical TECHNIQUE_DB.
_Inputs_: actor, tech_id
_Calls_: ValueError, deepcopy, get
_Called by_: auto_unlock_techniques

---

## 📦 definitions/effect.py

### `__init__()` – line 5
_Inputs_: self

---

## 📦 definitions/evolution_offer_generator.py

### `generate_evolution_offer()` – line 15
_Purpose_: Generate a set of mutation options for a technique based on the given skill.
_Inputs_: skill, boost_level, current, banks
_Calls_: _generate_base_technique, append, copy, evolve_technique
_Called by_: generate_evolution_offer_for_actor, get_mutation_offer

### `_generate_base_technique()` – line 52
_Purpose_: Stub function to generate a technique if none provided.
_Inputs_: skill
_Calls_: generate_technique
_Called by_: generate_evolution_offer

---

## 📦 definitions/faction.py

### `__init__()` – line 5
_Inputs_: self

---

## 📦 definitions/floorplan.py

### `create_empty_tile()` – line 23
_Purpose_: Create a blank tile with default fields.
_Called by_: create_floorplan

### `create_floorplan()` – line 43
_Purpose_: Generate a new floorplan map with initialized tiles.
_Inputs_: width, height, map_id, seed, label
_Calls_: create_empty_tile, range
_Called by_: enter_test_map

### `get_tile()` – line 75
_Purpose_: Retrieve a tile safely from the floorplan.
_Inputs_: floorplan, coord
_Calls_: get
_Called by_: enter_test_map

### `set_tile()` – line 92
_Purpose_: Overwrite a tile in the floorplan.
_Inputs_: floorplan, coord, tile_data
_Called by_: enter_test_map

---

## 📦 definitions/item.py

### `__init__()` – line 5
_Inputs_: self

---

## 📦 definitions/skill.py

### `__init__()` – line 11
_Inputs_: self, skill_id

### `add_xp()` – line 19
_Inputs_: self, amount

### `add_boost()` – line 24
_Inputs_: self, count

### `consume_boost()` – line 27
_Inputs_: self

### `has_boost()` – line 32
_Inputs_: self

---

## 📦 flow/action_flow.py

### `run_action_phase()` – line 9
_Purpose_: Executes the full action phase for an actor, including:
_Inputs_: actor, context
_Calls_: auto_unlock_techniques, get, handle_post_action_mutation, track_xp_gain

---

## 📦 flow/actor_mutation_flow.py

### `get_mutation_offer()` – line 24
_Purpose_: Generates 4 evolution options for the given skill, factoring in active boost.
_Inputs_: actor, skill
_Calls_: _boost_level_to_rarity, generate_evolution_offer, get

### `can_offer_boost()` – line 46
_Purpose_: Returns True if actor has 3+ banked mutations and no current offer boost on skill.
_Inputs_: actor, skill
_Calls_: get
_Called by_: apply_boost

### `apply_boost()` – line 52
_Purpose_: Consumes 3 banked mutations to boost rarity of next offer for a given skill.
_Inputs_: actor, skill
_Calls_: ValueError, can_offer_boost, setdefault

### `apply_mutation_choice()` – line 65
_Purpose_: Applies a chosen mutation result to the actor.
_Inputs_: actor, skill, choice
_Calls_: append, get, pop, setdefault
_Called by_: handle_pending_mutation_offer

### `handle_pending_mutation_offer()` – line 88
_Purpose_: Wrapper invoked during the action phase if the actor has a pending offer.
_Inputs_: actor, context
_Calls_: apply_mutation_choice, get, select_mutation_option

### `handle_post_action_mutation()` – line 100
_Purpose_: Checks if any visible technique is eligible for a mutation offer.
_Inputs_: actor
_Calls_: generate_evolution_offer_for_actor, get, getattr, items, random
_Called by_: run_action_phase

### `_boost_level_to_rarity()` – line 132
_Purpose_: Translates boost level to rarity tier.
_Inputs_: boost_level
_Called by_: generate_evolution_offer_for_actor, get_mutation_offer

---

## 📦 flow/dialogue_flow.py

### `start_dialogue()` – line 4
_Inputs_: npc, player

### `advance_dialogue_state()` – line 6
_Inputs_: npc, choice

### `resolve_dialogue_outcome()` – line 8
_Inputs_: npc, player

---

## 📦 flow/encounter_flow.py

### `detect_encounter()` – line 4
_Inputs_: actor, visible_entities

### `trigger_ambush()` – line 6
_Inputs_: enemy, player

---

## 📦 flow/engine.py

### `enter_test_map()` – line 31
_Purpose_: Stub function to simulate entering a test tactical map.
_Calls_: create_floorplan, get_tile, set_tile

---

## 📦 flow/exploration_flow.py

### `resolve_room_entry()` – line 4
_Inputs_: player, room

### `handle_travel_command()` – line 6
_Inputs_: command

---

## 📦 flow/story_flow.py

### `check_story_triggers()` – line 4
_Inputs_: state

### `fire_story_event()` – line 6
_Inputs_: event_id

---

## 📦 helpers/actor_helpers.py

### `initialize_skill_if_missing()` – line 7
_Purpose_: Adds a new skill block to the actor if it doesn't exist.
_Inputs_: actor, skill_id
_Called by_: initialize_skill_if_missing, track_xp_gain

### `initialize_technique_if_missing()` – line 22
_Purpose_: Adds a technique to the actor's skill block if missing.
_Inputs_: actor, skill_id, tech_id
_Calls_: ValueError, get
_Called by_: initialize_technique_if_missing, track_xp_gain

### `validate_skill_structure()` – line 55
_Inputs_: skill_block
_Calls_: issubset

### `validate_technique_structure()` – line 60
_Inputs_: tech_block
_Calls_: issubset

---

## 📦 io/input_handler.py

### `get_player_input()` – line 4

### `parse_command()` – line 6
_Inputs_: raw_input

---

## 📦 io/messaging.py

### `queue_room_description()` – line 4
_Inputs_: room

### `queue_entity_sightings()` – line 6
_Inputs_: entities

### `queue_player_action_feedback()` – line 8
_Inputs_: command

### `queue_enemy_action_feedback()` – line 10
_Inputs_: actor

### `queue_status_effect_messages()` – line 12
_Inputs_: actor

### `flush_message_queue()` – line 14

---

## 📦 legacy/map.py

### `__init__()` – line 22
_Inputs_: self, rooms

### `get_room()` – line 26
_Purpose_: Returns a Room object by its internal name.
_Inputs_: self, internal_name
_Calls_: get

### `set_starting_room()` – line 32
_Purpose_: Sets the initial room when the map is first loaded.
_Inputs_: self, internal_name
_Calls_: get

### `move_to_room()` – line 38
_Purpose_: Moves the current room pointer to a new room.
_Inputs_: self, internal_name

---

## 📦 legacy/tile.py

### `__init__()` – line 8
_Inputs_: self

---

## 📦 libraries/technique_component_library.py

### `validate_component()` – line 112
_Inputs_: comp
_Calls_: isinstance, issubset, keys, set

### `get_all_component_ids()` – line 123
_Calls_: extend, keys, values

---

## 📦 utils/action_utils.py

### `resolve_walk_action()` – line 4
_Inputs_: player, direction

### `resolve_search_action()` – line 6
_Inputs_: player

### `resolve_use_action()` – line 8
_Inputs_: player, item

---

## 📦 utils/actor_mutation_utils.py

### `apply_mutation_to_actor()` – line 7
_Purpose_: Applies a selected mutation offer to the actor's technique instance.
_Inputs_: actor, skill_id, technique_id, offer
_Calls_: ValueError, append, apply_mutation, get, setdefault

---

## 📦 utils/actor_offer_utils.py

### `generate_evolution_offer_for_actor()` – line 7
_Purpose_: Generates 4 mutation offers for the given actor's technique.
_Inputs_: actor, technique_id
_Calls_: ValueError, _boost_level_to_rarity, generate_evolution_offer, get
_Called by_: handle_post_action_mutation

### `_boost_level_to_rarity()` – line 34
_Purpose_: Converts integer boost level to a string rarity tier.
_Inputs_: boost_level
_Called by_: generate_evolution_offer_for_actor, get_mutation_offer

---

## 📦 utils/combat_utils.py

### `resolve_attack()` – line 4
_Inputs_: attacker, target

### `calculate_damage()` – line 6
_Inputs_: weapon, attacker, target

### `roll_hit()` – line 8
_Inputs_: attacker, target

---

## 📦 utils/cover_utils.py

### `get_cover_objects_along_path()` – line 26
_Purpose_: Scans the tiles along the given path and returns all objects that influence cover.
_Inputs_: path, floorplan
_Calls_: append, get
_Called by_: calculate_total_cover

### `calculate_total_cover()` – line 48
_Purpose_: Computes the total cover_rating from objects along the path.
_Inputs_: path, floorplan
_Calls_: get, get_cover_objects_along_path, isinstance, len, sum

---

## 📦 utils/debug_utils.py

### `debug()` – line 19
_Inputs_: message
_Calls_: print, replace, split, stack, upper
_Called by_: advance_actor_movement, find_path_between_zones, get_zone_by_feature, move_actor_to_zone, move_actor_toward_target, observe, resolve_target_to_zone, start_movement_to_target

---

## 📦 utils/evasion_utils.py

### `calculate_visibility()` – line 4
_Inputs_: actor, observer

### `get_stealth_modifier()` – line 6
_Inputs_: actor

---

## 📦 utils/evolution_offer_utils.py

### `get_allowed_rarities()` – line 13
_Purpose_: Returns the list of allowed rarities after applying boost filtering.
_Inputs_: boost
_Calls_: min
_Called by_: generate_evolution_offer_for_actor

### `generate_evolution_offer_for_actor()` – line 27
_Purpose_: Generates 4 weighted mutation offers for a given actor's visible technique.
_Inputs_: actor, technique_id
_Calls_: ValueError, append, choice, choices, generate_evolution_offer, get, get_allowed_rarities, keys, list, min, range, values
_Called by_: handle_post_action_mutation

---

## 📦 utils/general_utils.py

### `validate_tags()` – line 12
_Purpose_: Validates that all tags in a given definition dict exist in TAG_DB.
_Inputs_: defs, kind
_Calls_: ValueError, get, items, set
_Called by_: validate_all_tags

### `validate_all_tags()` – line 23
_Purpose_: Runs tag validation on both skills and techniques.
_Inputs_: skill_defs, technique_defs
_Calls_: validate_tags

### `trace_line()` – line 31
_Purpose_: Traces a straight line from `start` to `end` using a grid-based algorithm.
_Inputs_: start, end, floorplan, stop_at_block
_Calls_: abs, append, bresenham_line, get
_Called by_: test_diagonal_line_with_blocking_tile, test_missing_env_field, test_missing_tile_skipped, test_multiple_penalty_sources, test_no_environment_penalty, test_single_fog_tile, test_straight_line_unblocked, test_tile_with_blocking_thing

### `bresenham_line()` – line 58
_Purpose_: Bresenham's line algorithm (integer-based, grid-safe)
_Inputs_: x0, y0, x1, y1
_Calls_: abs, append
_Called by_: trace_line

### `compute_visibility_penalty_along_path()` – line 121
_Purpose_: Given a traced path from `trace_line`, compute the cumulative visibility penalty
_Inputs_: traced_path
_Calls_: get
_Called by_: test_empty_path, test_env_not_list, test_invalid_path_type, test_missing_env_field, test_missing_tile_dict, test_multiple_penalty_sources, test_no_environment_penalty, test_single_fog_tile, test_step_not_dict

---

## 📦 utils/initiative_queue.py

### `initialize_initiative_queue()` – line 4
_Inputs_: actors

### `pop_next_actor()` – line 6

### `schedule_next_turn()` – line 8
_Inputs_: actor

---

## 📦 utils/inventory_utils.py

### `add_item_to_inventory()` – line 4
_Inputs_: actor, item

### `remove_item_from_inventory()` – line 6
_Inputs_: actor, item

### `is_item_usable()` – line 8
_Inputs_: actor, item

---

## 📦 utils/loot_utils.py

### `roll_loot_table()` – line 4
_Inputs_: source

### `drop_loot_to_room()` – line 6
_Inputs_: room, items

---

## 📦 utils/movement_utils.py

### `move_actor_to_zone()` – line 28
_Purpose_: 🚶 Low-level zone transition function. Moves an actor from their current
_Inputs_: actor, destination_zone
_Calls_: append, debug, remove
_Called by_: advance_actor_movement, move_actor_toward_target

### `get_zone_by_feature()` – line 68
_Purpose_: Resolves a string like "broken pillar" or "pile of crates"
_Inputs_: room, feature_string
_Calls_: debug, values
_Called by_: resolve_target_to_zone

### `resolve_target_to_zone()` – line 88
_Purpose_: Resolves any navigation target to a Zone.
_Inputs_: target, room
_Calls_: debug, get_zone_by_feature, hasattr, isinstance, type
_Called by_: move_actor_toward_target, start_movement_to_target

### `find_path_between_zones()` – line 114
_Purpose_: Returns a list of zones connecting start_zone to target_zone
_Inputs_: start_zone, target_zone
_Calls_: add, append, debug, deque, popleft, set
_Called by_: move_actor_toward_target, start_movement_to_target

### `distance_between_zones()` – line 150
_Purpose_: Returns the number of hops between two zones using breadth-first search.
_Inputs_: start_zone, target_zone
_Calls_: add, append, deque, popleft, set
_Called by_: observe

### `move_actor_toward_target()` – line 179
_Purpose_: Generalized movement function that handles:
_Inputs_: actor, room, target
_Calls_: debug, find_path_between_zones, len, move_actor_to_zone, resolve_target_to_zone

### `start_movement_to_target()` – line 220
_Purpose_: Initializes multi-turn movement toward a feature or actor.
_Inputs_: actor, room, target
_Calls_: debug, find_path_between_zones, len, resolve_target_to_zone

### `advance_actor_movement()` – line 252
_Purpose_: Advances movement along actor's movement_path by one turn.
_Inputs_: actor
_Calls_: debug, move_actor_to_zone, pop

---

## 📦 utils/npc_ai.py

### `handle_npc_action()` – line 4
_Inputs_: npc

### `choose_npc_action()` – line 6
_Inputs_: npc

### `npc_can_see_player()` – line 8
_Inputs_: npc, player

---

## 📦 utils/skill_xp_utils.py

### `track_xp_gain()` – line 7
_Purpose_: Distributes XP to matching skills and techniques.
_Inputs_: actor, tags
_Calls_: _check_level_up, _tags_match, get, getattr, initialize_skill_if_missing, initialize_technique_if_missing, items
_Called by_: run_action_phase

### `_tags_match()` – line 45
_Purpose_: Returns True if any of the required tags are found in the observed list.
_Inputs_: observed, required
_Calls_: any
_Called by_: track_xp_gain

### `_check_level_up()` – line 56
_Purpose_: Performs a probabilistic level-up check for the given skill or technique block.
_Inputs_: block
_Calls_: get
_Called by_: track_xp_gain

---

## 📦 utils/skills_utils.py

### `tick_skill_progression()` – line 4
_Inputs_: actor

### `get_skill_modifier()` – line 6
_Inputs_: actor, skill_tag

### `add_skill_xp()` – line 8
_Inputs_: actor, tag, amount

---

## 📦 utils/status_effects.py

### `apply_status_effects()` – line 4
_Inputs_: actor

### `tick_status_effects()` – line 6
_Inputs_: actor

### `add_effect()` – line 8
_Inputs_: actor, effect_dict

---

## 📦 utils/technique_mutation_utils.py

### `generate_evolution_offer()` – line 12
_Purpose_: Given a technique dict, returns 4 possible evolution choices:
_Inputs_: base_technique, rarity
_Calls_: append, available_effects, choice, copy, get, len
_Called by_: generate_evolution_offer_for_actor, get_mutation_offer

### `available_effects()` – line 25
_Inputs_: existing
_Called by_: generate_evolution_offer

### `apply_mutation()` – line 62
_Purpose_: Applies the selected mutation offer to the base technique.
_Inputs_: base_technique, offer
_Calls_: ValueError
_Called by_: apply_mutation_to_actor

---

## 📦 utils/technique_unlock_utils.py

### `auto_unlock_techniques()` – line 7
_Purpose_: Scans canonical techniques and adds any to the actor whose
_Inputs_: actor
_Calls_: add_technique, get, int, items
_Called by_: run_action_phase

---

## 📦 utils/technique_utils.py

### `generate_technique()` – line 12
_Purpose_: Generate a base technique scaffold with random components for a given skill.
_Inputs_: skill_id
_Calls_: choice, keys, list
_Called by_: _generate_base_technique

### `evolve_replace_effect()` – line 36
_Purpose_: Replaces the first effect with a different one from the effect pool.
_Inputs_: tech
_Calls_: append, choice, get, keys, list, setdefault
_Called by_: evolve_technique

### `evolve_add_modifier()` – line 69
_Purpose_: Adds a new modifier from the pool. Does nothing if already added.
_Inputs_: tech, options
_Calls_: append, choice, get, setdefault
_Called by_: evolve_technique

### `evolve_add_effect()` – line 91
_Purpose_: Adds a new effect if not already present and not already added before.
_Inputs_: tech, options
_Calls_: append, choice, get, len, setdefault
_Called by_: evolve_technique

### `evolve_technique()` – line 122
_Purpose_: Dispatches to the correct mutation function for test scaffolding.
_Inputs_: tech, mode, options
_Calls_: ValueError, evolve_add_effect, evolve_add_modifier, evolve_replace_effect
_Called by_: generate_evolution_offer

### `get_available_mutations()` – line 141
_Purpose_: Returns a list of valid mutation types for a given technique.
_Inputs_: tech
_Calls_: append, get, len

---

## 📦 utils/test_trace_line.py

### `make_blank_tile()` – line 6
_Called by_: test_diagonal_line_with_blocking_tile, test_missing_tile_skipped, test_straight_line_unblocked, test_tile_with_blocking_thing

### `test_straight_line_unblocked()` – line 9
_Calls_: all, make_blank_tile, range, trace_line

### `test_diagonal_line_with_blocking_tile()` – line 17
_Calls_: make_blank_tile, range, trace_line

### `test_tile_with_blocking_thing()` – line 27
_Calls_: append, make_blank_tile, trace_line

### `test_missing_tile_skipped()` – line 34
_Calls_: make_blank_tile, trace_line

---

## 📦 utils/test_visibility_penalty.py

### `make_tile_with_env()` – line 6
_Purpose_: Helper: create tile with list of env objects, each with a visibility_penalty.
_Inputs_: penalties
_Calls_: enumerate
_Called by_: test_missing_env_field, test_multiple_penalty_sources, test_single_fog_tile

### `test_no_environment_penalty()` – line 14
_Calls_: compute_visibility_penalty_along_path, range, trace_line

### `test_single_fog_tile()` – line 19
_Calls_: compute_visibility_penalty_along_path, make_tile_with_env, trace_line

### `test_multiple_penalty_sources()` – line 28
_Calls_: compute_visibility_penalty_along_path, make_tile_with_env, trace_line

### `test_missing_env_field()` – line 37
_Calls_: compute_visibility_penalty_along_path, make_tile_with_env, trace_line

### `test_empty_path()` – line 46
_Calls_: compute_visibility_penalty_along_path

### `test_invalid_path_type()` – line 49
_Calls_: compute_visibility_penalty_along_path, raises

### `test_step_not_dict()` – line 53
_Calls_: compute_visibility_penalty_along_path, raises

### `test_missing_tile_dict()` – line 57
_Calls_: compute_visibility_penalty_along_path, raises

### `test_env_not_list()` – line 61
_Calls_: compute_visibility_penalty_along_path, raises

---

## 📦 utils/visibility_utils.py

### `get_visibility_caps()` – line 8
_Purpose_: Returns (max_clear, max_vague) based on light level.
_Inputs_: light_level
_Called by_: observe

### `visual_coverage()` – line 37
_Purpose_: Estimate how much of the target zone is visible from the observer.
_Inputs_: observer_zone, target_zone
_Calls_: len, trace_visibility_path
_Called by_: observe

### `observe()` – line 59
_Purpose_: Perception scan with:
_Inputs_: observer
_Calls_: append, debug, distance_between_zones, get, get_visibility_caps, getattr, max, trace_visibility_path, visual_coverage

### `trace_visibility_path()` – line 150
_Purpose_: Returns the list of intermediate zones (excluding origin and target)
_Inputs_: origin, target
_Calls_: add, append, deque, popleft, set
_Called by_: observe, visual_coverage

### `compute_visibility_penalty_along_path()` – line 182
_Inputs_: traced_path
_Calls_: TypeError, get, isinstance
_Called by_: test_empty_path, test_env_not_list, test_invalid_path_type, test_missing_env_field, test_missing_tile_dict, test_multiple_penalty_sources, test_no_environment_penalty, test_single_fog_tile, test_step_not_dict

---

## 📦 utils/world_utils.py

### `get_all_actors_in_room()` – line 4
_Inputs_: room

### `remove_dead_entities()` – line 6

### `transfer_loot_to_room()` – line 8
_Inputs_: npc

---

## 📦 world/discovery.py

### `__init__()` – line 8
_Inputs_: self, type, faction, seed

### `reveal()` – line 15
_Inputs_: self
_Calls_: instantiate

### `instantiate()` – line 19
_Inputs_: self
_Calls_: LocationInstance
_Called by_: reveal

### `__init__()` – line 24
_Inputs_: self, type, seed

### `generate_floorplan()` – line 32
_Inputs_: self

### `teardown()` – line 35
_Inputs_: self

---

## 📦 world/generation.py

### `__init__()` – line 8
_Inputs_: self, world_seed

### `generate_tile()` – line 11
_Inputs_: self, tile, neighbors
_Calls_: sample_biome, sample_elevation, sample_features, sample_moisture

### `sample_biome()` – line 18
_Inputs_: self, tile, neighbors
_Called by_: generate_tile

### `sample_elevation()` – line 21
_Inputs_: self, tile, neighbors
_Called by_: generate_tile

### `sample_moisture()` – line 24
_Inputs_: self, tile, neighbors
_Called by_: generate_tile

### `sample_features()` – line 27
_Inputs_: self, tile, neighbors
_Called by_: generate_tile

---

## 📦 world/hex.py

### `__init__()` – line 8
_Inputs_: self, q, r, seed
_Calls_: generate_seed

### `generate_seed()` – line 20
_Inputs_: self
_Calls_: hash
_Called by_: __init__

### `coord()` – line 23
_Inputs_: self

---

