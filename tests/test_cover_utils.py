# tests/test_cover_utils.py

"""
Tests for cover_utils.py — ensures correct behavior of cover detection
and accumulation across tactical tile paths.

Test cases cover:
- No cover on path
- Single object with cover_rating
- Multiple intervening objects
- blocks_sight edge case (future-proofing)
- Path of length 2 (edge case)
- Missing tiles
- Mixed-quality data (invalid or negative cover values)
"""

import pytest
from Adrift.utils import cover_utils


# Minimal mock helper to create a tile
def make_tile(things):
    return {"things": things}


def test_no_cover_on_path():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 0


def test_single_cover_object():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([{"cover_rating": 2}]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 2


def test_multiple_cover_objects():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([{"cover_rating": 1}]),
        (0, 2): make_tile([{"cover_rating": 2}]),
        (0, 3): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2), (0, 3)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 3


def test_blocks_sight_is_ignored():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([{"blocks_sight": True}]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 0  # blocks_sight has no cover_rating, so ignored


def test_path_too_short():
    floor = {
        (0, 0): make_tile([{"cover_rating": 99}]),
        (0, 1): make_tile([]),
    }
    path = [(0, 0), (0, 1)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 0  # no intervening tiles


# ---- Extended test cases ----

def test_multiple_things_in_tile():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([
            {"cover_rating": 2},
            {"cover_rating": 3}
        ]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 5


def test_mixed_things_in_tile():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([
            {"cover_rating": 2},
            {"some_unrelated_field": True},
            {"cover_rating": 1}
        ]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 3


def test_missing_tile_handled_gracefully():
    floor = {
        (0, 0): make_tile([]),
        # (0, 1) is intentionally missing
        (0, 2): make_tile([{"cover_rating": 2}]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 0  # Only (0, 1) is checked, and it's missing


def test_invalid_cover_rating_ignored():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([
            {"cover_rating": "high"},
            {"cover_rating": None},
            {"cover_rating": 2}
        ]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 2


def test_negative_cover_rating_allowed():
    floor = {
        (0, 0): make_tile([]),
        (0, 1): make_tile([
            {"cover_rating": -2},
            {"cover_rating": 5}
        ]),
        (0, 2): make_tile([]),
    }
    path = [(0, 0), (0, 1), (0, 2)]
    total = cover_utils.calculate_total_cover(path, floor)
    assert total == 3  # Negative rating included
