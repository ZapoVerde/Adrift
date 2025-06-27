# technique_utils.py
# Utility functions for technique generation and mutation.

import random
from Adrift.libraries import technique_component_library as lib

# ---------------------------
# 🎲 Generation
# ---------------------------


def generate_technique(skill_id: str) -> dict:
    """
    Generate a base technique scaffold with random components for a given skill.
    """
    technique = {
        "skill":
        skill_id,
        "effects": [random.choice(list(lib.EFFECT_COMPONENTS.keys()))],
        "modifier":
        random.choice(list(lib.MODIFIER_COMPONENTS.keys()))
        if lib.MODIFIER_COMPONENTS else None,
        "trigger":
        random.choice(list(lib.TRIGGER_COMPONENTS.keys()))
        if lib.TRIGGER_COMPONENTS else None,
        "mutations": [],  # ✅ Required for mutation history
    }
    return technique


# ---------------------------
# 🔁 Evolution (with deduplication)
# ---------------------------


def evolve_replace_effect(tech: dict) -> dict:
    """
    Replaces the first effect with a different one from the effect pool.
    Guarantees a change if at least 2 effects exist.
    Skips if same replacement already applied.
    """
    pool = list(lib.EFFECT_COMPONENTS.keys())
    if not pool:
        return tech

    current = tech["effects"][0]
    options = [e for e in pool if e != current]
    if not options:
        return tech

    chosen = random.choice(options)

    # Deduplicate: same from→to already done
    for m in tech.get("mutations", []):
        if m["type"] == "replace_effect" and m["from"] == current and m[
                "to"] == chosen:
            return tech

    tech["effects"] = [chosen]
    tech.setdefault("mutations", []).append({
        "type": "replace_effect",
        "from": current,
        "to": chosen
    })

    return tech


def evolve_add_modifier(tech: dict, options: list[str]) -> dict:
    """
    Adds a new modifier from the pool. Does nothing if already added.
    """
    if not options:
        return tech

    chosen = random.choice(options)

    for m in tech.get("mutations", []):
        if m["type"] == "add_modifier" and m["modifier"] == chosen:
            return tech  # already applied

    tech["modifier"] = chosen
    tech.setdefault("mutations", []).append({
        "type": "add_modifier",
        "modifier": chosen
    })

    return tech


def evolve_add_effect(tech: dict, options: list[str]) -> dict:
    """
    Adds a new effect if not already present and not already added before.
    """
    if len(tech["effects"]) >= 2:
        return tech

    available = [e for e in options if e not in tech["effects"]]
    if not available:
        return tech

    chosen = random.choice(available)

    for m in tech.get("mutations", []):
        if m["type"] == "add_effect" and m["effect"] == chosen:
            return tech  # already applied

    tech["effects"].append(chosen)
    tech.setdefault("mutations", []).append({
        "type": "add_effect",
        "effect": chosen
    })

    return tech


# ---------------------------
# 🔁 Central Dispatcher (for test scaffolding)
# ---------------------------


def evolve_technique(tech: dict, mode: str, options: list[str]) -> dict:
    """
    Dispatches to the correct mutation function for test scaffolding.
    Not intended for runtime use.
    """
    if mode == "add_modifier":
        return evolve_add_modifier(tech, options)
    elif mode == "add_effect":
        return evolve_add_effect(tech, options)
    elif mode == "replace_effect":
        return evolve_replace_effect(tech)
    else:
        raise ValueError(f"Unknown evolution mode: {mode}")


# ─────────────────────────────────────────────────────────────
# 🎯 get_available_mutations
# ─────────────────────────────────────────────────────────────

def get_available_mutations(tech: dict) -> list[str]:
    """
    Returns a list of valid mutation types for a given technique.

    Ensures we do not suggest evolutions that would exceed field limits
    or create invalid states. Used by the mutation offer generator.

    Possible mutations:
    - "replace_effect": always allowed if any effect exists
    - "add_effect": allowed if len(effects) < 2
    - "add_modifier": only allowed if modifier is None
    """
    options = []

    # Replace effect is always valid if we have any effect
    if tech.get("effects") and len(tech["effects"]) > 0:
        options.append("replace_effect")

    # Add effect only valid if under cap (2 effects max)
    if len(tech.get("effects", [])) < 2:
        options.append("add_effect")

    # Add modifier only if none exists yet
    if tech.get("modifier") is None:
        options.append("add_modifier")

    return options