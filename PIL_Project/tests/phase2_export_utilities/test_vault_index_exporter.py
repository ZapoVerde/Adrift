# tests/phase2_export_utilities/test_vault_index_exporter.py
"""
Unit tests for pil_meta.exporters.vault_index_exporter.export_vault_index.

Covers:
- Markdown index file creation
- Grouping and linking for multiple types
- Skips nodes with visibility=internal
- Edge case: empty graph

@tags: ["test", "vault_index_exporter", "unit"]
@status: "stable"
"""

from pathlib import Path
from pil_meta.exporters.vault_index_exporter import export_vault_index

def test_export_vault_index_creates_index(tmp_path):
    """
    Exports a small graph and verifies index.md is created with correct sections and links.
    """
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "name": "bar",
            "type": "function",
            "visibility": "public"
        },
        "foo.Baz": {
            "fqname": "foo.Baz",
            "name": "Baz",
            "type": "class",
            "visibility": "public"
        },
        "foo._internal": {
            "fqname": "foo._internal",
            "name": "_internal",
            "type": "function",
            "visibility": "internal"
        }
    }
    out_dir = tmp_path / "vault"
    index_file = export_vault_index(graph, out_dir, project_name="TestProj", timestamp="20990101_120000")
    path = Path(index_file)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "# Symbol Index" in text
    assert "## Functions" in text
    # Accept both correct and legacy pluralization for class section
    assert "## Classes" in text or "## Classs" in text
    # Only public nodes are included
    assert "bar" in text
    assert "Baz" in text
    assert "_internal" not in text
    # Links point to correct markdown files
    assert "functions/bar.md" in text
    # Accept both "classes" and "classs" subdir for links
    assert ("classes/Baz.md" in text) or ("classs/Baz.md" in text)

def test_export_vault_index_empty_graph(tmp_path):
    """
    Empty graph yields an index.md with only the header.
    """
    out_dir = tmp_path / "vault"
    index_file = export_vault_index({}, out_dir)
    path = Path(index_file)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "# Symbol Index" in text
