# tests/exporters/test_json_exporter.py

from pathlib import Path
from pil_meta.exporters.json_exporter import export_entity_graph

def test_export_entity_graph_writes_files(tmp_path):
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "type": "function",
            "module": "foo",
            "tags": [],
            "metadata": {}
        }
    }
    out_dir = tmp_path / "exports"
    out_dir.mkdir()
    result = export_entity_graph(graph, str(out_dir), project_name="TestProj", timestamp="20990101_120000")

    stable_path = Path(result["stable"])
    ts_path = Path(result["timestamped"])

    assert stable_path.exists()
    assert ts_path.exists()
    assert stable_path.name == "entity_graph.json"
    assert ts_path.name.startswith("entity_graph_TestProj_20990101_120000")

    with open(stable_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "foo.bar" in content
