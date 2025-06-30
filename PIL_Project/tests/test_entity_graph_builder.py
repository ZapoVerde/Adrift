# tests/builders/test_entity_graph_builder.py

import pytest
from pil_meta.builders.entity_graph_builder import build_entity_graph

def test_valid_entity_graph_build():
    entities = [
        {"fqname": "foo.bar", "type": "function", "module": "foo", "tags": ["core"]},
        {"fqname": "foo.baz", "type": "class", "module": "foo", "tags": []}
    ]
    graph = build_entity_graph(entities)
    assert isinstance(graph, dict)
    assert "foo.bar" in graph
    assert graph["foo.bar"]["type"] == "function"
    assert graph["foo.bar"]["tags"] == ["core"]
    assert graph["foo.bar"]["module"] == "foo"

def test_empty_input_returns_empty_graph():
    assert build_entity_graph([]) == {}

def test_missing_required_fqname_raises():
    entities = [{"type": "function", "module": "foo"}]
    with pytest.raises(KeyError):
        build_entity_graph(entities)

def test_entity_not_dict_raises():
    entities = [{"fqname": "foo.bar"}, "this is not a dict"]
    with pytest.raises(TypeError):
        build_entity_graph(entities)

def test_tags_must_be_list():
    entities = [{"fqname": "foo.bar", "type": "function", "module": "foo", "tags": "notalist"}]
    with pytest.raises(ValueError):
        build_entity_graph(entities)

def test_duplicate_fqnames_overwrites_last():
    entities = [
        {"fqname": "foo.bar", "type": "function", "module": "v1"},
        {"fqname": "foo.bar", "type": "function", "module": "v2"}
    ]
    graph = build_entity_graph(entities)
    assert graph["foo.bar"]["module"] == "v2"
