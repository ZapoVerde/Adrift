# action_flow.py
# Integrates action resolution, XP gain, technique unlocking, and mutation offers.

from Adrift.flow import actor_mutation_flow
from Adrift.utils.skill_xp_utils import track_xp_gain
from Adrift.utils.technique_unlock_utils import auto_unlock_techniques


def run_action_phase(actor, context: dict) -> None:
    """
    Executes the full action phase for an actor, including:
    1. Action resolution (stubbed)
    2. XP gain based on action tags
    3. Automatic technique unlocks
    4. Post-action mutation offers
    """
    # --- Placeholder for actual action logic ---
    # resolve_attack(actor, target), skill_use(actor), etc.

    # 1️⃣ XP Gain
    tags = context.get("tags", [])
    track_xp_gain(actor, tags)

    # 2️⃣ Technique Unlock
    auto_unlock_techniques(actor)

    # 3️⃣ Mutation Offer / Application
    actor_mutation_flow.handle_post_action_mutation(actor, context)
