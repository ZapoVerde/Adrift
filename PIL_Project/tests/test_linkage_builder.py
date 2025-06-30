# tests/builders/test_linkage_builder.py

import pytest
from pil_meta.builders.linkage_builder import inject_call_links

def test_injects_call_link_between_functions():
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "metadata": {"calls": ["module.func_b"]}
        },
        "module.func_b": {
            "fqname": "module.func_b",
            "type": "function",
            "module": "module",
            "metadata": {}
        }
    }
    result = inject_call_links(graph, "module")
    assert "links" in result["module.func_a"]
    assert any(link["target"] == "module.func_b" and link["type"] == "calls"
               for link in result["module.func_a"]["links"])

def test_missing_calls_field_results_in_no_links():
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "metadata": {}
        }
    }
    result = inject_call_links(graph, "module")
    assert "links" not in result["module.func_a"]

def test_nonexistent_target_is_ignored():
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "metadata": {"calls": ["missing.func"]}
        }
    }
    result = inject_call_links(graph, "module")
    # links will still be created even if target doesn't exist — just not resolved
    assert "links" in result["module.func_a"]
    assert result["module.func_a"]["links"][0]["target"] == "missing.func"

def test_empty_graph_returns_empty():
    result = inject_call_links({}, "any")
    assert result == {}
