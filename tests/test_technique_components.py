# test_technique_components.py

"""
Test suite for technique_component_library.py
Ensures component structure, field integrity, and uniqueness constraints
"""

import pytest
from Adrift.libraries import technique_component_library as lib

# ---------------------------
# 📦 Test Structure
# ---------------------------

def test_all_components_have_valid_fields():
    for category, components in lib.ALL_COMPONENTS.items():
        for cid, comp in components.items():
            assert isinstance(comp, dict), f"{cid} in {category} is not a dict"
            assert comp.get("id") == cid, f"{cid} has mismatched 'id' field"
            assert comp.get("type") == category, f"{cid} has wrong type: {comp.get('type')}"
            assert "description" in comp and isinstance(comp["description"], str)
            assert "rare" in comp and isinstance(comp["rare"], bool)
            assert "locked" in comp and comp["locked"] is True, f"{cid} is not locked"


def test_all_components_have_unique_ids():
    seen = set()
    for category, components in lib.ALL_COMPONENTS.items():
        for cid in components:
            assert cid not in seen, f"Duplicate component id found: {cid}"
            seen.add(cid)


def test_validate_component_function():
    for category, components in lib.ALL_COMPONENTS.items():
        for comp in components.values():
            assert lib.validate_component(comp), f"Failed validation: {comp}"


def test_component_type_distribution():
    # Ensure at least one of each type exists
    for t in ("effect", "modifier", "trigger"):
        assert t in lib.ALL_COMPONENTS
        assert len(lib.ALL_COMPONENTS[t]) >= 1, f"No components defined for type: {t}"


def test_get_all_component_ids():
    ids = lib.get_all_component_ids()
    expected = []
    for components in lib.ALL_COMPONENTS.values():
        expected.extend(components.keys())
    assert sorted(ids) == sorted(expected)
