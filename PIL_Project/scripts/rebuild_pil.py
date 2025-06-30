#!/usr/bin/env python3

import sys
from pathlib import Path

# Detect whether we're being run from inside PIL_Project or externally
this_file = Path(__file__).resolve()
pil_project_root = this_file.parent.parent  # e.g., PIL_Project/
pil_meta_path = pil_project_root / "pil_meta"

if not pil_meta_path.exists():
    print(f"❌ Could not find pil_meta at expected location: {pil_meta_path}")
    sys.exit(1)

# Ensure pil_meta is importable
sys.path.insert(0, str(pil_project_root))

from pil_meta.pipeline import run_pipeline

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "pilconfig.json"
    run_pipeline(config_path)
