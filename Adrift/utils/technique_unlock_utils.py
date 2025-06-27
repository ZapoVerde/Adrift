# technique_unlock_utils.py
# Auto-unlocks techniques when skill level thresholds are met.

from Adrift.definitions.technique_defs import TECHNIQUE_DB
from Adrift.definitions.actor import add_technique, Actor

def auto_unlock_techniques(actor: Actor):
    """
    Scans canonical techniques and adds any to the actor whose
    base_skill has reached its level_required.
    """
    for tech_id, base in TECHNIQUE_DB.items():
        skill_id = base.get("base_skill")
        required = base.get("level_required", 0)

        # Skip missing or low-level skills
        skill_block = actor.skills.get(skill_id)
        if not skill_block:
            continue

        try:
            level = int(skill_block.get("level", 0))
        except Exception:
            continue  # Skip mocks or broken data

        if level < required:
            continue

        # Unlock if not present
        if tech_id not in actor.techniques:
            add_technique(actor, tech_id)
