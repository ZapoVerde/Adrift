# pil_meta/utils/snapshot_utils.py
"""
Utility to create a zip snapshot of the full project for archival or traceability.

This should be called from within pipeline.py using:
    from pil_meta.utils.snapshot_utils import take_project_snapshot
"""

import zipfile
import os
from datetime import datetime
from pathlib import Path

IGNORED_FOLDERS = {
    ".git", "__pycache__", "node_modules", "snapshots", "exports",
    ".mypy_cache", ".venv", "env", ".idea"
}


def take_project_snapshot(config: dict,
                          entity_graph_path: str | None = None) -> Path:
    """
    Create a compressed zip snapshot of the entire project_root.
    Optionally attach entity_graph.json to aid traceability.

    Parameters:
        config (dict): The loaded pilconfig with required keys:
                       - project_root
                       - snapshot_dir
        entity_graph_path (str, optional): Path to entity_graph.json to attach

    Returns:
        Path: The full path to the created snapshot file.

    Raises:
        Exception: If snapshot folder is unwritable or config keys are missing.
    """
    project_root = Path(config["project_root"]).resolve()
    snapshot_dir = Path(config["snapshot_dir"]).resolve()
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_file = snapshot_dir / f"project_snapshot_{timestamp}.zip"

    file_count = 0
    with zipfile.ZipFile(snapshot_file,
                         "w",
                         zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zipf:
        for foldername, subfolders, filenames in os.walk(project_root):
            rel_folder = Path(foldername).relative_to(project_root)
            if any(part in IGNORED_FOLDERS for part in rel_folder.parts):
                continue

            for filename in filenames:
                file_path = Path(foldername) / filename
                rel_path = file_path.relative_to(project_root)
                zipf.write(file_path, arcname=str(rel_path))
                file_count += 1

        # 🔗 Attach the entity graph if provided
        if entity_graph_path:
            graph_file = Path(entity_graph_path)
            if graph_file.exists():
                arcname = f"entity_graph_{timestamp}.json"
                zipf.write(graph_file, arcname=arcname)
                print(f"📎 Attached entity graph as {arcname}")
            else:
                print(f"⚠️  Specified entity graph not found: {graph_file}")

    print(f"📦 Created snapshot with {file_count} files → {snapshot_file}")
    return snapshot_file
