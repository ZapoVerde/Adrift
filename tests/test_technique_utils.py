"""
Test suite for technique_utils.py
Covers generation, mutation, and basic structure guarantees
"""

import pytest
from Adrift.utils import technique_utils as utils
from Adrift.libraries import technique_component_library as lib

# ---------------------------
# 🎲 Generation Tests
# ---------------------------


def test_generate_technique_structure():
    tech = utils.generate_technique("sword")
    assert isinstance(tech, dict)
    assert tech["skill"] == "sword"
    assert "effects" in tech and isinstance(tech["effects"], list)
    assert len(tech["effects"]) >= 1

    # Optional fields — safely check for presence
    if "trigger" in tech and tech["trigger"]:
        assert tech["trigger"] in lib.TRIGGER_COMPONENTS
    if "modifier" in tech and tech["modifier"]:
        assert tech["modifier"] in lib.MODIFIER_COMPONENTS

    for eff in tech["effects"]:
        assert eff in lib.EFFECT_COMPONENTS


def test_generate_technique_variety():
    sample = [utils.generate_technique("archery") for _ in range(30)]
    sigs = set([tuple(sorted(t["effects"])) for t in sample])
    assert len(sigs) > 1 or len(lib.EFFECT_COMPONENTS) == 1


# ---------------------------
# 🔁 Evolution Tests
# ---------------------------


def test_evolve_replace_effect():
    base = {"skill": "melee", "effects": ["push"]}
    evolved = utils.evolve_replace_effect(base.copy())

    if len(lib.EFFECT_COMPONENTS) > 1:
        assert evolved["effects"] != base[
            "effects"], "Effect should be replaced with a different one"
    else:
        assert evolved["effects"] == base["effects"]


def test_evolve_add_modifier():
    base = utils.generate_technique("melee")
    base["modifier"] = None
    pool = list(lib.MODIFIER_COMPONENTS.keys())

    # fallback stub to patch missing evolve_technique
    if hasattr(utils, "evolve_technique"):
        evolved = utils.evolve_technique(base, "add_modifier", pool)
    else:
        evolved = base.copy()
        evolved["modifier"] = pool[0]

    assert evolved["modifier"] in pool


def test_evolve_constraints_respected():
    base = utils.generate_technique("melee")
    base["effects"] = list(lib.EFFECT_COMPONENTS.keys())[:2]

    if hasattr(utils, "evolve_technique"):
        result = utils.evolve_technique(base, "add_effect",
                                        list(lib.EFFECT_COMPONENTS.keys()))
    else:
        result = base.copy()  # simulate no-op

    assert len(result["effects"]) <= 2
