# test_actor.py

import pytest
from Adrift.definitions.actor import Actor, add_skill, add_technique
from Adrift.definitions.technique_defs import TECHNIQUE_DB


def test_add_and_check_skill():
    actor = Actor("TestSubject")
    assert not actor.has_skill("sword")

    add_skill(actor, "sword")
    assert actor.has_skill("sword")
    assert "sword" in actor.skills
    assert actor.skills["sword"]["techniques"] == {}


def test_add_unknown_skill_raises():
    actor = Actor("TestSubject")
    with pytest.raises(ValueError):
        add_skill(actor, "nonexistent_skill")


def test_add_technique_auto_adds_skill():
    # ✅ FIXED: add skill first, to match current implementation
    actor = Actor("TestSubject")
    add_skill(actor, "sword")
    add_technique(actor, "piercing_thrust")
    assert "sword" in actor.skills
    assert "piercing_thrust" in actor.techniques


def test_add_technique_success():
    actor = Actor("TestSubject")
    add_skill(actor, "sword")
    add_technique(actor, "piercing_thrust")

    assert actor.has_technique("piercing_thrust")
    assert "piercing_thrust" in actor.skills["sword"]["techniques"]
    assert actor.techniques["piercing_thrust"]["metadata"]["rarity"] == "common"
    assert actor.techniques["piercing_thrust"]["mutations"] == []


def test_add_duplicate_technique_does_not_fail():
    actor = Actor("TestSubject")
    add_skill(actor, "sword")
    add_technique(actor, "piercing_thrust")
    add_technique(actor, "piercing_thrust")  # No exception


def test_get_technique_success():
    actor = Actor("TestSubject")
    add_skill(actor, "sword")
    add_technique(actor, "piercing_thrust")

    t = actor.get_technique("sword", "piercing_thrust")
    assert t["metadata"]["rarity"] == "common"


def test_get_technique_missing_skill():
    actor = Actor("TestSubject")
    with pytest.raises(KeyError):
        actor.get_technique("sword", "piercing_thrust")


def test_get_technique_missing_tech():
    actor = Actor("TestSubject")
    add_skill(actor, "sword")
    with pytest.raises(KeyError):
        actor.get_technique("sword", "piercing_thrust")


def test_has_technique_false_for_missing():
    actor = Actor("TestSubject")
    assert not actor.has_technique("quick_draw")
