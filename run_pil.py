# run_pil.py
"""
Self-contained entry point for running the PIL pipeline for the Adrift project.
Writes the config to disk, then invokes the main pipeline logic with error handling.

@tags: ["entrypoint", "adrift", "self-contained"]
@status: "stable"
"""



import json
import sys
import traceback
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Callable



PIL_CONFIG = {
    # 📁 Root of the project to scan
    "project_root": "./PIL_Project",

    # 📂 Directories to scan for code and assets
    "scan_dirs": [
        "./PIL_Project/pil_meta",
        "./PIL_Project/scripts",
        "./PIL_Project/tests"
    ],

    # 📚 Location of markdown journal entries *OPTIONAL* *UNUSED*
    "journal_path": "./documents",

    # 📤 Where exports (JSON, vault, etc) are saved *MANDATORY*
    "output_dir": "./PIL_Project/exports",

    # 📝 Directory for user documentation (used by markdown loader) *OPTIONAL* *UNUSED*
    "docs_dir": "./docs",

    # 🗃️ Where the Obsidian vault is written
    "vault_dir": "./PIL_Project/exports/vault",

    # 🧳 Directory for full project snapshots
    "snapshot_dir": "./PIL_Project/snapshots",

    # 📌 Where this config is written (by this file)
    "config_self_path": "./pilconfig.json",

    # 📦 Where the PIL module is located (for function resolution)
    "pil_module_path": "./PIL_Project",

    # 🎨 Asset file extensions to include in scan
    "asset_extensions": [
        ".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"
    ],

    # 🚫 Folder names to ignore during scanning
    "ignored_folders": [
        ".git", "__pycache__", "snapshots", "exports",
        ".mypy_cache", ".venv", "env", ".idea", ".pytest_cache"
    ]
}


def import_pipeline_run_function(pil_module_path: str) -> Callable[[str], None]:
    """
    Dynamically imports run_pipeline() from pil_meta.pipeline inside pil_module_path.

    Raises:
        FileNotFoundError: if pipeline.py is missing
        ImportError: if spec or loader is None
    """
    pil_meta_path = Path(pil_module_path) / "pil_meta" / "pipeline.py"
    if not pil_meta_path.exists():
        raise FileNotFoundError(f"Pipeline file not found: {pil_meta_path}")

    spec = importlib.util.spec_from_file_location("pil_meta.pipeline", pil_meta_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create import spec for: {pil_meta_path}")

    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_pipeline

def main():
    try:
        # Write embedded config to disk
        config_path = Path(PIL_CONFIG["config_self_path"])
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(PIL_CONFIG, f, indent=2)

        # Dynamically import and run pipeline
        run_pipeline = import_pipeline_run_function(PIL_CONFIG["pil_module_path"])
        run_pipeline(str(config_path))

    except Exception as e:
        print("\n❌ [RUN_PIL ERROR] Pipeline execution failed.")
        print(f"   Reason: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

    finally:
        input("\n✅ Pipeline complete. Press Enter to exit...")

if __name__ == "__main__":
    main()