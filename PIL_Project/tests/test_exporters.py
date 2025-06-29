from PIL.exporters.json_exporter import export_entity_graph
import json
from pathlib import Path

def test_export_entity_graph_smoke(tmp_path):
    out = tmp_path / "graph.json"
    export_entity_graph({"a": {"fqname": "a"}}, str(out))
    assert json.loads(out.read_text())["a"]["fqname"] == "a"