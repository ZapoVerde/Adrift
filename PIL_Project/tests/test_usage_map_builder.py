# tests/builders/test_usage_map_builder.py
"""
Unit tests for pil_meta.builders.usage_map_builder.
Covers normal and edge cases, correct API output, cycles, and orphans.
"""

from pil_meta.builders.usage_map_builder import build_usage_map

def test_empty_graph_returns_empty_map():
    result = build_usage_map({})
    assert result == {}

def test_single_node_no_uses():
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "calls_fqns": []
        }
    }
    result = build_usage_map(graph)
    assert result == {"foo.bar": {"used_by": [], "uses": []}}

def test_call_links_are_registered_as_usage():
    graph = {
        "foo.a": {
            "fqname": "foo.a",
            "calls_fqns": ["foo.b"]
        },
        "foo.b": {
            "fqname": "foo.b",
            "calls_fqns": []
        }
    }
    result = build_usage_map(graph)
    assert result["foo.a"]["uses"] == ["foo.b"]
    assert result["foo.b"]["used_by"] == ["foo.a"]

def test_usage_map_cycle_and_orphan():
    graph = {
        "cycle.one": {"fqname": "cycle.one", "calls_fqns": ["cycle.two"]},
        "cycle.two": {"fqname": "cycle.two", "calls_fqns": ["cycle.one"]},
        "orphan": {"fqname": "orphan", "calls_fqns": []}
    }
    result = build_usage_map(graph)
    assert sorted(result["cycle.one"]["uses"]) == ["cycle.two"]
    assert sorted(result["cycle.two"]["used_by"]) == ["cycle.one"]
    assert result["orphan"] == {"used_by": [], "uses": []}

def test_missing_node_in_calls():
    graph = {
        "a": {"fqname": "a", "calls_fqns": ["b"]},
    }
    result = build_usage_map(graph)
    # Should record the use, and missing node 'b' will be included as key
    assert "b" in result
    assert result["b"]["used_by"] == ["a"]
