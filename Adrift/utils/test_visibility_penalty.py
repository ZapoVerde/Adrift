# test_visibility_penalty.py

import pytest
from utils.general_utils import trace_line
from utils.visibility_utils import compute_visibility_penalty_along_path 
def make_tile_with_env(penalties):
    """Helper: create tile with list of env objects, each with a visibility_penalty."""
    return {
        "terrain": {},
        "things": [],
        "env": [{"type": f"test_{i}", "visibility_penalty": p} for i, p in enumerate(penalties)]
    }

def test_no_environment_penalty():
    floor = {(x, 0): {"terrain": {}, "things": [], "env": []} for x in range(3)}
    path = trace_line((0, 0), (2, 0), floor)
    assert compute_visibility_penalty_along_path (path) == 0

def test_single_fog_tile():
    floor = {
        (0, 0): make_tile_with_env([]),
        (1, 0): make_tile_with_env([2]),  # Fog tile
        (2, 0): make_tile_with_env([])
    }
    path = trace_line((0, 0), (2, 0), floor)
    assert compute_visibility_penalty_along_path (path) == 2

def test_multiple_penalty_sources():
    floor = {
        (0, 0): make_tile_with_env([1]),         # Fog 1
        (1, 0): make_tile_with_env([2, 3]),      # Smoke + fire
        (2, 0): make_tile_with_env([])
    }
    path = trace_line((0, 0), (2, 0), floor)
    assert compute_visibility_penalty_along_path (path) == 6

def test_missing_env_field():
    floor = {
        (0, 0): {"terrain": {}, "things": []},  # No env key
        (1, 0): make_tile_with_env([1]),
        (2, 0): make_tile_with_env([1])
    }
    path = trace_line((0, 0), (2, 0), floor)
    assert compute_visibility_penalty_along_path (path) == 2

def test_empty_path():
    assert compute_visibility_penalty_along_path ([]) == 0

def test_invalid_path_type():
    with pytest.raises(TypeError):
        compute_visibility_penalty_along_path ("not a list")

def test_step_not_dict():
    with pytest.raises(TypeError):
        compute_visibility_penalty_along_path ([123, 456])

def test_missing_tile_dict():
    with pytest.raises(TypeError):
        compute_visibility_penalty_along_path ([{"tile": "not_a_dict"}])

def test_env_not_list():
    with pytest.raises(TypeError):
        compute_visibility_penalty_along_path ([{"tile": {"env": "fog"}}])
