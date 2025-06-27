# test_action_flow.py

import pytest
from Adrift.definitions.actor import Actor, add_skill
from Adrift.flow import action_flow


@pytest.fixture
def actor_with_sword():
    actor = Actor("Tester")
    add_skill(actor, "sword")
    return actor


def test_action_phase_without_mutation_offer(actor_with_sword):
    """
    Should apply XP and unlock visible skill/technique, no mutation triggered.
    """
    actor = actor_with_sword
    context = {"tags": ["combat", "melee", "piercing", "precise"]}

    # Run enough actions to trigger level-up and technique unlock
    for _ in range(10):
        action_flow.run_action_phase(actor, context)

    sword = actor.skills["sword"]
    tech = actor.techniques["piercing_thrust"]

    assert sword["level"] > 0
    assert sword["visible"] is True
    assert tech["level"] > 0
    assert tech["visible"] is True

    # No mutation should be triggered
    assert actor.pending_offer is None

def test_action_phase_with_mutation_offer_deterministic(actor_with_sword):
    with patch("Adrift.utils.skill_xp_utils.random.random", return_value=0.0):
        for _ in range(10):  # lower count OK now
            run_action_phase(actor_with_sword, {"tags": ["combat", "melee", "piercing", "precise"]})

    assert actor_with_sword.pending_offer is not None
    offer = actor.pending_offer

    assert offer["skill"] == "sword"
    assert offer["technique"] == "piercing_thrust"
    assert "options" in offer
    assert isinstance(offer["options"], list)

def test_mutation_trigger_manual_xp(actor_with_sword):
    tech = actor_with_sword.techniques["piercing_thrust"]
    tech["xp"] = 100
    tech["level"] = 2

    handle_post_action_mutation(actor_with_sword, context={"tags": []})
    assert actor_with_sword.pending_offer is not None