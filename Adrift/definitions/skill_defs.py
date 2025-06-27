# skill_defs.py
# Canonical skill definitions used by all actors.
# Tags support filtering, mutation logic, UI grouping, and AI targeting.

SKILL_DB = {
    "melee": {
        "name": "Melee",
        "parent": None,
        "tags": ["combat", "weapon", "close"]
    },
    "sword": {
        "name": "Sword",
        "parent": "melee",
        "tags": ["combat", "weapon", "bladed", "close"]
    },
    "unarmed": {
        "name": "Unarmed",
        "parent": "melee",
        "tags": ["combat", "weapon", "brawling", "close"]
    },
    "ranged": {
        "name": "Ranged",
        "parent": None,
        "tags": ["combat", "weapon", "projectile"]
    },
    "pistol": {
        "name": "Pistol",
        "parent": "ranged",
        "tags": ["combat", "weapon", "firearm", "short_range"]
    },
    "rifle": {
        "name": "Rifle",
        "parent": "ranged",
        "tags": ["combat", "weapon", "firearm", "long_range"]
    },
    "explosives": {
        "name": "Explosives",
        "parent": "ranged",
        "tags": ["combat", "area", "blast", "hazard"]
    },
    "stealth": {
        "name": "Stealth",
        "parent": None,
        "tags": ["mobility", "infiltration", "detection_resist"]
    },
    "observe": {
        "name": "Observe",
        "parent": None,
        "tags": ["scouting", "perception", "detection"]
    },
    "search": {
        "name": "Search",
        "parent": "observe",
        "tags": ["scouting", "perception", "active_detection"]
    }
}
