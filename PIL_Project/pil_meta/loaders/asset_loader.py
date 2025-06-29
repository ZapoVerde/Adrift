# pil_meta/loaders/asset_loader.py
"""
Extract asset metadata from tracked folders for non-code files.

Scans all configured asset directories (from `tracked_assets` in `pilconfig.json`)
and returns standardized metadata records for each valid asset. These are merged into
the main entity graph alongside code functions and modules.

Supports extensions like `.png`, `.tmx`, `.glb`, `.sh`, `.json`, etc.
"""

from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tmx", ".glb", ".shader",
    ".json", ".sh", ".bat", ".svg", ".csv", ".xml"
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
    Scan all configured asset folders and extract metadata records.

    Parameters:
        config (dict): Loaded config dictionary from pilconfig.json.
                       Must contain a `tracked_assets` list.

    Returns:
        list[dict]: Asset metadata entries in graph-compatible format

    Example Output:
        {
            "fqname": "assets/fx/fireball.png",
            "type": "asset",
            "filename": "fireball.png",
            "path": "assets/fx/fireball.png",
            "extension": ".png",
            "tags": ["assets", "fx", "png"],
            "referenced_by": [],
            "description": "",
            "docstring_present": False,
            "test_coverage": False,
            "linked_journal_entry": None,
            "is_orphaned": True,
            "links": []
        }
    """
    tracked_dirs = config.get("tracked_assets", [])
    # Determine config base dir for relative path resolution
    config_base_dir = Path(config.get("config_self_path", ".")).parent.resolve()
    all_assets = []

    # Make sure all tracked_dirs are absolute
    abs_dirs = export_path_list(tracked_dirs, config_base_dir)

    for root in abs_dirs:
        if not root.exists():
            continue
        for file in root.rglob("*"):
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    rel_path = file.relative_to(config["project_root"])
                except Exception:
                    rel_path = file.name  # fallback: just filename if not possible
                symbol = {
                    "fqname": str(rel_path).replace("\\", "/"),
                    "type": "asset",
                    "filename": file.name,
                    "path": str(rel_path).replace("\\", "/"),
                    "extension": file.suffix.lower(),
                    "tags": infer_tags_from_path(file.relative_to(root)),
                    "referenced_by": [],
                    "description": "",
                    "docstring_present": False,
                    "test_coverage": False,
                    "linked_journal_entry": None,
                    "is_orphaned": True,
                    "links": [],
                }
                all_assets.append(symbol)
    return all_assets
