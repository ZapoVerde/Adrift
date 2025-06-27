# actor_helpers.py
# Mutation-safe helpers for skill and technique initialization and validation.

from Adrift.definitions.technique_defs import TECHNIQUE_DB


def initialize_skill_if_missing(actor, skill_id: str) -> None:
    """
    Adds a new skill block to the actor if it doesn't exist.

    Includes all required fields to prevent downstream KeyErrors.
    """
    if skill_id not in actor.skills:
        actor.skills[skill_id] = {
            "level": 0,
            "xp": 0,
            "visible": False,
            "techniques": {}
        }


def initialize_technique_if_missing(actor, skill_id: str, tech_id: str) -> None:
    """
    Adds a technique to the actor's skill block if missing.

    Requires that the skill already exist. Initializes all required fields.
    """
    if skill_id not in actor.skills:
        raise ValueError(f"Skill '{skill_id}' must be initialized before adding technique '{tech_id}'")

    techs = actor.skills[skill_id]["techniques"]
    if tech_id not in techs:
        base = TECHNIQUE_DB.get(tech_id)
        if not base:
            raise ValueError(f"Technique ID '{tech_id}' not found in TECHNIQUE_DB")

        # Fully initialized technique block
        techs[tech_id] = {
            "level": 0,
            "xp": 0,
            "visible": False,
            "base_skill": skill_id,
            "mutations": [],
            "metadata": {
                "rarity": base.get("rarity", "common")
            }
        }
        actor.techniques[tech_id] = techs[tech_id]


# -----------------------------
# 🔍 Optional Validators
# -----------------------------

def validate_skill_structure(skill_block: dict) -> bool:
    required_keys = {"level", "xp", "visible", "techniques"}
    return required_keys.issubset(skill_block)


def validate_technique_structure(tech_block: dict) -> bool:
    required_keys = {"level", "xp", "visible", "base_skill", "mutations", "metadata"}
    return required_keys.issubset(tech_block)
