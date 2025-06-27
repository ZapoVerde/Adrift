# skill_xp_utils.py
# XP tracking for skills and techniques based on action tags.

from Adrift.definitions.technique_defs import TECHNIQUE_DB


def track_xp_gain(actor, tags: list[str]) -> None:
    """
    Distributes XP to matching skills and techniques.

    Automatically initializes skills/techniques if needed.
    
    XP gain is flat per success. Level-up is probabilistic.
    """
    for tech_id, definition in TECHNIQUE_DB.items():
        if not _tags_match(tags, definition.get("tags", [])):
            continue

        skill_id = definition["base_skill"]

        # Ensure both skill and technique exist
        actor.initialize_skill_if_missing(skill_id)
        actor.initialize_technique_if_missing(skill_id, tech_id)

        # Track XP
        skill_block = actor.skills[skill_id]
        tech_block = skill_block["techniques"][tech_id]

        skill_block["xp"] += 1
        tech_block["xp"] += 1

        # Add inside track_xp_gain(), after skill XP gain
        actor.mutation_xp = getattr(actor, "mutation_xp", 0) + 1


        # Check for skill level-up
        _check_level_up(skill_block)
        _check_level_up(tech_block)


# -----------------------------
# 🔍 Tag Matching
# -----------------------------

def _tags_match(observed: list[str], required: list[str]) -> bool:
    """
    Returns True if any of the required tags are found in the observed list.
    """
    return any(tag in observed for tag in required)


# -----------------------------
# ⬆️ Level-Up Check
# -----------------------------

def _check_level_up(block: dict) -> None:
    """
    Performs a probabilistic level-up check for the given skill or technique block.
    XP is preserved. Visibility is granted on first level.
    """
    xp = block.get("xp", 0)
    level = block.get("level", 0)

    # Compute chance to level up
    threshold = 5 * (2 ** level)
    if xp >= threshold:
        block["level"] = level + 1
        block["visible"] = True