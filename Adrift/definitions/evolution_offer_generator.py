# evolution_offer_generator.py
# Entry point for generating technique mutation offers.
# Selects mutation options based on skill, tier weight, and deduplication constraints.

from random import choices, sample
from Adrift.definitions import technique_defs
from Adrift.utils.technique_utils import evolve_technique, get_available_mutations
from Adrift.libraries import technique_component_library as lib

# ────────────────────────────────────────────────────────────────────────────────
# 🎯 Core Entry Point
# ────────────────────────────────────────────────────────────────────────────────


def generate_evolution_offer(skill: str,
                             boost_level: int = 0,
                             current=None,
                             banks: int = 0) -> list:
    """
    Generate a set of mutation options for a technique based on the given skill.
    If boost_level > 0, removes lowest rarity tier(s) and adjusts weights accordingly.

    Args:
        skill (str): The base skill this offer applies to (e.g. 'sword')
        boost_level (int): 0 (default) = no boost, 1 = skip common, etc.
        current (dict): Existing technique dict to mutate (optional)
        banks (int): If >= 3, includes a boost offer (if not already boosted)

    Returns:
        List of dicts, each representing a candidate evolved technique or bank option
    """
    base = current or _generate_base_technique(skill)
    mutation_types = ["add_effect", "replace_effect", "add_modifier"]

    offers = []
    for mtype in mutation_types:
        evolved = evolve_technique(base.copy(), mtype)
        evolved["_mutation"] = mtype  # track which kind of mutation this is
        offers.append(evolved)

    if banks >= 3:
        offers.append({"_mutation": "bank"})

    return offers


# ────────────────────────────────────────────────────────────────────────────────
# 🧱 Internal Helpers
# ────────────────────────────────────────────────────────────────────────────────


def _generate_base_technique(skill: str) -> dict:
    """Stub function to generate a technique if none provided."""
    from Adrift.utils.technique_utils import generate_technique
    return generate_technique(skill)


# ────────────────────────────────────────────────────────────────────────────────
# 🧪 TODO:
# - Hook rarity boost weight logic to boost_level
# - Score and sort offers for UI display
# - Support for optional mutation filter constraints
# - Unit tests covering all boost levels and fallback behavior
# - Reject duplicate effect/modifier combos if already present
