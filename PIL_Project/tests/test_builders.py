from PIL.builders.entity_graph_builder import build_entity_graph

def test_build_entity_graph_smoke():
    dummy = [{"fqname": "x.y", "type": "function", "module": "x", "source_file": "x/y.py", "docstring": "Test", "tags": [], "links": []}]
    graph = build_entity_graph(dummy)
    assert "x.y" in graph