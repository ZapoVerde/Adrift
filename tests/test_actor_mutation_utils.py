# actor_mutation_utils.py
# Bridges the functional mutation system with the actor state model.

from Adrift.utils.technique_mutation_utils import apply_mutation


def apply_mutation_to_actor(actor, skill_id: str, technique_id: str, offer: dict):
    """
    Applies a selected mutation offer to the actor's technique instance.

    Parameters:
        actor: Actor instance
        skill_id: Skill the technique belongs to (e.g., "melee", "sword")
        technique_id: The canonical technique ID (e.g., "piercing_thrust")
        offer: A mutation offer dict, as returned by generate_evolution_offer()

    Behavior:
        - Retrieves the actor’s current technique instance
        - Applies the mutation using pure-functional `apply_mutation`
        - Replaces the actor’s stored copy with the mutated result
        - Appends the offer to technique["mutations"] for traceability
    """
    # Grab the actor's current version
    skill_block = actor.skills.get(skill_id)
    if not skill_block:
        raise ValueError(f"Actor missing skill: {skill_id}")

    technique = skill_block["techniques"].get(technique_id)
    if not technique:
        raise ValueError(f"Actor missing technique: {technique_id} under skill {skill_id}")

    # Apply mutation (returns a new dict or same if 'bank')
    updated = apply_mutation(technique, offer)

    # Overwrite the actor's copy
    actor.skills[skill_id]["techniques"][technique_id] = updated
    actor.techniques[technique_id] = updated

    # Optionally: track this in the mutation history
    if offer["type"] != "bank":
        updated.setdefault("mutations", []).append({
            "applied_offer": offer,
            "via": "apply_mutation_to_actor"
        })

