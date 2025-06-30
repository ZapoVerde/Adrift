# tests/builders/test_usage_map_builder.py

from pil_meta.builders.usage_map_builder import build_usage_map

def test_empty_graph_returns_empty_map():
    result = build_usage_map({})
    assert result == {}

def test_single_node_no_links_produces_self_usage():
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "type": "function",
            "links": []
        }
    }
    result = build_usage_map(graph)
    assert result == {"foo.bar": []}

def test_call_links_are_registered_as_usage():
    graph = {
        "foo.a": {
            "fqname": "foo.a",
            "links": [{"type": "calls", "target": "foo.b"}]
        },
        "foo.b": {
            "fqname": "foo.b",
            "links": []
        }
    }
    result = build_usage_map(graph)
    assert "foo.b" in result
    assert "foo.a" in result["foo.b"]  # a uses b

def test_multiple_link_types_handled_correctly():
    graph = {
        "main.alpha": {
            "fqname": "main.alpha",
            "links": [
                {"type": "calls", "target": "main.beta"},
                {"type": "uses", "target": "main.gamma"}
            ]
        },
        "main.beta": {"fqname": "main.beta", "links": []},
        "main.gamma": {"fqname": "main.gamma", "links": []}
    }
    result = build_usage_map(graph)
    assert sorted(result["main.beta"]) == ["main.alpha"]
    assert sorted(result["main.gamma"]) == ["main.alpha"]
