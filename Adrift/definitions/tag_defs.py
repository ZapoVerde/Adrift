# tag_defs.py
# Canonical registry of known tags and their meanings.
# Used for validation, filtering, and documentation.

TAG_DB = {
    # ─── Combat Role Tags ───
    "combat": "Used directly in offensive or defensive combat actions.",
    "weapon": "Indicates this skill governs a weapon or physical technique.",
    "brawling": "Close-quarters hand-to-hand unarmed combat.",
    "bladed": "Includes swords, knives, and slashing weapons.",
    "firearm": "Uses explosive propulsion and ammunition.",
    "projectile": "Involves ballistic or thrown travel.",
    "area": "Affects multiple tiles or actors simultaneously.",
    "blast": "Causes AoE shock, force, or concussive effects.",
    "hazard": "Can create lingering danger zones (e.g., fire, poison).",

    # ─── Range / Positioning ───
    "close": "Effective at 1-tile (melee) range.",
    "short_range": "Effective at 2–5 tiles. Limited long reach.",
    "long_range": "Effective at 6+ tiles. Requires aiming or setup.",

    # ─── Tactical Utility ───
    "scouting": "Used to gather information about surroundings or enemies.",
    "perception": "Enhances visibility, detection, or reaction radius.",
    "detection": "Used to reveal hidden or obscured actors or zones.",
    "active_detection": "Requires an action to use (e.g., search).",
    "tactical": "Used to support positioning, suppression, control, or setup.",
    "utility":
    "Supports tactical effects, crowd control, or setup without direct damage.",

    # ─── Mobility and Stealth ───
    "mobility": "Involves movement, positioning, or evasion.",
    "infiltration": "Related to bypassing enemy perception or defenses.",
    "detection_resist": "Reduces likelihood of being seen or tracked.",

    # ─── Technique Behavior Tags (NEW) ───
    "melee": "Used at melee range; typically STR or DEX governed.",
    "slashing": "Delivers cutting or sweeping attacks.",
    "piercing": "Delivers thrusting or penetrative damage.",
    "precise": "Has improved hit chance, crit chance, or bypass effects.",
    "high_risk": "Has a cost in speed, vulnerability, or other drawback.",
    "reaction": "Can be triggered off-turn or in response to events.",
}
