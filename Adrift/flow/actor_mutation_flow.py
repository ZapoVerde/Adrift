# actor_mutation_flow.py
# Controls mutation application, banking, and rarity boosting per actor.

from Adrift.utils.technique_mutation_utils import generate_evolution_offer

from Adrift.definitions.technique_defs import TECHNIQUE_DB
from Adrift.utils.actor_offer_utils import generate_evolution_offer_for_actor
import random
# -----------------------------
# 🧠 Actor Mutation State Model
# -----------------------------
# Each actor should have a mutation state structure like:
# actor["mutations"] = {
#     "banked": 3,
#     "boosts": {"sword": 2, "archery": 1},
#     "history": []
# }

# -----------------------------
# 🎁 Offer Generation + Boost
# -----------------------------


def get_mutation_offer(actor: dict, skill: str) -> list:
    """
    Generates 4 evolution options for the given skill, factoring in active boost.
    Increments history but does not apply anything.
    """
    boosts = actor.get("mutations", {}).get("boosts", {})
    boost_level = boosts.get(skill, 0)
    rarity = _boost_level_to_rarity(boost_level)
    base_technique = {
        "skill": skill,
        "effects": [],
        "modifier": None
    }  # placeholder stub
    offers = generate_evolution_offer(base_technique, rarity=rarity)
    return offers


# -----------------------------
# 💰 Banking & Boosting Logic
# -----------------------------


def can_offer_boost(actor: dict, skill: str) -> bool:
    """Returns True if actor has 3+ banked mutations and no current offer boost on skill."""
    m = actor.get("mutations", {})
    return m.get("banked", 0) >= 3 and m.get("boosts", {}).get(skill, 0) == 0


def apply_boost(actor: dict, skill: str):
    """Consumes 3 banked mutations to boost rarity of next offer for a given skill."""
    if not can_offer_boost(actor, skill):
        raise ValueError("Cannot apply boost: conditions not met.")
    actor["mutations"]["banked"] -= 3
    actor["mutations"].setdefault("boosts", {})[skill] = 1


# -----------------------------
# ✅ Mutation Selection Handler
# -----------------------------


def apply_mutation_choice(actor: dict, skill: str, choice: dict):
    """
    Applies a chosen mutation result to the actor.
    - If type is 'bank', increments bank.
    - Otherwise, applies mutation and resets any skill boost.
    - Appends to mutation history.
    """
    m = actor.setdefault("mutations", {})
    if choice["type"] == "bank":
        m["banked"] = m.get("banked", 0) + 1
    else:
        # Apply mutation (stub: actual replacement logic pending)
        # Reset boost for the skill
        if "boosts" in m:
            m["boosts"].pop(skill, None)
    m.setdefault("history", []).append(choice)


# -----------------------------
# 🧪 Action Phase Hook
# -----------------------------


def handle_pending_mutation_offer(actor: dict, context: dict):
    """
    Wrapper invoked during the action phase if the actor has a pending offer.
    Delegates to the actor's mutation selection logic and applies the result.
    """
    choice = actor.select_mutation_option()
    if not choice:
        return  # Declined or timed out
    skill = choice.get("skill", actor.get("last_used_skill", "unknown"))
    apply_mutation_choice(actor, skill, choice)


def handle_post_action_mutation(actor):
    """
    Checks if any visible technique is eligible for a mutation offer.

    - Trigger threshold is probabilistic.
    - Stores pending_offer on the actor if triggered.
    """
    if getattr(actor, "pending_offer", None):
        return  # already has an offer

    for tech_id, tech in actor.techniques.items():
        if not tech.get("visible"):
            continue
        if tech.get("level", 0) < 1:
            continue

        mutation_xp = getattr(actor, "mutation_xp", 0)
        chance = mutation_xp / (mutation_xp + 20)

        if random.random() < chance:
            actor.pending_offer = {
                "technique_id": tech_id,
                "offers": generate_evolution_offer_for_actor(actor, tech_id),
            }
            actor.mutation_xp = 0
            return

# -----------------------------
# 📊 Helpers
# -----------------------------


def _boost_level_to_rarity(boost_level: int) -> str:
    """Translates boost level to rarity tier."""
    if boost_level >= 3:
        return "epic"
    elif boost_level == 2:
        return "rare"
    elif boost_level == 1:
        return "uncommon"
    return "common"


# -----------------------------
# 🧪 TODO
# -----------------------------
# - Build tests for boosting edge cases and boost stack cost
# - Connect with real skill-based technique stub
# - Store real mutation result on actor object
# - Create visual log formatter for mutation history
