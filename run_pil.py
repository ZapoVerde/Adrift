#!/usr/bin/env python3
# run_pil.py
"""
📦 Project-Side PIL Runner

Usage:
    ./run_pil.py

Requirements:
- This script must be in the project root alongside pilconfig.json
- pilconfig.json must contain:
    "pil_module_path": path to the PIL_Project folder

You can also run manually:
    python run_pil.py
"""

import json
import subprocess
import sys
from pathlib import Path

CONFIG_FILE = Path("pilconfig.json")

# 1. Validate config
if not CONFIG_FILE.exists():
    print("❌ Missing pilconfig.json in current directory.")
    sys.exit(1)

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

if "pil_module_path" not in config:
    print("❌ 'pil_module_path' not defined in pilconfig.json.")
    sys.exit(1)

# 2. Resolve pipeline script
pil_dir = Path(config["pil_module_path"]).resolve()
pipeline_script = pil_dir / "scripts" / "rebuild_pil.py"

if not pipeline_script.exists():
    print(f"❌ Could not find pipeline script at: {pipeline_script}")
    sys.exit(1)

# 3. Execute
print(f"🚀 Running PIL pipeline from: {pipeline_script}")
result = subprocess.run([
    sys.executable, "-c",
    (f"import sys; "
     f"sys.path.insert(0, '{pil_dir}'); "
     f"from pil_meta.pipeline import run_pipeline; "
     f"run_pipeline()")
])

if result.returncode == 0:
    print("✅ PIL completed successfully.")
else:
    print("❌ PIL pipeline failed.")
