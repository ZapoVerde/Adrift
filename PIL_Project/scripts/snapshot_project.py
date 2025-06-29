# scripts/snapshot_project.py

import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path
import json

IGNORED_FOLDERS = {
    '.git', '__pycache__', 'node_modules', 'snapshots', 'exports', '.mypy_cache', '.venv', 'env', '.idea'
}

def snapshot_project(src_dir, snapshot_dir, entity_graph_path=None):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"project_snapshot_{ts}.zip"
    snapshot_path = Path(snapshot_dir) / snapshot_name

    print(f"[INFO] Source dir: {src_dir} (exists: {os.path.exists(src_dir)})")
    print(f"[INFO] Saving snapshot to: {snapshot_path}")

    with zipfile.ZipFile(snapshot_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        file_count = 0
        for foldername, subfolders, filenames in os.walk(src_dir):
            rel_folder = os.path.relpath(foldername, src_dir)
            if any(part in IGNORED_FOLDERS for part in rel_folder.split(os.sep)):
                continue
            for filename in filenames:
                filepath = Path(foldername) / filename
                arcname = filepath.relative_to(src_dir)
                try:
                    zipf.write(filepath, arcname)
                    file_count += 1
                    if file_count % 100 == 0:
                        print(f"  Zipped {file_count} files so far...")
                except Exception as e:
                    print(f"  [SKIP] {filepath}: {e}", file=sys.stderr)
        # Add the entity_graph.json file explicitly, if provided
        if entity_graph_path and os.path.exists(entity_graph_path):
            arcname = "exports/entity_graph.json"
            zipf.write(entity_graph_path, arcname)
            print(f"  Included {entity_graph_path} as {arcname} in snapshot.")
    print(f"✅ Snapshot saved: {snapshot_path} ({file_count} files + entity graph archived)")

def load_config(config_path):
    config_file = Path(config_path).resolve()
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)
    base_dir = config_file.parent
    for field in [
        "project_root", "output_dir", "snapshot_dir"
    ]:
        if field in config:
            value = config[field]
            if not Path(value).is_absolute():
                config[field] = str((base_dir / value).resolve())
    config["config_self_path"] = str(config_file)
    return config

if __name__ == "__main__":
    try:
        # Allow the user to optionally specify a config path as the first CLI argument
        config_arg = sys.argv[1] if len(sys.argv) > 1 else "pilconfig.json"
        config = load_config(config_arg)
        src_dir = config["project_root"]
        snapshot_dir = config.get("snapshot_dir", "./exports/snapshots/")
        # The entity graph is always written to output_dir/entity_graph.json
        entity_graph_path = str(Path(config["output_dir"]) / "entity_graph.json")
        Path(snapshot_dir).mkdir(parents=True, exist_ok=True)
        snapshot_project(src_dir, snapshot_dir, entity_graph_path)
    except Exception as ex:
        print(f"[ERROR] {ex}", file=sys.stderr)
        sys.exit(1)
