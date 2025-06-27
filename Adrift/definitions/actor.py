# actor.py
# Defines the Actor class and skill/technique scaffolding.
# All skills and techniques are stored as mutable flat dictionaries,
# to support flexible mutation, serialization, and modular testing.

from Adrift.helpers.actor_helpers import (
    initialize_skill_if_missing,
    initialize_technique_if_missing,
)
from Adrift.definitions.skill_defs import SKILL_DB
from Adrift.definitions.technique_defs import TECHNIQUE_DB
from copy import deepcopy


class Actor:
    """
    Represents a single controllable or autonomous entity in the game world.
    Holds mutable skill and technique instances, along with movement and mutation state.
    """

    def initialize_skill_if_missing(self, skill_id: str) -> None:
        return initialize_skill_if_missing(self, skill_id)

    def initialize_technique_if_missing(self, skill_id: str, tech_id: str) -> None:
        return initialize_technique_if_missing(self, skill_id, tech_id)

    def __init__(self, name: str, current_zone=None):
        self.name = name  # e.g., "Player", "Cultist", "Watcher_7"
        self.current_zone = current_zone  # Zone object reference

        # ───── Movement and Navigation ─────
        self.movement_path = []           # Ordered list of Zones to traverse
        self.movement_progress = 0        # Accumulated movement ticks

        # ───── Skill and Technique Ownership ─────
        self.skills = {}                  # skill_id → { "techniques": {tech_id → technique_dict} }
        self.techniques = {}             # tech_id → technique_dict (flat cache)

        # ───── Mutation and Evolution Tracking ─────
        self.mutation_bank = []           # List of banked mutation tokens
        self.skill_boosts = {}            # skill_id → active boost level


        # ✅ Required for mutation system
        self.pending_offer = None

    def has_skill(self, skill_id: str) -> bool:
        """Returns True if the actor currently owns the given skill."""
        return skill_id in self.skills

    def has_technique(self, tech_id: str) -> bool:
        """Returns True if the actor has the given technique in their flat cache."""
        return tech_id in self.techniques

    def get_technique(self, skill_id: str, tech_id: str) -> dict:
        """
        Safe accessor for a technique the actor owns.
        Raises KeyError if either the skill or technique is missing.

        Returns:
            technique_dict (mutable) belonging to this actor
        """
        try:
            return self.skills[skill_id]["techniques"][tech_id]
        except KeyError:
            raise KeyError(f"Technique '{tech_id}' not found under skill '{skill_id}'")


def add_skill(actor: Actor, skill_id: str):
    """
    Adds a properly initialized skill block to the actor.

    Structure:
        actor.skills[skill_id] = {
            "level": 0,
            "xp": 0,
            "visible": False,
            "techniques": {}
        }

    Raises:
        ValueError: if the skill_id is not in SKILL_DB
    """
    if skill_id in actor.skills:
        return

    if skill_id not in SKILL_DB:
        raise ValueError(f"Unknown skill ID: {skill_id}")
    
    actor.skills[skill_id] = {
        "level": 0,
        "xp": 0,
        "visible": False,
        "techniques": {}
    }

def add_technique(actor: Actor, tech_id: str):
    """
    Adds a technique instance to the actor, based on canonical TECHNIQUE_DB.
    - Copies the static definition
    - Initializes mutations[] and metadata fields
    - Registers in both actor.skills[skill]["techniques"] and actor.techniques[tech]

    Requires:
        - Skill must already be present

    Raises:
        ValueError: if the technique is unknown or the required skill is missing
    """
    if tech_id in actor.techniques:
        return  # Already added

    base = TECHNIQUE_DB.get(tech_id)
    if not base:
        raise ValueError(f"Unknown technique ID: {tech_id}")

    skill_id = base["base_skill"]
    if skill_id not in actor.skills:
        raise ValueError(f"Skill '{skill_id}' required before adding technique '{tech_id}'")

    instance = deepcopy(base)
    instance["skill"] = skill_id
    instance["mutations"] = []  # Track all applied evolutions
    instance["metadata"] = instance.get("metadata", {})
    instance["metadata"]["rarity"] = base["metadata"].get("rarity", "common")

    actor.skills[skill_id]["techniques"][tech_id] = instance
    actor.techniques[tech_id] = instance
