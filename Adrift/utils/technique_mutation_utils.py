# technique_mutation_utils.py
# Handles mutation offer generation and evolution logic for techniques.
# All mutation-related operations for technique evolution should route through here.

from random import sample, choice
from Adrift.libraries import technique_component_library as lib

# -----------------------------
# 🎲 Evolution Option Generator
# -----------------------------

def generate_evolution_offer(base_technique: dict, rarity: str = "common") -> list:
    """
    Given a technique dict, returns 4 possible evolution choices:
    - Add effect (if legal)
    - Replace effect
    - Change modifier (if any)
    - Bank offer

    The rarity parameter influences the subcomponent weights.
    """
    offers = []

    # Helper to prevent duplicate effects
    def available_effects(existing):
        return [e for e in lib.EFFECT_COMPONENTS if e not in existing]

    # Replace Effect
    if base_technique["effects"]:
        new = base_technique.copy()
        pool = available_effects(base_technique["effects"])
        if pool:
            new["effects"] = [choice(pool)]
            offers.append({"type": "replace_effect", "result": new})

    # Add Effect (only if under cap)
    if len(base_technique["effects"]) < 2:
        new = base_technique.copy()
        pool = available_effects(base_technique["effects"])
        if pool:
            new["effects"] = base_technique["effects"] + [choice(pool)]
            offers.append({"type": "add_effect", "result": new})

    # Change Modifier
    if base_technique.get("modifier") in lib.MODIFIER_COMPONENTS:
        current = base_technique["modifier"]
        options = [m for m in lib.MODIFIER_COMPONENTS if m != current]
        if options:
            new = base_technique.copy()
            new["modifier"] = choice(options)
            offers.append({"type": "change_modifier", "result": new})

    # Bank option (always valid)
    offers.append({"type": "bank", "result": None})

    # Always return 4 choices (pad with duplicate banks if needed)
    while len(offers) < 4:
        offers.append({"type": "bank", "result": None})

    return offers

def apply_mutation(base_technique: dict, offer: dict) -> dict:
    """
    Applies the selected mutation offer to the base technique.

    Arguments:
        base_technique: The original technique dict before mutation.
        offer: A dict containing keys:
            - "type": One of "replace_effect", "add_effect", "change_modifier", "bank"
            - "result": The precomputed result technique (except for "bank")

    Returns:
        A new technique dict reflecting the chosen mutation.
        If type == "bank", returns the original technique unchanged.
    """
    mutation_type = offer["type"]

    if mutation_type == "bank":
        return base_technique  # No change

    if mutation_type in {"replace_effect", "add_effect", "change_modifier"}:
        return offer["result"]

    raise ValueError(f"Unknown mutation type: {mutation_type}")

# -----------------------------
# 🧪 TODO:
# -----------------------------
# - Add rarity-based weighting to evolution outcomes (currently stubbed)
# - Test interactions with rare-only components
# - Ensure tag validation on evolved results (reuse tag validator)
# - Track and log choices for mutation history per actor
