#!/usr/bin/env python3
"""
chmod +x run_pil.py
run_pil.py — Self-contained runner for external use

This version embeds the PIL config directly and writes it to disk at runtime.
It requires only this single file to exist in the project root.
"""

import subprocess
import sys
import json
from pathlib import Path

# Embedded config — originally from pilconfig_self.json
PIL_CONFIG = {
    "project_root": "./Adrift",
    "journal_path": "./documents",
    "output_dir": "./exports",
    "docs_dir": "./docs",
    "snapshot_dir": "./snapshots",
    "vault_dir": "./exports/vault",
    "config_self_path": "./pilconfig.json",
    "pil_module_path": "./PIL_Project",
    "asset_extensions": [".png", ".json", ".tmx", ".glb", ".shader", ".svg", ".csv"]
}

# Dynamically locate rebuild_pil.py inside PIL_Project/scripts/
pipeline_script = Path(PIL_CONFIG["pil_module_path"]) / "scripts" / "rebuild_pil.py"
config_file_path = Path("pilconfig.json")  # Written version used at runtime

def main():
    if not pipeline_script.exists():
        print(f"❌ Could not find pipeline script at: {pipeline_script.resolve()}")
        sys.exit(1)

    # Write config to disk before execution
    try:
        with open(config_file_path, "w") as f:
            json.dump(PIL_CONFIG, f, indent=2)
        print(f"📝 Wrote config to: {config_file_path.resolve()}")
    except Exception as e:
        print(f"❌ Failed to write config: {e}")
        sys.exit(1)

    print(f"🚀 Running PIL pipeline from: {pipeline_script.resolve()}")
    try:
        subprocess.run(
            [sys.executable, str(pipeline_script), str(config_file_path)],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Pipeline script failed with exit code {e.returncode}")
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")
    finally:
        input("\n📦 Press Enter to exit...")

if __name__ == "__main__":
    main()