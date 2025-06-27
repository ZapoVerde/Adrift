# test_trace_line.py

import pytest
from utils.general_utils import trace_line

def make_blank_tile():
    return {"terrain": {}, "things": [], "env": []}

def test_straight_line_unblocked():
    floor = {}
    for x in range(5):
        floor[(x, 0)] = make_blank_tile()
    path = trace_line((0, 0), (4, 0), floor)
    assert [step["coord"] for step in path] == [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    assert all(not step["blocking"] for step in path)

def test_diagonal_line_with_blocking_tile():
    floor = {}
    for i in range(5):
        floor[(i, i)] = make_blank_tile()
    floor[(2, 2)]["terrain"]["blocks_sight"] = True
    path = trace_line((0, 0), (4, 4), floor)
    coords = [step["coord"] for step in path]
    assert coords == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    assert path[2]["blocking"] == True

def test_tile_with_blocking_thing():
    floor = {(0, 0): make_blank_tile(), (1, 0): make_blank_tile()}
    floor[(1, 0)]["things"].append({"blocks_projectiles": True})
    path = trace_line((0, 0), (1, 0), floor)
    assert path[1]["coord"] == (1, 0)
    assert path[1]["blocking"] == True

def test_missing_tile_skipped():
    floor = {(0, 0): make_blank_tile(), (2, 0): make_blank_tile()}
    path = trace_line((0, 0), (2, 0), floor)
    coords = [step["coord"] for step in path]
    assert coords == [(0, 0), (2, 0)]
    assert (1, 0) not in coords
