# run_pil_self.py
"""
DO NOT RELOCATE OR REUSE THIS FILE OUTSIDE THE ADRIFT PROJECT.

Self-contained entry point for running the PIL pipeline locally.
Writes its own config and directly invokes the pipeline.
Intended for internal testing and standalone runs only.

@tags: ["entrypoint", "self-contained", "adrift-only"]
@status: "stable"
"""

import json
import traceback
import sys
from pathlib import Path
from pil_meta.pipeline import run_pipeline

PIL_CONFIG = {
    # 📁 Root of the project to scan
    "project_root": ".",

    # 📂 Directories to scan for code and assets
    "scan_dirs": [
        "./pil_meta",
        "./tests",
        "./scripts"
    ],

    # 📚 Location of markdown journal entries *OPTIONAL* *UNUSED*
    "journal_path": "./documents",

    # 📤 Where exports (JSON, vault, etc) are saved *MANDATORY*
    "output_dir": "./exports",

    # 📝 Directory for user documentation (used by markdown loader) *OPTIONAL* *UNUSED*
    "docs_dir": "./docs",

    # 🗃️ Where the Obsidian vault is written
    "vault_dir": "./exports/vault",

    # 🧳 Directory for full project snapshots
    "snapshot_dir": "./snapshots",

    # 📌 Where this config is written (by this file)
    "config_self_path": "./pilconfig.json",

    # 📦 Where the PIL module is located (for function resolution)
    "pil_module_path": ".",

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

def main():
    try:
        config_path = Path(PIL_CONFIG["config_self_path"])
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(PIL_CONFIG, f, indent=2)
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
