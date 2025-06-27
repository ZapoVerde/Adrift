# test_actor_offer_utils.py

import pytest
from Adrift.definitions.actor import Actor, add_skill, add_technique
from Adrift.utils.actor_offer_utils import generate_evolution_offer_for_actor


@pytest.fixture
def actor_with_tech():
    actor = Actor("Test")
    add_skill(actor, "sword")
    add_technique(actor, "piercing_thrust")
    actor.skills["sword"]["techniques"]["piercing_thrust"]["visible"] = True

    return actor


def test_offer_generation_returns_4_options(actor_with_tech):
    offers = generate_evolution_offer_for_actor(actor_with_tech, "piercing_thrust")
    assert len(offers) == 4
    for offer in offers:
        assert "type" in offer
        assert "result" in offer


def test_rarity_mapping():
    from Adrift.utils.actor_offer_utils import _boost_level_to_rarity
    assert _boost_level_to_rarity(0) == "common"
    assert _boost_level_to_rarity(1) == "uncommon"
    assert _boost_level_to_rarity(2) == "rare"
    assert _boost_level_to_rarity(3) == "epic"
    assert _boost_level_to_rarity(99) == "epic"


def test_missing_technique_raises():
    actor = Actor("Test")
    with pytest.raises(ValueError):
        generate_evolution_offer_for_actor(actor, "missing_tech")

def test_offer_fails_for_hidden_technique(actor_with_tech):
    actor = actor_with_tech
    actor.techniques["piercing_thrust"]["visible"] = False

    with pytest.raises(ValueError, match="not yet visible"):
        generate_evolution_offer_for_actor(actor, "piercing_thrust")
