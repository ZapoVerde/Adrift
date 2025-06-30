# pil_meta/loaders/asset_loader.py
"""
Extract asset metadata from tracked folders for non-code files.

Scans all configured asset directories (from `tracked_assets` in `pilconfig.json`)
and returns standardized metadata records for each valid asset. These are merged into
the main entity graph alongside code functions and modules.

Supports extensions like `.png`, `.tmx`, `.glb`, `.sh`, `.json`, etc.
"""

from pathlib import Path
import os

SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tmx", ".glb", ".shader", ".json", ".sh", ".bat",
    ".svg", ".csv", ".xml"
}


def infer_tags_from_path(filepath: Path) -> list[str]:
    """
    Infer semantic tags from the file path and extension.

    Parameters:
        filepath (Path): Relative or absolute path to the asset file

    Returns:
        list[str]: Sorted tag list (e.g. ["assets", "maps", "tmx"])
    """
    tags = set()
    for part in filepath.parts:
        lowered = part.lower()
        if lowered in {"assets", "images", "maps", "scripts", "fx", "icons"}:
            tags.add(lowered)
    ext = filepath.suffix.lower().replace('.', '')
    if ext:
        tags.add(ext)
    return sorted(tags)


def export_path_list(paths, config_base_dir):
    """
    Ensures all paths in the list are absolute, resolving relative paths from config file's directory.
    """
    abs_paths = []
    for p in paths:
        path_obj = Path(p)
        if not path_obj.is_absolute():
            abs_paths.append((config_base_dir / path_obj).resolve())
        else:
            abs_paths.append(path_obj.resolve())
    return abs_paths


def load_asset_symbols(config: dict) -> list[dict]:
    """
    Scan the entire project_root recursively and extract metadata
    for asset files matching supported extensions.

    Uses config["asset_extensions"] and config["ignored_folders"].
    """
    project_root = Path(config["project_root"]).resolve()
    extensions = set(config.get("asset_extensions", []))
    ignored = set(
        config.get("ignored_folders", [
            ".git", "__pycache__", "snapshots", "exports", ".mypy_cache",
            ".venv"
        ]))

    all_assets = []
    scanned_folders = set()
    skipped_folders = set()

    for root, dirs, files in os.walk(project_root):
        path_obj = Path(root)
        rel_path = path_obj.relative_to(project_root)

        # Check if any folder in path is ignored
        if any(part in ignored for part in rel_path.parts):
            skipped_folders.add(str(rel_path))
            dirs[:] = []  # don't descend further
            continue
        else:
            scanned_folders.add(str(rel_path))

        for file in files:
            fpath = path_obj / file
            if fpath.suffix.lower() in extensions:
                rel_file = fpath.relative_to(project_root)
                symbol = {
                    "fqname": str(rel_file).replace("\\", "/"),
                    "type": "asset",
                    "filename": file,
                    "path": str(rel_file).replace("\\", "/"),
                    "extension": fpath.suffix.lower(),
                    "tags": infer_tags_from_path(rel_file),
                    "referenced_by": [],
                    "description": "",
                    "docstring_present": False,
                    "test_coverage": False,
                    "linked_journal_entry": None,
                    "is_orphaned": True,
                    "links": [],
                }
                all_assets.append(symbol)

    print(f"📂 Scanned project_root: {project_root}")
    for f in sorted(scanned_folders):
        print(f"✅ Scanning: {f}/")
    for f in sorted(skipped_folders):
        print(f"🚫 Skipping ignored folder: {f}/")

    print(f"✅ Found {len(all_assets)} asset files ({', '.join(extensions)})")
    return all_assets
