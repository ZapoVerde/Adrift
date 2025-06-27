# technique_component_library.py
"""
Component registry for procedural technique generation.

Status: Locked
Date: 2025-06-25
Time: 00:00 UTC

All entries in this file are governed by Design Journal entry:
📚 Technique Component Library – Journal Summary

Components must follow strict schema and are divided by role:
- Triggers: Optional activation conditions
- Effects: Required technique payloads
- Modifiers: Optional conditional modifiers

Each component is a flat dictionary with the following fields:
- id (str): Unique identifier
- type (str): One of 'trigger', 'effect', 'modifier'
- description (str): Human-readable effect
- rare (bool): If True, excluded from base generation
- locked (bool): Must be True unless component is in test or dev state
"""

# ---------------------------
# 📦 Effect Components
# ---------------------------
EFFECT_COMPONENTS = {
    "bleed": {
        "id": "bleed",
        "type": "effect",
        "description": "Applies a bleed condition on hit.",
        "rare": False,
        "locked": True
    },
    "push": {
        "id": "push",
        "type": "effect",
        "description": "Shoves the target backward.",
        "rare": False,
        "locked": True
    },
    "daze": {
        "id": "daze",
        "type": "effect",
        "description": "Applies a temporary penalty to evasion and actions.",
        "rare": False,
        "locked": True
    }
}

# ---------------------------
# ⚙️ Modifier Components
# ---------------------------
MODIFIER_COMPONENTS = {
    "on_crit": {
        "id": "on_crit",
        "type": "modifier",
        "description": "Only activates on a critical hit.",
        "rare": False,
        "locked": True
    },
    "vs_bleeding": {
        "id": "vs_bleeding",
        "type": "modifier",
        "description": "Applies bonus if target is already bleeding.",
        "rare": False,
        "locked": True
    },
    "stat_scaling": {
        "id": "stat_scaling",
        "type": "modifier",
        "description": "Effect magnitude scales with skill-related stat.",
        "rare": True,
        "locked": True
    }
}

# ---------------------------
# 🧲 Trigger Components
# ---------------------------
TRIGGER_COMPONENTS = {
    "on_flank": {
        "id": "on_flank",
        "type": "trigger",
        "description": "Only activates if attacker is flanking.",
        "rare": False,
        "locked": True
    },
    "first_strike": {
        "id": "first_strike",
        "type": "trigger",
        "description": "Only usable if actor hasn't acted yet this round.",
        "rare": False,
        "locked": True
    }
}

# ---------------------------
# 📚 Unified Registry
# ---------------------------
ALL_COMPONENTS = {
    "effect": EFFECT_COMPONENTS,
    "modifier": MODIFIER_COMPONENTS,
    "trigger": TRIGGER_COMPONENTS
}


# ---------------------------
# 🧪 Validation Utilities
# ---------------------------
def validate_component(comp: dict) -> bool:
    required_keys = {"id", "type", "description", "rare", "locked"}
    if not isinstance(comp, dict):
        return False
    if not required_keys.issubset(set(comp.keys())):
        return False
    if comp["type"] not in {"effect", "modifier", "trigger"}:
        return False
    return True


def get_all_component_ids() -> list:
    ids = []
    for group in ALL_COMPONENTS.values():
        ids.extend(group.keys())
    return ids
