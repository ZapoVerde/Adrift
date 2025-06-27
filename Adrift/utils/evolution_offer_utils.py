# evolution_offer_utils.py

"""
Generates mutation offers based on rarity and actor boost state.
"""

import random
from Adrift.definitions.technique_defs import TECHNIQUE_DB
from Adrift.utils.technique_mutation_utils import generate_evolution_offer
from Adrift.constants.mutation_rarity_weights import RARITY_WEIGHTS_BY_BOOST


def get_allowed_rarities(boost: int) -> list[str]:
    """
    Returns the list of allowed rarities after applying boost filtering.

    Boost levels:
        0 → all rarities
        1 → uncommon, rare, epic
        2 → rare, epic
        3+ → epic only
    """
    tiers = ["common", "uncommon", "rare", "epic"]
    return tiers[min(boost, 3):]


def generate_evolution_offer_for_actor(actor, technique_id: str) -> list[dict]:
    """
    Generates 4 weighted mutation offers for a given actor's visible technique.

    Returns list of offer dicts:
        - type
        - skill
        - technique
        - value
    """
    technique = actor.techniques.get(technique_id)
    if not technique:
        raise ValueError(f"Technique '{technique_id}' not found on actor.")
    if not technique.get("visible", False):
        raise ValueError(f"Technique '{technique_id}' is not yet visible or unlocked.")

    skill_id = technique["base_skill"]
    boost_level = actor.get("mutations", {}).get("boosts", {}).get(skill_id, 0)
    allowed_rarities = get_allowed_rarities(boost_level)

    weights = {
        rarity: RARITY_WEIGHTS_BY_BOOST[min(boost_level, 3)][rarity]
        for rarity in allowed_rarities
    }

    offers = []
    for _ in range(4):
        rarity = random.choices(
            population=list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]
        offer_options = generate_evolution_offer(technique, rarity)
        offer = random.choice(offer_options)
        offers.append(offer)

    return offers
