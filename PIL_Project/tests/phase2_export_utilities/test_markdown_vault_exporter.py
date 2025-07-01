# tests/phase2_export_utilities/test_markdown_vault_exporter.py
"""
Unit tests for pil_meta.exporters.markdown_vault_exporter.export_markdown_vault.

Covers:
- File creation for each node
- Directory structure (by type)
- Content sanity (basic Markdown fields present)
- Handles edge: empty graph

@tags: ["test", "markdown_vault_exporter", "unit"]
@status: "stable"
"""

from pathlib import Path
from pil_meta.exporters.markdown_vault_exporter import export_markdown_vault

def test_export_markdown_vault_creates_files(tmp_path):
    """
    Exports a small graph and verifies .md files are created in correct folders.
    """
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "type": "function",
            "module": "foo",
            "name": "bar",
            "tags": ["core"],
            "description": "Doc for bar",
            "docstring_full": "def bar(): ...",
            "links": [{"type": "calls", "target": "foo.baz"}],
            "status": "stable",
            "visibility": "public",
            "deprecated": False
        },
        "foo.baz": {
            "fqname": "foo.baz",
            "type": "class",
            "module": "foo",
            "name": "baz",
            "tags": [],
            "description": "",
            "docstring_full": "",
            "links": [],
            "status": "beta",
            "visibility": "internal",
            "deprecated": True
        }
    }
    out_dir = tmp_path / "vault"
    written = export_markdown_vault(graph, out_dir, project_name="TestProj", timestamp="20990101_120000")
    # Check both files exist
    assert len(written) == 2
    for file in written:
        path = Path(file)
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "# " in text    # Has markdown heading
        assert "Fully qualified name:" in text
        assert "Type:" in text
        assert ".md" in path.name
    # Folder for function type
    assert (out_dir / "functions").exists()
    # Accept either correct or legacy pluralization for class type
    assert any(p.name.lower().startswith("class") for p in out_dir.iterdir())

def test_export_markdown_vault_empty_graph(tmp_path):
    """
    Exporting an empty graph returns an empty file list and creates no files.
    """
    out_dir = tmp_path / "vault"
    written = export_markdown_vault({}, out_dir, project_name="TestProj", timestamp="20990101_120000")
    assert written == []
    # Only the vault folder should exist, and it should be empty except possibly for subdirs
    files = list(out_dir.glob("**/*"))
    assert all(f.is_dir() for f in files)
