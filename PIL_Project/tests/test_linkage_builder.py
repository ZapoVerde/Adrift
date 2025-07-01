# tests/builders/test_linkage_builder.py
"""
Unit tests for pil_meta.builders.linkage_builder.
Covers call link injection and AST call extraction, including edge/error cases.
"""

import pytest
from pil_meta.builders.linkage_builder import inject_call_links, extract_called_functions

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

# ---- AST call extraction tests below ----

def test_extract_simple_function_calls():
    code = "foo()\nbar()"
    result = extract_called_functions(code)
    assert sorted(result) == ["bar", "foo"]

def test_extract_attribute_calls():
    code = "obj.func1()\nmodule.func2()"
    result = extract_called_functions(code)
    assert "func1" in result
    assert "func2" in result

def test_extract_nested_calls():
    code = "outer(inner())"
    result = extract_called_functions(code)
    assert "outer" in result
    assert "inner" in result

def test_extract_handles_empty_and_bad_code():
    assert extract_called_functions("") == []
    # Bad code should return empty
    assert extract_called_functions("def incomplete(:") == []
