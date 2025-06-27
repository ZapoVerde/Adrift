# technique_defs.py
# Canonical technique definitions.
# These are static and mutation-free — each actor owns mutable copies.

TECHNIQUE_DB = {
    "piercing_thrust": {
        "id":
        "piercing_thrust",
        "base_skill":
        "sword",
        "level_required":
        1,
        "effects": [
            {
                "type": "damage",
                "value": "×1.2",
                "damage_type": "piercing"
            },
            {
                "type": "crit_bonus",
                "value": +1
            },
        ],
        "modifiers": [
            {
                "type": "init_speed",
                "value": -1
            },
        ],
        "tags": ["combat", "melee", "piercing", "precise"],
        "metadata": {
            "rarity": "common",
        }
    },
    "overhead_cleave": {
        "id":
        "overhead_cleave",
        "base_skill":
        "sword",
        "level_required":
        2,
        "effects": [
            {
                "type": "damage",
                "value": "×1.5",
                "damage_type": "slashing"
            },
            {
                "type": "area",
                "radius": 1
            },  # Hits adjacent targets
        ],
        "modifiers": [
            {
                "type": "init_speed",
                "value": -2
            },
        ],
        "tags": ["combat", "melee", "slashing", "area", "high_risk"],
        "metadata": {
            "rarity": "uncommon",
        }
    },
    "quick_draw": {
        "id":
        "quick_draw",
        "base_skill":
        "pistol",
        "level_required":
        1,
        "effects": [
            {
                "type": "damage",
                "value": "×1.0",
                "damage_type": "ballistic"
            },
        ],
        "modifiers": [
            {
                "type": "init_speed",
                "value": +2
            },  # Very fast to act
        ],
        "tags": ["combat", "firearm", "short_range", "reaction"],
        "metadata": {
            "rarity": "common",
        }
    },
    "throw_flashbang": {
        "id":
        "throw_flashbang",
        "base_skill":
        "explosives",
        "level_required":
        1,
        "effects": [
            {
                "type": "blind",
                "duration": 2
            },
            {
                "type": "stagger",
                "duration": 1
            },
        ],
        "modifiers": [
            {
                "type": "range",
                "value": 4
            },
        ],
        "tags": ["utility", "area", "blast", "hazard", "tactical"],
        "metadata": {
            "rarity": "uncommon",
        }
    }
}
