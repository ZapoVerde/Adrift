# actor_offer_utils.py
# High-level mutation offer generator for actors using skill/technique state.

from Adrift.utils.technique_mutation_utils import generate_evolution_offer


def generate_evolution_offer_for_actor(actor, technique_id: str) -> list[dict]:
    """
    Generates 4 mutation offers for the given actor's technique.

    This is a pure function: no state is modified.

    Parameters:
        actor: Actor instance
        technique_id: ID of the technique to mutate

    Returns:
        List of 4 offer dicts, each with:
            - "type": str
            - "result": new technique dict (or None for 'bank')
    """
    technique = actor.techniques.get(technique_id)
    if not technique:
        raise ValueError(f"Technique '{technique_id}' not found on actor.")
    if not technique.get("visible", False):
        raise ValueError(f"Technique '{technique_id}' is not yet visible or unlocked.")
    skill_id = technique["skill"]
    boost_level = actor.skill_boosts.get(skill_id, 0)
    rarity = _boost_level_to_rarity(boost_level)

    return generate_evolution_offer(technique, rarity)


def _boost_level_to_rarity(boost_level: int) -> str:
    """
    Converts integer boost level to a string rarity tier.
    """
    if boost_level >= 3:
        return "epic"
    elif boost_level == 2:
        return "rare"
    elif boost_level == 1:
        return "uncommon"
    return "common"
