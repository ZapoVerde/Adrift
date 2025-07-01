# tests/builders/test_entity_graph_builder.py

import pytest
from pil_meta.builders.entity_graph_builder import build_entity_graph

def test_valid_entity_graph_build():
    """Valid entities yield expected graph nodes with correct fields."""
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
    """Empty input yields an empty graph dict."""
    assert build_entity_graph([]) == {}

def test_missing_required_fqname_raises():
    """Entity missing 'fqname' should raise KeyError."""
    entities = [{"type": "function", "module": "foo"}]
    with pytest.raises(KeyError):
        build_entity_graph(entities)

def test_entity_not_dict_raises():
    """Non-dict entity in list should raise TypeError."""
    entities = [{"fqname": "foo.bar"}, "this is not a dict"]
    with pytest.raises(TypeError):
        build_entity_graph(entities)

def test_tags_must_be_list():
    """Entity with non-list 'tags' should raise ValueError."""
    entities = [{"fqname": "foo.bar", "type": "function", "module": "foo", "tags": "notalist"}]
    with pytest.raises(ValueError):
        build_entity_graph(entities)

def test_duplicate_fqnames_overwrites_last():
    """Duplicate FQ names: last entity should overwrite prior."""
    entities = [
        {"fqname": "foo.bar", "type": "function", "module": "v1"},
        {"fqname": "foo.bar", "type": "function", "module": "v2"}
    ]
    graph = build_entity_graph(entities)
    assert graph["foo.bar"]["module"] == "v2"

def test_extra_fields_are_preserved():
    """Entities with extra/unknown fields retain them in output."""
    entities = [
        {"fqname": "foo.bar", "type": "function", "module": "foo", "custom_field": 123}
    ]
    graph = build_entity_graph(entities)
    assert "custom_field" in graph["foo.bar"]
    assert graph["foo.bar"]["custom_field"] == 123

def test_tags_none_raises():
    """Entity with 'tags' set to None should raise ValueError."""
    entities = [{"fqname": "foo.bar", "type": "function", "module": "foo", "tags": None}]
    with pytest.raises(ValueError):
        build_entity_graph(entities)
