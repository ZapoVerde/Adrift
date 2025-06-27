# test_skill_xp_utils.py

import pytest
from Adrift.definitions.actor import Actor
from Adrift.definitions.technique_defs import TECHNIQUE_DB
from Adrift.utils.skill_xp_utils import track_xp_gain  # ✅ REQUIRED IMPORT

@pytest.fixture
def actor():
    """
    Returns a fresh Actor with no skills or techniques.
    """
    return Actor("Dummy")


def test_track_xp_gain_tags(actor):
    # Ensure initial state has no relevant skills or techniques
    assert "sword" not in actor.skills
    assert "piercing_thrust" not in actor.techniques

    # Apply XP gain with tags matching 'piercing_thrust'
    matching_tags = TECHNIQUE_DB["piercing_thrust"]["tags"]
    for _ in range(10):
        track_xp_gain(actor, matching_tags)

    # After XP, skill and technique should exist and have xp
    skill_block = actor.skills.get("sword")
    tech_block = actor.techniques.get("piercing_thrust")

    assert skill_block is not None, "Skill 'sword' should be added"
    assert skill_block["xp"] > 0, "Skill should have gained xp"
    assert skill_block.get("visible") is True, "Skill should be visible after leveling"

    assert tech_block is not None, "Technique 'piercing_thrust' should be added"
    assert tech_block["xp"] > 0, "Technique should have gained xp"
    assert tech_block.get("visible") is True, "Technique should be visible after leveling"


def test_nonmatching_tags_do_nothing(actor):
    # Use tags guaranteed to not match any techniques
    track_xp_gain(actor, ["magic", "fire", "arcane"])
    # Skills dict remains empty
    assert not actor.skills
    assert not actor.techniques
