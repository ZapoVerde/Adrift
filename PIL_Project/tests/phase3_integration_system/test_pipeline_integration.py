# tests/phase3_integration_system/test_pipeline_integration.py
"""
Integration/system tests for pil_meta.pipeline.run_pipeline.

Covers:
- End-to-end happy path: config, scanning, and all artifact creation
- Fails gracefully if config missing or broken
- Checks reporting, governance fields, and snapshot file

@tags: ["test", "pipeline", "integration", "system"]
@status: "stable"
"""

import shutil
import os
from pathlib import Path
import pytest
from pil_meta.pipeline import run_pipeline, PipelineResult

def make_minimal_project(tmp_path):
    """
    Sets up a minimal fake project with pilconfig.json, src file, and journal.
    Returns project_root and config_path.
    """
    proj = tmp_path / "Adrift"
    proj.mkdir()
    (proj / "sample.py").write_text("def foo():\n    '''foo does bar'''\n    pass", encoding="utf-8")
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()
    (journal_dir / "entry.md").write_text("# Journal", encoding="utf-8")

    config = {
        "project_root": str(proj),
        "scan_dirs": [str(proj)],
        "asset_extensions": [],
        "output_dir": str(tmp_path / "exports"),
        "vault_dir": str(tmp_path / "vault"),
        "journal_path": str(journal_dir),
        "snapshot_dir": str(tmp_path / "snapshots")
    }
    config_path = tmp_path / "pilconfig.json"
    import json
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return proj, config_path

def test_full_pipeline_happy_path(tmp_path):
    """
    Full pipeline run completes, produces all main artifacts, and populates result fields.
    """
    proj, config_path = make_minimal_project(tmp_path)
    result = run_pipeline(str(config_path))
    # Core outputs exist
    assert isinstance(result, PipelineResult)
    assert Path(result.snapshot_path).exists()
    assert Path(result.index_path).exists()
    # Exports folder created and contains at least one .json
    export_dir = Path(result.config["output_dir"])
    assert any(str(f).endswith(".json") for f in export_dir.iterdir())
    # Vault has at least one markdown file
    vault_dir = Path(result.config["vault_dir"])
    assert any(str(f).endswith(".md") for f in vault_dir.rglob("*.md"))
    # Governance summary fields populated
    assert isinstance(result.missing_docstrings, int)
    assert isinstance(result.orphaned, int)

def test_pipeline_fails_gracefully_on_missing_config(tmp_path):
    """
    Pipeline exits with code 1 if config is missing.
    """
    import sys
    import subprocess
    script = """
import sys
from pil_meta.pipeline import run_pipeline
run_pipeline('doesnotexist.json')
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True)
    assert result.returncode == 1

def test_pipeline_handles_empty_project(tmp_path):
    """
    Handles empty scan dir and produces no artifacts but no crash.
    """
    proj = tmp_path / "empty_proj"
    proj.mkdir()
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()
    config = {
        "project_root": str(proj),
        "scan_dirs": [str(proj)],
        "asset_extensions": [],
        "output_dir": str(tmp_path / "exports"),
        "vault_dir": str(tmp_path / "vault"),
        "journal_path": str(journal_dir),
        "snapshot_dir": str(tmp_path / "snapshots")
    }
    config_path = tmp_path / "pilconfig.json"
    import json
    config_path.write_text(json.dumps(config), encoding="utf-8")
    result = run_pipeline(str(config_path))
    assert isinstance(result, PipelineResult)
    # May not produce outputs, but doesn't crash
    assert Path(result.config["output_dir"]).exists()
    assert Path(result.config["vault_dir"]).exists()
