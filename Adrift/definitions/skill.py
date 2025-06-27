# skill.py
# Defines per-actor SkillInstance for XP tracking, leveling, and technique management.


class SkillInstance:
    """
    Represents a single actor-owned skill.
    Instances are created from static SKILL_DB definitions.
    """

    def __init__(self, skill_id: str):
        self.skill_id = skill_id
        self.level = 0
        self.xp = 0
        self.known = False  # Becomes True once actor hits level 1
        self.boosts = 0  # Active rarity boosts for evolution offers
        self.techniques = {}  # tech_id → TechniqueInstance

    def add_xp(self, amount: int):
        self.xp += amount
        # Level-up logic is handled externally using difficulty curves
        return self.xp

    def add_boost(self, count: int = 1):
        self.boosts += count

    def consume_boost(self):
        if self.boosts > 0:
            self.boosts -= 1
        return self.boosts

    def has_boost(self):
        return self.boosts > 0
